'''
    @Author: zuoqian26 
    @Time: 2023/6/1 18:58
'''
from peewee import *

db = MySQLDatabase(
    'weibo_monitor',
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    charset='utf8mb4',
    autoconnect=True
)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    type = CharField()
    number_of_followers = BigIntegerField()
    email = CharField()
    created_at = CharField()

class Weibo(BaseModel):
    weiboid = CharField(primary_key=True)
    content = CharField()
    releasetime = CharField()
    forwards = CharField()
    location = CharField()
    created_at = CharField()
    user = ForeignKeyField(User)

db.connect()
db.create_tables([User, Weibo])
