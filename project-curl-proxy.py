from bs4 import BeautifulSoup
import csv
import urllib.request
import requests
import time
import re
import random

proxies = [{"https": "https://107.175.14.34:80"},
           {"https": "https://104.140.243.86:80"},
           {"https": "https://23.106.237.196:80"},
           {"https": "https://172.245.103.212:80"},
           {"https": "https://172.245.211.239:80"},
           {"https": "https://206.41.185.79:80"},
           {"https": "https://104.223.23.217:80"},
           {"https": "https://185.198.222.120:80"},
           {"https": "https://107.174.150.201:80"},
           {"https": "https://45.61.169.68:80"},
           {"https": "https://198.23.216.196:80"},
           {"https": "https://155.94.219.123:80"},
           {"https": "https://196.247.5.104:80"},
           {"https": "https://173.44.154.241:80"},
           {"https": "https://154.16.45.32:80"},
           {"https": "https://200.10.37.124:80"},
           {"https": "https://209.99.164.122:80"},
           {"https": "https://64.110.132.237:80"},
           {"https": "https://198.245.69.10:80"},
           {"https": "https://107.172.170.224:80"},
           {"https": "https://173.44.165.130:80"}]

def getproxy():
	proxy = random.randint(0, 20)
	return proxy

def getLast_SubCategoryData(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, proxy):
	print("---------- Last_sub_Category-------------")
	print(sub_sub_Category_url)
	uidArray = sub_sub_Category_url.split('/')

	uid = uidArray[len(uidArray)-1].split('?')[1].split('&')[0].split('=')[1]

	soup = ''
	pagenation = True
	page = 1
	last_proxy = 1000
	while pagenation:

		last_proxy_status = True
		count = ''
		while last_proxy_status:
			if last_proxy == 1000:
				last_proxy = getproxy()
					
			try:
				cookies = {
					'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
					'_ga': 'GA1.2.368746558.1542651026',
					'_gid': 'GA1.2.2113382898.1542651026',
					'_gcl_au': '1.1.1739095652.1542651028',
					'ajs_user_id': 'null',
					'ajs_group_id': 'null',
					'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
					'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
					'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
					'PublixWeeklyAdBreakDay': '5',
					'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
					'rememberLogin': 'james.wmsoft%40outlook.com',
					'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
					'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
					'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
					'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
					'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
					'_instacart_session': 'anNaaXVPd0l6SC92VS9BcW1HTjlEMWJpYVlWZE13TExaN2NrYkw0YUFFQVpZSzRlcnFOTWVzQUJzNzVKQ2hwUTk4SzFyNUZiajZWSlJGeFV0UTdBL09mektKbGR1Sjl5MExzQUVYNVpOUC8zWFBKVkNhdkR2cnZGWUk1Y09TdlRqMXhzTnhYVkpnamd2WnB2dVFiS2o4M1NnYzl4aFFyNXd2UDNzUU9JRHc1M0pvc21YWFJDeTJIUXQ0REJQSnBiTjJRN0g5R0FwSWVFM1lLNVRFME81Zz09LS1LOHAwbW9zV25UTDF6R2p3Yk9XTUh3PT0%3D--38ba29e0e960b120a0d5c5ee91346f62979ec3a9',
					'_fbp': 'fb.1.1542751470414.206344019',
					'_litra_ses.6f02': '*',
					'sitecore_rcp': 'RIO-PCI-127944|RIO-PCI-130614|RIO-PCI-132901|RIO-PCI-197707|RIO-PCI-102884|RIO-PCI-129601|RIO-PCI-120900|RIO-PCI-109687|RIO-PCI-108986|RIO-PCI-114611|RIO-PCI-119232|RIO-BPL-282299|RIO-PCI-102979|RIO-PCI-106711|RIO-PCI-116836|RIO-PCI-152574',
					'__AntiXsrfToken': '16c39591944d4afbb55cd22c28c7e23a',
					'_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.14.1542758026.1542751470.c2eb9561-d14b-403f-a7eb-2bb288916fca',
					'_4c_': 'dVFdi9swEPwrxz70yedIsmRZhlBKD47%2BgKOPhyzJsakTGVmuU4L%2Fe1b5oCFwNizanfHsaHyCpXMHqKngTIqKKsYUz%2BCP%2BzdBfQIzpvo3lTkMUEMX4zjVm82yLPk4N0N%2FzI3fb8bg7Wziq9FRD35374d%2Biv1h9910W5VTfL%2BNeue2FDJogl8mF1DyZxf83r1IglPjrcMRVXmRl9i3uB%2BKspK8FKLKk8tSUMIS5tEh%2FO4PFoWwDa51IVwUsZv6mIT%2BW8RZdGGfvsHjiFcCgYfBGz0kJoaQwfuPz49fb1%2BvtJgUWNfqeYiwZnC8BldxjiRJKe6ImFJVcpIeZITe3hKEhjjVWikrizkLUzCrnOSscVqXjpYG9S96guCvIEwVgqEAbrsJsEecFoxKmnC0dNW%2F%2B3qiCZ589HeWfsIFqVTyudwID4Aiz1RF1nU9Aw%3D%3D',
				}

				headers = {
					'Connection': 'keep-alive',
					'Pragma': 'no-cache',
					'Cache-Control': 'no-cache',
					'Upgrade-Insecure-Requests': '1',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept-Language': 'en-US,en;q=0.9',
				}

				params = (
					('ch', str(uid)),
					('page', str(page)),
				)

				response = requests.get('https://www.publix.com/product-catalog/productlisting', headers=headers, params=params, cookies=cookies, proxies=proxies[last_proxy])
				soup = BeautifulSoup(response.text,'html.parser')
				count = soup.find('div',class_='item-count pull-left').find('span').text
				last_proxy_status = False
			except Exception as e:
				last_proxy = 1000
				continue

		if int(count)<page * 24:
			pagenation = False

		page = page + 1	

		last_sub_Category = True
		lsc = 0
		stop = 0
		while last_sub_Category:
			try:
				last_sub_Category_url = soup.find('a',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(lsc)+"_mainImageLink_"+str(lsc)+""}).get('href')
				
				last_sub_Title = soup.find('span',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(lsc)+"_productSummary_"+str(lsc)+"_productTitleforLink_"+str(lsc)+""}).get_text().strip()
			
				print("Last_sub_Category_Url: " + last_sub_Category_url + "	Last_sub_title: " + last_sub_Title)
				try:

					imageUrl = soup.find('a',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(lsc)+"_mainImageLink_"+str(lsc)+""}).img['src']
					imageName=imageUrl.split('/')
					image = re.sub('[^A-Za-z0-9]+', '', last_sub_Title)

					urllib.request.urlretrieve(imageUrl,'images/' + image + '.jpg')
				except Exception as e:
					image = ''	
				
				# stop = stop + 1
				# if stop == 10:
				# 	exit()
				getproductData(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, last_sub_Category_url,last_sub_Title,last_proxy)

			except Exception as e:
				print("<<<<<<<<<<<<<<<<<<<<<<<<< Next page")
				last_sub_Category = False
				break
			lsc = lsc + 1


def getSub_Sub_CategoryData(category_url, category_title, subCategory_url, subCategory_title, proxy):
	print("---------- Sub_sub_Category-------------")

	page = ''
	soup = ''
	try:
		page = requests.get(subCategory_url, proxies=proxies[proxy])
		soup = BeautifulSoup(page.content,'html.parser')
	except Exception as e:
		page = requests.get("https://www.publix.com"+subCategory_url, proxies=proxies[proxy])
		soup = BeautifulSoup(page.content,'html.parser')

	if category_title == "Baby" or category_title == "Housewares" or category_title == "Non-Foods":
		uidArray = subCategory_url.split('/')

		uid = uidArray[len(uidArray)-1].split('?')[1].split('&')[0].split('=')[1]

		soup = ''
		pagenation = True
		page = 1

		while pagenation:

			sub_sub_proxy = True

			count = ''

			while sub_sub_proxy:
				try:
					cookies = {
						'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
						'_ga': 'GA1.2.368746558.1542651026',
						'_gid': 'GA1.2.2113382898.1542651026',
						'_gcl_au': '1.1.1739095652.1542651028',
						'ajs_user_id': 'null',
						'ajs_group_id': 'null',
						'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
						'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
						'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
						'PublixWeeklyAdBreakDay': '5',
						'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
						'rememberLogin': 'james.wmsoft%40outlook.com',
						'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
						'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
						'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
						'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
						'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
						'_instacart_session': 'anNaaXVPd0l6SC92VS9BcW1HTjlEMWJpYVlWZE13TExaN2NrYkw0YUFFQVpZSzRlcnFOTWVzQUJzNzVKQ2hwUTk4SzFyNUZiajZWSlJGeFV0UTdBL09mektKbGR1Sjl5MExzQUVYNVpOUC8zWFBKVkNhdkR2cnZGWUk1Y09TdlRqMXhzTnhYVkpnamd2WnB2dVFiS2o4M1NnYzl4aFFyNXd2UDNzUU9JRHc1M0pvc21YWFJDeTJIUXQ0REJQSnBiTjJRN0g5R0FwSWVFM1lLNVRFME81Zz09LS1LOHAwbW9zV25UTDF6R2p3Yk9XTUh3PT0%3D--38ba29e0e960b120a0d5c5ee91346f62979ec3a9',
						'_fbp': 'fb.1.1542751470414.206344019',
						'_litra_ses.6f02': '*',
						'sitecore_rcp': 'RIO-PCI-130614|RIO-PCI-106711|RIO-PCI-144137|RIO-PCI-127944|RIO-PCI-132901|RIO-PCI-197707|RIO-PCI-102884|RIO-PCI-129601|RIO-PCI-120900|RIO-PCI-109687|RIO-PCI-108986|RIO-PCI-114611|RIO-PCI-119232|RIO-BPL-282299|RIO-PCI-102979|RIO-PCI-116836|RIO-PCI-152574',
						'__AntiXsrfToken': '004885c13cd14a4880d16c29c27ec5e6',
						'_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.14.1542760679.1542751470.c2eb9561-d14b-403f-a7eb-2bb288916fca',
						'_4c_': 'dZHfypwwEMVfpcxFr6ybxPxTWEppoXwPUHpZYhJXqbuRGOuWxXf%2FJvuHLgv1ImRmjr85Hi%2Bw9v4EDRWcKUk0V5LrAn77vzM0F7BTPv%2FkY4kjNNCnNM3Nbreuazkt7TicSxuOuykGt9j0yZpkxnB41OMwp%2BF0%2BGz7PaUlKz9O5uD3FApoY1hnH5H4tY%2Fh6D8ogl0bnMcWrcuqlFh3uB4qqRWXQugym5SCEpZnAQ3Cz%2BHkEIRl9J2P8UrEah5SBv1ziL3k4zG%2Fg9cJvwgEXsZgzZiVmEEB37%2F8%2BvH27f8rHQYFzndmGRNsBZxvuWFoRGkuKe5IGJKWnOQHFXFw9wChJb7unFLaCU2FrZirveKs9cZIT6VF%2FpUnCP4JwupKMATgtjuAPc9pxaiieY6WbvyHrxeZ4NnH8FCZl7kgus4%2B17vgaVCTV2lNtm17Bw%3D%3D',
					}

					headers = {
						'Connection': 'keep-alive',
						'Pragma': 'no-cache',
						'Cache-Control': 'no-cache',
						'Upgrade-Insecure-Requests': '1',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'en-US,en;q=0.9',
					}

					params = (
						('ch', str(uid)),
						('page', page),
					)

					response = requests.get('https://www.publix.com/product-catalog/productlisting', headers=headers, params=params, cookies=cookies, proxies=proxies[proxy])
					soup = BeautifulSoup(response.text,'html.parser')

					count = soup.find('div',class_='item-count pull-left').find('span').text

					sub_sub_proxy = False
				except Exception as e:
					continue

			if int(count)<page * 24:
				pagenation = False

			page = page + 1			

			sub_sub_Category = True
			stop = 0
			ssc = 0

			while sub_sub_Category:
				try:
					# exit
					sub_sub_Category_url = soup.find('a',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(ssc)+"_mainImageLink_"+str(ssc)+""}).get('href')

					sub_sub_Title = soup.find('span',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(ssc)+"_productSummary_"+str(ssc)+"_productTitleforLink_"+str(ssc)+""}).get_text().strip()
					print("sub_sub_Category_Url: " + sub_sub_Category_url + "	sub_sub_Category_title: " + sub_sub_Title)

					try:
						imageUrl = soup.find('a',attrs={"id":"content_2_3fourthswidth2colright_1_LinksRepeater_ProductResultsDetail_"+str(ssc)+"_mainImageLink_"+str(ssc)+""}).img['src']

						image = re.sub('[^A-Za-z0-9]+', '', sub_sub_Title)
					
						urllib.request.urlretrieve(imageUrl,'images/' + image + '.jpg')
					except Exception as e:					
						image = ""
					# stop = stop + 1
					# if stop == 10:
					# 	exit()

					getproductData(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, "","", proxy)
				except Exception as e:
					print("<<<<<<<<<<<<<<<<<<<<< Next page")
					sub_sub_Category = False

				ssc = ssc + 1
	
	else:
		sub_sub_Category = True
		stop = 0
		ssc = 0

		while sub_sub_Category:
			try:
				sub_sub_Category_url = soup.find('a',attrs={"id":"content_1_3fourthswidth2colright_4_LinksRepeater_LinkURL_"+str(ssc)+""}).get('href')

				sub_sub_Title = soup.find('a',attrs={"id":"content_1_3fourthswidth2colright_4_LinksRepeater_LinkURL_"+str(ssc)+""}).find('h3').get_text().strip()
			
				print("sub_sub_Category_Url: " + sub_sub_Category_url + "	sub_sub_Category_title: " + sub_sub_Title)
				try:

					imageUrl = soup.find('a',attrs={"id":"content_1_3fourthswidth2colright_4_LinksRepeater_LinkURL_"+str(ssc)+""}).img['src']

					imageName = imageUrl.split('/')

					image = re.sub('[^A-Za-z0-9]+', '', sub_sub_Title)

					urllib.request.urlretrieve(imageUrl,'images/' + image + '.jpg')

				except Exception as e:
					image = ''	

				getLast_SubCategoryData(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, proxy)			
			except Exception as e:
					print("<<<<<<<<<<<<<<<<<<<<< Sub_sub_Category End")
					sub_sub_Category = False

			ssc = ssc + 1
def getSubCategoryData(category_url, category_title, proxy):
	print("----------SubCategory-------------")
	print("category: "+ category_url + "	category Title:"+ category_title)

	try:
		page = requests.get(category_url, proxies=proxies[proxy])
		soup = BeautifulSoup(page.content,'html.parser')
	except Exception as e:
		page = requests.get("https://www.publix.com"+category_url, proxies=proxies[proxy])
		soup = BeautifulSoup(page.content,'html.parser')
	
	subCategory = True
	sc = 0
	while subCategory:
		try:
			subCategoryInfo = soup.find('a',attrs={"id":"content_1_3fourthswidth2colright_4_LinksRepeater_LinkURL_"+str(sc)+""})
			subCategory_url = subCategoryInfo.get('href')
			subCategory_title = subCategoryInfo.find('h3').get_text().strip()
			print("subCategory_Url: " + subCategory_url + "	subCategory_title: " + subCategory_title)

			try:

				imageUrl = subCategoryInfo.img['src']

				imageName = imageUrl.split('/')

				image = re.sub('[^A-Za-z0-9]+', '', subCategory_title)

				urllib.request.urlretrieve(imageUrl,'images/' + image + '.jpg')
			except Exception as e:
				image = ''	

			getSub_Sub_CategoryData(category_url, category_title, subCategory_url, subCategory_title, proxy);
		except Exception as e:
			print("<<<<<<<<<<<<<<<<<<< SubCategory End")
			subCategory = False
			break
		sc = sc + 1	

def getCategory(url):
	print("------------Category------------")
	print(url)

	cat_proxy = True

	proxy = ''
	count = ''
	soup = ''
	while cat_proxy:
		proxy = getproxy()
		try:
			cookies = {
				'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
				'_ga': 'GA1.2.368746558.1542651026',
				'_gid': 'GA1.2.2113382898.1542651026',
				'_gcl_au': '1.1.1739095652.1542651028',
				'_fbp': 'fb.1.1542651030544.949403707',
				'ajs_user_id': 'null',
				'ajs_group_id': 'null',
				'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
				'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
				'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
				'PublixWeeklyAdBreakDay': '5',
				'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
				'rememberLogin': 'james.wmsoft%40outlook.com',
				'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
				'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
				'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
				'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
				'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
				'_instacart_session': 'MUxjNFRzZFRBZFJoYnY5T0VmQkphMWtBa1ZnbWZrQnByeDV0MnZqeDBLY3hwL2dMMnlGZDBPbzFZakJ2OFpUclBGZ045S290bDI3Q0JFTHRVYmtMV28wc0NnVG91Smg0MEZ4cS9RYnBwdDNRVHVMNUhhV0VBZDZTbDFJMjRJM2NmTGxlVUc0RGRJNEpBbHcybEpMSmRsN1VuWFlFRDIyWkw5anBheDYwdXJQQW1rQkR4RWxoT0Fsbnc2VzhaNGF3R3dOT2oyS3VPNkJFNEx5UGp6aGowdz09LS04emFYOURpQWxXK3EyTEU5b3Y0c3pRPT0%3D--4ff8c9781234d799b48ba5c8bafac7e7b3afa44b',
				'_litra_ses.6f02': '*',
				'sitecore_rcp': 'RIO-PCI-119232|RIO-BPL-282299|RIO-PCI-102979|RIO-PCI-120900|RIO-PCI-106711|RIO-PCI-116836|RIO-PCI-129601|RIO-PCI-108986|RIO-PCI-132901|RIO-PCI-152574|RIO-PCI-102884',
				'__AntiXsrfToken': 'bc008a83ff6543b2bea10b7908a52285',
				'_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.7.1542693972.1542682767.fbaf71b6-0e51-4a23-ac3c-14d31baf927c',
				'_4c_': 'dVDLjptAEPyVqM8sngc9D25RVor2A1Z7jIAZZBRs0ADBkcW%2FuwfbsteWOYzo7uqq6jrCvPV7yDlmQtkMtURUCfz1%2FwfIj1D18f0Xnym0kMN2HPsh32zmeU77qWybQ1p1u03Rtm996NxUjQMkUIZuHnwg%2FK9t6Hb%2Bh2bUrTrnqcVtKlNFdU3kIJXRmUI06WoBORNx1pE8fDV7R0RUBl%2F7EFZGqoZmjEQ3feqNPuziDv325BeQftquKtqIpAsT%2BP3zz%2BfH%2B2tJRzGA83UxtSMsCRzOqWjDpOZCZ6QxUgRGZSx%2BhAiNu8QDJfO2dlobh4ZjJYWzXmei9EWhPFcV8a98yIiRCStREEF0uu7jTU5qlIIr8yx3TvX1jmbPO3TPBS7uHfAI53FOR58vuF7%2BAMMs0jRXVPEwR2ZsTGK%2BAO4Glux8h1q2LMsJ',
			}

			headers={
				'Connection': 'keep-alive',
				'Pragma': 'no-cache',
				'Cache-Control': 'no-cache',
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, br',
				'Accept-Language': 'en-US,en;q=0.9',
			}

			response = requests.get('https://www.publix.com/all-products', headers=headers, cookies=cookies, proxies=proxies[proxy])

			soup = BeautifulSoup(response.text,'html.parser')
			categoryInfo = soup.find('a', {"id": "content_1_3fourthswidth2colright_2_LinksRepeater_LinkURL_3"})
			cat_proxy = False
		except Exception as e:
			continue

	categories = [3, 5]

	for x in categories:
		# print(x)
		try:
			categoryInfo = soup.find('a',{"id":"content_1_3fourthswidth2colright_2_LinksRepeater_LinkURL_"+str(x)+""})
			category_url = categoryInfo.get('href')
			category_title = categoryInfo.find('h3').get_text().strip()
			imageUrl = categoryInfo.img['src']
			imageName = imageUrl.split('/')
			image = re.sub('[^A-Za-z0-9]+', '', category_title)
			urllib.request.urlretrieve(imageUrl,'images/' + image + '.jpg')
			# print(category_url, category_title)
			getSubCategoryData(category_url, category_title, proxy)
		except Exception as e:
			print("<<<<<<<<<<<<<<<<<<<<< Categories End")
			break

def getproductData(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, last_sub_Category_url,last_sub_Title,proxy):
	print("----------product info-------------")

	uidArray = ''

	uidLast = ''

	uid = ''

	if last_sub_Category_url == "":

		uidArray = sub_sub_Category_url.split('/')

		uidLast = uidArray[len(uidArray)-1]

		uid = uidLast.split('?')[0]

		try:
			page = requests.get(sub_sub_Category_url, proxies=proxies[proxy])
			soup = BeautifulSoup(page.content,'html.parser')			
		except Exception as e:
			page = requests.get("https://www.publix.com"+sub_sub_Category_url, proxies=proxies[proxy])
			soup = BeautifulSoup(page.content,'html.parser')
	else:

		uidArray = last_sub_Category_url.split('/')

		uidLast = uidArray[len(uidArray)-1]

		uid = uidLast.split('?')[0]

		try:
			page = requests.get(last_sub_Category_url, proxies=proxies[proxy])
			soup = BeautifulSoup(page.content,'html.parser')
		except Exception as e:
			page = requests.get("https://www.publix.com"+last_sub_Category_url, proxies=proxies[proxy])
			soup = BeautifulSoup(page.content,'html.parser')

	try:
		overview_status = soup.find('li',attrs={'id':'content_1_3fourthswidth2colright_1_ProductTabs_li_tab_overview'}).get_text()
		
		cookies = {
		   'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
            '_ga': 'GA1.2.368746558.1542651026',
            '_gid': 'GA1.2.2113382898.1542651026',
            '_gcl_au': '1.1.1739095652.1542651028',
            '_fbp': 'fb.1.1542651030544.949403707',
            'ajs_user_id': 'null',
            'ajs_group_id': 'null',
            'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
            'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
            'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
            'PublixWeeklyAdBreakDay': '5',
            'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
            'rememberLogin': 'james.wmsoft%40outlook.com',
            'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
            'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
            'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
            'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
            'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
            '_instacart_session': 'MUxjNFRzZFRBZFJoYnY5T0VmQkphMWtBa1ZnbWZrQnByeDV0MnZqeDBLY3hwL2dMMnlGZDBPbzFZakJ2OFpUclBGZ045S290bDI3Q0JFTHRVYmtMV28wc0NnVG91Smg0MEZ4cS9RYnBwdDNRVHVMNUhhV0VBZDZTbDFJMjRJM2NmTGxlVUc0RGRJNEpBbHcybEpMSmRsN1VuWFlFRDIyWkw5anBheDYwdXJQQW1rQkR4RWxoT0Fsbnc2VzhaNGF3R3dOT2oyS3VPNkJFNEx5UGp6aGowdz09LS04emFYOURpQWxXK3EyTEU5b3Y0c3pRPT0%3D--4ff8c9781234d799b48ba5c8bafac7e7b3afa44b',
            '_litra_ses.6f02': '*',
            'sitecore_rcp': str(uid) +'|RIO-PCI-102979|RIO-PCI-120900|RIO-PCI-106711|RIO-PCI-116836|RIO-PCI-129601|RIO-PCI-108986|RIO-PCI-132901|RIO-PCI-152574|RIO-PCI-102884',
            '_4c_': 'dVHZitwwEPyV0M%2FjQ7J1DYSQA8JCICEQ8hhkqb028YyMrIk3LPPv25qDbHYZPwipu7qqq%2FwI64B72DLRcmlY22gtxQZ%2B498Fto%2Fg5nz%2BycchTrCFIaV52VbVuq7lfOim8aF0YVfNvgrdFPb3hRuCC5NNWNzbvXUDFsnGVKxjGoo%2B4jIUS4p27TDGEZfq%2B93X4sO3LwXXnBvzzg1veclkCRvoYlgXjKT5cYhhh29UTVUXPFKJmbIpJb17WhAaqVUrhdDlyYZgNc%2B9QBbg57j3RETPiD2JnhjptYwpE%2F3zQLWEcZdn6DqTZxB0mYKzU0ZSShv4%2FP7Xj7tPtyU9RQkee3uYEhw38HBOVinVCtUqRRqJYtSyrfNHiDj6S8TQ1Wh6r5T2QjPhGu4NqpZ3aK1EJh3xn%2FhETYw1N43gRJA3Pc3Tb7vKNUo0nEn9Wu6c6u0ZVb%2BeIT8XOH%2B%2BActwlvtk%2Buzg6vwFTLSZZryi7Iu%2BqLXJSawXwLOGoXX%2Bh5r6eDw%2BAQ%3D%3D',
            '__AntiXsrfToken': '7aa457fedb8140329b7e0cb2488a5309',
            '_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.7.1542691455.1542682767.fbaf71b6-0e51-4a23-ac3c-14d31baf927c',
            '_gat': '1',
		}

		headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.publix.com/pd/oblong-chocolate-ganache-tart-with-fresh-strawberries/'+ str(uidLast),
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }

		params = (
            ('pid',  str(uid) ),
            ('tab', 'overview'),
            ('storeid', '794'),
        )

		response = requests.get('https://www.publix.com/product%20catalog/ProductContent', headers=headers, params=params, cookies=cookies, proxies=proxies[proxy])

		soup_text = BeautifulSoup(response.text, 'html.parser')

		try:
			overview = soup_text.find_all('p')[0].text
		except Exception as e:
			overview = ''

	except Exception as e:
	
		overview = ''
	
	try:
		moreinfo_status = soup.find('li',attrs={'id':'content_1_3fourthswidth2colright_1_ProductTabs_li_tab_more_info'}).get_text()
		
		cookies = {
		    'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
		    '_ga': 'GA1.2.368746558.1542651026',
		    '_gid': 'GA1.2.2113382898.1542651026',
		    '_gcl_au': '1.1.1739095652.1542651028',
		    '_fbp': 'fb.1.1542651030544.949403707',
		    'ajs_user_id': 'null',
		    'ajs_group_id': 'null',
		    'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
		    'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
		    'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
		    'PublixWeeklyAdBreakDay': '5',
		    '_instacart_session': 'Tk5RMGc0dU1ib2lLV1NkN05jZ2VoUGZiclIrMjlzUEp4SkJJcEJMMmNQRm5EMGlTQTdudzJvMUZjb0tHcGR5RUFHTjhlMmxpSCtzRXhiclJFMUdCT3ZpNjV2cDF4eUwyTmpJVWdUSE5VaGdnbTRBRkxhcEIvWWRhNFd3TkJUNmtVZE11MUNOQUgrejhGc1E4enFscUtWcDEwTFJDTkl4VjhrQURFb1UwNzV0VzByWWJvWHY3UXJPN2VOTmRTT1BCN3duS0tjZ25SZTVKN3B6SWltVWw5QT09LS1Xb2RudEdhekdpd1V6ZFR2MmtJb2FBPT0%3D--f0ac3ce65f9d153314cf777c65fafe4b8d06e5df',
		    'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
		    'rememberLogin': 'james.wmsoft%40outlook.com',
		    'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
		    'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
		    'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
		    'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
		    'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
		    'sitecore_rcp': str(uid) +'|RIO-PCI-132901|RIO-PCI-152574|RIO-PCI-102979|RIO-PCI-102884',
		    '__AntiXsrfToken': '0fd63e8622f14c0f9a2d9623dd9f0184',
		    '_litra_ses.6f02': '*',
		    '_4c_': 'dVLRitswEPyVss%2BxvbItyQqUUq5Q8tSjUPpYbGmDRR3byEqdcuTfb5XkSHvHYRBa7czszuAnWHsaYStkXSptBKJsyg38pr8LbJ%2FAzun8k45jGGALfYzzsi2KdV3z%2BdgN%2FpTb6VDMrnDH0bZj1vuRlsyRbR2NMevCtI6esoM%2FZTH4eaDM9pOdhjZS8X33LXt82GUClRbik%2B0%2FmlzwBxtIvIUCT3zow3SgDxr51U6O%2BEmYvMoV13teDyrV6FpJ2eQXE1JgmXoTG4CffnQsxGWgPYVwUeRq8TEJ3R3wW6RwSBy%2BzuwYJF%2BGybZDQnJGG%2Fj6%2BdeP3Zf3RzoOEhzt2%2BMQ4byB0zVXzUhEVDXPiBxio2ouERkRvLsFDB2S2TutGycbIW1VOkO6LjtqW0VCWda%2F6ElkRSxNJUsWSJte%2BPI%2BrtKyKoVq3o67pvo%2BR%2BNbDvu5wfm%2FuG8gElykPpu%2BOnhx%2Fgom6yTjX1Dtq77ExqQk1hvgn4bhdf6HGjyfz88%3D',
		    '_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.5.1542679102.1542677240.8f4fe27b-1ef5-4ca7-99e6-062c7cc97423',
		}

		headers = {
		    'Pragma': 'no-cache',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'en-US,en;q=0.9',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		    'Accept': '*/*',
		    'Referer': 'https://www.publix.com/pd/duncan-hines-decadent-brownie-mix-triple-chocolate/RIO-PCI-'+ str(uidLast),
		    'X-Requested-With': 'XMLHttpRequest',
		    'Connection': 'keep-alive',
		    'Cache-Control': 'no-cache',
		}

		params = (
		    ('pid', str(uid)),
		    ('tab', 'moreinfo'),
		)

		response_more = requests.get('https://www.publix.com/product%20catalog/ProductContent', headers=headers, params=params, cookies=cookies, proxies=proxies[proxy])

		soup_more = BeautifulSoup(response_more.text, 'html.parser')

		moreinfo = ''
		try:
			moreinfo = soup_more.find('p').text
		except Exception as e:
			moreinfo = ''
	except Exception as e:
		moreinfo = ''

	try:
		nutrition_status = soup.find('li',attrs={'id':'content_1_3fourthswidth2colright_1_ProductTabs_li_tab_nutritional_info'}).get_text()
		
		cookies = {
		    'ASP.NET_SessionId': 'txvylolglc1ppjmts0z10p0h',
		    '_ga': 'GA1.2.368746558.1542651026',
		    '_gid': 'GA1.2.2113382898.1542651026',
		    '_gcl_au': '1.1.1739095652.1542651028',
		    '_fbp': 'fb.1.1542651030544.949403707',
		    'ajs_user_id': 'null',
		    'ajs_group_id': 'null',
		    'ajs_anonymous_id': '%22b1315b87-a219-47ff-a455-f20ef53fb329%22',
		    'amplitude_idundefinedpublix.com': 'eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==',
		    'PublixStore': '794%7CPublix%2Bat%2BMiami%2BShores',
		    'PublixWeeklyAdBreakDay': '5',
		    '_instacart_session': 'Tk5RMGc0dU1ib2lLV1NkN05jZ2VoUGZiclIrMjlzUEp4SkJJcEJMMmNQRm5EMGlTQTdudzJvMUZjb0tHcGR5RUFHTjhlMmxpSCtzRXhiclJFMUdCT3ZpNjV2cDF4eUwyTmpJVWdUSE5VaGdnbTRBRkxhcEIvWWRhNFd3TkJUNmtVZE11MUNOQUgrejhGc1E4enFscUtWcDEwTFJDTkl4VjhrQURFb1UwNzV0VzByWWJvWHY3UXJPN2VOTmRTT1BCN3duS0tjZ25SZTVKN3B6SWltVWw5QT09LS1Xb2RudEdhekdpd1V6ZFR2MmtJb2FBPT0%3D--f0ac3ce65f9d153314cf777c65fafe4b8d06e5df',
		    'amplitude_id_b87e0e586f364c2c189272540d489b01publix.com': 'eyJkZXZpY2VJZCI6Ijc0YTljOWM3LWJlNDctNDY4Ny05NWUxLWQwYjE3NTRhN2Y3NVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU0MjY1MzczMDEzOSwibGFzdEV2ZW50VGltZSI6MTU0MjY1Mzk4OTUxMCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjYsInNlcXVlbmNlTnVtYmVyIjoxNn0=',
		    'rememberLogin': 'james.wmsoft%40outlook.com',
		    'PublixUser': '%7b%22FirstName%22%3a%22alex%22%2c%22Email%22%3a%22james.wmsoft%40outlook.com%22%2c%22EcmsId%22%3a%22t5DXXuFpKCWnb9kee2eF4A%3d%3d%22%7d',
		    'DCUserToken': 'AEvd9hoJQo0U3zJcPX9PxmwLTTzYSNCB3udGQ2Ie2x0M0YyIjoI7ZjneC2BtKvds',
		    'touAccepted': '11%2f18%2f2018+10%3a32%3a00+PM',
		    'JWT_FedAuth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InhfcDN1ZWNRWnR1QzFjakNkNGwwdUxqMDNMSSJ9.eyJpc3MiOiJQdWJsaXguV2Vic2l0ZSIsImF1ZCI6InVybjphZGZzOmZlZGVyYXRpb246UENPTTpwcmQiLCJuYmYiOjE1NDI1OTg0NzAsImV4cCI6MTU0MjYwMjA3MCwiZW1haWwiOiJqYW1lcy53bXNvZnRAb3V0bG9vay5jb20iLCJyb2xlIjpbIkRvbWFpbiBVc2VycyIsIkV4dGVybmFsX1VzZXJzX1Bhc3N3b3JkX1BvbGljeSJdLCJodHRwOi8vc2NoZW1hcy5wdWJsaXguY29tL3Nzby8yMDEzLzA2L2lkZW50aXR5L2NsYWltcy9vYmplY3RndWlkIjoiOGUzOWQyYWItZDMzOC00NzA4LWFiOWQtMzA0N2FiMDYyMWM0In0.nwdrcgZ99kHW7W_ttMjA6LRzZDJ6SzNJbnn0G_6JEKgKgZOSmrKIElWJm76ITfDLr8TdVthM9KFa6wsKi-M8pYRK-j-386fjT3IF8QyVjnvmQIC5daBR68iiMEnfg2dRZ02Mwm9DCqkp5OhHispgPGqiPYhKr8dDw1HrFUYWytKKRMwMoepNXG_0H9Tw_WSRN4CoC27PojSwU6G0dxieFrYXj8CgWJisjpNWhXED0GxZEBSlzBxCAjlTl8g1AutgoOI7K-UJnChHwMrQkaXQSDtxG6EUVLsI2fjeygYLhNjlgyO9tgbToUqGrsG9gzi4XIpFGZ-JLPiqda4qTCRxmw',
		    'GroceryList': '%7B%22id%22%3A%22vkaF6WAdHo579yrC7-a3zw%3D%3D%22%2C%22name%22%3A%22Shopping%20List%2011%2F18%2F2018%22%2C%22itemCount%22%3A0%7D',
		    'sitecore_rcp': str(uid) +'|RIO-PCI-132901|RIO-PCI-152574|RIO-PCI-102979|RIO-PCI-102884',
		    '_litra_ses.6f02': '*',
		    '__AntiXsrfToken': 'ca7278df3b1c414c9a105d2eddfa8904',
		    '_gat': '1',
		    '_litra_id.6f02': 'a-00zb--2db6bad9-55eb-41b0-9cc7-eaf9b0cdd9b6.1542651028.5.1542679570.1542677240.8f4fe27b-1ef5-4ca7-99e6-062c7cc97423',
		    '_4c_': 'dVFdi9wwDPwrRc%2FrxHZiO14opVyh7FNLofSxJLaWmGaT4HibPY797yfvB71eew4YSxqNNJMnWHscYStULbWxyvCKqw38wscFtk%2Fg5nz%2FztcxDrCFPqV52Zbluq7FfOyGcCrcdChnX%2Frj6NqR9WHEhXl0rccxsS5O6xiQHcKJpRjmAZnrJzcNbcLy2%2B4L%2B%2FqwY4JrI8QH17%2B3haAPNpD7Fow08aGP0wHfGU5ZN3mklLBFVWiK97QeVLoxtVaqKS4ilOAy1yYSAD%2FC6ImIwoh7jPHCSNESUib6o4ByCeMh99BzJsWg6DFMrh0ykjzawOePP7%2FvPr090pOR4HHfHocE5w2crr4aray2puI0I5GJja55PoSIwd8Mho6j3XtjGq8aoVwlvUVTyw7bVqPQjvgvfIoTI5e2UpII8qaXfvpp93GVUZUUuvl33NXVt3vMf1YkPTe4fLmByHCR6yT6quCu%2FBVM1Zkm3FHtq7rijc1OrDfAi4Kldf6GWn4%2Bn58B',
		}

		headers = {
		    'Pragma': 'no-cache',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'en-US,en;q=0.9',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		    'Accept': '*/*',
		    'Referer': 'https://www.publix.com/pd/duncan-hines-decadent-brownie-mix-triple-chocolate/'+ str(uidLast),
		    'X-Requested-With': 'XMLHttpRequest',
		    'Connection': 'keep-alive',
		    'Cache-Control': 'no-cache',
		}

		params = (
		    ('pid', str(uid)),
		    ('tab', 'nutrition'),
		)

		response_nutrition = requests.get('https://www.publix.com/product%20catalog/ProductContent', headers=headers, params=params, cookies=cookies, proxies=proxies[proxy])

		nutritional_info = BeautifulSoup(response_nutrition.text, 'html.parser')

		try:
			Calories = nutritional_info.find('input',class_='nutritionalData_Calories').get('value')

			CaloriesfromFat = nutritional_info.find('input',class_='nutritionalData_CaloriesfromFat').get('value')
		except Exception as e:
			Calories = 0
			CaloriesfromFat=0
		
		try:
			TotalFat = nutritional_info.find('input',class_='nutritionalData_TotalFat').get('value')

			TotalFat_Percent = nutritional_info.find('input',class_='nutritionalData_TotalFat_Percent').get('value')
		except Exception as e:
			TotalFat = 0
			TotalFat_Percent = 0

		try:
			SaturatedFat = nutritional_info.find('input',class_='nutritionalData_SaturatedFat').get('value')

			SaturatedFat_Percent = nutritional_info.find('input',class_='nutritionalData_SaturatedFat_Percent').get('value')
		except Exception as e:
			SaturatedFat = 0
			SaturatedFat_Percent = 0

		try:
			PolyunsaturatedFat = nutritional_info.find('input',class_='nutritionalData_PolyunsaturatedFat').get('value')
			
		except Exception as e:
			PolyunsaturatedFat = 0
		
		try:
			MonounsaturatedFat = nutritional_info.find('input',class_='nutritionalData_MonounsaturatedFat').get('value')
		except Exception as e:
			MonounsaturatedFat = 0

		try:
			Cholesterol = nutritional_info.find('input',class_='nutritionalData_Cholesterol').get('value')

			Cholesterol_Percent = nutritional_info.find('input',class_='nutritionalData_Cholesterol_Percent').get('value')
		except Exception as e:
			Cholesterol = 0
			Cholesterol_Percent = 0
		
		try:
			Sodium = nutritional_info.find('input',class_='nutritionalData_Sodium').get('value')

			Sodium_Percent = nutritional_info.find('input',class_='nutritionalData_Sodium_Percent').get('value')
		except Exception as e:
			Sodium = 0
			Sodium_Percent = 0

		try:
			TotalCarbohydrate = nutritional_info.find('input',class_='nutritionalData_TotalCarbohydrate').get('value')

			TotalCarbohydrate_Percent = nutritional_info.find('input',class_='nutritionalData_TotalCarbohydrate_Percent').get('value')
		except Exception as e:
			TotalCarbohydrate = 0
			TotalCarbohydrate_Percent = 0
		
		try:
			DietaryFiber = nutritional_info.find('input',class_='nutritionalData_DietaryFiber').get('value')

			DietaryFiber_Percent = nutritional_info.find('input',class_='nutritionalData_DietaryFiber_Percent').get('value')
		except Exception as e:
			DietaryFiber = 0
			DietaryFiber_Percent = 0

		try:
			Sugars = nutritional_info.find('input',class_='nutritionalData_Sugars').get('value')
		except Exception as e:
			Sugars = ''
		
		try:
			Protein = nutritional_info.find('input',class_='nutritionalData_Protein').get('value')
		except Exception as e:
			Protein = 0
		
		try:
			VitaminA = nutritional_info.find('input',class_='nutritionalData_VitaminA').get('value')

			VitaminA_Percent = nutritional_info.find('input',class_='nutritionalData_VitaminA_Percent').get('value')
		except Exception as e:
			VitaminA = 0
			VitaminA_Percent = 0

		try:
			VitaminC = nutritional_info.find('input',class_='nutritionalData_VitaminC').get('value')

			VitaminC_Percent = nutritional_info.find('input',class_='nutritionalData_VitaminC_Percent').get('value')
		except Exception as e:
			VitaminC = 0
			VitaminC_Percent = 0

		try:
			Calcium = nutritional_info.find('input',class_='nutritionalData_Calcium').get('value')

			Calcium_Percent = nutritional_info.find('input',class_='nutritionalData_Calcium_Percent').get('value')
		except Exception as e:
			Calcium = 0
			Calcium_Percent = 0
		
		try:
			Iron = nutritional_info.find('input',class_='nutritionalData_Iron').get('value')

			Iron_Percent = nutritional_info.find('input',class_='nutritionalData_Iron_Percent').get('value')
		except Exception as e:
			Iron = 0
			Iron_Percent = 0

		Ingredients_info = nutritional_info.find('div',attrs={'id':'NutritionalFacts'})
		try:
			Ingredients = Ingredients_info.find_all('p')[0].text
		except Exception as e:
			Ingredients = 0

		try:
			Allergens = Ingredients_info.find_all('p')[1].text
		except Exception as e:
			Allergens = 0
	except Exception as e:
		Calories = ''
		CaloriesfromFat=''
		TotalFat = ''
		TotalFat_Percent = ''
		SaturatedFat = ''
		SaturatedFat_Percent = ''
		PolyunsaturatedFat = ''
		MonounsaturatedFat = ''
		Cholesterol = ''
		Cholesterol_Percent = ''
		Sodium = ''
		Sodium_Percent = ''
		TotalCarbohydrate = ''
		TotalCarbohydrate_Percent = ''
		DietaryFiber = ''
		DietaryFiber_Percent = ''
		Sugars = ''
		Protein = ''
		VitaminA = ''
		VitaminA_Percent = ''
		VitaminC = ''
		VitaminC_Percent = ''
		Calcium = ''
		Calcium_Percent = ''
		Iron = ''
		Iron_Percent = ''
		Ingredients = ''
		Allergens = ''

	print("===================== print =========================")
	print(category_url, category_title, subCategory_url, subCategory_title, sub_sub_Category_url, sub_sub_Title, last_sub_Category_url,last_sub_Title,
		overview, moreinfo, Calories, CaloriesfromFat, TotalFat, 
		TotalFat_Percent, SaturatedFat, SaturatedFat_Percent, PolyunsaturatedFat, MonounsaturatedFat, Cholesterol,
		Cholesterol_Percent,Sodium, Sodium_Percent, TotalCarbohydrate_Percent, DietaryFiber, DietaryFiber_Percent, Sugars, Protein,
		VitaminA, VitaminA_Percent, VitaminC, VitaminC_Percent, Calcium, Calcium_Percent, Iron, Iron_Percent, Ingredients, Allergens)

	productname = ''

	if last_sub_Title == "":
		productname = sub_sub_Title
	else:
		productname = last_sub_Title
	print("-----------------------------------------------------")
	print(productname)
	writer.writerow({
        'category_title':category_title,
        'subCategory_title':subCategory_title,
        'sub_sub_Title':sub_sub_Title,
        'productname':productname,
        'overview':overview,
        'moreinfo':moreinfo,
        'Calories':Calories,
        'CaloriesfromFat':CaloriesfromFat,
        'TotalFat':TotalFat,
        'TotalFat_Percent':TotalFat_Percent,
        'SaturatedFat':SaturatedFat,
		'PolyunsaturatedFat':PolyunsaturatedFat,
        'MonounsaturatedFat':MonounsaturatedFat,
        'Cholesterol':Cholesterol,
        'Cholesterol_Percent':Cholesterol_Percent,
        'Sodium':Sodium,
        'Sodium_Percent':Sodium_Percent,
        'SaturatedFat_Percent':SaturatedFat_Percent,
        'TotalCarbohydrate_Percent':TotalCarbohydrate_Percent,
        'DietaryFiber':DietaryFiber,
        'DietaryFiber_Percent':DietaryFiber_Percent,
        'Sugars':Sugars,
        'Protein':Protein,
        'VitaminA':VitaminA,
        'VitaminA_Percent':VitaminA_Percent,
        'VitaminC':VitaminC,
        'VitaminC_Percent':VitaminC_Percent,
        'Calcium':Calcium,
        'Calcium_Percent':Calcium_Percent,
        'Iron':Iron,
        'Iron_Percent':Iron_Percent,
        'Ingredients':Ingredients,
        'Allergens':Allergens
    })
	print("======== Save End ============")

if __name__ == "__main__":
	print('welcome start:')

	fieldnames = [
        'category_title','subCategory_title','sub_sub_Title','productname',
    	'overview', 'moreinfo', 'Calories','CaloriesfromFat', 'TotalFat', 
		'TotalFat_Percent', 'SaturatedFat', 'SaturatedFat_Percent', 'PolyunsaturatedFat', 'MonounsaturatedFat', 'Cholesterol',
		'Cholesterol_Percent','Sodium', 'Sodium_Percent', 'TotalCarbohydrate_Percent', 'DietaryFiber', 'DietaryFiber_Percent', 'Sugars', 'Protein',
		'VitaminA', 'VitaminA_Percent', 'VitaminC', 'VitaminC_Percent', 'Calcium', 'Calcium_Percent', 'Iron', 'Iron_Percent', 'Ingredients', 'Allergens'
    ]

	fw = open('data/baby.csv', 'w', newline='')
	writer = csv.DictWriter(fw, fieldnames=fieldnames)
	writer.writeheader()
	getCategory("https://www.publix.com/all-products")

print('-------------------------- ALL SUCCESS!----------------------------')





#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.publix.com/product%20catalog/ProductContent?pid=RIO-PCI-106711&tab=overview&storeid=794', headers=headers, cookies=cookies)
