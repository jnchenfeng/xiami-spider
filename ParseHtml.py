# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

def getSongIdByAlbumUrl(url):
    albumurl = 'http://www.xiami.com/album/eTKf5d165'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(albumurl, headers=headers)
    if r.status_code == 200:
        htmlObject = BeautifulSoup(r.content, from_encoding="utf-8")
        musicTable = htmlObject.find("table",class_="track_list")
        for tr in musicTable.findAll("tr"):
            checkBox = tr.find("input")
            if not checkBox:
                continue
            yield checkBox.get("value")


if __name__ == '__main__':
    print list(getSongIdByAlbumUrl("http://www.xiami.com/album/kjDkae9a9"))