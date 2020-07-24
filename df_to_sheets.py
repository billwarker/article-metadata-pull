
import gspread
import google.auth
import pandas as pd
from gspread_dataframe import set_with_dataframe
import json
import os

def df_to_google_sheets(df, scope, spreadsheet, sheet_ix, user_share_list):
    creds, project = google.auth.default(scopes=scope)
    client = gspread.authorize(creds)
    print(f"""
    successful connection to Google Drive.
    project: {project}
    scopes: {scope}
    """)

    sheets = client.list_spreadsheet_files()
    if sheets == None or spreadsheet not in [file['name'] for file in sheets]:
        print(f"creating new spreadsheet '{spreadsheet}'")
        client.create(spreadsheet)
    
    google_sheet = client.open(spreadsheet)
    worksheet = google_sheet.get_worksheet(sheet_ix)
    set_with_dataframe(worksheet, df)
    print(f"uploaded data into Google Sheet: '{google_sheet.title}'")

    print(f"sharing '{google_sheet.title}' with users...")
    for user in user_share_list:
        google_sheet.share(value=user['email'], perm_type=user['perm_type'], role=user['role'])
        print(f"shared with {user['email']}. role: {user['role']}")