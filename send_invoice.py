'''
Created on 7 okt. 2017

@author: hakan
'''

import json
def get_memdata():
    return json.load(open("memdata.json","r"))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
def send_to(m, server):
    def v(m,f):
        return m[f]['value'] if f in m else ""
    
    mname = v(m,'first_name')+" "+v(m,'last_name')
    subject = "[Scouterna] Obetald terminsavgift för "+mname
    frommail = "Trollbäckens Scoutkår Medlemsregistret <medlemsregistret@trollbackensscoutkar.se>"
    tolist = []
    if v(m,'email') != "":
        tolist.append(v(m,'email'))
    if v(m,'contact_email_mum') != "":
        tolist.append(v(m,'contact_email_mum'))
    if v(m,'contact_email_dad') != "":
        tolist.append(v(m,'contact_email_dad'))
    if v(m,'contact_alt_email') != "":
        tolist.append(v(m,'contact_alt_email'))
    message = """
    <html><head></head><body>
    Hej!<br><br>
    För en knapp månad sedan fick ni en faktura på terminsavgiften i Trollbäckens Scoutkår och som skulle betalts senast sista september.<br>
    Tyvärr ser det inte ut som ni betalt denna än och vi skulle uppskatta om ni kan göra detta <b>omgående</b>, typ idag. Fakturan bifogas.<br><br>
    Om ni <b>har</b> betalt terminsavgiften eller om ni <b>inte</b> vill vara medlem längre, så behöver ni kontakta oss på medlemsregistret@trollbackensscoutkar.se.<br><br>
    Med vänliga hälsningar,<br><i>Håkan Persson</i><br>Trollbäckens Scoutkår<br><br><br>
    </body></html>
    """
    
#     tolist = ["hakan@violaberg.nu"]
    
    mmsg = MIMEMultipart('mixed')
    mmsg['Subject'] = subject
    mmsg['From'] = frommail
    mmsg['To'] = ", ".join(tolist)
    amsg = MIMEMultipart('alternative')
    amsg.attach(MIMEText("Kontakta medlemsregistret@trollbackensscoutkar.se om du ser den här texten!", 'plain'))
    amsg.attach(MIMEText(message, 'html'))
    mmsg.attach(amsg)
    with open("Fakturor/"+v(m,'member_no')+".pdf", 'rb') as fp:
        pdf = MIMEApplication(fp.read(),'application/pdf')
        pdf.add_header('Content-Disposition', 'attachment', filename=mname+".pdf")
    mmsg.attach(pdf)
    q = server.sendmail(frommail, tolist, mmsg.as_string())
    print(v(m,'member_no')+","+mname+"\t\t"+mmsg['To'])


import os    
from smtplib import SMTP
def send_invoces():
    overdue = ["3289755","3289580","3265752","3264333","3264332","3308227","3300592","3286482","3308212","3300734","3232356","3290169","3290964","3252103","3209825","3264318","3211601","3261153","3276805","3306738","3307421","3306739","3209725","3237511","3291661","3197850","3305171","3261074","3298979","3291407","3002638","3224049","3191514","3252351","3209823","3291426","3264321","3307425","3304972","3291416","3277633","3257963","3276978","3285860","3236156","3293462","3300589","3309476","3286483","3306519","3304952","3276883","3257965","3095326","3295867","3275789","3290897","3305079","3291380","3306528","3301432","3301431","3277935","3258204","3277936","3236630","3121231","3087093","3073420","3249827","3249826","3209824","3136566","3305949"]
#     overdue = ["3290964"]
    memdata = get_memdata()['data']
    
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("medlemsregistret@trollbackensscoutkar.se", os.getenv('EMAIL_PWD','NO DEFAULT!'))

    for member in overdue:
        send_to(memdata[member], server)

    server.quit()
    
    
if __name__ == '__main__':
    send_invoces()