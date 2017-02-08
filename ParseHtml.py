# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time


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


def get_collect_album_list_by_key(keyword):
    """ 根据标签获取标签下的精选专辑列表 """
    i = 0
    while True:
        url = "http://www.xiami.com/search/collect/page/{0}?key={1}".format(i, keyword)
        html_object = get_html_content(url)
        if html_object:
            block_list = html_object.find("div",class_="block_list")
            if block_list:
                album_list = block_list.findAll("li")
                for album_info in album_list:
                    album_href = album_info.find("div",class_="block_cover").find("a")["href"]
                    yield album_href
            else:
                break


def get_html_content(url):
    """  从url中获取html内容 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html_object = BeautifulSoup(r.content, from_encoding="utf-8")
        return html_object
    else:
        return None


def get_song_url_sollect_album(url):
    """ 根据精选专辑获取歌曲主页url """
    html_object = get_html_content(url)
    if html_object:
        song_list_div = html_object.find("div", class_="quote_song_list")
        song_list = song_list_div.findAll("li")
        for song_info in song_list:
            song_span_lable = song_info.find("span",class_="song_name")
            song_a_list = song_span_lable.findAll("a")
            url = None
            for song_a in song_a_list:
                if song_a.get("href").find("song") != -1:
                    url = song_a.get("href")
            if url:
                song_html_object = get_html_content("http://www.xiami.com"+str(url))
                link_list = song_html_object.findAll("link")
                for link_info in link_list:
                    if link_info.get("rel") and link_info.get("rel")[0]== "canonical":
                        yield link_info.get("href")

def get_song_tag(url):
    """根据歌曲的url获取歌曲的tag"""
    html_object = get_html_content(url)
    if html_object:
        song_tag_div = html_object.find("div", id="song_tags_block")
        tag_div = (song_tag_div.findAll("div"))[0]
        tag_a_label_list = tag_div.findAll("a")
        for tag in tag_a_label_list:
            yield tag.string

if __name__ == '__main__':
    # genreList = get_song_id_by_genre_url("http://www.xiami.com/genre/detail/sid/3223")
    # print genreList
    # song_url_list = get_song_url_sollect_album("http://www.xiami.com/collect/186224109")
    tagList = get_song_tag("http://www.xiami.com/song/1773368757")
    print(list(tagList))
