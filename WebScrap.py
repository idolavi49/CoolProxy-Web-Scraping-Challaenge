from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


class CoolProxy:

    # Initialize variables
    URL = "https://cool-proxy.net/"
    ipList = []
    portList = []

    # Configure the Webdriver automation settings
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options, executable_path=r'chromedriver.exe')

    # Click the next page button and move to the next page on the table
    def nextPage(self):
        next_page = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/table/tbody/tr[23]/th/dir-pagination-controls/ul/li[5]/a')
        next_page.click()

    # Get the all the ip's and ports from the table page
    def getPage(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        rows = soup.find_all('tr', class_='proxy-row ng-scope')
        for row in rows:
            result = row.find_all('td')
            ip = result[0].text
            port = result[1].text
            self.ipList.append(ip)
            self.portList.append(port)

    # Save all the ip's and ports from all pages into a csv file
    def addToCSV(self):
        with open('WebScrap.csv', 'a+', newline='') as file:
            fieldnames = ['IP', 'Port']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for index in range(1, len(self.ipList)):
                ip = self.ipList[index]
                port = self.portList[index]
                writer.writerow({'IP': ip, 'Port': port})
            file.close()

    # Start the whole scraping process and calling all the functions, last it will stop the automation
    def scrap_website(self):
        self.driver.get(self.URL)
        self.getPage()
        self.nextPage()
        self.getPage()
        self.addToCSV()
        self.driver.quit()

# Main: start the web scraper
if __name__ == '__main__':
    cp = CoolProxy()
    cp.scrap_website()
