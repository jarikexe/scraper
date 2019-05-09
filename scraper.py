#! /usr/bin/python
# from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup
import requests
import json
from colorama import Fore, Style
import pprint
pp = pprint.PrettyPrinter(indent=4)



def getJsonFromLinks(html):
	"""Takes html with <a> and return json with title:url"""
	links = dict()
	for link in html:
		print(Style.RESET_ALL)
		title = link.getText().strip()
		_link = link['href']
		links.update({title : _link})
	return links
def save_to_file(data):
	"""Save parsed data to file"""
	try:
		output_file = open("output.json", "w")
		output_file.write(json.dumps(data))
	except:
	    print(Fore.GREEN  + "File not found or path is incorrect")
	finally:
	    print(Fore.GREEN  +  "Success go to output.json to look at the json")

main_website = "https://n1.kabbalaha.site/bbs/board.php?bo_table=enter&sca=&sop=and&sfl=wr_subject&stx=%EB%9F%B0%EB%8B%9D%EB%A7%A8&x=0&y=0"

req = urllib.request.Request(main_website, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)

if(res):
	print(Fore.BLUE + "Connection asteblished \n")

page_soup = soup(res, 'html.parser')
table_soup = page_soup.find("table", {"class": "fz_board"})
all_items = table_soup.findAll("tr")

items = []
res.close()

for item in all_items:
	try:
		title = item.find('td', {'class':'fz_subject'})
		link = title.a['href']
		items.append({"title" : title.getText().strip(), "first_lvl_link": link})

		print(Fore.GREEN + "I found such lik: ")
		print(Style.RESET_ALL)
		print(link)
	except:
		print(Fore.RED + "no title")
for item in items:
	link = item["first_lvl_link"]
	req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	print(Fore.BLUE + "try to go to :" + link)
	res = urllib.request.urlopen(req)
	page_soup = soup(res, 'html.parser')
	container_div = page_soup.find("section", {"id": "bo_v_atc"})
	links_html = container_div.findAll("a");
	item.update({"liks": getJsonFromLinks(links_html)})


	print(Style.RESET_ALL)
	res.close()
save_to_file(items)
print(Style.RESET_ALL)
