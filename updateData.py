import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of your spreadsheet.
SPREADSHEET_ID = '150NSVkA3dKJGXme6cg6fWuDkOF3iB2my-YbgUn-x9v0'
RANGE_NAME = 'Sheet1!A:C'  # Assuming columns A, B, and C correspond to num1, num2, and addition

def main():
    creds = None
    # Load credentials from token.json, or go through OAuth flow
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Get current data from the sheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print("No data found in the sheet.")
            return

            
        updated_values = [values[0]]  # Keep the header row
        # Process each row to calculate addition
        values = values[1:]  # Skip the header row
        
        for row in values:
            if len(row) >= 2:  # Ensure there are at least num1 and num2
                try:
                    num1 = float(row[0])
                    num2 = float(row[1])
                    addition = num1 + num2
                except ValueError:
                    addition = "Error"  # Handle any non-numeric values gracefully
                row.append(addition)  # Append the calculated addition
            else:
                row.append("Error")  # Handle rows with missing values

            updated_values.append(row)

        # Update the addition column in the sheet
        body = {
            'values': updated_values
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"{result.get('updatedCells')} cells updated.")

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()