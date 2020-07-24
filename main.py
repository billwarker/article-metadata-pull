import requests
import json
import pandas as pd
from df_to_sheets import df_to_google_sheets
from config import Config
import flask

def contentful_api_request(url, headers, params):
    """Makes a GET request to Contentful's Content Delivery API.
    Args:
        url (string): URL
        headers (dict): header with token to insert into request
        params (tuple): nested tuples with parameters to insert into request
    Returns:
        response (requests.models.response): request object with API data
    """
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"successful request to contentful api [{response.status_code}]")
        return response
    else:
        print(f"ERROR: [{response.status_code}]")
    assert response.status_code == 200

def articles_to_df(response, sys_data, fields_data):
    """Extracts data fields from article entries and loads them into a dataframe.
    Args:
        response (requests.models.response): response to extract list on article entries from
        sys_data (list): list of fields to extract from the article entry's sys json
        fields_data (list): list of fields to extract from the article entry's fields json
    Returns:
        df (pandas.Dataframe): dataframe object
    """
    df_dict = {}

    article_count = 0
    json_response = json.loads(response.text)
    entries = json_response['items']
    for article in entries:
        article_metadata = {}
        for key in sys_data:
            try:
                article_metadata[key] = article['sys'][key]
            except KeyError:
                article_metadata[key] = ''
        for key in fields_data:
            try:
                article_metadata[key] = article['fields'][key]
            except KeyError:
                article_metadata[key] = ''
        df_dict[article_count] = article_metadata
        article_count += 1

    df = pd.DataFrame(df_dict.values(), columns=(sys_data + fields_data))
    assert len(df) != 0
    return df

def main(request):  
    print('executing function...')
    status = {"success": False}

    if "run" in request.get_json(force=True):
        c = Config()
        response = contentful_api_request(c.REQUEST_URL, c.REQUEST_HEADERS, c.REQUEST_PARAMS)
        df = articles_to_df(response, sys_data=c.SYS_DATA, fields_data=c.FIELDS_DATA)
        if c.SAVE_CSV_FILE == 'Y':
            df.to_csv(c.CSV_FILE, index=False)
        df_to_google_sheets(df=df,
                            scope=c.SCOPE,
                            spreadsheet=c.SPREADSHEET,
                            sheet_ix=c.SHEET_IX,
                            user_share_list=c.USER_SHARE_LIST)
        status["success"] = True
    
    return flask.jsonify(status)

if __name__ == "__main__":

    app = flask.Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def test():
        request = flask.request
        result = main(request)
        return result

    app.run(host='0.0.0.0')