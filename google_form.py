
import time
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

def getData(sheet_id):
    sheet_link = 'https://docs.google.com/spreadsheets/d/e/' + sheet_id + '/pubhtml'

    # Send an HTTP GET request to the published Google Sheet
    response = requests.get(sheet_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    # Extract data from the table (assuming the first row contains headers)
    data = []
    for row in table.find_all('tr')[1:]:  # Skip the first row (headers)
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]
        data.append(row_data)

    return data

def updateData():
    client = MongoClient("mongodb+srv://ams1234:ams1234@cluster0.ph4hzjn.mongodb.net/")
    db = client["AMS-Test"]
    col = db["Doctor"]
    sheet_id = "2PACX-1vQ_tqXWFpe_JWnY80yyRid4_JjAdlnoGb235Abbf9MUHQBYZQ4LdRLwgBVuZMvNp6q3HDX8oQJSlh4w"
    for i in getData(sheet_id):
        document = col.find_one({"doctor_id": i[1]})
        document["status"] = i[2]
        