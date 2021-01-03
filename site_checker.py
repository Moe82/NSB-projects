import requests
import pandas as pd
from tqdm import tqdm
import sys
from csv import DictReader
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

class SiteChecker:
	def __init__(self, url_list, csv=False):
		if csv == True:
			self.url_list = self.csv_to_list(url_list, 'Site')
		else:
			self.url_list = url_list 
		self.updated_url_list = []
		self.unresponsive = []
		self.start()

	def strip_scheme(self, url):
	    parsed = urlparse(url)
	    scheme = "%s://" % parsed.scheme
	    return parsed.geturl().replace(scheme, '', 1)

	def csv_to_list(self, filename, column_name):
		df = pd.read_csv(filename, header=0)
		column = getattr(df, column_name)
		return column.to_list()

	def list_to_csv(self, filename, list):
		df = pd.DataFrame(list, columns=["Site"])
		df.to_csv(filename, index=False)

	def start(self):
		with tqdm(total=len(self.url_list), file=sys.stdout) as pbar:
			self.url_list = ["bodybuilding.com"]
			for url in self.url_list:
				try:
					domain = self.strip_scheme(url)
					req = requests.get("http://" + url, timeout=10)
					updated_url = req.url
					self.updated_url_list.append(updated_url)
					pbar.update(1)
				except Exception as e:
					self.unresponsive.append(url)
					pbar.update(1)
					continue
				list_to_csv(filename + "_updated.csv", self.updated_url_list)
