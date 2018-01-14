import mechanicalsoup
import csv
from html.parser import HTMLParser
import re #module to support Regular Expressions
import time
import random

#============================ ALTERNATE STEPS ==================================================# 
# Alternate steps are to follow the route of reading all the data from a single html file.
# If there is no alternate route for that step, that step works for both routes (except step 2)
#===============================================================================================#

#Date the data was last generated
last_run_date="8/17/18"

###### STEP 1 ALTERNATE
browser = mechanicalsoup.StatefulBrowser()

###### STEP 2 SKIPPED

###### ALTERNATE STEP 3
f = open('wa.html', 'r')
temp_array = re.findall(r'title=".*?"',f.read())

###### ALTERNATE STEP 4
#Parses out each company name and adds them to an array
company_names_array=[]
for title in temp_array:
    temp=title.split('"')
    temp[1] = re.sub(r",", "", temp[1]) #gets rid of commas in names that will screw with our csv formatting
    temp[1] = re.sub(r"&amp;", "&", temp[1]) #turns html escaped ampersands into normal ampersands
    temp[1] = re.sub(r"&amp", "&", temp[1]) #turns html escaped ampersands into normal ampersands
    temp[1] = re.sub(r"&#39;", "'", temp[1]) #turns html escaped apostrophes into normal apostrophes
    temp[1] = re.sub(r"&#39", "'", temp[1]) #turns html escaped apostrophes into normal apostrophes
    company_names_array.append(temp[1])

company_names_array.remove('Directory Search')
company_names_array.remove('Home')
company_names_array.remove('Visit our Facebook page')
company_names_array.remove('Visit our Twitter page')
company_names_array.remove('Visit our LinkedIn page')
company_names_array.remove('Enter Value')
company_names_array.remove('Click here to sort')
company_names_array.remove('Click here to sort')
company_names_array.remove('Click here to sort')
company_names_array.remove('Click here to sort')
company_names_array.remove('Click here to sort')
company_names_array.remove('Click here to sort')

###### ALTERNATE STEP 5
f = open('wa.html', 'r')
temp_array = re.findall(r'href="https://directory.agc.org/Party.aspx\?ID=.*?"',f.read())

###### STEP 6
# parses out each company id and adds them to an array
# parses out each company link and adds them to an array
company_id_array=[]
company_link_array=[]
for data in temp_array:
    temp=data.split('=')
    temp[2] = re.sub(r'"', "", temp[2]) #gets rid of the last double quote attached to the end of the split
    temp[1] = re.sub(r'"', "", temp[1]) #gets rid of the first double quote attached to the end of the split
    company_id_array.append(temp[2])
    company_link_array.append(temp[1] + "=" + temp[2])

###### STEP 7
# Using mechanical soup, follow each link for each company and scrape the work-phone, website, and full address
# Due to trying to seem less-like-a-bot, this step may take awhile
company_phone_array=[]
company_address_array=[]
company_website_array=[]
for link in company_link_array:
    browser.open(link)
    time.sleep(1) #assign a sleep time (2-16 seconds) before getting data to help simulate non-bot actions
    #code to correctly parse out the phone
    phone=browser.get_current_page().find(id=re.compile("CsContact.WorkPhone"))
    phone=str(phone)
    phone=phone.split('>')
    phone=re.sub(r'</span', "", phone[1])
    phone=re.sub(r'\(', "", phone)
    phone=re.sub(r'\) ', "-", phone)
    #code to correctly parse out the website
    website=browser.get_current_page().find(id=re.compile("CsContact.Website"))
    website=str(website)
    website=website.split('>')
    website=re.sub(r'</a', "", website[2])
    #code to correctly parse out the full mailing address
    address=browser.get_current_page().find(id=re.compile("ciNewContactAddress__address"))
    address=str(address)
    address=address.split('>')
    address[1]=re.sub(r'<br/', " ", address[1])
    address[1]=re.sub(r',', "", address[1])
    address[2]=re.sub(r'</span', "", address[2])
    address[2]=re.sub(r'<br/', "", address[2])
    address[2]=re.sub(r'  ', " ", address[2])
    address[2]=re.sub(r',', "", address[2])
    address=address[1]+address[2]
    company_phone_array.append(phone)
    company_address_array.append(address)
    company_website_array.append(website)

###### ALTERNATE STEP 8
f = open('wa.html', 'r')
temp_array = re.findall(r'</a></td><td role="gridcell">.*?</td><td role="gridcell">.*?</td><td role="gridcell">.*?</td><td role="gridcell">.*?</td>',f.read())

###### ALTERNATE STEP 9
company_city_array=[]
company_state_array=[]
company_chapter_array=[]
company_description_array=[]
for info in temp_array:
    temp=info.split('<td role="gridcell">')
    temp[1] = re.sub(r'</td>', "", temp[1]) #gets rid of the end tag on the city
    temp[2] = re.sub(r'</td>', "", temp[2]) #gets rid of the end tag on the state
    temp[3] = re.sub(r'</td>', "", temp[3]) #gets rid of the end tag on the chapter
    temp[4] = re.sub(r'</td>', "", temp[4]) #gets rid of the end tag on the description
    temp[4] = re.sub(r"&amp;", "&", temp[4]) #turns html escaped ampersands into normal ampersands
    company_city_array.append(temp[1])
    company_state_array.append(temp[2])
    company_chapter_array.append(temp[3])
    company_description_array.append(temp[4])

###### STEP 10 (& Alternate Step 10)
#Creates a bigger list that all the little lists are merged into
biglist=[]
i=0
for name in company_names_array:
    templist = []
    templist.append(name)
    templist.append(company_id_array[i])
    templist.append(company_city_array[i])
    templist.append(company_state_array[i])
    templist.append(company_chapter_array[i])
    templist.append(company_description_array[i])
    templist.append(company_address_array[i])
    templist.append(company_phone_array[i])
    templist.append(company_website_array[i])
    i+=1
    biglist.append(templist)

###### STEP 11 (FINAL STEP)
#If you're not familiar with the 'with' statement, it basically encloses its contents in a try...finally block that closes the file in the finally part.
# - 'https://stackoverflow.com/questions/3216954/python-no-csv-close' 
with open('agc_site_wa_data.csv', 'w') as f:
    #z = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    z = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    z.writerow(["Data Generated %s" % last_run_date])
    z.writerow(["Company", "AGC ID", "City", "State",  "AGC Chapter", "Description", "Address", "Work-Phone", "Website"])
    for _list in biglist:
        z.writerow(_list)
