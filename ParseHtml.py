# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

def getSongIdByAlbumUrl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        htmlObject = BeautifulSoup(r.content, from_encoding="utf-8")
        musicTable = htmlObject.find("table",class_="track_list")
        for tr in musicTable.findAll("tr"):
            checkBox = tr.find("input")
            if not checkBox:
                continue
            yield checkBox.get("value")

def getGenreUrlList(url):
    genreUrl = "http://www.xiami.com/genre"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        htmlObject = BeautifulSoup(r.content,from_encoding="utf-8")
        sidebar = htmlObject.find(id="sidebar")
        genreTagList = sidebar.findAll("a")
        for genereTag in genreTagList:
            href = genereTag.get("href")
            if(str(href).encode("utf-8").find("gid")==-1):
                c={}
                c["title"] = genereTag.get("title")
                c["url"] = href
                yield c

def getSongIdByGenreUrl(url):
    #将url中detail替换成songs获取到更多里面的歌曲
    url = str(url).replace("detail","songs")
    url = str(url)+"/page/%s"
    i = 1
    songIdList=[]
    while True:
        urlTemp = url % str(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = requests.get(urlTemp, headers=headers)
        if r.status_code == 200:
            htmlObject = BeautifulSoup(r.content, from_encoding="utf-8")
            songsDiv = htmlObject.find(id="songs")
            contentDiv = songsDiv.find("div",class_="content")
            songDivList = contentDiv.findAll("div",class_="songwrapper")
            if not songDivList:
                break
            for songDiv in songDivList:
                songIdList.append(songDiv.get("data-demoid"))
        i = i+1
    return songIdList

if __name__ == '__main__':
    genreList = getSongIdByGenreUrl("http://www.xiami.com/genre/detail/sid/3223")
    print genreList