import psycopg2


# this will load the data from result.txt file to the database



def read_data(path):
	f = open(path, "r")
	content = '[{}]'.format(f.read())
	return eval(content)


def combien_dict(data):
	big_li = list()
	for li in data:
		for dict_ in li:
			big_li.append(dict_)
	return big_li



def mapper_p(c):
	"""
	this will map arrondi to code 
	"""
	mp = {'Paris 1er arrondissement':'32682',	'Paris 2me arrondissement':'32683',
	'Paris 3me arrondissement':'32684',	'Paris 4me arrondissement':'32685',
	'Paris 5me arrondissement':'32686',	'Paris 6me arrondissement':'32687',
	'Paris 7me arrondissement':'32688',	'Paris 8me arrondissement':'32689',
	'Paris 9me arrondissement':'32690',	'Paris 10me arrondissement':'32691',
	'Paris 11me arrondissement':'32692','Paris 12me arrondissement':'32693',
	'Paris 13me arrondissement':'32694',	'Paris 14me arrondissement':'32695',
	'Paris 15me arrondissement':'32696',	'Paris 16me arrondissement':'32697',
	'Paris 17me arrondissement':'32698',	'Paris 18me arrondissement':'32699',
	'Paris 19me arrondissement':'32700',	'Paris 20me arrondissement':'32701'}
	return mp[c]



def clean_data(data):
	"""
	this will process data and convert it to int
	"""
	processed_list=list()
	for d in data:	
		try : 
			d['id_']=int(d['id_'].split('|')[0])
			d['area_']=int(d['area'].split(' - ')[1].replace('m',''))
			
			# check if it is a studio or appart
			rc = d['area'].split(' - ')[0].replace('Appartement ','').replace('pices','')
			if rc == 'Studio':
				d['room_count']= 1
			else: 
				d['room_count']= int(rc)

			d['price']=int(d['price'])
			d['place']=int(mapper_p(d['place']))
			# del area no used
			d.pop('area')
			processed_list.append(d)
		except:
			pass
	return processed_list


def connect_upsert(data):


	try:
	
		connection = psycopg2.connect(user="meilleursagents",
		                                  password="pikachu42!@",
		                                  host="localhost",
		                                  port="5432",
		                                  database="meilleursagents")

		cursor = connection.cursor()

		postgres_insert_query = """ INSERT INTO spec (listing_id ,area, room_count, price, palce_id) VALUES (%s,%s,%s,%s,%s)"""
		for d in data:
			   record_to_insert = (d['id_'],d['area_'],d['room_count'],d['price'],d['place'])
			   cursor.execute(postgres_insert_query, record_to_insert)

			   connection.commit()
		count = cursor.rowcount
		print (count, "Record inserted successfully into spec table")

	except (Exception, psycopg2.Error) as error :
	    if(connection):
	        print("Failed to insert record into spec table", error)

	finally:
	    #closing database connection.
	    if(connection):
	        cursor.close()
	        connection.close()
	        print("PostgreSQL connection is closed")

def workflow_injection():

	# read the data from result.txt
	data  = read_data('result.txt')
	# combien all list and dict 
	combiened = combien_dict(data)
	# final clean and convert to int
	cleaned_data = clean_data(combiened)
	# connect and insert data in db
	connect_upsert(cleaned_data)

#workflow_injection()