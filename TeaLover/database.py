from peewee import *

conn = SqliteDatabase('users.sqlite')

class BaseModel(Model):
    class Meta:
        database = conn

class Users(BaseModel):
    user_id = AutoField(column_name='UserID')
    login = TextField(column_name='UserName', null=False)
    password = TextField(column_name="Password", null=False)    
    isAdmin = BooleanField(column_name="isAdmin", default=False)
    fullname = TextField(column_name="FullName", null=False)
    class Meta:
        table_name = 'Users'
        
conn.create_tables([Users])
cursor = conn.cursor()