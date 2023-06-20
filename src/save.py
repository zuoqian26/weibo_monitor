'''
    @Author: zuoqian26 
    @Time: 2023/6/1 19:57
'''
from src.database import User,Weibo
import time
import datetime

# 存用户信息
def save_user(user_data):
    '''
    把用户个人信息存进MYSQL

    :param user_data: 用户信息
    :return: None
    '''

    User.select(User.id == user_data['user_id'])
    try:
        User.insert(
            name=user_data['user_name'],
            type=user_data['user_type'],
            number_of_followers=user_data['followers_count'],
            email=user_data['user_email'],
            id=user_data['user_id'],
            created_at=str(datetime.datetime.now())[:-7]
        ).execute()
    except Exception as e:
        print(e)

def save_weibo(datalist,uid):
    for temp in datalist:
        Weibo.insert(
            weiboid=temp[0]['weiboid'],
            content=temp[0]['content'],
            releasetime=temp[0]['releasetime'],
            forwards=temp[0]['forwards'],
            location=temp[0]['location'],
            user_id=uid,
            created_at=str(datetime.datetime.now())[:-7]
        ).execute()
        time.sleep(1)


