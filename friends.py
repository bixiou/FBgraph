# -*- coding: utf-8 -*-
from __future__ import division
import httplib2,json
import zlib
import zipfile
import sys
import re
import datetime
import operator
import sqlite3
import os
from datetime import datetime
from datetime import date
import pytz
from tzlocal import get_localzone
import requests
from termcolor import colored, cprint
from pygraphml import GraphMLParser
from pygraphml import Graph
from pygraphml import Node
from pygraphml import Edge

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time,re,sys
from selenium.webdriver.common.keys import Keys
import datetime
from bs4 import BeautifulSoup
from StringIO import StringIO

requests.adapters.DEFAULT_RETRIES = 10

h = httplib2.Http(".cache")


facebook_username = "rastaquouere@hotmail.fr"
facebook_password = ""

global uid
uid = 689014374
username = "" #"689014374" #"tryptonik"
internetAccess = True
cookies = {}
all_cookies = {}
reportFileName = ""

#For consonlidating all likes across Photos Likes+Post Likes
peopleIDList = []
likesCountList = []
timePostList = []
placesVisitedList = []

#Chrome Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
prefs = {"profile.default_content_setting_values.notifications":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)



def createDatabase():
    conn = sqlite3.connect('facebook.db')
    c = conn.cursor()
    sql1 = 'create table if not exists friends (sourceUID TEXT, name TEXT, userName TEXT unique, friendList TEXT)'
    sql2 = 'create table if not exists friends (sourceUID TEXT, name TEXT, userName TEXT unique, month TEXT, year TEXT)'
    sql3 = 'create table if not exists friendsDetails (sourceUID TEXT, userName TEXT unique, userEduWork TEXT, userLivingCity TEXT, userCurrentCity TEXT, userLiveEvents TEXT, userGender TEXT, userStatus TEXT, userGroups TEXT)'

    c.execute(sql1)
    c.execute(sql2)
    c.execute(sql3)
    conn.commit()

createDatabase()
conn = sqlite3.connect('facebook.db')

def createMaltego(username):
    g = Graph()
    totalCount = 50
    start = 0
    nodeList = []
    edgeList = []

    while(start<totalCount):
            nodeList.append("")
            edgeList.append("")
            start+=1

    nodeList[0] = g.add_node('Facebook_'+username)
    nodeList[0]['node'] = createNodeFacebook(username,"https://www.facebook.com/"+username,uid)


    counter1=1
    counter2=0
    userList=[]

    c = conn.cursor()
    c.execute('select userName from friends where sourceUID=?',(uid,))
    dataList = c.fetchall()
    nodeUid = ""
    for i in dataList:
        if i[0] not in userList:
            userList.append(i[0])
            try:
                nodeUid = str(convertUser2ID2(driver,str(i[0])))
                #nodeUid = str(convertUser2ID(str(i[0])))
                nodeList[counter1] = g.add_node("Facebook_"+str(i[0]))
                nodeList[counter1]['node'] = createNodeFacebook(i[0],'https://www.facebook.com/'+str(i[0]),nodeUid)
                edgeList[counter2] = g.add_edge(nodeList[0], nodeList[counter1])
                edgeList[counter2]['link'] = createLink('Facebook')
                nodeList.append("")
                edgeList.append("")
                counter1+=1
                counter2+=1
            except IndexError:
                continue
    if len(nodeUid)>0:
        parser = GraphMLParser()
        if not os.path.exists(os.getcwd()+'/Graphs'):
                os.makedirs(os.getcwd()+'/Graphs')
        filename = 'Graphs/Graph1.graphml'
        parser.write(g, "Graphs/Graph1.graphml")
        cleanUpGraph(filename)
        filename = username+'_maltego.mtgx'
        print 'Creating archive: '+filename
        zf = zipfile.ZipFile(filename, mode='w')
        print 'Adding Graph1.graphml'
        zf.write('Graphs/Graph1.graphml')
        print 'Closing'
        zf.close()

def createLink(label):
    xmlString = '<mtg:MaltegoLink xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.link.manual-link">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Description" hidden="false" name="maltego.link.manual.description" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Style" hidden="false" name="maltego.link.style" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>0</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Label" hidden="false" name="maltego.link.manual.type" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+label+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Show Label" hidden="false" name="maltego.link.show-label" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>0</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Thickness" hidden="false" name="maltego.link.thickness" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>2</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Color" hidden="false" name="maltego.link.color" nullable="true" readonly="false" type="color">'
    xmlString += '<mtg:Value>8421505</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoLink>'
    return xmlString

def createNodeFacebook(displayName,url,uid):
    xmlString = '<mtg:MaltegoEntity xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.affiliation.Facebook">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Name" hidden="false" name="person.name" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+displayName+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Network" hidden="false" name="affiliation.network" nullable="true" readonly="true" type="string">'
    xmlString += '<mtg:Value>Facebook</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="UID" hidden="false" name="affiliation.uid" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+str(uid)+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Profile URL" hidden="false" name="affiliation.profile-url" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+url+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoEntity>'
    return xmlString

def cleanUpGraph(filename):
    newContent = []
    with open(filename) as f:
        content = f.readlines()
        for i in content:
            if '<key attr.name="node" attr.type="string" id="node"/>' in i:
                i = i.replace('name="node" attr.type="string"','name="MaltegoEntity" for="node"')
            if '<key attr.name="link" attr.type="string" id="link"/>' in i:
                i = i.replace('name="link" attr.type="string"','name="MaltegoLink" for="edge"')
            i = i.replace("&lt;","<")
            i = i.replace("&gt;",">")
            i = i.replace("&quot;",'"')
            print i.strip()
            newContent.append(i.strip())

    f = open(filename,'w')
    for item in newContent:
        f.write("%s\n" % item)
    f.close()

def normalize(s):
    if type(s) == unicode:
               return s.encode('utf8', 'ignore')
    else:
            return str(s)

def findUser(findName):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE contains('"+findName+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    results = json.loads(content)
    count=1
    for x in results['data']:
        print str(count)+'\thttp://www.facebook.com/'+x['username']
        count+=1

def convertUser2ID2(driver,username):
    url="http://graph.facebook.com/"+username
    resp, content = h.request(url, "GET")
    if resp.status==200:
        results = json.loads(content)
        if len(results['id'])>0:
            fbid = results['id']
            return fbid

def convertUser2ID(username):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE username=('"+username+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    if resp.status==200:
        results = json.loads(content)
        if len(results['data'])>0:
            return results['data'][0]['uid']
        else:
            print "[!] Can't convert username 2 uid. Please check username"
            sys.exit()
            return 0
    else:
        print "[!] Please check your facebook_access_token before continuing"
        sys.exit()
        return 0

def convertID2User(uid):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE uid=('"+uid+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    results = json.loads(content)
    return results['data'][0]['uid']


def loginFacebook(driver):
    driver.implicitly_wait(120)
    driver.get("https://www.facebook.com/")
    #assert "Welcome to Facebook" in driver.title
    time.sleep(1)
    driver.find_element_by_id('email').send_keys(facebook_username)
    driver.find_element_by_id('pass').send_keys(facebook_password)
    driver.find_element_by_id("loginbutton").click()
    global all_cookies
    all_cookies = driver.get_cookies()
    html = driver.page_source
    if "Incorrect Email/Password Combination" in html:
        print "[!] Incorrect Facebook username (email address) or password"
        sys.exit()

def write2Database(dbName,dataList):
    try:
        cprint("[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName,"white")
        #print "[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName
        numOfColumns = len(dataList[0])
        dbName = unicode(dbName)
        c = conn.cursor()
        if numOfColumns==3:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==4:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==5:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==9:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?,?,?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
    except TypeError as e:
        print e
        pass
    except IndexError as e:
        print e
        pass

def downloadFile(url):
    global cookies
    for s_cookie in all_cookies:
            cookies[s_cookie["name"]]=s_cookie["value"]
    r = requests.get(url,cookies=cookies)
    html = r.content
    return html

def downloadFriends(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/friends')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Friends list is hidden"
        return ""
    else:
        #assert "Friends of " in driver.title
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            while(match==False):
                    time.sleep(1)
                    lastCount = lenOfPage
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage:
                            match=True
    return driver.page_source

def downloadFriends2(driver,userid):
    driver.get('https://www.facebook.com/'+str(userid)+'/friends')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Friends list is hidden"
        return ""
    else:
        #assert "Friends of " in driver.title
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            while(match==False):
                    time.sleep(0.5)
                    lastCount = lenOfPage
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage:
                            match=True
    return driver.page_source


def downloadPage(url):
    driver.get(url)
    html = driver.page_source
    return html

def sidechannelFriends(uid):
    userList = []
    c = conn.cursor()
    c.execute('select distinct username from photosLiked where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    c.execute('select distinct username from photosCommented where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    c.execute('select distinct username from photosOf where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    return userList

def getFriends(uid):
    userList = []
    c = conn.cursor()
    c.execute('select username from friends where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            userList.append([uid,'',str(normalize(i)),'',''])
    return userList

def parseFriends(html):
    if len(html)>0:
        soup = BeautifulSoup(html)
        friendBlockData = soup.findAll("div",{"class" : "_3u1"})
        friendList=[]
        for i in friendBlockData:
            soup1 = BeautifulSoup(str(i))
            friendIDData = soup1.find("div",{"class" : "_42ef"})
            friendNameData = soup1.find("div",{"class" : "_5d-5"})
            r = re.compile('a href=(.*?)\?ref')
            m = r.search(str(friendIDData))
            month = 1
            year = 2000
            if m:
                try:
                    friendName = friendNameData.text
                    fbID = m.group(1).replace('"https://www.facebook.com/','')
#                    friendList.append([str(uid),friendName,fbID])
                    friendList.append([str(uid),friendName,fbID, month, year])
                except IndexError:
                    continue
                except AttributeError:
                    continue

        filename = uid.encode('utf8')+'.txt'
        if not os.path.lexists(filename):
            print 'Writing to '+filename
            text_file = open(filename, "w")
            text_file.write(normalize(str(friendList)))
            #text_file.write(html.encode('utf8'))
            text_file.close()
#        for x in friendList:
#            print x
        return friendList

def parseFriends2(html, uid):
    if len(html)>0:
        soup = BeautifulSoup(html)
        friendBlockData = soup.findAll("div",{"class" : "_5qo4"})
        friendList=[]
        j = 0
        for i in friendBlockData:
            soup1 = BeautifulSoup(str(i))
            friendIDData = soup1.find("div",{"class" : "fsl"})
            friendNameData = soup1.find("div",{"class" : "fsl"})
            r = re.compile('href=(.*?)\?fref')
            #TODO: parfois, des &amp au lieu de fref
            m = r.search(str(friendIDData))
            month = 1
            year = 2000
            if m:
                try:
                    friendName = friendNameData.text
                    fbID = m.group(1).replace('"https://www.facebook.com/','')
#                    friendList.append([str(uid),friendName,fbID])
                    friendList.append([str(uid),friendName,fbID, month, year])
                except IndexError:
                    continue
                except AttributeError:
                    continue

        filename = uid.encode('utf8')+'.txt'
        if not os.path.lexists(filename):
            print 'Writing to '+filename
            text_file = open(filename, "w+")
            for x in friendList:
                text_file.write(str(x))
                text_file.write(",\n")
            #text_file.write(html.encode('utf8'))
            text_file.close()
#        for x in friendList:
#            print x
        return friendList

"""
def analyzeFriends(userid):
    c = conn.cursor()
    c.execute('select * from friends where sourceUID=?',(userid,))
    dataList = c.fetchall()
    photosliked = []
    photoscommented = []
    userID = []
    for i in dataList:
        #print i[1]+'\t'+i[2]
        #c.execute('select username from photosLiked')
        c.execute('select * from photosLiked where sourceUID=? and username=?',(userid,i[2],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:
            str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
            photosliked.append(str1)

        c.execute('select * from photosCommented where sourceUID=? and username=?',(userid,i[2],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:
            str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
            photoscommented.append(str1)
    print "[*] Videos Posted By "+str(username)
    filename = username+'_videosBy.htm'
    if not os.path.lexists(filename):
        html = downloadVideosBy(driver,uid)
        text_file = open(filename, "w")
        text_file.write(html.encode('utf8'))
        text_file.close()
    else:
        html = open(filename, 'r').read()
    dataList = parseVideosBy(html)
    count=1
    for i in dataList:
        print str(count)+') '+i[1]+'\t'+i[2]
        count+=1
    print "\n"

    print "[*] Pages Liked By "+str(uid)
    filename = username+'_pages.htm'
    if not os.path.lexists(filename):
        html = downloadPagesLiked(driver,uid)
        text_file = open(filename, "w")
        text_file.write(html.encode('utf8'))
        text_file.close()
    else:
        html = open(filename, 'r').read()
    dataList = parsePagesLiked(html)
    for i in dataList:
        print "[*] "+normalize(i[1])
        #print "[*] "+normalize(i[2])+"\t"+normalize(i[1])+"\t"+normalize(i[3])
        #print normalize(i[1])+"\t"+normalize(i[2])+"\t"+normalize(i[3])
    print "\n"

"""


def mainProcess(username):
    username = username.strip()
    print "[*] Username:\t"+str(username)
    global uid

    loginFacebook(driver)
    uid = 689014374 #convertUser2ID2(driver,username)
    if not uid:
        print "[!] Problem converting username to uid"

    tmpInfoStr = []
    userID =  getFriends(uid)
    for x in userID:
        i = str(normalize(x[2]))
        i = i.replace("(u'","").replace("',","").replace(')','')
        i = i.replace('"https://www.facebook.com/','')
        print "[*] Looking up information on "+i
        #TODO: correct this bug of wrong id
        if len(i) < 40:
            filename = i.encode('utf8')+'.html'
            if "/" not in filename:
                if not os.path.lexists(filename):
                    print 'Writing to '+filename
                    url = 'https://www.facebook.com/'+i.encode('utf8')+'/friends'
                    html = downloadFriends2(driver,i)
                    #html = downloadUserInfo(driver,i.encode('utf8'))
                    if len(html)>0:
                        text_file = open(filename, "w")
                        text_file.write(normalize(html))
                        #text_file.write(html.encode('utf8'))
                        text_file.close()
                else:
                    print 'Skipping: '+filename
            text_file = open(filename, 'r').read()
            parseFriends2(text_file, i)

    #cprint("[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName,"white")
    cprint("[*] Report has been written to: "+str(reportFileName),"white")
    cprint("[*] Preparing Maltego output...","white")
    createMaltego(username)
    cprint("[*] Maltego file has been created","white")

    driver.close()
    driver.quit
    conn.close()


def options(arguments):
    user = ""
    count = 0
    for arg in arguments:
        if arg == "-user":
            count+=1
            user = arguments[count+1]
        if arg == "-report":
            count+=1
            global reportFileName
            reportFileName = arguments[count+1]
    mainProcess(user)


def showhelp():

    print ""
    print "    MMMMMM$ZMMMMMDIMMMMMMMMNIMMMMMMIDMMMMMMM"
    print "    MMMMMMNINMMMMDINMMMMMMMZIMMMMMZIMMMMMMMM"
    print "    MMMMMMMIIMMMMMI$MMMMMMMIIMMMM8I$MMMMMMMM"
    print "    MMMMMMMMIINMMMIIMMMMMMNIIMMMOIIMMMMMMMMM"
    print "    MMMMMMMMOIIIMM$I$MMMMNII8MNIIINMMMMMMMMM"
    print "    MMMMMMMMMZIIIZMIIIMMMIIIM7IIIDMMMMMMMMMM"
    print "    MMMMMMMMMMDIIIIIIIZMIIIIIII$MMMMMMMMMMMM"
    print "    MMMMMMMMMMMM8IIIIIIZIIIIIIMMMMMMMMMMMMMM"
    print "    MMMMMMMMMMMNIIIIIIIIIIIIIIIMMMMMMMMMMMMM"
    print "    MMMMMMMMM$IIIIIIIIIIIIIIIIIII8MMMMMMMMMM"
    print "    MMMMMMMMIIIIIZIIIIZMIIIIIDIIIIIMMMMMMMMM"
    print "    MMMMMMOIIIDMDIIIIZMMMIIIIIMMOIIINMMMMMMM"
    print "    MMMMMNIIIMMMIIII8MMMMM$IIIZMMDIIIMMMMMMM"
    print "    MMMMIIIZMMM8IIIZMMMMMMMIIIIMMMM7IIZMMMMM"
    print "    MMM$IIMMMMOIIIIMMMMMMMMMIIIIMMMM8IIDMMMM"
    print "    MMDIZMMMMMIIIIMMMMMMMMMMNIII7MMMMNIIMMMM"
    print "    MMIOMMMMMNIII8MMMMMMMMMMM7IIIMMMMMM77MMM"
    print "    MO$MMMMMM7IIIMMMMMMMMMMMMMIII8MMMMMMIMMM"
    print "    MIMMMMMMMIIIDMMMMMMMMMMMMM$II7MMMMMMM7MM"
    print "    MMMMMMMMMIIIMMMMMMMMMMMMMMMIIIMMMMMMMDMM"
    print "    MMMMMMMMMII$MMMMMMMMMMMMMMMIIIMMMMMMMMMM"
    print "    MMMMMMMMNIINMMMMMMMMMMMMMMMOIIMMMMMMMMMM"
    print "    MMMMMMMMNIOMMMMMMMMMMMMMMMMM7IMMMMMMMMMM"
    print "    MMMMMMMMNINMMMMMMMMMMMMMMMMMZIMMMMMMMMMM"
    print "    MMMMMMMMMIMMMMMMMMMMMMMMMMMM8IMMMMMMMMMM"

    print """
    #####################################################
    #                  fbStalker.py                 #
    #               [Trustwave Spiderlabs]              #
    #####################################################
    Usage: python fbStalker.py [OPTIONS]

    [OPTIONS]

    -user   [Facebook Username]
    -report [Filename]
    """

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        showhelp()
        driver.close()
        driver.quit
        conn.close()
        sys.exit()
    else:
        if len(facebook_username)<1 or len(facebook_password)<1:
            print "[*] Please fill in 'facebook_username' and 'facebook_password' before continuing."
            sys.exit()
        options(sys.argv)


