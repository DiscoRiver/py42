from threading import Lock

from py42._compat import str
from py42.exceptions import Py42StorageSessionInitializationError
from py42.services._connection import Connection
from py42.services.storage._auth import FileArchiveTmpAuth
from py42.services.storage._auth import SecurityArchiveTmpAuth
from py42.services.storage.archive import StorageArchiveService
from py42.services.storage.preservationdata import StoragePreservationDataService
from py42.services.storage.securitydata import StorageSecurityDataService


class StorageServiceFactory(object):
    def __init__(self, connection, device_service, connection_manager):
        self._connection = connection
        self._device_service = device_service
        self._connection_manager = connection_manager

    def create_archive_service(self, device_guid, destination_guid=None):
        if destination_guid is None:
            destination_guid = self._auto_select_destination_guid(device_guid)

        auth = FileArchiveTmpAuth(
            self._connection, u"my", device_guid, destination_guid
        )
        connection = self._connection_manager.get_storage_connection(auth)
        return StorageArchiveService(connection)

    def create_security_data_service(self, plan_uid, destination_guid):
        auth = SecurityArchiveTmpAuth(self._connection, plan_uid, destination_guid)
        connection = self._connection_manager.get_storage_connection(auth)
        return StorageSecurityDataService(connection)

    def create_preservation_data_service(self, host_address):
        main_connection = self._connection.clone(host_address)
        streaming_connection = Connection.from_host_address(host_address)
        return StoragePreservationDataService(main_connection, streaming_connection)

    def _auto_select_destination_guid(self, device_guid):
        response = self._device_service.get_by_guid(
            device_guid, include_backup_usage=True
        )
        # take the first destination guid we find
        destination_list = response["backupUsage"]
        if not destination_list:
            raise Exception(
                u"No destinations found for device guid: {}".format(device_guid)
            )
        return destination_list[0][u"targetComputerGuid"]


class ConnectionManager(object):
    def __init__(self, session_cache=None):
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_connection_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_storage_connection(self, tmp_auth):
        try:
            url = tmp_auth.get_storage_url()
            connection = self.get_saved_connection_for_url(url)
            if connection is None:
                with self._list_update_lock:
                    connection = self.get_saved_connection_for_url(url)
                    if connection is None:
                        connection = Connection.from_host_address(url, auth=tmp_auth)
                        self._session_cache[url.lower()] = connection
        except Exception as ex:
            message = u"Failed to create or retrieve connection, caused by: {}".format(
                str(ex)
            )
            raise Py42StorageSessionInitializationError(ex, message)
        return connection
