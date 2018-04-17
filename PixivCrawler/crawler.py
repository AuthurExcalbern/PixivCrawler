#!/urs/bin/env python3
# -*- coding=utf-8 -*-

import os
import time
import threading
import requests
from urllib import request, error
from multiprocessing import Process, Queue
import re

from PIL import Image
from io import BytesIO

from PixivCrawler.login import PixivLogin


class Crawler(object):
    def __init__(self, session_obj):
        self.session_obj = session_obj
        self.save_path = './PixivDownload'
        self.save_name = ''
        self.cnt = 0
        self.bookmark_params ={
            'rest':'show',
            'p':''
        }
        self.image_params ={
            'mode':'medium',
            'illust_id':''
        }
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                            "Connection": "keep-alive",
                            "Referer": ""}
    
    def save_image(self, original_image_url, save_file):
        image = self.session_obj.get(original_image_url.strip())
        
        image_path = self.save_path + "/" + save_file
        if (os.path.exists(image_path)):
            return
        
        i = image.content
        with open(image_path, 'wb') as f:
            f.write(i)
    
    def get_image(self):
        if not (os.path.exists(self.save_path)):
            print("Build save file:" + self.save_path)
            os.mkdir(self.save_path)
        else:
            print("Already build save file:" + self.save_path)
        
        bookmark_url = 'https://www.pixiv.net/bookmark.php'
        self.bookmark_params['p'] = input('Please input your bookmark page:')
        self.save_name = self.bookmark_params['p'] + '-'
        
        bookmark_html = self.session_obj.get(bookmark_url, params=self.bookmark_params)
        bookmark_pattern = re.compile(r'class="image-item".+?data-type="illust"data-id="(.*?)"')
        image_id = bookmark_pattern.findall(bookmark_html.text)
        
        image_midium_url = 'https://www.pixiv.net/member_illust.php'
        
        if image_id == []:
            print("No find image")
            return
        
        thread_stack = []
        miss = 0
        for i in image_id:
            self.cnt += 1
            self.image_params['illust_id'] = i
            self.headers['Referer'] = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=" + i + "&page=0"
            
            image_html = self.session_obj.get(image_midium_url, params=self.image_params)
            image_pattern = re.compile(r'class="wrapper".+?data-src="(.+?)"')
            original_image_url = image_pattern.findall(image_html.text)
            
            self.session_obj.headers = self.headers
            
            if original_image_url == []:
                print("url miss")
                miss += 1
            else:
                print("Download: " + original_image_url[0])
                download_thread = threading.Thread(target=self.save_image, args=(original_image_url[0], self.save_name + i))
                download_thread.start() #self.save_image(original_image_url[0], self.save_name + i)
                thread_stack.append(download_thread)
        
        for i in thread_stack:
            i.join()
        
        print("url miss:" + "%d" % miss)