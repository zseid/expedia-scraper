import unittest, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class ExpediaScraper():

    def main(self):
        print("\nI'll help you lookup the cheapest roundtrip ticket on expedia.com\n")
        self.getargs()

    def getargs(self):
        
        """
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
        
        Get max price
        self.desiredprice = input("What's the maximum you'd like to spend in dollars? (e.g. 550): ")
        """
        self.departfrom = "SFO"
        self.flyto = "LAS"
        self.departdate = "03/02/2017"
        self.returndate = "03/04/2017"
        self.passengers = "4"

        
        self.scrape()
    
    def scrape(self):
        driver = webdriver.Firefox()
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
        select_adults.click()
        driver.implicitly_wait(15)
        select_adults.send_keys(Keys.TAB)
        select_adults.click()
        select_adults.send_keys(Keys.TAB)
        select_adults.send_keys(Keys.TAB)
        select_adults.send_keys(Keys.TAB)
        select_adults.send_keys(Keys.TAB)




if __name__ == "__main__":
    scraper = ExpediaScraper()
    scraper.main()
