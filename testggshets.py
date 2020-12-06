import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Jorge Cano/Documents/GitHub/huiini/credentials.json', scope)
client = gspread.authorize(credentials)
#work_sheet = gspread.create("Huinni intento 1")

# title = "huevos google"
#
# drive_api = build('drive', 'v3', credentials=credentials)
#
# #logger.info("Creating Sheet %s", title)
# body = {
#     'name': title,
#     'mimeType': 'application/vnd.google-apps.spreadsheet',
# }
#
#
# req = drive_api.files().create(body=body)
# new_sheet = req.execute()
# spread_id = new_sheet["id"]
# print(spread_id)

spread_id = "16cb7j7JgFRvwNp3Acw5tY6WCqNFWr1GKCql1t8ry88s"
spread = client.open_by_key(spread_id)

# rfc_sheet = spread.add_worksheet(title="por RFC", rows="100", cols="20")
# facturas_sheet = spread.add_worksheet(title="por factura", rows="100", cols="20")

rfc_sheet = spread.worksheet("por RFC")
facturas_sheet = spread.worksheet("por factura")

# rfc_sheet.update_cell(1, 2, 'Bingo!')
#
# facturas_sheet.update_cell(1, 2, 'bamba!')
val = rfc_sheet.cell(1, 2).value
val2 = facturas_sheet.cell(1, 2).value
print(val, val2)


#libro = client.open("Metropoli2019")
# ss = client.open("Metropoli2019")
# ws = ss.worksheet("Bancos")
