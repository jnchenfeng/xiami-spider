# -*- coding: utf-8 -*-
from ParseXiamiUrl import XiamiDownload
import ParseHtml as htmlParseProcessor


if __name__ == '__main__':
    songIdList = htmlParseProcessor.get_song_id_by_album_url("http://www.xiami.com/album/kjDkae9a9")
    for songid in songIdList:
        url = "http://www.xiami.com/song/" + str(songid)
        print(url)
        xi = XiamiDownload(url)
        if xi.url_location == "exception":
            continue
        url_download = str(xi.get_url()).encode('utf-8')
        url_pic = str(xi.pic).encode('utf-8')
        url_lyc = str(xi.lyc).encode('utf-8')
        print ('下载地址是: ' + url_download)
        print('下载地址是: ' + url_pic)
        print('下载地址是: ' + url_lyc)
