**flask** 

#### 内置方法及学习使用注释

#### Flask
##### render_template  构造模版，传html模版和必须的数据，返回对应的完整的html 字符串/文件
##### redirect  重定向传入值是 url 自付串 
##### url_for  构造一个完整的url 传入方法名
```python
from flask import render_template, redirect, url_for, Flask

app = Flask(__name__)
@app.route('/home/<id>')
def home():
    return render_template('index.html')  
 
redirect(url_for('home', id=12))
```

##### request
##### session 全局变量 一般用来存储登录的session状态
##### g 全局变量 一般用来存储数据库db


##### flash 传入实时提醒信息，在前端通过 get_flashed_messages 获取信息
###### Flashes a message to the next request.  In order to remove the 
###### flashed message from the session and to display it to the user,
######   the template has to call :func:`get_flashed_messages`



### functools
##### wraps 用来写装饰器的

```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in '':
            return f(*args, **kwargs)
        else:
            return ''
    return wrap

```
 

#### SQLLite3 连接db 实现小功能
```python
import sqlite3
# create a new database if the database doesn't already exist
with sqlite3.connect('sample.db') as connection:
    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    # create the table
    c.execute('CREATE TABLE posts(title TEXT, details TEXT)')
    # insert dummy data into the table
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')
```

#### 简单连接数据库并进行取数据展示的代码
```python
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
import sqlite3
app = Flask(__name__)
app.database = 'sample.db' # 根目录下随意的一个db文件
# connect to database
def connect_db():
    return sqlite3.connect(app.database)
    
g.db = connect_db()
cur = g.db.execute('select * from posts')
posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
g.db.close()

```
#### 使用 SQLAlchemy 库

```python
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

# from models import *


# models.py

#from app import db
class BlogPost(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    def __init__(self, title, description):
        self.title = title
        self.description = description    
    
    def __repr__(self):
        return "<title {}>".format(self.title)
```

```python

from app import db
from models import BlogPost

# create the database and the db table
db.create_all()

# insert data
db.session.add(BlogPost("Good", "I\'m good."))
db.session.add(BlogPost("Well", "I\'m well."))
db.session.add(BlogPost("Excellent", "I\'m excellent."))
db.session.add(BlogPost("Okay", "I\'m okay."))

# commit the changes
db.session.commit()


```


#### Bcrypt 对整个App进行处理，获得加密器

```python

from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
app = Flask(__name__)
bcrypt = Bcrypt(app)
# 可进行加密 hunter2 字符
pw_hash = bcrypt.generate_password_hash('hunter2')



```



















































