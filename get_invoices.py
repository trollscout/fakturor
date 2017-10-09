'''
Created on 5 okt. 2017

@author: hakan
'''

import os
import requests
from bs4 import BeautifulSoup

dataurl = "https://www.scoutnet.se/reports/groups/members/group_id/784/download/true/format/json"
loginurl = "https://www.scoutnet.se/login"
auth = {'signin[username]': os.getenv('SCOUTNET_UID','hakan@violaberg.nu'), 'signin[password]': os.getenv('SCOUTNET_PWD','NO DEFAULT!')}

def get_url(session,url):
    r = session.get(url)
    if r.status_code != 200:
#         print("*")
        r = session.post(loginurl,data=auth)  # Need to login
        if r.status_code != 200:
            raise Exception('Bad Scoutnet credentials')
    return r
  
def get_memdata(session):
    r = get_url(session,dataurl)
    return r.json()

def is_invoice(tag):
    return tag.name == "tr" and tag.has_attr('id') and "invoice_" in tag['id'] and "_row" in tag['id'] 

def get_invoice(session,userid):
    qqq = get_url(session, "https://www.scoutnet.se/organisation/user/"+userid).text
    soup = BeautifulSoup(qqq, 'html.parser')
    invs = soup.find_all(is_invoice)
    asl = invs[0].find_all('a')
#     print(asl[1].get('href'))
    pdfurl = "https://www.scoutnet.se"+asl[1].get('href')
    qqq = get_url(session,pdfurl)
    with open("Fakturor/"+userid+".pdf","wb") as fp:
        fp.write(qqq._content)

il = ["3289580","3289755","3290996","3265752","3262920","3264333","3264332","3308227","3300592","3286482","3308212","3300734","3228455","3308357","3232356","3290169","3290964","3252103","3233490","3209825","3306175","3295127","3211601","3264318","3276805","3261153","3249103","3306739","3306738","3307421","3209725","3197850","3291661","3237511","3305171","3261074","3298979","3002638","3291407","3224049","3291426","3191514","3252351","3209823","3264321","3307425","3304972","3291416","3306174","3276526","3276978","3277633","3257963","3285860","3236156","3293462","3300589","3309476","3286483","3263017","3261829","3306519","3304952","3276883","3257965","3095326","3295867","3275789","3290897","3305079","3291380","3306528","3301432","3301431","3292580","3292487","3258204","3277936","3277935","3236630","3121231","3087093","3073420","3249827","3249826","3209824","3136566","3305949","3234914","3274900"]

if __name__ == '__main__':
    s = requests.Session()
#     j = get_memdata(s)
    for iv in il:
        get_invoice(s,iv)
    
    
