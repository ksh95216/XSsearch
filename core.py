from bs4 import BeautifulSoup
from requests import *
from urllib.parse import *
import re
import time


class XSsearch:


	def __init__(self, url, cookies={}):
	
		self.url = url
		self.cookies = cookies
		self.parameter = []
		self.result = []

	def parser(self):

		html = get_html(self.url, self.cookies)
		soup = get_soup(html)
		inputs = get_input(soup)

		for Input in inputs:
	
			if Input.get('name') != None:

				self.parameter.append(Input.get('name'))

		self.parameter = list(set(self.parameter))

	def check(self):

		p = re.compile('(<[\x00-;=\x3f-\xff>]*?_XS_.*?_XS_[<\x00-;=\x3f-\xff]*?>)')

		for param in self.parameter:

			url = set_param(self.url, param)		
			html = get_html(url, self.cookies)
			matchs = p.finditer(html)
			
			idx = 0
			for match in matchs:

				line = html[0:match.start()].count("\n")
	
				
				if (match.group()[0] == '\'' or match.group()[0] == '"') and match.group()[0] in match.group():
		
					self.result.append({param : match.group()[1:], "line":line})
				
				else:

					self.result.append({param : match.group(), "line":line})
				

				idx += 1

			print("[*] {} => {}".format(param, idx))

	def run(self):
		
		self.parser()
		print("[*] find parameters ",self.parameter)
		self.check()
		print("[*] result ", self.result)
		return self.result
			

def get_html(url, cookies):

	if cookies != {}:

		tmp_cookies = {}
		for cookie in cookies.split(";"):

			try:

				key = cookie.split("=")[0]
				value = cookie.split("=")[1]
				tmp_cookies[key] = value
		
			except:

				0			
		
		cookies = tmp_cookies
		
	res = get(url,cookies=cookies)


	html = res.text
	return html

def get_soup(html):

	soup = BeautifulSoup(html.encode(),'html.parser')
	return soup

def get_form(soup):

	forms = soup.findAll("form")
	return forms

def get_input(form):
	
	inputs = form.findAll("input")
	return inputs


def set_param(url, parameter):

	scheme, netloc, path, params, query, fragment = urlparse(url)

	if query != '':

		query += "&"

	value = '_XS_\'"><_XS_'
	query += "{}={}&".format(parameter, value)	
	
	return "{}://{}{}?{}#{}".format(scheme, netloc, path, query, fragment)
