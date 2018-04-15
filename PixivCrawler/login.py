#!/urs/bin/env python3
# -*- coding=utf-8 -*-

import requests
import re
import http.cookiejar

class PixivLogin(object):
    
    def __init__(self, session_obj):
        self.session_obj = session_obj
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                            "Connection": "keep-alive",
                            "Referer": ""}
        self.session_obj.headers = self.headers
        self.session_obj.cookies = http.cookiejar.LWPCookieJar(filename='PixivCookies')
        
        try:
            self.session_obj.cookies.load(filename='PixivCookies', ignore_discard=True)
        except:
            print('Can not load "PixivCookies"')
        
        self.params ={
            'lang': 'en',
            'source': 'pc',
            'view_type': 'page',
            'ref': 'wwwtop_accounts_index'
        }
        self.datas = {
            'pixiv_id': '',
            'password': '',
            'captcha': '',
            'g_reaptcha_response': '',
            'post_key': '',
            'source': 'pc',
            'ref': 'wwwtop_accounts_indes',
            'return_to': 'https://www.pixiv.net/'
            }
    
    def get_post_key(self):
        """
        Pixiv will give a post_key when you want to login.
        """
        login_url = 'https://accounts.pixiv.net/login'
        login_page_html = self.session_obj.get(login_url, params=self.params)
        
        # Get post_key
        post_key_pattern = re.compile(r'name="post_key" value="(.*?)">')
        post_key = post_key_pattern.findall(login_page_html.text)
        self.datas['post_key'] = post_key[0]
    
    def is_already_login(self):
        """
        Use setting_user page to judge whether we already login.
        """
        setting_user_url = 'https://www.pixiv.net/setting_user.php'
        
        # Use status_code to judge
        login_statues_code = self.session_obj.get(setting_user_url, allow_redirects=False).status_code
        if login_statues_code == 200:
            return True
        else:
            return False
    
    def login(self, account, password):
        """
        Use post to login.
        """
        post_url = 'https://accounts.pixiv.net/api/login?lang=en'
        self.get_post_key()
        self.datas['pixiv_id'] = account
        self.datas['password'] = password
        result = self.session_obj.post(post_url, data=self.datas)
        #print(result.json())
        
        # save cookies
        if self.is_already_login():
            self.session_obj.cookies.save(ignore_discard=True, ignore_expires=True)
            return True
        else:
            return False

