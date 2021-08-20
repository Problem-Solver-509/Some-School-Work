# webscraper v.4
# Updated 12/5/2019 1:02pm
# Added Y or N for emailing
# Added input phone for texting
# Added clean string for list of deals

# To be added - user input email address?

from bs4 import BeautifulSoup
import re
import requests
from tabulate import tabulate
import smtplib
import json
from twilio.rest import Client
import random
import time

# requesting website and "soupifying" it

url = "https://dealsea.com/Laptops-Desktops-Tablets/b?node=3001"
main_url = 'https://dealsea.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table = []

# loop to sort into list with embedded dictionary

for d in soup.findAll('div', class_='dealbox'):

    # Get deal name
    find_a = d.findAll('a')
    deal_name = str(find_a[1].find(text=True).encode('utf-8'))

    # Get vendor name
    find_a = d.findAll('a')
    vendor_name = str(find_a[2].find(text=True))

    # Get Vendors
    vendors = d.find_all(href=re.compile(r"\/j\/4\/\?pid\="))
    vendors_dict = {}
    for v in vendors:
        vendor_name = str(v.find(text=True).encode('utf-8'))
        vendor_link = main_url + str(v['href'])
        if vendor_name not in vendors_dict:
            vendors_dict[vendor_name] = []
        vendors_dict[vendor_name].append(vendor_link)

    # Get deal content
    deal_content = d.findAll('div', class_='dealcontent')[0].find(text=True)

    # Add information to the table
    table.append([deal_name, vendors_dict, deal_content])

# Output Message
print('There are', len(table), 'deals found.')
print('A list of deals can be found in the file named scraper_table.txt')

# Write table to text file

with open('scraper_table.txt', 'w') as scraper_table:
    scraper_table.write(tabulate(table))


# scraper_table.txt

# Email list of deals

def send_email(subject2, message_from_space):
    email_address = 'XXXXXXXXXXXXXXXXXX'
    password = 'XXXXXXXXXXXX!'
    try:
        server = smtplib.SMTP('XXXXXXXXXXXX')
        server.ehlo()
        server.starttls()
        server.login(email_address, password)
        message = 'Subject: {}\n\n{}'.format(subject2, message_from_space)
        server.sendmail(email_address, email_address, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


def cleanString(inputstring):
    inputstring = inputstring.replace("b'", "")
    lastpos = len(inputstring) - 1
    if inputstring[lastpos] == "'":
        inputstring = inputstring[:-1]
    return inputstring


dealInfoList = []
dealstring = ''

# This loop makes a list of deals and cleans up the text
for i in range(len(table)):
    tempdeal = cleanString(table[i][0])
    dealInfoList.append(table[i][0])
    # dealstring = dealstring + dealInfoList[i] + '\n'
    dealstring = dealstring + 'Deal #' + str(i + 1) + ': ' + tempdeal + '\n'

# subject1 = "Emailed list of what was scraped from Dealsea"
subject1 = "Emailed list of DEALS from Dealsea"

json_output = json.dumps(table)

sendEmail = input('Would you like an email sent with the list of deals? (Y or N) ')
# sendEmail = 'N'
if sendEmail.upper() == 'Y':
    send_email(subject1, json_output)
    send_email(subject1, dealstring)

# Send a text message


account_sid = 'XXXXXXXXXXXXXXXXXXXXX'  # Found on Twilio Console Dashboard
auth_token = 'XXXXXXXXXXXXXXXXXXXXX'  # Found on Twilio Console Dashboard
TwilioNumber = '+XXXXXXXXX  # Phone number given to you by Twilio'
client = Client(account_sid, auth_token)

myPhoneAG = 'XXXXXXXXXX'  # Anthony's number
myPhoneRV = 'XXXXXXXXX'  # Raul's number
myPhoneSS = 'XXXXXXXX'  # Steve's number
myPhoneED = 'XXXXXXXXXX'  # Eden's number
PhoneNumbers = ['XXXXXXXXXXXXX', 'XXXXXXXXXXXX', 'XXXXXXXXXXX', 'XXXXXXXXXXXXX']

# Below will select a random deal to text


dealnum = random.randint(0, len(table))
dealtotext = cleanString(table[dealnum][0])

UserinputNumber = eval(input('Enter your phone number to text a deal or 0 for quit, e.g. XXXXXXXXXXXXX: '))

if UserinputNumber != 0:
    UserinputNumber = '+1' + str(UserinputNumber)
    client.messages.create(
        to=UserinputNumber,
        from_=TwilioNumber,
        body=dealtotext)
    print('Messsage Sent, good luck with your deal!')
else:
    print('Thanks and enjoy your deal!')

# Change for loop below to send to all or just a few of the numbers in the list PhoneNumbers
# for i in range(len(PhoneNumbers)):

for i in range(0):  # This will send a text to the first number in the list or Raul
    client.messages.create(
        to=PhoneNumbers[i],
        from_=TwilioNumber,
        body=dealtotext)

print('Deals Display')
time.sleep(3)

for i in range(len(table)):
    for j in range(3):
        print(table[i][j])
