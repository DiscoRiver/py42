from py42.services import BaseService


class RestoreService(BaseService):
    def create_restore_session(
        self,
        device_guid,
        data_key_token=None,
        private_password=None,
        encryption_key=None,
    ):
        """Creates a web restore connection.
        See https://console.us.code42.com/apidocviewer/#WebRestoreSession
        """
        uri = u"/api/WebRestoreSession"
        json_dict = {
            u"computerGuid": device_guid,
            u"dataKeyToken": data_key_token,
            u"privatePassword": private_password,
            u"encryptionKey": encryption_key,
        }
        return self._connection.post(uri, json=json_dict)

    def get_file_path_metadata(
        self,
        session_id,
        device_guid,
        file_id=None,
        timestamp=None,
        show_deleted=None,
        batch_size=None,
        last_batch_file_id=None,
        backup_set_id=None,
        include_os_metadata=None,
    ):
        # session_id is a web restore session ID (see create_restore_session)
        uri = u"/api/WebRestoreTreeNode"
        params = {
            u"webRestoreSessionId": session_id,
            u"guid": device_guid,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
            u"batchSize": batch_size,
            u"lastBatchFileId": last_batch_file_id,
            u"backupSetId": backup_set_id,
            u"includeOsMetadata": include_os_metadata,
        }
        return self._connection.get(uri, params=params)
