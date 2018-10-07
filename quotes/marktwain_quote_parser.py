from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import json

my_url =  "https://www.goodreads.com/quotes/search?q=mark+twain&commit=Search";

client = urlopen(my_url)
expedia_html = client.read()
client.close()

quote_soup = soup(expedia_html,"html.parser")
quote_container = quote_soup.find("div",{"class":"leftContainer"}).findAll("div",{"class","quoteDetails"})

quoteList = []
counter = 0

for each in quote_container:
	if(counter>=10):
		break

	child_soup = soup(str(each),"html.parser")
	quoteContent = child_soup.find("div",{"class":"quoteText"})
	

	if not quoteContent.span or not quoteContent.span.text or "mark twain" not in quoteContent.span.text.lower() or not quoteContent.children:
		continue
	
	counter+=1

	obj = {}
	
	obj['quote'] = quoteContent.children.__next__().encode("ascii", errors="ignore").decode().strip()
	obj['likes'] = child_soup.find("div",{"class":"quoteFooter"}).find("a",{"class","smallText"}).text

	quoteList.append(obj)

with open('quotes.json','w+') as f:
	json.dump(quoteList, f, indent=4)