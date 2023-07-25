# import configparser
# import time
import csv
from whatsapp_scrapper import WhatsappScrapper

def start_scraping(BASE_URL, numbers):
    """ Loading all the configuration and opening the website
        (Browser profile where whatsapp web is already scanned)
    """
    web = WhatsappScrapper()
    with open("WA.csv",'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Number','Name','Profile_pic','last_seen','status'])
        
    with open("WA.csv",'a+') as csvfile:
        csvwriter = csv.writer(csvfile)

        for num in numbers:
            page = BASE_URL.format(num)
            web.driver.get(page)

            # open_conversation() not in use currently
            # if scrapper.open_conversation(f'+91 {num[:5]} {num[5:]}'):

            contact_name, profile_pic, last_seen, status = web.get_contact_info()
            csvwriter.writerow([num,contact_name, profile_pic, last_seen, status])



if __name__ == '__main__':
    BASE_URL = 'https://web.whatsapp.com/send/?phone={}&text&type=phone_number&app_absent=1'

    print("Input format:\n9876543210 9988776655 9898767654")
    print("NOTE: program will not function stop is number is not on registered on WhatsApp.")
    numbers = input("Enter WhatsApp numbers seperated by space:\n").split(" ")
    start_scraping(BASE_URL, numbers)