from google.cloud import secretmanager

class Config:
    # access secrets from GCP secret manager
    client = secretmanager.SecretManagerServiceClient()
    api_token_secret = client.secret_version_path('article-metadata-pull',
                                                  'amp-contentful-api-token',
                                                  '1')
    space_secret = client.secret_version_path('article-metadata-pull',
                                              'amp-contentful-space-id',
                                              '1')

    # settings for contentful-fetch.py
    CONTENTFUL_API_TOKEN = client.access_secret_version(api_token_secret).\
                           payload.data.decode('UTF-8')
    CONTENTFUL_SPACE_ID = client.access_secret_version(space_secret).\
                          payload.data.decode('UTF-8')
    REQUEST_URL = f'https://cdn-mr.contentful.com/spaces/{CONTENTFUL_SPACE_ID}/environments/master/entries'
    REQUEST_HEADERS = {'Authorization': f'Bearer {CONTENTFUL_API_TOKEN}',}
    REQUEST_PARAMS = (('skip', '0'),
                      ('content_type', 'article'),
                      ('limit', '1000'))
    SYS_DATA = ['id', 'createdAt', 'updatedAt']
    FIELDS_DATA = ['articleTitle', 'subTitle', 'slug', 'status', 'lifecycleTag']
    SAVE_CSV_FILE = 'N'
    CSV_FILE = 'tmp.csv'

    # settings for df-to-sheets.py
    SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    SPREADSHEET = 'Business Support - Contentful Articles'
    SHEET_IX = 0
    USER_SHARE_LIST = [{'email': 'will.barker@telus.com', 'perm_type': 'user', 'role': 'writer'},
                       {'email': 'will.barker1@telus.com', 'perm_type': 'user', 'role': 'writer'}]

if __name__ == "__main__":
    c = Config()
    print(c.CONTENTFUL_API_TOKEN)
    print(c.CONTENTFUL_SPACE_ID)