'''
    @Author: zuoqian26 
    @Time: 2023/6/1 19:17
'''

import requests
import re
from src.database import Weibo

months = {
    'Jan': '1月',
    'Feb': '2月',
    'Mar': '3月',
    'Apr': '4月',
    'May': '5月',
    'Jun': '6月',
    'Jul': '7月',
    'Aug': '8月',
    'Sep': '9月',
    'Oct': '10月',
    'Nov': '11月',
    'Dec': '12月'
}
weeks = {
    'Mon' : '星期一',
    'Tue' : '星期二',
    'Wed' : '星期三',
    'Thu' : '星期四',
    'Fri' : '星期五',
    'Sat' : '星期六',
    'Sun' : '星期日'
}

# 获取响应
def getresponse(uid):
    '''
    这里返回一个用户最原始的数据

    :param uid: 用户的uid
    :return: 一大串dict
    '''

    respponse = requests.get(
        url='https://m.weibo.cn/api/container/getIndex?',
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        },
        params={
            'type': 'uid',
            'value': uid,
            'luicode': '10000011',
            'containerid': str(107603) + str(uid),
        }
    ).json()
    return respponse

# 获取用户数据
def getuser(response,uid):
    '''
    这里返回一个用户的数据

    :param response: 用户的原始数据
    :return: 需要的数据 ： dict
    '''

    user_data = response['data']['cards'][1]['mblog']['user']

    # 用户名
    user_name = user_data['screen_name']
    # 粉丝数
    followers_count = user_data['followers_count']
    if followers_count[-1] == '万':
        followers_count = float(followers_count[:-1]) * 10000
    elif followers_count[-1] == '亿':
        followers_count = float(followers_count[:-1]) * 100000000

    # ID
    user_id = uid
    # type
    user_type = user_data['verified_reason']
    # email
    user_email = user_data['description']

    return {
        'user_name': user_name,
        'followers_count': followers_count,
        'user_id': user_id,
        'user_type': user_type,
        'user_email': user_email
    }

def getweibo(response,uid):
    '''
    处理响应传过来的信息，取出想要的数据

    :param response:  用户最原始的数据
    :param uid: 用户uid
    :return: 需要的数据：dict
    '''

    weibo_datas_list = response['data']['cards']
    datalist = []
    for temp in weibo_datas_list:
        datas = []
        if 'mblog' in temp:

            weiboid = temp['mblog']['id']
            if Weibo.select().where(Weibo.weiboid == weiboid):
                continue

            else:

                content = re.sub(r'<[^>]+>', "", temp['mblog']['text'])

                releases = temp['mblog']['created_at']
                releasetime = releases[-4:] + months[releases[4:7]] + releases[8:10] + '日' + weeks[releases[:3]] + releases[11:19]

                forwards = temp['mblog']['reposts_count']

                if 'region_name' in temp['mblog']:
                    location = temp['mblog']['region_name'][4:]
                else:
                    location = '空白'

                datas.append({
                    'weiboid': weiboid,
                    'content': content,
                    'releasetime': releasetime,
                    'forwards': forwards,
                    'location': location
                })
            datalist.append(datas)
    return datalist



