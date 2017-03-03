import time
import sys
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from twilio.rest import TwilioRestClient 


class ExpediaScraper():

    def main(self):  
        while True:
            self.searchsite()
            time.sleep(3600) #try again every hour if deal isn't found

    def getargs(self):
        
       
        self.departfrom = input("Flying From (e.g, SFO): ")
        self.flyto = input("Flying To: ")
        self.departdate = input("Departure Date (e.g, 03/02/2017): ")
        self.returndate = input("Return Date: ")

        #Make sure passenger input is correct
        while True:
            try:
                self.passengers = int(input("Enter Number of Adults (Up to 6): "))
            except ValueError:
                print("That's not a valid input")
            else:
                if 1 <= self.passengers <= 6:
                    break
                else:
                    print("Still not in range. Try Again.")
        
        #Get max price
        self.desiredprice = input("What's the maximum you'd like to spend in dollars? (e.g. 550): ")

        self.searchsite()
    
    def searchsite(self):
        driver = webdriver.PhantomJS()
        driver.get("http://www.expedia.com")
        
        #Flights only
        select_flight = driver.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
        select_flight.click()

        #Input Origin
        select_origin = driver.find_element_by_id('flight-origin-hp-flight')
        select_origin.send_keys(self.departfrom)

        #Input Destination
        select_destination = driver.find_element_by_id('flight-destination-hp-flight')
        select_destination.send_keys(self.flyto)

        #Input Departure Date
        select_departure = driver.find_element_by_id('flight-departing-hp-flight')
        select_departure.send_keys(self.departdate)

        #Input Returning Date
        select_returning = driver.find_element_by_id('flight-returning-hp-flight')
        select_returning.send_keys(self.returndate)

        #Input # of Adults & Search button workaround
        select_adults = driver.find_element_by_id('flight-adults-hp-flight')
        select_adults.send_keys(self.passengers)

        #Locate and click the search button
        select_search = driver.find_elements_by_class_name('btn-label')[18]
        select_search.click()

        #Send to scrape function
        time.sleep(15)
        self.scrape(driver)
        
        
    def scrape(self, driver):
        price_array = []
        #get prices
        prices = driver.find_elements_by_xpath("//span[@class='dollars price-emphasis']")
        for theprices in prices:
            finalprice = theprices.text
            price_array.append(finalprice[1:])
        min_price = min(price_array)

        if int(min_price) <= self.desiredprice:
            self.notifyuser(min_price)
        else:
            print("No match found in this run. We'll try again.")
            driver.quit()
            return

    def notifyuser(self, min_price):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        print("\nWe found a steal!", min_price,"for roundtrip from",self.departfrom,"to",self.flyto, current_time)
        #send twilio SMS message alert
        # EDIT THESE SETTINGS
        ACCOUNT_SID = "TWILIO ACCOUNT SID" 
        AUTH_TOKEN = "TWILIO AUTH TOKEN"        
        FROM_NUMBER = "TWILIO ASSIGNED NUMBER"
        TO_NUMBER = "SEND DEAL UPDATE TO THIS NUMBER" 

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
        
        client.messages.create(
        to=TO_NUMBER, 
        from_=FROM_NUMBER, 
        body=("Deal found. ",min_price)
        )
        sys.exit()


if __name__ == "__main__":
    print("\nI'll help you lookup the cheapest roundtrip ticket on expedia.com\n")
    scraper = ExpediaScraper()
    scraper.getargs()
    scraper.main()
