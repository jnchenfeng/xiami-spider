# -*- coding: utf-8 -*-
from ParseXiamiUrl import XiamiDownload
import ParseHtml as htmlParseProcessor


if __name__ == '__main__':
    songIdList = htmlParseProcessor.get_song_id_by_album_url("http://www.xiami.com/album/kjDkae9a9")
    for songid in songIdList:
        url = "http://www.xiami.com/song/" + str(songid)
        print(url)
        xi = XiamiDownload(url)
        print(xi.info)
