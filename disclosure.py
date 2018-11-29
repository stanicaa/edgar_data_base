import re, os
import numpy
import pymysql
from bs4 import BeautifulSoup
from urllib import request
import codecs

#program builds the database for the Edgar disclosure, for the 10K forms

db = pymysql.connect([YOUR_SERVER],[DATABASE_USER],[DATABASE_USER_NAME],[DATABASE_NAME], charset="utf8" )
cursor = db.cursor()

### defining the REGEX patterns
b=re.compile(r'10-K\s+\d+\s+\d+\W\d+\W\d+\s+\w+\/\w+\/\d+\/\d+\W\d+\W\d+.txt')
bb=re.compile(r'\s\d+\s')
cc=re.compile(r'\s\d+\-\d+\-\d+\s')
p=re.compile(r'\d+\W\d+\W\d+.txt')

### create the array with the filings, by using the files on Edgar website
enc=codecs.open('company.idx', encoding='ISO-8859-1')
a_list=numpy.loadtxt(enc, dtype='str', delimiter='\t', skiprows=10)


for i in range(len(a_list)):
    link=a_list[i]
    
    
### pattern for 10-K   r'10-K\s+\d+\s+\d+\W\d+\W\d+\s+\w+\/\w+\/\d+\/\d+\W\d+\W\d+.txt'

    k=b.findall(link)
    
    ### making sure the program identifies only the 10K files
    if k!=[]:
    
        k_string=k[0]

### identifying the relevant CIK


        kk=bb.findall(k_string)
        cik=kk[0].strip()


### identifying the filing date


        kkk=cc.findall(k_string)
        filed_date=kkk[0].strip()

### the pattern: r'(/)(\d+)(-)(\d+)(-)(\d)(.txt)'
### identifying the ending in txt from the index file


        t=p.findall(link)
        tt=t[0].replace('-', '').strip('.txt')


### getting the folder link
        folder='https://www.sec.gov/Archives/edgar/data/'+cik+'/'+tt


### getting the link to the Excel file
        financials=folder+'/'+'Financial_Report.xlsx'

### getting the link to the disclosure file
### accessing first the index page

        index_page=folder+'/'+t[0][:-4]+'-index.html'

###print(index_page)

        html=request.urlopen(index_page).read().decode('utf8')
        raw=BeautifulSoup(html,"lxml")
        trs=raw("tr")
###print(trs)
        aa=0
        for tr in trs:
            doc_link=tr.find("a")
            aa+=1
            if aa==2:
                break

        doc_file_link='https://www.sec.gov'+doc_link.get('href')
        cursor.execute(""" INSERT INTO disclosure VALUES ('%s', '%s', '10-K', '%s', '%s', '%s', '%s') """ % (cik, filed_date, doc_file_link, financials, index_page, folder))
        db.commit()


db.close()





