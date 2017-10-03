from splinter import Browser
import time
import re
from mysql.connector import MySQLConnection, Error
from splinter.exceptions import ElementDoesNotExist
import sys

browser = Browser('phantomjs')
time.sleep(1)
try:
	conn = MySQLConnection(host='localhost',database='gujarat_test',user='root',password='messi123')
	cursor =  conn.cursor()
	cursor1 = conn.cursor()
	cursor2 = conn.cursor()
	cursor3 = conn.cursor()
	cursor4 = conn.cursor()
	cursor5 = conn.cursor()
	cursor6 = conn.cursor()
except Error as e:
	print(e)

t=""

# 4 for loops to hierarchically accessing state -> district -> tehsil -> village, if execution stops at a certain point due to some
# error replace 0 in range of i with current state id, 0 of x with current district id, 0 of y with current tehsil id and so on for z and village id
# to resume execution but reset them after on going tehsil or district is done to access next tehsil or district from the first element. 
i = 11
district_id=1
village_id=1
tehsil_id=1
FLAGprime = True
for x in range(0,75):
	if FLAGprime:
		flagPr = True
		for y in range(0,100):
			if flagPr:
				tnumv =0
				flagP = True
				for z in range(0,160):
					if flagP:
						url = "https://villageinfo.in/"
						browser.visit(url)
						# time.sleep(1)
						state = browser.find_by_xpath(".//div[@class='tab']")
						elements = state.find_by_tag('a')

						flag = True
						try:
							state_id = i+1
							state_name = str(elements[i].text)
							slink = elements[i]['href']
						except ElementDoesNotExist as e:
							print(e)
							flag = False
							break

						squery = "INSERT INTO state(stateID,stateName) VALUES (%s,%s);"
						sargs = (str(state_id),state_name)
						sqry = "SELECT stateName FROM state;"
						try:
							if conn.is_connected():
								cursor1.execute(sqry)
								result1 = cursor1.fetchall()
								f = 1
								for row in result1:
									if (state_name == row[0]):
										f = 0
								if f == 1:
									print("MySQL connected!")
									cursor.execute(squery,sargs)
									conn.commit()
						except Error as e:
							print(e)

						if flag :
							browser.visit(slink)
							# time.sleep(1)
							state_population_type = browser.find_by_xpath('.//div[@class="column"][@data-label="Population Type"]')
							state_male_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Male Population"]')
							state_female_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Female Population"]')
							state_total_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Total Population"]')
							siquery = "INSERT IGNORE INTO stateinfo(stateID,popType,malePop,femalePop,totalPop) VALUES (%s,%s,%s,%s,%s);"
							siqry = "SELECT stateID,popType from stateinfo;"
							for k in range(1,len(state_population_type)):
								siargs = (str(state_id),str(state_population_type[k].text),str(state_male_population[k].text),str(state_female_population[k].text),str(state_total_population[k].text))
								try:
									if conn.is_connected():
										cursor2.execute(siqry)
										result2 = cursor2.fetchall()
										f = 1
										for row in result2:
											if ((str(state_id) == row[0]) and (str(state_population_type[k].text) == row[1])):
												f = 0
										if f == 1:
											print("state info pushed.")
											cursor.execute(siquery,siargs)
											conn.commit()
								except Error as e:
									print(e)

							# time.sleep(1)
							district = browser.find_by_xpath('.//div[@class="tab"]')
							elem = district.find_by_tag('a')
							flag2 = True

							try:
								district_id = x+1
								print(district_id)
								district_name = str(elem[x].text)
								dlink = elem[x]['href']
							except ElementDoesNotExist as e:
								print(e)
								flag2 = False
								FLAGprime = False
								break

							dquery = "INSERT INTO district(stateID,districtID,districtName) VALUES (%s,%s,%s);"
							dargs = (str(state_id),str(district_id),district_name)
							dqry = "SELECT districtName FROM district;"
							try:
								if conn.is_connected():
									cursor3.execute(dqry)
									result3 = cursor3.fetchall()
									f=1
									for row in result3:
										if (district_name == row[0]):
											f=0

									if f==1:
										print("MySQL connected..")
										cursor.execute(dquery,dargs)
										conn.commit()
							except Error as e:
								print(e)

							if flag2:
								browser.visit(dlink)
								# time.sleep(1)
								district_population_type = browser.find_by_xpath('.//div[@class="column"][@data-label="Population Type"]')
								district_male_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Male Population"]')
								district_female_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Female Population"]')
								district_total_population = browser.find_by_xpath('.//div[@class="column"][@data-label="Total Population"]')

								diquery = "INSERT INTO districtinfo(stateID,districtID,popType,malePop,femalePop,totalPop) VALUES (%s,%s,%s,%s,%s,%s);"
								diqry = "SELECT stateID,districtID,popType from districtinfo;"
								for k in range(1,len(district_population_type)):
									diargs = (str(state_id),str(district_id),str(district_population_type[k].text),str(district_male_population[k].text),str(district_female_population[k].text),str(district_total_population[k].text))
									try:
										if conn.is_connected():
											cursor4.execute(diqry)
											result4 = cursor4.fetchall()
											f = 1
											for row in result4:
												if((str(state_id)==row[0]) and (str(district_id)==row[1]) and (str(district_population_type[k].text)==row[2])):
													f=0

											if f==1:
												print("District info pushed")
												cursor1.execute(diquery,diargs)
												conn.commit()
									except Error as e:
										print(e)

								# time.sleep(1)
								tehsil = browser.find_by_xpath(".//div[@class='tab']")
								elems = tehsil.find_by_tag('a')
								flag3 = True

								try:
									tehsil_id = y+1
									print(tehsil_id)
									tehsil_name = str(elems[y].text)
									tlink = elems[y]['href']
								except ElementDoesNotExist as e:
									print(e)
									flag3 = False
									flagPr = False
									break

								tquery = "INSERT INTO tehsil(tehsilID,tehsilName,stateID,districtID) VALUES (%s,%s,%s,%s);"
								targs = (str(tehsil_id),tehsil_name,str(state_id),str(district_id))
								tqry = "SELECT tehsilName from tehsil;"
								try:
									if conn.is_connected():
										cursor5.execute(tqry)
										result5 = cursor5.fetchall()
										f = 1
										for row in result5:
											if (tehsil_name==row[0]):
												f = 0
												print(row[0],"I am here")
										if f==1:
											print("MySQL connected....")
											cursor.execute(tquery,targs)
											conn.commit()
											print("Tehsil pushed")
								except Error as e:
									print(e)

								if flag3:
									browser.visit(tlink)
									# time.sleep(1)
									village = browser.find_by_xpath(".//div[@class='tab']")
									el = village.find_by_tag('a')
									tnumv = len(el)

									flag4 = True
									try:
										village_id = z+1
										village_name = str(el[z].text)
										vlink = el[z]['href']
									except ElementDoesNotExist as e:
										print(e)
										flag4 = False
										flagP = False
										break

									vquery = "INSERT INTO village(villageID,villageName,tehsilID,districtID,stateID) VALUES (%s,%s,%s,%s,%s);"
									vargs = (str(village_id),village_name,str(tehsil_id),str(district_id),str(state_id))
									print(village_id)
									print(village_name)
									print(tehsil_id)
									print(district_id)
									print(state_id)
									try:
										if conn.is_connected():
											print("Village added")
											cursor.execute(vquery,vargs)
											conn.commit()
									except Error as e:
										print(e,'inf not pushed')

									if flag4:
										browser.visit(vlink)
										print(vlink)
										# time.sleep(10)
										village_desc = browser.find_by_xpath(".//p[@class='text-justify']")
										village_info = str(village_desc.text)
										try:

											villageName = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[1]/td").first.value
											print(villageName)
											Gram_Panchayat =  browser.find_by_xpath('/html/body/div/div[2]/div[2]/table/tbody/tr[2]/td[2]').first.value
											print(Gram_Panchayat)
											Tehsil = browser.find_by_xpath('//html/body/div/div[2]/div[2]/table/tbody/tr[3]/td[2]').first.value
											print(Tehsil)
											District = browser.find_by_xpath('/html/body/div/div[2]/div[2]/table/tbody/tr[4]/td[2]').first.value
											print(District)
											State = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[5]/td[2]").first.value
											print(State)
											Pincode = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[6]/td[2]").first.value
											print(Pincode)
											Area = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[7]/td[2]").first.value
											print(Area)
											Population = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[8]/td[2]").first.value
											print(Population)
											Households = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[9]/td[2]").first.value
											print(Households)
											Nearest_town = browser.find_by_xpath("/html/body/div/div[2]/div[2]/table/tbody/tr[10]/td[2]").first.value
											print(Nearest_town)

											viquery = "INSERT INTO villageinfo(stateID,districtID,villageID,villageName,Gram_Panchayat,Tehsil,District,State,Pincode,Area,Population,Households,Nearest_town ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
											viargs = (str(state_id),str(district_id),str(village_id),village_name,Gram_Panchayat,Tehsil,District,State,str(Pincode),str(Area),str(Population),str(Households),Nearest_town)
											print(state_id,type(Population),len(Population.encode('utf-8')),'display type of msg')
											viqry = "SELECT villageName FROM villageinfo;"
											try:
												if conn.is_connected():
													cursor6.execute(viqry)
													result6 = cursor6.fetchall()
													f = 1
													for row in result6:
														if (str(village_name)==row[0]):
															f=0

													if f==1:
														print("village info pushed.")
														cursor.execute(viquery,viargs)
														conn.commit()
											except Error as e:
												print(e,"villageinfo not pushed")
										except:
											print("no table found")

										t = str(tehsil_id)
				n = ("'"+str(tnumv)+"'")
				tuquery = ("UPDATE `tehsil` SET `numVillage`="+n+" WHERE tehsilID="+t+";")
				try:
					cursor.execute(tuquery)
					conn.commit()
					print("updated tehsil")
				except Error as e:
					print(e)

	cursor.close()
	cursor1.close()
	cursor2.close()
	cursor3.close()
	cursor4.close()
	cursor5.close()
	cursor6.close()
	conn.close()
