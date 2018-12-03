from bs4 import BeautifulSoup
import csv
import urllib.request
import requests
import time
import re
import random
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='animes-Streaming')

def getCategory(url):
	print("------------first page------------")

	response = requests.get(url)

	soup = BeautifulSoup(response.content,'html.parser')
	table = soup.find('table')
	# print(table)

	animeNum = 0
	nextpage = True
	while nextpage:
		animeNum = animeNum + 1
		print(animeNum)
		try:
			tableTitleTr = table.find_all('tr')[animeNum]
			titleTd = tableTitleTr.find_all('td')[1]
			animeUrl = titleTd.find('a').get('href')

			response = requests.get(animeUrl)
			soup = BeautifulSoup(response.content,'html.parser')
			Title = soup.find('div',attrs={'id':'contentWrapper'}).find_all('div')[0].find('h1').get_text().strip()

			spaceit_pad = 0;

			try:
				EnglishGroup = soup.find_all('div',class_='spaceit_pad')[spaceit_pad]
				EnglishName = EnglishGroup.find_all('span')[0].text.strip()

				if EnglishName == 'English:':
					EnglishGroup.find('span').decompose()
					English = EnglishGroup.get_text().strip()
					spaceit_pad = spaceit_pad + 1
				else:
					English = ''	
			except Exception as e:
				English = ''

			try:
				SynonymsGroup = soup.find_all('div',class_='spaceit_pad')[spaceit_pad]
				SynonymsName = SynonymsGroup.find_all('span')[0].text.strip()

				if SynonymsName == 'Synonyms:':
					SynonymsGroup.find('span').decompose()
					Synonyms = SynonymsGroup.get_text().strip()
					spaceit_pad = spaceit_pad + 1
				else:
					Synonyms = ''
			except Exception as e:
				Synonyms = ''

			try:
				JapaneseGroup = soup.find_all('div',class_='spaceit_pad')[spaceit_pad]
				JapaneseName = JapaneseGroup.find_all('span')[0].text.strip()

				if JapaneseName == 'Japanese:':
					JapaneseGroup.find('span').decompose()
					Japanese = JapaneseGroup.get_text().strip()
				else:
					Japanese = ''
				
			except Exception as e:
				Japanese = ''
			
			try:
				TypeTxt = soup.find_all('div',class_='spaceit_pad')[spaceit_pad].find_next_sibling("div").find('a').text
				spaceit_pad = spaceit_pad + 1
			except Exception as e:
				TypeTxt = ''
				spaceit_pad = spaceit_pad + 1

			spaceit = 0
			try:
				EpisodesGroup = soup.find_all('div',class_='spaceit')[0]		
				EpisodesName = EpisodesGroup.find('span').text.strip()

				if EpisodesName == 'Episodes:':
					EpisodesGroup.find('span').decompose()
					Episodes = EpisodesGroup.get_text().strip()	
				else:
					Episodes = ''
				
			except Exception as e:
				Episodes = ''
			
			try:
				StatusGroup = soup.find_all('div',class_='spaceit')[spaceit].find_next_sibling("div")
				StatusName = StatusGroup.find('span').text.strip()
				if StatusName == 'Status:':			
					StatusGroup.find('span').decompose()
					Status = StatusGroup.get_text().strip()
					spaceit = spaceit + 1
				else:
					Status = ''
				
			except Exception as e:
				Status = ''

			try:
				AiredGroup = soup.find_all('div',class_='spaceit')[spaceit]
				AiredName = AiredGroup.find_all('span')[0].text.strip()

				if AiredName == 'Aired:':
					AiredGroup.find('span').decompose()
					Aired = AiredGroup.get_text().strip()
				else:
					Aired = ''
				
			except Exception as e:
				Aired = ''
			
			try:
				PremieredGroup = soup.find_all('div',class_='spaceit')[spaceit].find_next_sibling("div")
				PremieredName = PremieredGroup.find('span').text.strip()
				if PremieredName == 'Premiered:':			
					PremieredGroup.find('span').decompose()
					Premiered = PremieredGroup.get_text().strip()
					spaceit = spaceit + 1
				else:
					Premiered = ''
				
			except Exception as e:
				Premiered = ''

			try:
				BroadcastGroup = soup.find_all('div',class_='spaceit')[spaceit]
				BroadcastName = BroadcastGroup.find_all('span')[0].text.strip()

				if BroadcastName == 'Broadcast:':
					BroadcastGroup.find('span').decompose()
					Broadcast = BroadcastGroup.get_text().strip()
				else:
					Broadcast = ''
				
			except Exception as e:
				Broadcast = ''
			
			try:
				ProducersGroup = soup.find_all('div',class_='spaceit')[spaceit].find_next_sibling("div")
				ProducersName = ProducersGroup.find('span').text.strip()
				if ProducersName == 'Producers:':			
					ProducersGroup.find('span').decompose()
					Producers = ProducersGroup.get_text().strip()
					spaceit = spaceit + 1
				else:
					Producers = ''
				
			except Exception as e:
				Producers = ''	
			
			try:
				LicensorsGroup = soup.find_all('div',class_='spaceit')[spaceit]
				LicensorsName = LicensorsGroup.find_all('span')[0].text.strip()

				if LicensorsName == 'Licensors:':
					LicensorsGroup.find('span').decompose()
					Licensors = LicensorsGroup.get_text().strip()
				else:
					Licensors = ''
				
			except Exception as e:
				Licensors = ''
			
			try:
				StudiosGroup = soup.find_all('div',class_='spaceit')[spaceit].find_next_sibling("div")
				StudiosName = StudiosGroup.find('span').text.strip()
				if StudiosName == 'Studios:':			
					StudiosGroup.find('span').decompose()
					Studios = StudiosGroup.get_text().strip()
					spaceit = spaceit + 1
				else:
					Studios = ''
				
			except Exception as e:
				Studios = ''
			
			try:
				SourceGroup = soup.find_all('div',class_='spaceit')[spaceit]
				SourceName = SourceGroup.find_all('span')[0].text.strip()

				if SourceName == 'Source:':
					SourceGroup.find('span').decompose()
					Source = SourceGroup.get_text().strip()
				else:
					Source = ''
				
			except Exception as e:
				Source = ''
			
			try:
				GenresGroup = soup.find_all('div',class_='spaceit')[spaceit].find_next_sibling("div")
				GenresName = GenresGroup.find('span').text.strip()
				if GenresName == 'Genres:':			
					GenresGroup.find('span').decompose()
					Genres = GenresGroup.get_text().strip()
				else:
					Genres = ''
			except Exception as e:
				Genres = ''
			

			cursor = cnx.cursor()
			sql = "INSERT INTO `animes` (`Title`, `TypeTxt`, `Episodes`, `Status`, `Aired`, `Premiered`, `Broadcast`, `Producers`, `Licensors`, `Studios`, `Source`, `Genres`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (Title, TypeTxt, Episodes, Status, Aired, Premiered, Broadcast, Producers, Licensors, Studios, Source, Genres))	

			print(Title + " " + TypeTxt + " " + Episodes + " " +Status)
			print('----------------------------------------')

			cnx.commit()

			cursor.close()
			

		except Exception as e:
			print('== nextpage ==')
			nextpage = False

if __name__ == "__main__":
	print('welcome start:')

	getCategory("https://myanimelist.net/topanime.php?limit=0")

cnx.close()

print('-------------------------- ALL SUCCESS!----------------------------')





#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.publix.com/product%20catalog/ProductContent?pid=RIO-PCI-106711&tab=overview&storeid=794', headers=headers, cookies=cookies)
