# -*- coding: utf-8 -*-
import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
# import json
import os
import datetime
import time
import re

print('Loading-------')

currentDT = datetime.datetime.now()

print('current date:' + str(currentDT))

driver = webdriver.Chrome()
driver.set_window_size(1400, 1000)

driver.get("https://www.masterani.me/anime")
time.sleep(3)
a = 1
direct = True

while direct:
	try:
		driver.find_element_by_xpath("//*[@id='explore']/div/div[2]/div/div/div[2]/div[1]/a").click()
		time.sleep(3)
		driver.find_element_by_xpath("//*[@id='details']/div[1]/a").click()
		time.sleep(3)
		
		iframe = driver.find_element_by_xpath("/html/body/div[2]/div/div/iframe").get_attribute("src")
		print(iframe)
		time.sleep(1)
		driver.find_element_by_xpath("/html/body/div[2]/div/i").click()
		time.sleep(1)

		driver.find_element_by_xpath("//*[@id='stats']/div/div[3]/div[2]/div[1]/div[1]/div/a").click()
		time.sleep(3)

		anime = driver.find_element_by_xpath("//*[@id='watch']/div/div[1]/div/div[3]/div/div/iframe").get_attribute("src")

		print(anime)
		exit()
		if direct_phone_name == "Telefon:" :
			direct_phone = driver.find_element_by_xpath("//main[@class='o-grid__item  o-content-section  [ u-2/3@lap-and-up ]  s-content']/div[@class='o-grid'][1]/div/div[1]/div[@class='c-post__text']/div["+str(a)+"]").text
			direct_phone = direct_phone.split(":")[-1].strip()
			print(direct_phone)

		elif direct_phone_name == "E-post:" :
			email = driver.find_element_by_xpath("//main[@class='o-grid__item  o-content-section  [ u-2/3@lap-and-up ]  s-content']/div[@class='o-grid'][1]/div/div[1]/div[@class='c-post__text']/div["+str(a)+"]/a").text
			print(email)
	except Exception as e:
		direct = False
		break
	a = a + 1	

driver.close()