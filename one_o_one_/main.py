from extraction import start_point_extraction
from loader import workflow_injection


def main():
	# try to extarct data + process level1+2 + store data in txt 
	"""
	try:
		start_point_extraction()
	except Exception as e:
		print(e)
"""
	# read data from txt + process final level + insert into database
	try : 
		workflow_injection()
	except Exception as e:
		print(e)

main()