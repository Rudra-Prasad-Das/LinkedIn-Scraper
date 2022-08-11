from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo
browser=webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get('https://www.linkedin.com/uas/login')
file=open('config.txt')
lines=file.readlines()
username=lines[0]
password=lines[1]
element_ID=browser.find_element(By.ID,"username")
element_ID.send_keys(username)
# print(username)
# print(password)
element_ID=browser.find_element(By.ID,"password")
element_ID.send_keys(password)
element_ID.submit()
visitingProfile='/in/<profile-name>/'
fullLink='https://www.linkedin.com'+visitingProfile
browser.get(fullLink)
src=browser.page_source
soup=BeautifulSoup(src,'lxml')
# print(soup)
name_div=soup.find_all('h1')
# print(name_div)
# name_loc=name_div.find_all('ul')
name=soup.find('h1').get_text().strip()
print(name)
loc_div=soup.find('span',{'class':'text-body-small'}).get_text().strip()
# name_loc=loc_div.find_all('span')
print(loc_div)
contact_link='overlay/contact-info/'
profileLink='https://www.linkedin.com'+visitingProfile+contact_link
browser.get(profileLink)
src=browser.page_source
soup=BeautifulSoup(src,'lxml')
contact_dict=[]
contact_details=soup.find_all('a',{'class':'pv-contact-info__contact-link'})
for i in range(len(contact_details)):
    contact_dict.append(contact_details[i].get_text().strip())
# print(contact_details[0].get_text().strip())
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["LinkedInContact-db"]
mycol = mydb["users"]
mydict = { "name": name, "location":loc_div,"contact-info":contact_dict}
mycol.insert_one(mydict)

