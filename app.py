# 导入模块和文件
import jieba
import jieba.analyse
from flask import Flask,render_template,request
from src.spider import getresponse,getuser,getweibo
from src.save import save_user,save_weibo
from src.database import User,Weibo
from peewee import fn
from wordcloud import WordCloud

# 创建一个 Flask 应用程序实例
app = Flask(__name__)

# 主页面 /
@app.route('/',methods=['POST','GET'])
def user():
    # 对地点进行分组聚合,{‘地点’：数量}
    locas = Weibo.select(Weibo.location, fn.Count(Weibo.location).alias('count')).group_by(Weibo.location)
    loca_dicts = {}
    for temp in locas:
        loca_dicts[f'{temp.location}'] = temp.count
    loca_y = loca_dicts.keys()
    loca_x = loca_dicts.values()
    l_y = [item for item in loca_y]
    l_x = [item for item in loca_x]

    # 粉丝数排名
    followers = User.select()
    follower_dict = {}
    for f in followers:
        follower_dict[f.name] = f.number_of_followers
    f_name_datas = [f for f in dict(sorted(follower_dict.items(), key=lambda x: x[1], reverse=True)).keys()]
    f_follow_datas = [f for f in dict(sorted(follower_dict.items(), key=lambda x: x[1], reverse=True)).values()]

    # 微博排名
    weibocounts = Weibo.select(Weibo.user_id, fn.Count(Weibo.user_id).alias('count')).group_by(Weibo.user_id)
    weiborank_dict = {}
    for w in weibocounts:
        id = w.user_id
        user = User.select().where(User.id == id).first().name
        weiborank_dict[user] = w.count
    weiborank = [
        [w for w in dict(sorted(weiborank_dict.items(), key=lambda x:x[1], reverse=True)).keys()],
        [w for w in dict(sorted(weiborank_dict.items(), key=lambda x:x[1], reverse=True)).values()]
    ]

    #词云
    # 读取文件
    pd_data = Weibo.select()
    datas = []
    for pd in pd_data:
        datas.append(pd.content)

    # 切割分词
    result = ' '.join(jieba.lcut_for_search(''.join(datas)))
    # 设置停用词
    stop_words = ['@', '#', '，', '“', '：', '/', '_', '我', '微博', '的', '视频', '了']
    ciyun_words = ''

    for word in result:
        if word not in stop_words:
            ciyun_words += word

    # 设置参数，创建WordCloud对象
    wc = WordCloud(
        font_path='msyh.ttc',  # 中文
        background_color='white',  # 设置背景颜色为白色
        stopwords=stop_words,  # 设置禁用词，在生成的词云中不会出现set集合中的词
        height=500,
        width=700,
    )
    # 根据文本数据生成词云
    wc.generate(ciyun_words)
    # 保存词云文件
    wc.to_file('./static/img/word.png')

    # 传递的数据
    datas = {
        'count': Weibo.select().count(),
        'follow': User.select().where(User.number_of_followers),
        'loca_': [l_x, list(l_y)],
        'followrank': [f_name_datas,f_follow_datas],
        'weiborank': weiborank
    }

    # 获取在页面输入的ID，进行操作
    if request.method == 'POST':
        uid = request.form.get('uid')
        if User.select().where(User.id == uid):
            print('你已经监控过改用户！')
        else:
            response = getresponse(uid)
            try:
                user_data = getuser(response, uid)
                save_user(user_data)
            except Exception as e:
                print(e)

    return render_template('user.html',datas=datas)

@app.route('/weibo/',methods=['POST','GET'])
def weibo():
    if request.method == 'POST':
        uid = request.form.get('uid')
        response = getresponse(uid)
        try:
            datalist = getweibo(response, uid)
            save_weibo(datalist, uid)
        except Exception as e:
            print(e)
    return render_template('weibo.html')

if __name__ == '__main__':
    app.run(debug=True)
