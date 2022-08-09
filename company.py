from random import randint
from time import sleep
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
all_dict=[]
def collect_users(fullLink):
    browser.get(fullLink)
    src=browser.page_source
    soup=BeautifulSoup(src,'lxml')
    company_people=soup.find_all('span',{'class':'entity-result__title-text'})
    company_people_place=soup.find_all('div',{'class':'entity-result__secondary-subtitle'})
    people_designation=soup.find_all('div',{'class':'entity-result__primary-subtitle'})
    people_list=[]
    place_list=[]
    designation_list=[]
    for i in range(len(company_people)):
        people_list.append(company_people[i].find('a').get_text().strip())
        place_list.append(company_people_place[i].get_text().strip())
        designation_list.append(people_designation[i].get_text().strip())
    for i in range(len(people_list)):
        mydict={"name":people_list[i],"designation":designation_list[i],"place":place_list[i]}
        all_dict.append(mydict)


for i in range(1,4):  #Enter the pages (1,total pages+1) 
    x=randint(1,10)
    sleep(x)
    visitingProfile='/search/results/people/?keywords=<company_name>&page='+str(i)
    fullLink='https://www.linkedin.com'+visitingProfile
    collect_users(fullLink)
        # print(people_list[i],place_list[i])
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["TurtlefinEmp-db"]
mycol = mydb["Employees"]
for dict in all_dict:
        # print(dict)
    mycol.insert_one(dict)





