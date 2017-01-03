# -*- coding: utf-8 -*-
import re
import urllib2


class XiamiDownload(object):
    """虾米音乐下载"""

    def __init__(self, url_song):

        """ 初始化，得到请求xml和加密的下载地址 """

        self.url_song = url_song
        self.url_xml = self.__get_xml()
        self.info = self.__get_info()
        #歌曲下载地址
        self.url_location = self.info[0]
        #歌词
        self.lyc = self.info[1]
        #封面
        self.pic = self.info[2]

    def __get_xml(self):

        """ 得到请求的 xml 地址 """
        return 'http://www.xiami.com/song/playlist/id/%s/object_name/default/object_id/0' % re.search('\d+',
                                                                                                      self.url_song).group()

    def __get_info(self):

        """ 伪装浏览器请求，处理xml，得到 加密的 location """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        req = urllib2.Request(
            url=self.url_xml,
            headers=headers
        )
        try:
            xml = urllib2.urlopen(req).read().decode('utf-8')
            print("xml:"+xml)
            pattern_location = re.compile('<location>(.*?)</location>', re.S)
            location = re.search(pattern_location, xml).group(1)
            print("location:"+location)
            lyc_location = re.compile('<lyric>(.*?)</lyric>', re.S)
            lyc = re.search(lyc_location, xml).group(1)
            pic_location = re.compile('<pic>(.*?)</pic>', re.S)
            pic = re.search(pic_location, xml).group(1)
            length = re.compile('<length>(.*?)</length>', re.S)
            songName = re.compile('<songName>(.*?)</songName>', re.S)
            artist_name = re.compile('<artist_name>(.*?)</artist_name>', re.S)
            return (location, lyc, pic, length, songName,artist_name)
        except:
            return ("exception", "exception", "exception", "exception", "exception", "exception")

    def get_url(self):

        """ 解密 location 获得真正的下载地址 """

        strlen = len(self.url_location[1:])
        rows = int(self.url_location[0])
        cols = strlen // rows
        right_rows = strlen % rows
        new_str = self.url_location[1:]
        url_true = ''
        # print(strlen)
        for i in range(strlen):
            x = i % rows
            y = i / rows
            p = 0
            if x <= right_rows:
                p = x * (cols + 1) + y
            else:
                p = right_rows * (cols + 1) + (x - right_rows) * cols + y
                # print(p)
            url_true += new_str[int(p)]
            # print(url_true)
        return urllib2.unquote(url_true).replace('^', '0')