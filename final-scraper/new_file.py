from splinter import Browser
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import time
import csv
import time

#urls = [
#'https://infoseek.wunderground.com/history/airport/VOHY/2015/7/1/CustomHistory.html?dayend=1&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=', 
#'https://infoseek.wunderground.com/history/airport/VELR/2016/8/1/CustomHistory.html?dayend=1&monthend=8&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=', 
#'https://infoseek.wunderground.com/history/airport/VOBG/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VEPT/2016/8/1/CustomHistory.html?dayend=1&monthend=8&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VAGO/2016/8/1/CustomHistory.html?dayend=1&monthend=8&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VOTV/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VABP/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VABB/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VEGT/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VEBS/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VOMM/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VILK/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=',
#'https://infoseek.wunderground.com/history/airport/VERC/2015/8/5/CustomHistory.html?dayend=5&monthend=8&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
#]

browser = Browser('firefox')
urls = open('custom-info.csv','r')
csvreader = csv.reader(urls)

for url in urls:
	print("second")
	browser.visit(url)
	time.sleep(3)
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html5lib')
	for x in range(1,15):

		for i in range(2000,2016):
			browser.select("month","7")
			dropdown = browser.find_by_xpath("//*[@name='year']").first
			for option in dropdown.find_by_tag('option'):
				if option.text ==  str(i):
					option.click()
			dropdown = browser.find_by_xpath("//*[@name='yearend']").first
			for option in dropdown.find_by_tag('option'):
				if option.text ==  str(i + 1):
					option.click()

			csvFile = open(str(x) + "-" + str(i) + '.csv','wt')
			writer = csv.writer(csvFile)
			print("here")
			data = soup.find_all('table', id='obsTable')[0]
			writer.writerow (["month","highTemp","avgTemp","lowTemp","highDew","avgDew","lowDew","highHumid","avgHumid","lowHumid","highSeaPressure","avgSeaPressure","lowSeaPressure","highVisi","avgVisi","lowVisi","highWind","avgWind","lowWind","sum_1","events"])
			print("hello")


			for row in data.findAll('tr')[1:]:
				try:	
					col = row.findAll('td')



					month= col[0].getText().strip("\n")
					highTemp= col[1].getText().strip("\n")
					avgTemp= col[2].getText().strip("\n")
					lowTemp= col[3].getText().strip("\n")
					highDew= col[4].getText().strip("\n")
					avgDew = col[5].getText().strip("\n")
					lowDew = col[6].getText().strip("\n")
					highHumid = col[7].getText().strip("\n")
					avgHumid = col[8].getText().strip("\n")
					lowHumid = col[9].getText().strip("\n")
					highSeaPressure = col[10].getText().strip("\n")
					avgSeaPressure = col[11].getText().strip("\n")
					lowSeaPressure = col[12].getText().strip("\n")
					highVisi = col[13].getText().strip("\n")
					avgVisi = col[14].getText().strip("\n")
					lowVisi = col[15].getText().strip("\n")
					highWind = col[16].getText().strip("\n")
					avgWind = col[17].getText().strip("\n")
					lowWind = col[18].getText().strip("\n")
					sum_1 = col[19].getText().strip("\n")
					events = col[20].getText().strip("\n")
					fieldnames = (month,highTemp,avgTemp,lowTemp,highDew,avgDew,lowDew,highHumid,avgHumid,lowHumid,highSeaPressure,avgSeaPressure,lowSeaPressure,highVisi,avgVisi,lowVisi,highWind,avgWind,lowWind,sum_1,events)
					writer.writerow(fieldnames)
				except IndexError:
					continue
					time.sleep(10)
					browser.find_by_xpath("//*[@class='button radius custom-date-get-history']").first.click()

