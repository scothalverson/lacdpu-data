import mechanize
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar as cookielib
import json
import datetime
import time

def getAccountAttributes():
    #read login details from file
    with open("login.txt") as f:
        auth = f.readlines()

    ret = {}

    for line in auth:
        line = line.strip().split()
        ret[line[0]] = line[1]

    return ret

def initBrowser(auth):
    #create browser context
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    #open LACDPU login page
    br.open("https://my-lacnm.sensus-analytics.com/login.html#/signin")
    br.select_form(nr=0)
    #set user/pass 
    br.form['j_username'] = auth['user']
    br.form['j_password'] = auth['pswd']
    #login
    br.submit()
    #return for use elsewhere
    return br
def get24hData(br, customer, meter, met_type, y, m, d):
    #calulate a unix timestamp in ms for start and end of the day
    startDate = int(time.mktime(datetime.date(year=y,day=d,month=m).timetuple()))
    endDate = int(time.mktime(datetime.date(year=y,day=d+1,month=m).timetuple()))
    startDate *= 1000
    endDate = endDate * 1000 - 1
    #buld a URL 
    url = "https://my-lacnm.sensus-analytics.com/" \
            + met_type +"/usage/" + customer + "/" + meter + "?start=" \
            + str(startDate) + "&end=" + str(endDate) + "&zoom=day"
    #open URL
    br.open(url)
    #get the response
    data = (br.response().read())
    #parse as json
    data = json.loads(data)
    #return the important array
    return data['data']['usage']


auth = getAccountAttributes()
br = initBrowser(auth)

if 'electric' in auth:
    print(get24hData(br, auth['customer'], auth['electric'], 'electric', 2022, 11, 1))
if 'water' in auth:
    print(get24hData(br, auth['customer'], auth['water'], 'water', 2022, 11, 1))
if 'gas' in auth:
    print(get24hData(br, auth['customer'], auth['gas'], 'gas', 2022, 11, 1))
