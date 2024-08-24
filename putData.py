import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1C5es17V2rmtma1iFW3h9xhhKwaBdZf2yTLaMrsiTWU0"
SAMPLE_RANGE_NAME = "Sheet1!A1:C"


def main():
    """Shows basic usage of the Sheets API.
    Writes data to a sample spreadsheet.
    """
    creds = None
    # Load or authenticate credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        # The data you want to insert into the sheet
        # values = [
        #     ["Name", "Age", "Major"],
        #     ["John Doe", "21", "Computer Science"],
        #     ["Jane Smith", "22", "Mathematics"],
        # ]
        body = {"values": data}

        # Write the data to the sheet
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                valueInputOption="RAW",  # 'RAW' means input as entered; 'USER_ENTERED' interprets data types
                insertDataOption="INSERT_ROWS",  # To append new rows
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updates').get('updatedCells')} cells appended.")

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()