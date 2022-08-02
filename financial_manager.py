import csv
import gspread
import time
# ACCOUNT = input("Enter Account: (chequing/mastercard): ")
# MONTH = input("Enter the month in lowercase: ")
ACCOUNT = "chequing"
MONTH = "july"
file = f'./data/{ACCOUNT}/{MONTH}.csv'
print("Now handling: " + file)
transactions = []

CHECK_CRIT = {"SALARY": [],
              "FOOD": ["FANTUAN", "FACEDRIVEFOODRIDESHARE", "MCDONALD'S", "STARBUCKS",
                       "DOMINOS", "A&W", "YIFANG", "ROLLTATION", "IDP", "YUNXI", "ORIENTAL"],
              "RENT_BILLS": ["CARRY", "BIRDIE", "ROGERS", "CHEQUE"],
              "TRANSPORT_TRAVEL": ["UBER", "LYFT", "PRESTO"],
              "SUBSCRIPTION": ["ADOBE", "GOOGLE*YOUTUBE", "Netflix.com",
                               "Amazon.ca", "Spotify", "NOTION", "Wix.com", "HAHAHA", "APPLE.COM/BILL",
                               "GENIUSLINK", "GOOGLE*YOUTUBEPREMIUM", "Hostinger", "LAF", "TWITCH"],
              "GROCERIES": ["DOLLARAMA", "AMZN", "WAL-MART", "METRO", "SHOPPERS", "NOFRILLS", "FOODY"],
              "OTHERS": ["BLIZZARD", "E-TRANSFER", "PTB", "RBC", "CANVAPE", "WWW",
                         "OLG", "C", "1", "OD",  "Wealthsimple", ],
              "EDUCATION": ["Centennial", "CENTENNIAL", "MCGRAW", "NEWEB-Schools", ]
              }


def check_all(trans_name):
    check_complete = False
    while check_complete == False:
        for categories, checking in CHECK_CRIT.items():
            final = check_categories(trans_name, categories, checking)
            if final == "next":
                continue
            else:
                return final


def check_categories(tranaction_name, categories_name, checking_method):
    for word in tranaction_name.split():
        if word == "PAYMENT":
            return "PAYMENT"
        if word in checking_method:
            return categories_name
        else:
            return "next"


def rbcFin(file):
    print(ACCOUNT)
    if ACCOUNT == 'chequing':
        with open(file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                account = row[0]
                date = row[2]
                name = row[5]
                amount = float(row[6])
                transaction = (date, name, check_all(name), amount, account)
                print(transaction)
                transactions.append(transaction)
    else:
        with open(file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # print(row)
                account = row[0]
                date = row[2]
                name = row[4]
                amount = float(row[6])
                transaction = (date, name, check_all(name), amount, account)
                transactions.append(transaction)
    return transactions


sa = gspread.service_account()
sh = sa.open("Personal Finances - 2022")
wks = sh.worksheet(f"{MONTH}")

rows = rbcFin(file)

for row in rows:
    wks.insert_row([row[0], row[1], row[2], row[3], row[4]], 3)
    time.sleep(1)
