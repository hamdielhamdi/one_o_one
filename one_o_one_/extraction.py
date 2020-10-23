import requests 
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent
import time
import json


def send_r(url):
		"""
		send a requests and change user agent evry time, to avoid being blocked.
		"""	
		print(url)
		ua = UserAgent(cache=False)
		header = {'User-Agent':str(ua.random)}
		response = requests.get(url, headers=header)
		return response


def process_level_1(content):
	"""
	process dhtml code and get info
	"""
	soup = BeautifulSoup(content, features="html.parser")

	#r = soup.findAll('div',{"class":"listing-item__content"})
	r = soup.findAll('div',{"class":"listing-item search-listing-result__item"})
	res=list()
	# extract information from the source code if the page 
	for i in r:
		listing_id = str(i)[str(i).index('data-wa-data="')+len("data-wa-data=")+1:str(i).index("|source=listings_results")+len("|source=listings_results")]
		type_area = i.find('div',{'class':'listing-characteristic margin-bottom'}).text
		price = i.find("div",{"class":"listing-price margin-bottom"}).text
		palce = i.find("div",{"class":"text--muted text--small"}).text
		res.append({"id_":listing_id,
		 "area":type_area,
		 "price":price,
		 "place":palce})
	return res



def save_file(data, path_file='result.txt'):
	 output_file = open(path_file, 'a', encoding='utf-8')
	 # save the data in the result.txt file as a tmp store
	 json.dump(data, output_file) 
	 output_file.write(",\n")



def send_loop(q):
	# when we query cities by 10 in evry request, we get 12 dict in evry page 
	# then we iterat thru page to target 5000 page which is too large 
	# the loop break when "msg error is presente in the html code"	
	for index in range(1,5000):
		url_ = "https://www.meilleursagents.com/annonces/achat/search/?transaction_types=TRANSACTION_TYPE.SELL&place_ids={0}&item_types=ITEM_TYPE.APARTMENT&page={1}".format(q,index)
		
		content = send_r(url_).content



		# if this msg is found then stop 
		if "Désolé, l’adresse que vous demandez est introuvable" in str(content):
			return 

		processed_data = process_level_1(content)

		# handel error do to the blocked requests we wait for 10 s and we retry
		# this is used to minimize the data loss.
		if not processed_data:
			print("waiting 10 s")
			time.sleep(10)
			content = send_r(url_).content
			processed_data = process_level_1(content)

			

		print(index)
		# this will process data and delete some unwanted caracter
		data = process_data(processed_data)
		# save the data in tmp file
		save_file(data)
	


def process_data(l_):

	# list of unwanted car to replace by ''
	list_toreplace=['listing_id=',
	'|realtor_id=43662|source=listings_results',
	'\n','\u00a0','\u00b2','                    ',
	 '\u00e8','                ',
	'\u202f','\u20ac']

	new_l_=list()
	# iterat thru the list of dict and replace
	for dict_ in l_:
		for k in dict_:
			for repl in list_toreplace:

				dict_[k] = dict_[k].replace(repl,'')
		# create a new list of dict and return val
		new_l_.append(dict_)
	return new_l_


"""
this part is add to handle date, can be optimized and integrated in the procedd data method
aaaaaaaaaaaaaa not used 
"""
def read_file(path):
	f = open(path, "r")
	content = '[{}]'.format(f.read())
	return eval(content)


def search_of_date(data):
	soup = BeautifulSoup(data.content, 'html.parser')
	return (soup.find('div',{'class':'text--right text--muted margin-top margin-bottom-triple'}).text).replace('Mise à jour le','')
	
def update_result_file(data):
	 output_file = open("result_l1.txt", 'w', encoding='utf-8')
	 # save the data in the result.txt file as a tmp store
	 json.dump(data, output_file) 
	 output_file.write()

def update_date_mel():
	url_date = "https://www.meilleursagents.com/annonces/achat/"
	content = read_file("result.txt")
	new_list = list()
	# itert thru list of dict
	for k in content:
		# iter thru dict key , get id and send requests 
		for dict_ in k:
			url__ = url_date + str(dict_['id_'].split('|')[0])
			result = send_r(url__)
			# search for date mise a jour in html code
			dict_['date_mel'] = search_of_date(result)	
		new_list.append(dict_)
	return new_list


"""
end of the added part
"""



def start_point_extraction():
	"""
	we will query cities by 10 in evry request
	"""
	query_palce_id = ["32682%2C32683%2C32684%2C32685%2C32686%2C32687%2C32688%2C32689%2C32690%2C32691",
						"32692%2C32693%2C32694%2C32695%2C32696%2C32697%2C32698%2C32699%2C32700%2C32701"]
	for i in query_palce_id:
		send_loop(q=i)


#start_point_extraction()

