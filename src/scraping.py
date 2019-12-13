#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from pandas import Series,DataFrame
import math
import requests
from bs4 import BeautifulSoup
import json


# In[1]:


def glassdoor_get(keyword_job,username_user,password_user,location_job,jobs_num):
    #keyword means the job title you want to search
    #username and password is the information of your glassdoor account
    #location is the place where you want to find a job
    #job_num means the number of jobs that you want to scraping
    browser = webdriver.Chrome()
    url = 'https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK' 
    browser.get(url)

    #wait the website is loaded. The time is determined by your computer speed.
    time.sleep(5)
    email = browser.find_element_by_xpath('//*[@id="userEmail"]')
    email.send_keys(username_user)
    time.sleep(1)
    password = browser.find_element_by_xpath('//*[@id="userPassword"]')
    password.send_keys(password_user)
    password.submit()
    
    time.sleep(5)
    job_title = browser.find_element_by_xpath('//*[@id="sc.keyword"]')
    job_title.send_keys(keyword_job)
    time.sleep(.5)
    location = browser.find_element_by_xpath('//*[@id="sc.location"]')
    location.clear()
    location.send_keys(location_job)
    location.submit()


    num_job = 0
    time.sleep(5)

    #compared with dictionary of dictionaries, I prefer to use list of dictionaries. Because the list can show the order of data,
    #which means it can show the ranking of companies by Glassdoor
    content = []
    while num_job <jobs_num:
        status_pagedetail = False
        status_buttonclick = False
        
        while status_pagedetail == False:
            try:
                job_buttons = browser.find_elements_by_class_name("jl")
                time.sleep(1)
                status_pagedetail = True
            except NoSuchElementException:
                print('page detail for the jobs cannot be found. Trying to fix it')
                try:
                    browser.refresh()
                    print('refresh page')
                except:
                    print('refresh page fail')
                
                try:
                    browser.switch_to.alert.accept()
                    print('Alert accept successfully')
                except:
                    print('Alert accept fail')
        status_pagedetail = False
                    
        for job in job_buttons:
            #click the button
            try:
                while status_buttonclick == False:
                    try:
                        button_for_click = job.find_element_by_css_selector('li > div > a')
                        button_for_click.click()
                        time.sleep(2)
                        status_buttonclick = True
                    except NoSuchElementException:
                        print('page detail for the jobs cannot be found. Trying to fix it')
                        try:
                            browser.refresh()
                            print('refresh page')
                        except:
                            print('refresh page fail')

                        try:
                            browser.switch_to.alert.accept()
                            print('Alert accept successfully')
                        except:
                            print('Alert accept fail')
                status_buttonclick = False

                # find the name of company and the overall rating
                try:
                    employerName = browser.find_element_by_xpath('.//div[@class="empInfo newDetails"]/div[@class="employerName"]').text
                    if ('\n'in employerName):
                        employerName = employerName[:-4]
                except NoSuchElementException:
                    employerName = -1

                # job title
                try:
                    title = browser.find_element_by_xpath('.//div[@class="empInfo newDetails"]/div[@class="title"]').text
                except NoSuchElementException:
                    title = -1

                # location of job
                try:
                    location = browser.find_element_by_xpath('.//div[@class="empInfo newDetails"]/div[@class="location"]').text
                except NoSuchElementException:
                    location = -1

                # estimated salary of this job
                try:
                    salary = browser.find_element_by_xpath('//.//div[@class="empInfo newDetails"]/div[@class="salary"]').text
                except NoSuchElementException:
                    salary = -1

                test_num = 0
                status_des = False
                while status_des == False:
                    try:
                        description = browser.find_element_by_xpath('//*[@class="jobDesc"]').text
                        status_des = True
                    except NoSuchElementException:
                        print('no such item')
                        time.sleep(2)
                        test_num += 1
                    if test_num >3:
                        description = -1
                        status_des = True

                #change to company tab
                try:
                    time.sleep(2)
                    browser.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                    time.sleep(2)

                    #company size
                    try:
                        size = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1

                    #company headquarters
                    try:
                        Headquarters = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div//label[text()="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        Headquarters = -1

                    # the revenue of this company
                    try:
                        Revenue = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        Revenue = -1

                    #the industry
                    try:
                        industry = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1

                    # sector
                    try:
                        sector = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1

                # It is possible that there is no company tab for this job
                except NoSuchElementException:
                    print('no such company tab')
                    size = -1
                    Headquarters = -1
                    Revenue = -1
                    industry = -1
                    sector = -1

                #change to rating tab
                try:
                    time.sleep(2)
                    browser.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="rating"]').click()
                    time.sleep(2)

                    # detailed rating for Comp_Benefits,Culture_Values,Career_Opportunities,Work_Life_Balance,Senior_Management.
                    try:
                        rating = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/div/span[2]').text
                    except NoSuchElementException:
                        rating = -1

                    try:
                        Comp_Benefits = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/ul/li[1]/span[2]/span').text
                    except NoSuchElementException:
                        Comp_Benefits = -1

                    try:
                        Culture_Values = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/ul/li[2]/span[2]/span').text
                    except NoSuchElementException:
                        Culture_Values = -1

                    try:
                        Career_Opportunities = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/ul/li[3]/span[2]/span').text
                    except NoSuchElementException:
                        Career_Opportunities = -1

                    try:
                        Work_Life_Balance = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/ul/li[4]/span[2]/span').text
                    except NoSuchElementException:
                        Work_Life_Balance = -1

                    try:
                        Senior_Management = browser.find_element_by_xpath('//*[@id="RatingsTrends"]/div[1]/ul/li[5]/span[2]/span').text
                    except NoSuchElementException:
                        Senior_Management = -1

                # not rating tab possible
                except NoSuchElementException:
                    print('no such rating tab')
                    rating = -1
                    Comp_Benefits = -1
                    Culture_Values = -1
                    Career_Opportunities = -1
                    Work_Life_Balance = -1
                    Senior_Management = -1

                #add to content list/ store
                content.append({'company':employerName,
                                'rating_overall':rating,
                                'job title':title,
                                'job location':location,
                                'salary':salary,
                                'company size':size,
                                'headquarters':Headquarters,
                                'company revenue':Revenue,
                                'industry':industry,
                                'sector':sector,
                                'Comp & Benefits':Comp_Benefits,
                                'Culture & Values':Culture_Values,
                                'Career Opportunities':Career_Opportunities,
                                'Work/Life Balance':Work_Life_Balance,
                                'Senior Management':Senior_Management,
                                'description':description})
                print(f'finish search for company {num_job+1} {employerName}')
                num_job += 1
                if num_job >= jobs_num:
                    browser.quit()
                    return content
                
            except ElementClickInterceptedException:
                print('stop')
                time.sleep(10)
                num_job +=1
                pass
        # change to the next page
        browser.find_element_by_xpath('//li[@class="next"]/a').click()    
        time.sleep(5)
    browser.quit()
    return content





def content_to_description(content):
    n = 0
    desc_database = {}
    for item in content:
        if item['company'] == -1 or item['description'] == -1:
            pass
        else:
            desc_database[f'{n}'] = {'company':item['company'],
                                     'description':item['description']}
        n += 1
    return desc_database






def content_to_dataframe(content):
#creat a new content database without the description.
#Meanwhile, some missing data, whose company name is -1, would be reoved.
    n = 0
    content_new = {}
    for item in content:
        if item['company'] == -1:
            pass
        else:
            content_new[f'{n}'] = {'company':item['company'],
                                    'rating_overall':item['rating_overall'],
                                    'job title':item['job title'],
                                    'job location':item['job location'],
                                    'salary':item['salary'],
                                    'company size':item['company size'],
                                    'headquarters':item['headquarters'],
                                    'company revenue':item['company revenue'],
                                    'industry':item['industry'],
                                    'sector':item['sector'],
                                    'Comp & Benefits':item['Comp & Benefits'],
                                    'Culture & Values':item['Culture & Values'],
                                    'Career Opportunities':item['Career Opportunities'],
                                    'Work/Life Balance':item['Work/Life Balance'],
                                    'Senior Management':item['Senior Management']}
        n += 1

    pd_table_content = []
    index_list = []
    for item in content_new:
        pd_table_content.append(content_new[item])
        index_list.append(item)

    # build Pandas DataFrame
    pdtable_content=DataFrame(pd_table_content, index=index_list)
    pdtable_content = pdtable_content.reindex(columns = ['company','rating_overall','job title','job location',
                                              'salary','company size','headquarters','company revenue',
                                              'industry', 'sector','Comp & Benefits','Culture & Values',
                                              'Career Opportunities','Work/Life Balance','Senior Management'])
    return pdtable_content






# In[ ]:
# unfortunately, the number of seriesid is limited to 25
def cpi_get(item_code,area_code,api_bls):
    headers = {'Content-type': 'application/json'}
    series_code = []
    for area in area_code:
        series_code.append(f'CUUR{area}{item_code}')
    data = json.dumps({"seriesid": series_code,"startyear":"2017", "endyear":"2019",'registrationKey': api_bls})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    p=p.json()
    return p





def bls_area():    
    url = 'https://www.bls.gov/lau/laurdqa.htm'
    response3 = requests.get(url)
    soup2 = BeautifulSoup(response3.content, 'lxml')
    main_table = soup2.find('table').find('tbody')
    heading = main_table.find_all('th')
    things = main_table.find_all('td')
    
    pd_table = {}
    thing = []
    
    for he in heading:
        pd_table[he.text] = []
    
    row = 0
    test = 0
    for thing in things:
        if 'rowspan' in thing.attrs:
            row = int(thing['rowspan'])
            pd_table['REGION'] += ([thing.text]*row)
            test = row*2
            continue
        if test == 0:
            continue
        if (test % 2)==0:
            pd_table['DIVISION'] += [thing.text]
            test += -1
        else:
            pd_table['STATES'] += [thing.text]
            test += -1
            
    # build Pandas DataFrame
    pdtable_reigions = DataFrame(pd_table)
    
    return pdtable_reigions


def region_cpi():
    api_bls = 'bc32c0c699704727953b8ed1b9833376'
    url = 'https://download.bls.gov/pub/time.series/cw/cw.area'
    response2 = requests.get(url)
    soup = BeautifulSoup(response2.content, 'lxml')
    file_text = soup.p.text
    
    result1 = file_text.split('\n')[1:-1]
    area_code = []
    area_name = []
    combine_code = {}
    for item in result1:
        area_code.append(item.split('\t')[0])
        area_name.append(item.split('\t')[1])
        combine_code[item.split('\t')[0]] = item.split('\t')[1]
    
    #the code is for All Item. For detail expression, url:https://download.bls.gov/pub/time.series/cw/cw.item
    item_code = 'SA0'
    #there is a limitation of the number, 25, of seriesID. Therefore,multi requests are required
    if len(area_code)>25:
        time_run = math.ceil(len(area_code)/25)
    
    result_final = []
    for num in range(time_run):
        location_now = num*25
        result2 = cpi_get(item_code,area_code[location_now:(location_now+25)],api_bls)['Results']['series']
        time.sleep(1)
        result_final += result2 
    
    result_final_2 = []
    for item in result_final:
        bol_2017 = False
        for issue in item['data']:
            if issue['year'] == '2017':
                bol_2017 = True
                break
        if bol_2017 == True:
            result_final_2.append(item)
            pass
        elif bol_2017 == False:
            pass
    # we just want to the latest data, the CPI in the latest Month in everywhere. Because the data frequency is different,
    # the latest month could be any month in 2019. Moreover, from the last database {result_fina}, there are some data is missing.
    # The missing data:{'seriesID': 'CUURA104SA0', 'data': []},
    #{'seriesID': 'CUURA210SA0', 'data': []},
    #{'seriesID': 'CUURA212SA0', 'data': []},
    #{'seriesID': 'CUURA213SA0', 'data': []},
    #{'seriesID': 'CUURA214SA0', 'data': []},
    #{'seriesID': 'CUURA311SA0', 'data': []},
    #{'seriesID': 'CUURA421SA0', 'data': []},
    #{'seriesID': 'CUURA425SA0', 'data': []},
    #{'seriesID': 'CUURD000SA0', 'data': []},
    #{'seriesID': 'CUURD200SA0', 'data': []},
    #{'seriesID': 'CUURD300SA0', 'data': []},
    # In this step, this missing data will also be removed.
    result_final_clean = []
    for item in result_final_2:
        data_area = item['data']
        result_final_clean.append({'seriesID':item['seriesID'],'data':round(((eval(data_area[0]['value'])
                                                                       -eval(data_area[-1]['value']))
                                                                       /eval(data_area[-1]['value']))*100 + 100,2)})
                
    # the output is a list of dictionary. However, we just need the vaue of CPI and the area. Therefore, the extra data would be removed.
    # Moreover, the seriesID, such as CUUR0000SA0L1E, would be replaced by the area_name, such as East North Central.
    
    
    name_value = {}
    for item in result_final_clean:
        for issue in combine_code.keys():
            if item['seriesID'][4:8] == issue:
                name_value[f'{combine_code[issue]}'] = item['data']
                
    pd_table_name_value = {}
    pd_table_name_value_region = []
    pd_table_name_value_CPI = []
    for item in name_value:
        pd_table_name_value_region.append(item)
        pd_table_name_value_CPI.append(name_value[item])
    
    pd_table_name_value = {'region':pd_table_name_value_region,'CPI_value': pd_table_name_value_CPI}
    
    # build Pandas DataFrame
    pdtable_name_value = DataFrame(pd_table_name_value)
    
    return pdtable_name_value


def google_map(apikey,address):
    result = ''
    address_change = address.replace(' ','+')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_change}&key={apikey}'
    response = requests.get(url)
    try:
        response = response.json()['results'][0]['address_components']
        for item in response:
            if item['types'][0] == 'administrative_area_level_1' :
                result = item['short_name']
        return result
    except:
        return []


def location_bls_api(apikey, content):
    lie = []
    for item in content.STATES:
        hang = []
        for issue in item.split(','):
            hang.append(google_map(apikey,(issue+' Political State')))
            time.sleep(.2)
        lie.append(hang)
    content['api_sate'] = lie
    return content

def lat_long(apikey,address):
    address_change = address.replace(' ','+')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_change}&key={apikey}'
    try:
        response = requests.get(url)
        response = response.json()['results'][0]['address_components']
        result = []
        for item in response:
            if 'administrative_area_level_2' in item['types']:
                result = item['long_name']
            elif 'administrative_area_level_1' in item['types']:
                result =result + ', ' + item['short_name']
        result = result.replace(' County','')
        return result
    except TypeError:
        response = requests.get(url)
        response = response.json()['results'][0]['formatted_address']
        result = response.replace(', USA','')
        return result
    except:
        return ''


def personal_income(path):
    data=pd.read_excel(path)
    df = data.iloc[:,[0,3]]
    df.columns = ['area','personal_income']
    return df