from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.forms import formset_factory
from googletrans import Translator
from googlesearch import search
import logging as log
#import boto3
import json
import requests
from bs4 import BeautifulSoup
import datetime
import uuid
import pandas as pd

# Create your views here.

def job_scrape(jobsearch, location, firms_undesired, titles_undesired):
    page = requests.get('https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%5D&companyID=0&cityID=0&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke=' + str(jobsearch) + '&ws=' +str('+'.join(location.split(' ')))+'&ra=10')
    soup = BeautifulSoup(page.text, "html.parser")
    content = soup.select(".col-lg-9")
    for posting in content:
        title = posting.find_all("h2")
        company = posting.find_all("div", attrs={"class":"styled__CompanyName-iq4jvn-0 cForES"})

    # creating new empy lists to store information
    ID = []
    job_title = []
    company_name = []
    date1 = []

    # we only want the text being stored in our lists
    for x in range(len(title)):
        ID.append(str(uuid.uuid4()))
        date1.append(str(datetime.datetime.now()))
        job_title.append(title[x].text)

    for x in range(len(company)):
        company_name.append(company[x].text)

    data = [(ID, date1, job_title, company_name) for ID, date1, job_title, company_name in  zip(ID,date1,job_title,company_name)]
    
    
    jobs_filtered_num = []
    
    for i in range(len(data)):
        
        for a in range(len(firms_undesired)):
            if firms_undesired[a] in data[i][3]:
                jobs_filtered_num.append(i)
                
        for h in range(len(titles_undesired)):
            if titles_undesired[h] in data[i][2]:
                jobs_filtered_num.append(i)
                
    jobs_filtered = []
    
    for i in range(len(data)):
        if i in jobs_filtered_num:
            pass
        else:
            jobs_filtered.append(data[i])
            
            
    ## translate search if entwickler or developer
    
    jobsearch = jobsearch.lower().split()
    titles_found = [i[2].lower() for i in jobs_filtered]
    
    
    
    translator = Translator(service_urls=['translate.google.com'])

    jobsearch_translated_1 = []
    jobsearch_translated_2 = []

    translations_eng = translator.translate(jobsearch, dest='en')
    translations_de = translator.translate(jobsearch, dest='de')
    
    if 'entwickler' in jobsearch:
        for translation in translations_eng:
            if translation.origin == 'entwickler':
                jobsearch_translated_1.append(translation.text.lower())
            else:
                jobsearch_translated_1.append(translation.origin)
            
    if 'developer' in jobsearch:
        for translation in translations_de:
            if translation.origin == 'developer':
                jobsearch_translated_2.append(translation.text.lower())
            else:
                jobsearch_translated_2.append(translation.origin)
                
    
    jobsearch = ' '.join(jobsearch).lower()            

    jobsearch_translated_1 = list(set(jobsearch_translated_1))
    jobsearch_translated_1 = ' '.join(jobsearch_translated_1).lower()
    
    jobsearch_translated_2 = list(set(jobsearch_translated_2))
    jobsearch_translated_2 = ' '.join(jobsearch_translated_2).lower()
    

    result_num = []
    for (i,k) in zip(titles_found, range(len(titles_found))):
        if set(jobsearch)<= set(i):
            result_num.append(k)
            
    if len(jobsearch_translated_1) != 0:
        for (i,k) in zip(titles_found, range(len(titles_found))):
            if set(jobsearch_translated_1)<= set(i):
                result_num.append(k)
                
    if len(jobsearch_translated_2) != 0:
        for (i,k) in zip(titles_found, range(len(titles_found))):
            if set(jobsearch_translated_2)<= set(i):
                result_num.append(k)
            
    result_num = list(set(result_num))
            
    results = []
    for i in result_num:
        results.append(jobs_filtered[i])

        
    return results


def get_career_url(company):
    query = str(company.replace('_', ' ')) + "Karriere Stellenangebote"
    for j in search(query, tld="co.in", num=1, stop=1): 
        return(j)

def jobs_form(request):
    if request.method == 'GET': # get resurest = open website
        if 'data' in request.GET:
            alldata=request.GET
            data = alldata.get("data")
            url1 = get_career_url(data)
            return redirect(url1)
             
        else:
            form = SearchForm() #call the searchForm method - display content
            return render(request, 'job_app/jobs_form.html', {'form': form})
    else:
        if 'submittingsearch' in request.POST:
            form = SearchForm(request.POST) # post request - select submit, use the content from searchForm
            if form.is_valid():
                form.save()
            data = form.cleaned_data

            jobsearch = data['search_term']
            location = data['location']
            All_values = list(data.values())
            firms_undesired = ['Wirtschaftsprüfung', 'Bridging', 'berat', 'Beratung', 'Consult', 'BearingPoint', 'Deloitte', 'Sopra Steria']
            titles_undesired = ['Consult', 'Berater']
            results= job_scrape(jobsearch, location, firms_undesired, titles_undesired)
            df = pd.DataFrame(results, columns=['Id', 'date', 'JobTitle', 'CompanyName'])

            df['CompanyName1'] = df.apply(lambda row: row['CompanyName'].replace(' ', '_'), axis=1)

            results = df.to_dict('records')
            #print(results)


            context = {'jobs_found_list' : results}

            return render(request, 'job_app/jobs_list.html', context)


def jobs_list(request):
    return render(request, 'job_app/jobs_list.html')


def request_page(request):
    if request.GET.get('button_home'):
        return redirect('/')












