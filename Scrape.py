from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import requests
import mechanize
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(
    "event-hotspot-firebase-adminsdk-7w7p3-1dd2809173.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def getEleInfo():
    cj = CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.open('https://apps.ucsiuniversity.edu.my/ecas')

    url = br.geturl()
    sessionKey = url.replace(
        'https://apps.ucsiuniversity.edu.my/ecas/', '').replace('/front.aspx', '')
    print("Session Key: "+sessionKey+"\n")

    br.select_form(nr=0)
    br.form['ctl00$ContentPlaceHolder1$TxtLoginID'] = '1001851873@ucsiuniversity.edu.my'
    br.form['ctl00$ContentPlaceHolder1$TxtLoginPass'] = 'Modern070700'
    br.submit()

    url_final = "https://apps.ucsiuniversity.edu.my/ecas/" + \
        sessionKey+"/Student_UpComingEvent.aspx"

    html_text = requests.get(url_final).text
    soup = BeautifulSoup(html_text, 'lxml')
    event_all = soup.find_all('table', class_='style62')
    num = 2
    total_event = 0
    for event in event_all:
        if num <= 6:
            for event_title in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label1'}):
                print(event_title.text)
            for event_organization in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label3'}):
                print('Organizer: '+event_organization.text)
            for event_pic in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label6'}):
                print('PIC: '+event_pic.text)
            for event_email in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label10'}):
                print('Email: '+event_email.text)
            for event_date in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label4'}):
                print(event_date.text)
            for event_time in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_Label13'}):
                print(event_time.text)
            for event_point in event.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_grvEventList_ctl0' + str(num) + '_lblPoints'}):
                print('Ele Point: '+event_point.text)
                num += 1
            doc_ref = db.collection(u'eventList').document(
                event_title.text)
            doc_ref.set({
                u'organizer': event_organization.text,
                u'pic': event_pic.text,
                u'email': event_email.text,
                u'date': event_date.text,
                u'time': event_time.text,
                u'elePoint': float(event_point.text)
            })
            doc_ref.delete()

        print('')
    num = 2


