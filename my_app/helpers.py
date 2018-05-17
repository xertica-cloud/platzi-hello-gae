import httplib2
from oauth2client import service_account
from googleapiclient.discovery import build


GCS_SCOPE = 'https://www.googleapis.com/auth/devstorage.read_write ' \
            'https://www.googleapis.com/auth/devstorage.read_only ' \
            'https://www.googleapis.com/auth/devstorage.full_control'

SERVICE_ACCOUNT_KEY_FILE = 'platzi-test-001-02865d9f20fc.json'
BUCKET = 'platzi-test-001.appspot.com'

class CloudStorageHelper():

    def __init__(self):

        self.credentials = service_account.ServiceAccountCredentials\
            .from_json_keyfile_name(
                SERVICE_ACCOUNT_KEY_FILE,
                GCS_SCOPE)

        self.http = self.credentials.authorize(httplib2.Http())
        self.service = build('storage', 'v1', http=self.http)


    def list_buckets(self):

        links = []
        request = self.service.objects().list(bucket=BUCKET)
        list_objects = request.execute()


        return list_objects['items']