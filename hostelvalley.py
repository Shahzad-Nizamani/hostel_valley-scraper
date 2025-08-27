from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import json

def scroll():
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get("https://hostelvalley.com/hostels?city=Karachi")

    scroll_pause = 2 
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("✅ Reached end of page, all hostels loaded")
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html , "html.parser")
    div = soup.find("div", "Hostelcard")
    tags = div.find_all('a')
    
    links = []
    for tag in tags:
        link = "https://hostelvalley.com" + tag.get("href")
        links.append(link)

    print("Scrolled until the end and got all the links>>>")
    driver.quit()
    return links

def scrap_page():
     service = Service('chromedriver.exe')
     driver = webdriver.Chrome(service=service)
     
     data = []
     links = scroll()

     for link in links:
        hostel = {}
        driver.get(link)

        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "phone-button")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button) 
        driver.execute_script("arguments[0].click();", button) 


        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        namediv = soup.find("div", class_="left-column")
        name = namediv.find("h1").text.strip()
        hostel["name"] = name
        print(name)

        hostel["price"] = soup.find("h2", class_="price").text
        print(hostel["price"])

        descrpition_div = soup.find("div", class_="description")
        desc = descrpition_div.find("p").text.strip()
        hostel["description"] = desc
        print(desc)

        lis = descrpition_div.find_all("li")
        hostel["location"] = lis[0].text.split(":")[1].strip()
        print(hostel["location"])

        hostel["city"] = lis[1].text.split(":")[1].strip()
        print(hostel["city"])
    
        hostel["gender"] = lis[2].text.split(":")[1].strip()
        print(hostel["gender"])

        hostel["owner"] = soup.find("div", class_="seller-name").text.strip()
        print(hostel["owner"])

        hostel["number"] = soup.find("div", "number-container").text.strip()
        print(hostel["number"])

        data.append(hostel)
    
     with open("hv_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
     driver.quit()
        

if __name__ == "__main__":
    scrap_page()