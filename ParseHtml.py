# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def get_song_id_by_album_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html_object = BeautifulSoup(r.content, from_encoding="utf-8")
        music_table = html_object.find("table",class_="track_list")
        for tr in music_table.findAll("tr"):
            check_box = tr.find("input")
            if not check_box:
                continue
            yield check_box.get("value")


def get_genre_url_list(url):
    genre_url = "http://www.xiami.com/genre"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html_object = BeautifulSoup(r.content,from_encoding="utf-8")
        sidebar = html_object.find(id="sidebar")
        genre_tag_list = sidebar.findAll("a")
        for genere_tag in genre_tag_list:
            href = genere_tag.get("href")
            if(str(href).encode("utf-8").find("gid")==-1):
                c={}
                c["title"] = genere_tag.get("title")
                c["url"] = href
                yield c


def get_song_id_by_genre_url(url):
    """将url中detail替换成songs获取到更多里面的歌曲"""
    url = str(url).replace("detail","songs")
    url = str(url)+"/page/%s"
    i = 1
    song_id_list=[]
    while True:
        url_temp = url % str(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = requests.get(url_temp, headers=headers)
        if r.status_code == 200:
            html_object = BeautifulSoup(r.content, from_encoding="utf-8")
            songs_div = html_object.find(id="songs")
            content_div = songs_div.find("div",class_="content")
            song_div_list = content_div.findAll("div",class_="songwrapper")
            if not song_div_list:
                break
            for songDiv in song_div_list:
                song_id_list.append(songDiv.get("data-demoid"))
        i += 1
    return song_id_list


def get_collect_list_by_key(keyword):
    i = 0
    while True:
        url = "http://www.xiami.com/search/collect/page/{0}?key={1}".format(i, keyword)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            htmlObject = BeautifulSoup(r.content, from_encoding="utf-8")

if __name__ == '__main__':
    genreList = get_song_id_by_genre_url("http://www.xiami.com/genre/detail/sid/3223")
    print genreList