# -*- coding: UTF-8 -*-
import mechanicalsoup
import csv
from html.parser import HTMLParser
import re #module to support Regular Expressions
import time
import random

#====================================== NOTES ==================================================# 
# This script follows the route of reading all the data from a single html file.
# This code has been altered so as to not reveal the nature of it's intent for any particular website.
# Author: Devin Carpenter
#===============================================================================================#

#Date the data was last generated
last_run_date="8/17/18"

###### STEP 1
f = open('slimmed.html', mode='r',encoding="utf-8") #open file
temp = f.read() #assign data in file to variable
temp = re.sub(r"\n", "", temp) #remove newline special chars

browser = mechanicalsoup.StatefulBrowser()
member_array=re.findall(r'div class="memberBox .*?qqqqq',temp) #get memberBox array of data
company_name_array=[]
company_description_array=[]
company_classifications_array=[]
company_special_info_array=[]
company_website_array=[]
company_phone_array=[]
company_toll_free_array=[]
company_fax_array=[]
company_unknown_group_data_array=[]
company_address_array=[]
company_mailing_address_array=[]
company_contacts_array=[]
member_count=0
#for each company in the array of data...dollect its data...then add it to appropriate lists
for member in member_array:
    print("Starting Member "+str(member_count))
    browser.open_fake_page(member) #opens a page with temp as its data...so can still use mechanicalSoup once the data is got in a variable.
    company_name=''
    company_description=''
    company_classifications=''
    company_special_info=''
    company_website=''
    company_phone=''
    company_toll_free=''
    company_fax=''
    company_unknown_group_data=[]
    company_address=''
    company_mailing_address=''
    company_contacts=[]
    #parses out the company name
    company_name = browser.get_current_page().find("h2") # Gets the name of the company
    company_name=str(company_name)
    company_name=re.sub('<.*?>','',company_name)
    company_name = re.sub(r"&amp;", "&", company_name)
    company_name = re.sub(r"&amp", "&", company_name)
    print('FIRST')
    #parses out the company description
    company_description = browser.get_current_page().find_all("div", class_="groupWrapper")[0:1] #Get first groupWrapper (descr.)
    print(100)
    if len(company_description) != 0:
        company_description[0]=str(company_description[0]) #turns the tag in the list to a string
        company_description=''.join(company_description) #joins the list to an empty string, making the variable a single string
        company_description=re.sub('<.*?>','',company_description)
        company_description = re.sub(r"&amp;", "&", company_description)
        company_description = re.sub(r"&amp", "&", company_description)
        company_description = re.sub(r"\\n", " ", company_description)
        company_description = re.sub(r";", "::", company_description)
    print('SECOND')
    #parses out the company classifications
    company_classifications = browser.get_current_page().find_all("div", class_="groupWrapper")[1:2] #Get second groupWrapper (class.)
    print(200)
    if len(company_classifications) != 0:
        company_classifications[0]=str(company_classifications[0])
        company_classifications=''.join(company_classifications)
        company_classifications=re.sub('<.*?>','',company_classifications)
        company_classifications = re.sub(r"&amp;", "&", company_classifications)
        company_classifications = re.sub(r"&amp", "&", company_classifications)
        company_classifications = re.sub(r";", "::", company_classifications)
    print('THIRD')
    #parses out the company special info
    company_special_info = browser.get_current_page().find_all("div", class_="groupWrapper")[2:3] #Get third groupWrapper (special)
    print(300)
    if len(company_special_info) != 0:
        company_special_info[0]=str(company_special_info[0])
        company_special_info=''.join(company_special_info)
        company_special_info=re.sub('<.*?>','',company_special_info)
    print('FOURTH')
    #parses out the website, phone number, toll-free number, and fax number
    company_grouped_info = browser.get_current_page().find_all("div", class_="groupWrapper")[3:4] #Get fourth groupWrapper (grouping)
    print(400)
    if len(company_grouped_info) != 0:
        company_grouped_info[0]=str(company_grouped_info[0])
        company_grouped_info=''.join(company_grouped_info)
        company_grouped_info=company_grouped_info.split('<span>')
    website_regex='^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9A-Z]+([\-\.]{1}[a-z0-9A-Z]+)*\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
    i=0
    for group in company_grouped_info:
        group=re.sub('<.*?>','',group)
        group=re.sub(';','',group)
        group=group.strip()
        print (group)
        if str(type(re.search(website_regex, group))) == "<class '_sre.SRE_Match'>":#check for website group
            #within 4th groupWrapper, get website
            company_website=group
        elif re.search('Phone', group):#check for phone group
            #within 4th groupWrapper, get phone number
            company_phone=group
            company_phone=re.sub(r'Phone: ','',company_phone)
            company_phone=re.sub(r'Phone:','',company_phone)
            company_phone=re.sub(r'\(','',company_phone)
            company_phone=re.sub(r'\) ','-',company_phone)
            company_phone=re.sub(r'\)','-',company_phone)
        elif re.search('Toll Free', group):#check for toll free group
            #within 4th groupWrapper, get toll-free number
            company_toll_free=group
            company_toll_free=re.sub(r'Toll Free: ','',company_toll_free)
            company_toll_free=re.sub(r'Toll Free:','',company_toll_free)
            company_toll_free=re.sub(r'\(','',company_toll_free)
            company_toll_free=re.sub(r'\) ','-',company_toll_free)
            company_toll_free=re.sub(r'\)','-',company_toll_free)
        elif re.search('Fax', group):#check for fax group
            #within 4th groupWrapper, get fax number
            company_fax=group
            company_fax=re.sub(r'Fax: ','',company_fax)
            company_fax=re.sub(r'Fax:','',company_fax)
            company_fax=re.sub(r'\(','',company_fax)
            company_fax=re.sub(r'\) ','-',company_fax)
            company_fax=re.sub(r'\)','-',company_fax)
        else: #otherwise add to unknown group data
            if i != 0:#if not the first group (empty data), then dunno what the data is
                group=group.replace(',',' ') #replaces commas in string with a space
                group=group.strip() #removes all leading and ending whitespace
                company_unknown_group_data.append(group)
        i+=1
    #parses out the regular address (possibly mailing address)
    company_address = browser.get_current_page().find_all("div", class_="groupWrapper")[4:5] #Get fifth groupWrapper (mailing or reg/street address)
    print(500)
    if len(company_address) > 0:
        temp = company_address[0]
        if company_address[0] is not None:
            if temp.has_attr("class"):
                if 'groupWrapper' in temp.get("class"):
                    temp = temp.find_next_sibling("div") #get the next sibling of the fifth groupWrapper
                    #Start the actual parsing, element is the fifth groupWrapper
                    if len(company_address) != 0:
                        company_address[0]=str(company_address[0])
                        company_address=''.join(company_address)
                        company_address=re.sub('<.*?>','',company_address)
                        company_address=re.sub('\\xa0\\xa0',' ',company_address)
                        company_address=re.sub('  ',' ',company_address)
                        if str(type(re.search('Mailing Address', company_address))) == "<class '_sre.SRE_Match'>":
                            company_mailing_address=company_address
                            company_address=''
    else:
        company_address=''
    #parses out the mailing address, if there isn't already a mailing address
    if temp is not None:
        if temp.has_attr("class"):
            if 'groupWrapper' in temp.get("class"):
                if type(company_mailing_address) != str:#If company_mailing_address wasn't already defined above
                    #Start actual parsing, element is sixth groupWrapper
                    company_mailing_address = browser.get_current_page().find_all("div", class_="groupWrapper")[5:6]#Get sixth groupWrapper (mailing address)
                    print(600)
                    if len(company_mailing_address) != 0:
                        company_mailing_address=re.sub('<.*?>','',company_mailing_address)
                        company_mailing_address=re.sub('\\xa0\\xa0',' ',company_mailing_address)
                        company_mailing_address=re.sub('  ',' ',company_mailing_address)
            elif 'contactWrapper' in temp.get("class"):
                #Get all the contactWrappers and parse their information into a list string to be inserted into csv
                temp_contacts = browser.get_current_page().find_all("div", class_="contactWrapper") #Get contacts from contactWrapper
                print(700)
                if len(company_mailing_address) != 0:
                    company_contacts='['
                    first='true'
                    for contact in temp_contacts:
                        description=''
                        contact=str(contact)
                        contact=contact.split('">')
                        contact[3]=re.sub(r'</a></strong> ','',contact[3])
                        contact[3]=re.sub(r'</a></strong>','',contact[3])
                        contact[3]=re.sub(r'</div> <div class="groupWrapper','',contact[3])
                        contact[3]=re.sub(r'</div><div class="groupWrapper','',contact[3])
                        has_description='<em>' in contact[3]
                        if '<em>' in contact[3]:
                            temp=contact[3].split('<em>')
                            contact[3]=temp[0] #sets the name
                            description=temp[1] #sets the description
                            description=re.sub(r'</em></div> ','',description)
                            description=re.sub(r'</em></div>','',description)
                            description+=': '
                            contact[3]=re.sub(r'<div>','',contact[3])
                        contact[6]=re.sub(r'</a></div></div>','',contact[6])
                        contact[3]=contact[3].replace(',',' ') #replaces commas in string with a space
                        contact[3]=contact[3].strip() #removes all leading and ending whitespace
                        contact[6]=contact[6].replace(',',' ') #replaces commas in string with a space
                        contact[6]=contact[6].strip() #removes all leading and ending whitespace
                        company_contacts+=(contact[3] + ': ' + description + contact[6] + '][')
                    company_contacts=company_contacts[:-1] # remove the last opening square bracket
            else:
                print('Class in last element was neither groupWrapper nor contactWrapper!')
    
    company_name=company_name.replace(',',' ') #replaces commas in string with a space
    company_name=company_name.strip() #removes all leading and ending whitespace
    company_description=company_description.replace(',',' -') #replaces commas in string with a space
    company_description=company_description.strip() #removes all leading and ending whitespace
    company_classifications=company_classifications.replace(',','::') #replaces commas in string with a space
    company_classifications=company_classifications.strip() #removes all leading and ending whitespace
    company_special_info=company_special_info.replace(',',' ') #replaces commas in string with a space
    company_special_info=company_special_info.strip() #removes all leading and ending whitespace
    company_website=company_website.replace(',',' ') #replaces commas in string with a space
    company_website=company_website.strip() #removes all leading and ending whitespace
    company_phone=company_phone.replace(',',' ') #replaces commas in string with a space
    company_phone=company_phone.strip() #removes all leading and ending whitespace
    company_toll_free=company_toll_free.replace(',',' ') #replaces commas in string with a space
    company_toll_free=company_toll_free.strip() #removes all leading and ending whitespace
    company_fax=company_fax.replace(',',' ') #replaces commas in string with a space
    company_fax=company_fax.strip() #removes all leading and ending whitespace
    #print(company_address)
    company_address=company_address.replace(',',' ') #replaces commas in string with a space
    company_address=company_address.strip() #removes all leading and ending whitespace
    company_mailing_address=company_mailing_address.replace(',',' ') #replaces commas in string with a space
    company_mailing_address=company_mailing_address.strip() #removes all leading and ending whitespace
    #if any variables are undefined from the parsing, then just write yyemptyy
    try:
        company_name_array.append(company_name)
    except NameError:
        company_name_array.append("yyemptyy")
    try:
        company_description_array.append(company_description)
    except NameError:
        company_description_array.append("yyemptyy")
    try:
        company_classifications_array.append(company_classifications)
    except NameError:
        company_classifications_array.append("yyemptyy")
    try:
        company_special_info_array.append(company_special_info)
    except NameError:
        company_special_info_array.append("yyemptyy")
    try:
        company_website_array.append(company_website)
    except NameError:
        company_website_array.append("yyemptyy")
    try:
        company_phone_array.append(company_phone)
    except NameError:
        company_phone_array.append("yyemptyy")
    try:
        company_toll_free_array.append(company_toll_free)
    except NameError:
        company_toll_free_array.append("yyemptyy")
    try:
        company_fax_array.append(company_fax)
    except NameError:
        company_fax_array.append("yyemptyy")
    try:
        company_unknown_group_data_array.append(company_unknown_group_data)
    except NameError:
        company_unknown_group_data_array.append("yyemptyy")
    try:
        company_address_array.append(company_address)
    except NameError:
        company_address_array.append("yyemptyy")
    try:
        company_mailing_address_array.append(company_mailing_address)
    except NameError:
        company_mailing_address_array.append("yyemptyy")
    try:
        company_contacts_array.append(company_contacts)
    except NameError:
        company_contacts_array.append("yyemptyy")
    member_count+=1

#Creates a bigger list that all the little lists are merged into
biglist=[]
i=0
for name in company_name_array:
    templist = []
    templist.append(name)
    templist.append(company_description_array[i])
    templist.append(company_classifications_array[i])
    templist.append(company_special_info_array[i])
    templist.append(company_website_array[i])
    templist.append(company_phone_array[i])
    templist.append(company_toll_free_array[i])
    templist.append(company_fax_array[i])
    templist.append(company_unknown_group_data_array[i])
    templist.append(company_address_array[i])
    templist.append(company_mailing_address_array[i])
    templist.append(company_contacts_array[i])
    i+=1
    biglist.append(templist)

#Writes the data from each list in biglist to a .csv file that can be viewed with an Excel type program
with open('data2.csv', mode='w',encoding="utf-8") as f:
    #z = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    z = csv.writer(f, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    z.writerow(["Data Generated %s" % last_run_date])
    z.writerow(["Company", "Description", "Classifications", "Special Info",  "Website", "Phone", "Toll Free Number", "Fax Number",
        "Unknown_Grouped_data", "Address", "Mailing Address", "Contacts"])
    for _list in biglist:
        z.writerow(_list)


