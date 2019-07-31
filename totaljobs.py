from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

skills = ["javascript"]
records = []


def getUrl():
    UrlList = []
    x = 2
    for i in skills:
        for x in range(2, 5):
            baseUrl = f"https://www.totaljobs.com/jobs/{i}?page={x}"
            x += 1
            UrlList.append(baseUrl)
    return UrlList


def Getcwurl():
    UrlList = []
    x = 2
    for i in skills:
        for x in range(2, 5):
            baseUrl = f"https://www.cwjobs.co.uk/jobs/{i}?page={x}"
            x += 1
            UrlList.append(baseUrl)
    return UrlList


urls = getUrl()

cwurls = Getcwurl()

for url in cwurls:
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    joblist = bsObj.findAll("div", {"class": "job"})

    for job in joblist:
        job_title = job.h2.text
        print(job_title)
        try:
            location = job.find('li', {"class:location"}).span.a.text
        except:
            location = "not listed"
        salary = job.find('li', {'class': 'salary'}).string
        application_link = job.find('div', {'class': 'job-title'}).a['href']
        company = job.find('li', {'class': 'company'}).h3.a.text
        records.append((job_title, company, location,
                        salary.replace("Â", ""), application_link))


for url in urls:
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    joblist = bsObj.findAll("div", {"class": "job"})
    for job in joblist:
        job_title = job.h2.text
        application_link = job.find('div', {'class': 'job-title'}).a['href']
        company = job.find('li', {'class': 'company'}).h3.a.text
        try:
            location = job.find('li', {'class': 'location'}).a.text
        except:
            location = "not found"
        date_posted = job.find(
            'li', {'class': 'date-posted'}).span.text.strip()
        employment_type = job.find('span', {'title': 'employment type'}).text
        salary = job.find('li', {'class': 'salary'}).string
        records.append((job_title, company,
                        location, salary, application_link))


df = pd.DataFrame(records, columns=[
                  'Title', 'Company', 'Location', 'Salary', 'Details'])
df.to_csv('jobber.csv', index=False, encoding='utf-8')
