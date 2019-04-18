import sqlite3
import os
from tqdm import tqdm #progress bar
import pandas as pd
import numpy as np
import json
import glob
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.image import imread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint

def login_selenium():

    '''initiates a chrome_driver window and logs into account'''

    chromedriver_path = ('/Users/Beto/galvanize/Instagram-API-python/InstagramAPI/chromedriver')
    webdriver = webdriver.Chrome(executable_path = chromedriver_path)
    sleep(2)
    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

    username = webdriver.find_element_by_name('username')
    username.send_keys('sf_clout')
    password = webdriver.find_element_by_name('password')
    password.send_keys('20190101')
    sleep(10)

    button_login = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')
    button_login.click()
    sleep(5)

    notnow = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow.click()

def start_script():

    '''initiates IGPY script to follow, comment, and like users based on hashtag_list (may need to update css_selector/xpath occasionally)'''

    hashtag_list = ['sanfrancisco', 'bayarea']

    #prev_user_list = [] #when instantiating for the first time
    prev_user_list = pd.read_csv('data/users_followed_list.csv') #user log
    prev_user_list = list(prev_user_list['0'])

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hashtag in hashtag_list:
        tag += 1
        webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
        sleep(5)
        first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

        first_thumbnail.click()
        sleep(randint(1,2))

    # try:
        for x in range(1, 50):
            #print('username')
            username = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a').text

            if username not in prev_user_list:
                if webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.bY2yH > button').text == 'Follow':
                    webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.bY2yH > button').click()
                    new_followed.append(username)
                    followed += 1

                    button_like = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')
                    button_like.click()
                    likes += 1
                    sleep(randint(18, 25))

                    comm_prob = randint(1, 10)
                    print('{}_{}: {}'.format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button > span').click()
                        comment_box = webdriver.find_element_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                        if (comm_prob < 7):
                            comment_box.send_keys('#yayarea nice!')
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys('if this isnt pure #yayarea then I dont know what is')
                        elif comm_prob == 9:
                            comment_box.send_keys('best of the #bayarea :)')
                        elif comm_prob == 10:
                            comment_box.send_keys('haha.. iconic #sf')
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(22,28))


                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(25,29))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(20,26))
    #     except:
    #         print('exception error')

    for n in range(0, len(new_followed)):
        prev_user_list.append(new_followed[n])

    updated_user_df = pd.DataFrame(prev_user_list)
    updated_user_df.to_csv('data/users_followed_list.csv')
    print('Liked {} photos.'.format(likes))
    print('Commented {} photos.'.format(comments))
    print('Followed {} new people.'.format(followed))


if __name__=="__main__":
    login_selenium()
    sleep(10)
    start_script()
