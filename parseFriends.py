# -*- coding: utf-8 -*-
import os
import re
import operator
from bs4 import BeautifulSoup

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
            if m:
                try:
                    friendName = friendNameData.text
                    fbID = m.group(1).replace('"https://www.facebook.com/','')
                    friendList.append([str(uid),friendName,fbID])
#                    friendList.append([str(uid),friendName,fbID, 1, 2000])
                except IndexError:
                    continue
                except AttributeError:
                    continue
        for x in friendList:
            print x
        return friendList

#def parseFriends2(html, uid):
#    if len(html)>0:
#        soup = BeautifulSoup(html)
#        friendBlockData = soup.findAll("div",{"class" : "_5qo4"})
#        friendList=[]
#        j = 0
#        for i in friendBlockData:
#            soup1 = BeautifulSoup(str(i))
#            friendIDData = soup1.find("div",{"class" : "fsl"})
#            friendNameData = soup1.find("div",{"class" : "fsl"})
#            r = re.compile('href=(.*?)\?fref')
#            #TODO: parfois, des &amp au lieu de fref
#            m = r.search(str(friendIDData))
#            month = 1
#            year = 2000
#            if m:
#                try:
#                    friendName = friendNameData.text
#                    fbID = m.group(1).replace('"https://www.facebook.com/','')
##                    friendList.append([str(uid),friendName,fbID])
#                    friendList.append([str(uid),friendName,fbID, month, year])
#                except IndexError:
#                    continue
#                except AttributeError:
#                    continue
#
#        filename = uid.encode('utf8')+'.txt'
#        if not os.path.lexists(filename):
#            print 'Writing to '+filename
#            text_file = open(filename, "w+")
#            for x in friendList:
#                text_file.write(str(x))
#                text_file.write(",\n")
#            #text_file.write(html.encode('utf8'))
#            text_file.close()
##        for x in friendList:
##            print x
#        return friendList

global uid
uid = 689014374
username = "tryptonik"
filename = username+'_friends.htm'
html = open(filename, 'r').read()
parseFriends(html)
#global uid2
#uid2 = "bruce.bourguignon"
#username2 = "bruce.bourguignon"
#filename2 = username2+'.html'
#html = open(filename2, 'r').read()
#parseFriends2(html, uid2)
