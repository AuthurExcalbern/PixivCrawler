#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from PisivCrawler import PixivLogin, Crawler

if __name__ == "__main__":
    session_obj = requests.Session()
    spider = PixivLogin(session_obj)
    if spider.is_already_login():
        print('user already login.')
    else:
        account = input('Input your user name:\n> ')
        password = input('Input your password\n> ')
        if spider.login(account, password):
            print("login sucess.")
        else:
            print("login false.")
            exit()
    c = Crawler(session_obj)
    while(True):
        c.get_image()
        judge = input("Do you want to quit?(Y or y)[Enter other to continue]")
        if judge == 'Y' or judge == 'y':
            break