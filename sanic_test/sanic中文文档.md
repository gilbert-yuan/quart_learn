[TOC]

快速开始
在安装Sanic之前，让我们一起来看看Python在支持异步的过程中，都经历了哪些比较重大的更新。

首先是Python3.4版本引入了asyncio，这让Python有了支持异步IO的标准库，而后3.5版本又提供了两个新的关键字async/await，目的是为了更好地标识异步IO，让异步编程看起来更加友好，最后3.6版本更进一步，推出了稳定版的asyncio，从这一系列的更新可以看出，Python社区正迈着坚定且稳重的步伐向异步编程靠近。

安装
Sanic是一个支持 async/await 语法的异步无阻塞框架，这意味着我们可以依靠其处理异步请求的新特性来提升服务性能，如果你有Flask框架的使用经验，那么你可以迅速地使用Sanic来构建出心中想要的应用，并且性能会提升不少，我将同一服务分别用Flask和Sanic编写，再将压测的结果进行对比，发现Sanic编写的服务大概是Falsk的1.5倍。

仅仅是Sanic的异步特性就让它的速度得到这么大的提升么？是的，但这个答案并不标准，更为关键的是Sanic使用了uvloop作为asyncio的事件循环，uvloop由Cython编写，它的出现让asyncio更快，快到什么程度？这篇文章中有介绍，其中提出速度至少比 nodejs、gevent 和其他Python异步框架要快两倍，并且性能接近于用Go编写的程序，顺便一提，Sanic的作者就是受这篇文章影响，这才有了Sanic。

怎么样？有没有激起你学习Sanic的兴趣，如果有，就让我们一起开始学习吧，在开始之前，你只需要有一台安装了Python的电脑即可。

说明：由于Windows下暂不支持安装uvloop，故在此建议使用Mac或Linux
虚拟环境
程序世界一部分是对应着现实的，在生活中，我们会在不同的环境完成不同的任务，比如在厨房做饭、卧室休息，分工极其明确。

其实用Python编写应用服务也是如此，它们同样希望应用服务与开发环境是一对一的关系，这样做的好处在于，每个独立的环境都可以简洁高效地管理自身对应服务所依赖的第三方库，如若不然，各个服务都安排在同一环境，这样不仅会造成管理上的麻烦，还会使第三方库之间产生冲突。

通过上面的叙述，我们是不是可以得出这样一个核心观点：应该在不同的环境下做不同的事 ，以此类推，写项目的时候，我们也需要为每个不同的项目构建一个无干扰的的环境，发散思维，总结一下：

不同的项目，需要为其构建不同的虚拟环境，以免互相干扰
构建虚拟环境的工具很多，如下：

virtualenv
pyenv
anaconda
venv
…...

以上三个工具都可以快速地帮助我们构建当前需要的Python环境，如果你之前没有使用过，可直接点开链接进行下载，如果你正在使用其它的环境管理工具，也不要紧，因为不论你使用哪一种方式，我们最终目的都是针对一个新项目构建一个新的环境。

安装配置好之后，简单看看官方提供的使用方法，就可以开始了，比如我本机使用的是venv(python3.5以后官方推荐使用这个venv来管理虚拟环境)，安装完成后可以很方便地创建一个虚拟环境，比如这里使用Python3.6来作为本书项目的默认环境：

cd ~/
# 新建一个python3.6环境
python3 -m venv pyenv
# 安装好之后 输入下面命令进入名为python36的环境
cd pyenv/
source bin/activate
# 查看版本
python -V
若安装速度比较慢，可以考虑换国内源，比如 国内镜像 ，至于为什么选择python3.6作为默认环境，一是因为Sanic只支持Python3.5+，二则是我们构建的项目最终是要在生产环境下运行的，所以建议最好安装Python3.6下稳定版本的asyncio。

安装Sanic
Python安装第三方模块都是利用pip工具进行安装，这里也不例外，首先进入上一步我们新建的 python3.6 虚拟环境，然后安装：

# 安装Sanic，请先使用 source activate python36 进入虚拟环境
pip install sanic
# 如果不想使用uvloop和ujson 可以这样安装
SANIC_NO_UVLOOP=true SANIC_NO_UJSON=true pip install sanic
通过上面的命令，你就可以在 python3.6 虚拟环境中安装Sanic以及其依赖的第三方库了，若想查看Sanic是否已经正确安装，可以进入终端下对应的虚拟环境，启动Python解释器，导入Sanic库：

python
>>> 
>>> import sanic
如果没有出现错误，就说明你已经正确地安装了Sanic，请继续阅读下一节，了解下如何利用Sanic来构建一个Web项目吧。

开始
我们将正式使用Sanic来构建一个web项目，让我们踏出第一步，利用Sanic来编写一个返回Hello World!字符串的服务程序。

新建一个文件夹sanicweb：

$ mkdir sanicweb
$ cd sanicweb/
$ pwd
/Users/junxi/pyenv/sanicweb
创建一个sanic例子，保存为 main.py :

from sanic import Sanic
from sanic.response import text

app = Sanic()


@app.route("/")
async def index(request):
    return text('Hello World!')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
运行main.py，然后访问地址http://127.0.0.1:9000/

$ curl -X GET http://127.0.0.1:9000/
Hello World!
这样我们就完成了第一个sanic例子。

接下来，你将逐渐地了解到Sanic的一些基本用法，如路由的构建、接受请求数据以及返回响应的内容等。

路由
路由允许用户为不同的URL端点指定处理程序函数。

实例:

from sanic.response import json
@app.route("/")
async def index(request):
    return json({ "hello": "world" })
url http://server.url/ 被访问(服务器的基本url)，最终/被路由器匹配到处理程序函数，测试，然后返回一个JSON对象。

必须使用async def语法来定义Sanic处理函数，因为它们是异步函数。

请求参数
要指定一个参数，可以用像这样的角引号<PARAM>包围它。请求参数将作为关键字参数传递给路线处理程序函数。

实例：

@app.router('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))
重启服务，输入地址http://127.0.0.1:9000/tag/python进行访问

$ curl -X GET http://127.0.0.1:9000/tag/python
Tag - python
为参数指定类型，在参数名后面添加（：类型）。如果参数不匹配指定的类型，Sanic将抛出一个不存在的异常，导致一个404页面

@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))


@app.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))


@app.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))


@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))
测试结果如下：

$ curl -X GET http://127.0.0.1:9000/number/1
Integer - 1
$ curl -X GET http://127.0.0.1:9000/number/asds
Error: Requested URL /number/asds not found
$ curl -X GET http://127.0.0.1:9000/number/12.0
Number - 12.0
$ curl -X GET http://127.0.0.1:9000/person/junxi
Person - junxi
$ curl -X GET http://127.0.0.1:9000/person/123
Error: Requested URL /person/123 not found
$ curl -X GET http://127.0.0.1:9000/folder/img
Folder - img
$ curl -X GET http://127.0.0.1:9000/folder/img1
Folder - img1
$ curl -X GET http://127.0.0.1:9000/folder/images
Error: Requested URL /folder/images not found
$ curl -X GET http://127.0.0.1:9000/folder/2018
Folder - 2018
请求类型
路由装饰器接受一个可选的参数，方法，它允许处理程序函数与列表中的任何HTTP方法一起工作。

实例1:

@app.route('/post1', methods=['POST'])
async def post_handler(request):
    return text('POST request - {}'.format(request.json))


@app.route('/get1', methods=['GET'])
async def get_handler(request):
    return text('GET request - {}'.format(request.args))
实例2：

@app.post('/post2')
async def post_handler(request):
    return text('POST request - {}'.format(request.json))


@app.get('/get2')
async def get_handler(request):
    return text('GET request - {}'.format(request.args))
测试结果：

$ curl -X GET http://127.0.0.1:9000/get1?name=junxi
GET request - {'name': ['junxi']}
$ curl -X GET http://127.0.0.1:9000/get2?name=junxi
GET request - {'name': ['junxi']}
$ curl -H "Content-type: application/json" -X POST -d '{"name":"junxi", "gender":"male"}' http://127.0.0.1:9000/post1 
POST request - {'name': 'junxi', 'gender': 'male'}
$ curl -H "Content-type: application/json" -X POST -d '{"name":"junxi", "gender":"male"}' http://127.0.0.1:9000/post2
POST request - {'name': 'junxi', 'gender': 'male'}
增加路由
实例：

async def handler1(request):
    return text('ok')


async def handler2(request, name):
    return text('Folder - {}'.format(name))


async def personal_handler2(request, name):
    return text('Person - {}'.format(name))


app.add_route(handler1, '/test1')
app.add_route(handler2, '/folder2/<name>')
app.add_route(personal_handler2, '/personal2/<name:[A-z]>', methods=['GET'])
测试结果：

$ curl -X GET http://127.0.0.1:9000/test1 
ok
$ curl -X GET http://127.0.0.1:9000/folder2/aaa
Folder - aaa
$ curl -X GET http://127.0.0.1:9000/personal2/A
Person - A
$ curl -X GET http://127.0.0.1:9000/personal2/a
Person - a
url_for
Sanic提供了一个urlfor方法，根据处理程序方法名生成url。避免硬编码url路径到您的应用程序

实例：

@app.router("/")
async def index(request):
    url = app.url_for('post_handler', post_id=5)
    return redirect(url)


@app.route('posts/<post_id>')
async def post_handler(request, post_id):
    return text('Post - {}'.format(post_id))
给url_for的关键字参数不是请求参数，它将包含在URL的查询字符串中。例如:

url = app.url_for('post_handler', post_id=5, arg_one='one', arg_two='two')
# /posts/5?arg_one=one&arg_two=two
所有有效的参数必须传递给url以便构建一个URL。如果没有提供一个参数，或者一个参数与指定的类型不匹配，就会抛出一个URLBuildError

可以将多值参数传递给url

url = app.url_for('post_handler', post_id=5, arg_one=['one', 'two'])
# /posts/5?arg_one=one&arg_one=two
经过测试访问/我们会发现，url跳转到了/posts/5 ，并打印出来Post - 5 的结果。

redirect是从sanic.response导入的方法，用于处理url的重定向。

网络套接字路由
WebSocket routes

websocket可以通过装饰路由实现

实例：

@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending：' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received：', data)
另外，添加websocket路由方法可以代替装饰器

async def feed(request, ws):
    pass
app.add_websocket_route(my_websocket_handler, '/feed')
请求
request

常用类型
当一个端点收到一个HTTP请求时，路由功能被传递给一个 Request对象。

以下变量可作为Request对象的属性访问：

json (any) - JSON body
from sanic.response import json

@app.route("/json")
def post_json(request):
    return json({ "received": True, "message": request.json })
args（dict） - 查询字符串变量。查询字符串是类似于URL的部分?key1=value1&key2=value2。如果该URL被解析，则args字典将如下所示：{'key1': ['value1'], 'key2': ['value2']}。请求的query_string变量保存未解析的字符串值。
from sanic.response import json

@app.route("/query_string")
def query_string(request):
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })
raw_args（dict） - 在许多情况下，您需要访问压缩程度较低的字典中的url参数。对于之前的同一个URL ?key1=value1&key2=value2， raw_args字典看起来就像：{'key1': 'value1', 'key2': 'value2'}。
​

files（dictionary of File objects） - 具有名称，正文和类型的文件列表
from sanic.response import json

@app.route("/files")
def post_json(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type,
    }

    return json({ "received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters })
form （dict） - post表单变量。
from sanic.response import json

@app.route("/form")
def post_json(request):
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })
body（bytes） - 发送原始主体。无论内容类型如何，该属性都允许检索请求的原始数据。
from sanic.response import text

@app.route("/users", methods=["POST",])
def create_user(request):
    return text("You are trying to create a user with the following POST: %s" % request.body)
headers （dict） - 包含请求标头的不区分大小写的字典。
ip （str） - 请求者的IP地址。
port （str） - 请求者的端口地址。
socket （tuple） - 请求者的（IP，端口）。
app - 对处理此请求的Sanic应用程序对象的引用。当模块内部的蓝图或其他处理程序无法访问全局app对象时，这非常有用。

from sanic.response import json
from sanic import Blueprint

bp = Blueprint('my_blueprint')

@bp.route('/')
async def bp_root(request):
    if request.app.config['DEBUG']:
        return json({'status': 'debug'})
    else:
        return json({'status': 'production'})
​

url：请求的完整URL，即： http://localhost:8000/posts/1/?foo=bar
scheme：与请求关联的URL方案：http或https
host：与请求关联的主机： localhost:8080
path：请求的路径： /posts/1/
query_string：请求的查询字符串：foo=bar或一个空白字符串''
uri_template：匹配路由处理程序的模板： /posts/<id>/
token：授权标头(Authorization)的值： Basic YWRtaW46YWRtaW4=
使用get和getlist访问数据
返回字典的请求属性实际上会返回一个dict被调用的子类 RequestParameters。使用这个对象的关键区别在于get和getlist方法之间的区别。

get(key, default=None)按照正常操作，除了当给定键的值是列表时，只返回第一个项目。
getlist(key, default=None)正常操作，返回整个列表。
响应
response

text
from sanic import response

@app.route('/text')
def handle_request(request):
    return response.text('Hello world!')
HTML
from sanic import response

@app.route('/html')
def handle_request(request):
    return response.html('<p>Hello world!</p>')
JSON
from sanic import response

@app.route('/json')
def handle_request(request):
    return response.json({'message': 'Hello world!'})
File
from sanic import response

@app.route('/file')
async def handle_request(request):
    return await response.file('/srv/www/whatever.png')
Streaming
流媒体

from sanic import response

@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        response.write('foo')
        response.write('bar')
    return response.stream(streaming_fn, content_type='text/plain')
File Streaming
对于大文件，文件和流的组合

from sanic import response

@app.route('/big_file.png')
async def handle_request(request):
    return await response.file_stream('/srv/www/whatever.png')
Redirect
from sanic import response

@app.route('/redirect')
def handle_request(request):
    return response.redirect('/json')
Raw
没有进行编码的响应

from sanic import response

@app.route('/raw')
def handle_request(request):
    return response.raw('raw data')
Modify headers or status
要修改头部或状态代码，将头部或状态参数传递给这些函数

from sanic import response

@app.route('/json')
def handle_request(request):
    return response.json(
        {'message': 'Hello world!'},
        headers={'X-Served-By': 'sanic'},
        status=200
    )
静态文件
static_files

静态文件和目录，比如一个图像文件，在Sanic注册时使用。该方法使用一个端点URL和一个文件名。指定的文件将通过指定的端点访问。

from sanic import Sanic

app = Sanic(__name__)
# Serves files from the static folder to the URL /static
app.static('/static', './static')
# Serves the file /home/ubuntu/test.png when the URL /the_best.png
# is requested
app.static('/the_best.png', '/home/ubuntu/test.png')

app.run(host="0.0.0.0", port=8000)
Note：目前，您不能使用url构建一个静态文件的URL

模版
html templates编写

编写web服务，自然会涉及到html，sanic自带有html函数，但这并不能满足有些需求，故引入jinja2迫在眉睫。使用方法也很简单：

# novels_blueprint.py片段
from sanic import Blueprint
from jinja2 import Environment, PackageLoader, select_autoescape

# 初始化blueprint并定义静态文件夹路径
bp = Blueprint('novels_blueprint')
bp.static('/static', './static/novels')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.novels_blueprint', '../templates/novels'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))

def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))
    
@bp.route("/")
async def index(request):
    return template('index.html', title='index')
这样，就实现了jinja2 模版的引入。

异常
Exceptions

抛出异常
要抛出异常，只需从sanic异常模块中提出相应的异常。

from sanic.exceptions import ServerError
@app.route('/killme')
def i_am_ready_to_die(request):
    raise ServerError("Something bad happened", status_code=500)
也可以自定义状态码

from sanic.exceptions import abort
from sanic.response import text
@app.route('/youshallnotpass')
def no_no(request):
        abort(401)
        # this won't happen
        text("OK")
处理异常
Handling exceptions

装饰器一个异常列表作为参数来处理。你可以通过SanicException来捕获它们！装饰异常处理函数必须将请求和异常对象作为参数。

from sanic.response import text
from sanic.exceptions import NotFound

@app.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))

@app.exception(NotFound)
def handle_404_redirect(request, exception):
    uri = app.url_for('index')
    return redirect(uri)
有用的异常
Useful exceptions

常用

NotFound:在没有找到合适的请求路径时调用
ServerError:当服务器内部出现问题时调用。如果在用户代码中出现异常，通常会出现这种情况。
中间件和监听
Middleware And Listeners

中间件
Middleware

有两种类型的中间件: 请求和响应。两者都是使用@app声明的。中间件装饰器，装饰器的参数是一个代表其类型的字符串:“请求”或“响应”。响应中间件接收请求和响应作为参数。

最简单的中间件根本不修改请求或响应

@app.middleware('request')
async def print_on_request(request):
    print("I print when a request is received by the server")
    
@app.middleware('response')
async def print_on_response(request, response):
    print("I print when a response is returned by the server")
修改请求或响应
中间件可以修改它所提供的请求或响应参数，只要它不返回它

app = Sanic(__name__)

@app.middleware('response')
async def custom_banner(request, response):
    response.headers["Server"] = "Fake-Server"
    
@app.middleware('response')
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"
    
app.run(host="0.0.0.0", port=8000)
上述代码将按顺序应用这两个中间件。首先，中间件custombanner将把HTTP响应头服务器更改为假服务器，而第二个中间件防止XSS将添加HTTP头来防止跨站点脚本攻击(XSS)攻击。这两个函数是在用户函数返回响应之后调用的。

监听者
Listeners

如果想在服务器启动或关闭时执行启动/分解代码，可以使用以下侦听器:

before_server_start
after_server_start
before_server_stop
after_server_stop
这些监听器在函数中实现为修饰符，它们接受应用程序对象和asyncio循环

@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = await db_setup()
    
@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')
    
@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')
    
@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.close()
如果你想在循环开始后运行一个后台任务，那么Sanic就提供了addtask方法来轻松地完成这一任务。

async def notify_server_started_after_five_seconds():
    await asyncio.sleep(5)
    print('Server successfully started!')
    
app.add_task(notify_server_started_after_five_seconds())
蓝图
Blueprints

蓝图是可以用于应用程序中的子路由的对象。除了向应用程序实例添加路由，蓝图还定义了类似的添加路由的方法，然后以灵活的可插入的方式在应用程序中注册。

simple Blueprint

假设将该文件保存为myblueprint。py，稍后可以导入到您的主应用程序中。

from sanic.response import json
from sanic import Blueprint

bp = Blueprint('my_blueprint')

@bp.route('/')
async def bp_root(request):
    return json({'my': 'blueprint'})
注册蓝图
registering blueprints

蓝图必须在应用程序中注册

from sanic import Sanic
from my_blueprint import bp

app = Sanic(__name__)
app.blueprint(bp)

app.run(host='0.0.0.0', port=8000, debug=True)
使用蓝图
Use_blueprint

网络套接字路由
WebSocket routes

WebSocket处理程序可以注册,使用@bp.websocket装饰或bp.add_websocket_route方法

中间件
Middleware

使用蓝图还可以在全局内注册中间件。

@bp.middleware
async def print_on_request(request):
    print("I am a spy")
    
@bp.middleware('request')
async def halt_request(request):
    return text('I halted the request')

@bp.middleware('response')
async def halt_response(request, response):
    return text('I halted the response')
异常
Exception

异常情况可以用于全局的蓝图

@bp.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))
静态文件
Static files

静态文件可以添加前缀

bp.static('/folder/to/serve', '/web/path')
Start and stop
蓝图可以在服务器的启动和停止过程中运行函数。如果在多处理器模式下运行(超过1个worker)，这些都是在workers fork之后触发的。

before_server_start:在服务器开始接受连接之前执行
after_server_start:在服务器开始接受连接后执行
before_server_stop:在服务器停止接受连接之前执行
after_server_stop:在服务器停止后执行，所有请求都完成了
bp = Blueprint('my_blueprint')

@bp.listener('before_server_start')
async def setup_connection(app, loop):
    global database
    database = mysql.connect(host='127.0.0.1'...)
    
@bp.listener('after_server_stop')
async def close_connection(app, loop):
    await database.close()
用例：API版本控制
Use-case: API versioning

蓝图对于API版本控制是非常有用的，其中一个蓝图可能指向/v1/<route>，另一个指向/v2/<route>。

当一个蓝图被初始化时，它可以选择一个可选的url_prefix参数，这个参数将被预先定义到蓝图中定义的所有路由。该特性可用于实现我们的API版本控制方案

# blueprints.py
from sanic.response import text
from sanic import Blueprint

blueprint_v1 = Blueprint('v1', url_prefix='/v1')
blueprint_v2 = Blueprint('v2', url_prefix='/v2')

@blueprint_v1.route('/')
async def api_v1_root(request):
    return text('Welcome to version 1 of our documentation')

@blueprint_v2.route('/')
async def api_v2_root(request):
    return text('Welcome to version 2 of our documentation')
当我们在应用程序上注册我们的蓝图时，路径/v1和/v2将指向单个的蓝图，它允许为每个API版本创建子站点。

# main.py
from sanic import Sanic
from blueprints import blueprint_v1, blueprint_v2

app = Sanic(__name__)
app.blueprint(blueprint_v1, url_prefix='/v1')
app.blueprint(blueprint_v2, url_prefix='/v2')

app.run(host='0.0.0.0', port=8000, debug=True)
用url_for构建url
如果希望在blueprint内部路由生成一个URL，记住，端点名称采用格式<blueprint_name>.<handler_name>

@blueprint_v1.route('/')
async def root(request):
    url = app.url_for('v1.post_handler', post_id=5) # --> '/v1/post/5'
    # url = request.app.url_for('v1.post_handler', post_id=5) # --> '/v1/post/5'
    return redirect(url)

@blueprint_v1.route('/post/<post_id>')
async def post_handler(request, post_id):
    return text('Post {} in Blueprint V1'.format(post_id))
Note: 当app和blueprint不在同一个模块内记得加上request

例如：url = request.app.url_for('v1.post_handler', post_id=5) # --> '/v1/post/5'

配置
Configuration

任何一个相当复杂的应用程序都需要配置，而不是在实际代码中进行。对于不同的环境或安装，设置可能是不同的。

基本配置
Sanic在应用程序对象的配置属性中保持配置。配置对象仅仅是一个可以使用点符号或字典来修改的对象。

app = Sanic('myapp')
app.config.DB_NAME = 'appdb'
app.config.DB_USER = 'appuser'
因为配置对象实际上是一个字典，所以可以使用它的update方法来一次设置几个值:

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)
一般来说，该约定只具有大写的配置参数。下面描述的加载配置的方法只会查找这些大写的参数。

载入配置
如何加载配置有几种方法。

从环境变量
使用SANIC_前缀定义的任何变量都将应用于sanic config。例如，设置SANIC_REQUEST_TIMEOUT将由应用程序自动加载并输入REQUEST_TIMEOUT配置变量。你可以通过一个不同的前缀到Sanic:

app = Sanic(load_env='MYAPP_')
然后，上面的变量将是MYAPP_REQUEST_TIMEOUT。如果您想要禁用环境变量的加载，您可以将其设置为False:

app = Sanic(load_env=False)
从对象
如果有很多配置值，而且它们有合理的默认值，那么将它们放到一个模块中可能会有帮助:

import myapp.default_settings

app = Sanic('myapp')
app.config.from_object(myapp.default_settings)
您也可以使用类或任何其他对象。

从文件
通常，您需要从一个不属于分布式应用程序的文件中加载配置。可以使用from_pyfile(/path/to/config_file)从文件加载配置。但是，这需要程序知道配置文件的路径。因此，您可以在一个环境变量中指定配置文件的位置，并告诉Sanic使用它来查找配置文件:

app = Sanic('myapp')
app.config.from_envvar('MYAPP_SETTINGS')
然后，您可以使用MYAPP_SETTINGS环境变量集运行您的应用程序:

$ MYAPP_SETTINGS=/path/to/config_file python3 myapp.py
INFO: Goin' Fast @ http://0.0.0.0:8000
配置文件是常规的Python文件，这些文件是为了加载它们而执行的。这允许您使用任意逻辑来构造正确的配置。在配置中只添加了大写的变量。最常见的配置包括简单的键值对：

# config_file
DB_HOST = 'localhost'
DB_NAME = 'appdb'
DB_USER = 'appuser'
内置配置值
在这个框中，只有几个预定义值，在创建应用程序时可以重写。

| Variable           | Default   | Description                                   |
| ------------------ | --------- | --------------------------------------------- |
| REQUEST_MAX_SIZE   | 100000000 | How big a request may be (bytes)              |
| REQUEST_TIMEOUT    | 60        | How long a request can take to arrive (sec)   |
| RESPONSE_TIMEOUT   | 60        | How long a response can take to process (sec) |
| KEEP_ALIVE         | True      | Disables keep-alive when False                |
| KEEP_ALIVE_TIMEOUT | 5         | How long to hold a TCP connection open (sec)  |
不同的超时变量
请求超时度量在新打开的TCP连接被传递给Sanic后端服务器时的时间间隔，以及接收整个HTTP请求的瞬间。如果时间超过了REQUEST_TIMEOUT值(以秒为单位)，那么这将被视为客户端错误，因此Sanic生成一个HTTP 408响应并将其发送给客户端。如果您的客户经常通过非常大的请求负载或者非常缓慢地上传请求，请调整这个值。

响应超时度量在Sanic服务器将HTTP请求传递到Sanic应用程序的时间之间的时间，以及发送到客户机的HTTP响应的时间。如果时间超过了RESPONSE_TIMEOUT值(以秒为单位)，这被认为是服务器错误，因此Sanic生成一个HTTP 503响应并将其设置为客户机。如果应用程序很可能长时间运行，延迟响应的生成，则将此值调整得更高。

Keep-Alive是什么? Keep Alive Timeout value的作用是什么呢?
Keep-Alive是HTTP 1.1中的一个HTTP特性。发送HTTP请求时，客户端(通常是web浏览器应用程序)可以设置一个keepalive消息头，以指示HTTP服务器(Sanic)在发送响应之后不关闭TCP连接。这允许客户端重用现有的TCP连接来发送后续的HTTP请求，并确保客户机和服务器的网络流量更高效。

在Sanic中，KEEP_ALIVE配置变量默认设置为True。如果您在应用程序中不需要此功能，则将其设置为False，以便在发送响应后立即关闭所有客户端连接，而不考虑请求上的keepalive消息头。

服务器保持TCP连接打开的时间量由服务器本身决定。在Sanic中，该值使用KEEP_ALIVE_TIMEOUT值进行配置。默认情况下，它设置为5秒，这是与Apache HTTP服务器相同的默认设置，在允许客户端发送新请求的足够时间和不同时打开太多连接之间保持良好的平衡。不要超过75秒，除非你知道你的客户正在使用支持TCP连接的浏览器。

供参考:

Apache httpd server default keepalive timeout = 5 seconds
Nginx server default keepalive timeout = 75 seconds
Nginx performance tuning guidelines uses keepalive = 15 seconds
IE (5-9) client hard keepalive limit = 60 seconds
Firefox client hard keepalive limit = 115 seconds
Opera 11 client hard keepalive limit = 120 seconds
Chrome 13+ client keepalive limit > 300+ seconds
Cookie
cookie是保存在用户浏览器内的数据块。Sanic既可以读写cookie，也可以存储为键-值对。

Warning

cookie可以由客户机自由修改。因此，您不能仅在cookie中存储诸如登录信息这样的数据，因为客户机可以随意更改这些数据。为了确保存储在cookie中的数据不会被客户伪造或篡改， use something like itsdangerous to cryptographically sign the data.
读取cookies
用户的cookie可以通过请求对象的cookie字典访问。

from sanic.response import text

@app.route("/cookie")
async def test(request):
    test_cookie = request.cookies.get('test')
    return text("Test cookie set to: {}".format(test_cookie))
写入cookies
返回响应时，可以在响应对象上设置cookie。

from sanic.response import text

@app.route("/cookie")
async def test(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response
删除cookies
cookie可以通过语义或显式删除。

from sanic.response import text

@app.route("/cookie")
async def test(request):
    response = text("Time to eat some cookies muahaha")

    # This cookie will be set to expire in 0 seconds
    del response.cookies['kill_me']

    # This cookie will self destruct in 5 seconds
    response.cookies['short_life'] = 'Glad to be here'
    response.cookies['short_life']['max-age'] = 5
    del response.cookies['favorite_color']

    # This cookie will remain unchanged
    response.cookies['favorite_color'] = 'blue'
    response.cookies['favorite_color'] = 'pink'
    del response.cookies['favorite_color']

    return response
响应cookie可以设置为字典值，并具有以下参数:
expires (datetime): cookie在客户机浏览器上过期的时间。
path(string): 此cookie应用的url的子集。默认为/。
comment(string): 注释(元数据)。
domain(string): 指定cookie有效的域。显式指定的域必须总是以一个点开始。
max-age(number): cookie应该存活的秒数。
secure (boolean): 指定cookie是否只通过HTTPS发送。
httponly (boolean): 指定Javascript是否不能读取cookie。
session
sanic对此有一个第三方插件sanic_session，用法非常简单，见官方例子如下：

import asyncio_redis

from sanic import Sanic
from sanic.response import text
from sanic_session import RedisSessionInterface

app = Sanic()


# Token from https://github.com/subyraman/sanic_session

class Redis:
    """
    A simple wrapper class that allows you to share a connection
    pool across your application.
    """
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(
                host='localhost', port=6379, poolsize=10
            )

        return self._pool


redis = Redis()

# pass the getter method for the connection pool into the session
session_interface = RedisSessionInterface(redis.get_redis_pool, expiry=604800)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session_interface.save(request, response)


@app.route("/")
async def test(request):
    # interact with the session like a normal dict
    if not request['session'].get('foo'):
        request['session']['foo'] = 0

    request['session']['foo'] += 1

    response = text(request['session']['foo'])

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
Handler Decorators
由于Sanic处理程序是简单的Python函数，您可以用类似于Flask的方式向它们应用decorator。一个典型的用例是，当您需要一些代码在处理程序的代码执行之前运行。

Authorization Decorator
假设您想要检查用户是否被授权访问某个特定的端点。您可以创建包装处理函数的decorator，检查客户端是否被授权访问某个资源，并发送适当的响应。

from functools import wraps
from sanic.response import json

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized. 
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


@app.route("/")
@authorized()
async def test(request):
    return json({status: 'authorized'})
Streaming
流媒体

Request Streaming
Sanic允许您通过流获取请求数据，如下所示。当请求结束时，request.stream.get()返回None。只有post, put和patch decorator 有流参数。

from sanic import Sanic
from sanic.views import CompositionView
from sanic.views import HTTPMethodView
from sanic.views import stream as stream_decorator
from sanic.blueprints import Blueprint
from sanic.response import stream, text

bp = Blueprint('blueprint_request_stream')
app = Sanic('request_stream')


class SimpleView(HTTPMethodView):

    @stream_decorator
    async def post(self, request):
        result = ''
        while True:
            body = await request.stream.get()
            if body is None:
                break
            result += body.decode('utf-8')
        return text(result)


@app.post('/stream', stream=True)
async def handler(request):
    async def streaming(response):
        while True:
            body = await request.stream.get()
            if body is None:
                break
            body = body.decode('utf-8').replace('1', 'A')
            response.write(body)
    return stream(streaming)


@bp.put('/bp_stream', stream=True)
async def bp_handler(request):
    result = ''
    while True:
        body = await request.stream.get()
        if body is None:
            break
        result += body.decode('utf-8').replace('1', 'A')
    return text(result)


async def post_handler(request):
    result = ''
    while True:
        body = await request.stream.get()
        if body is None:
            break
        result += body.decode('utf-8')
    return text(result)

app.blueprint(bp)
app.add_route(SimpleView.as_view(), '/method_view')
view = CompositionView()
view.add(['POST'], post_handler, stream=True)
app.add_route(view, '/composition_view')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
Response Streaming
Sanic允许您使用stream 方法将内容流到客户机。该方法接受一个coroutine回调，该回调将传递给写入的StreamingHTTPResponse对象。一个简单的例子如下:

from sanic import Sanic
from sanic.response import stream

app = Sanic(__name__)

@app.route("/")
async def test(request):
    async def sample_streaming_fn(response):
        response.write('foo,')
        response.write('bar')

    return stream(sample_streaming_fn, content_type='text/csv')
在您希望将内容流到来自外部服务(如数据库)的客户端时，这很有用。例如，您可以使用asyncpg提供的异步游标将数据库记录流到客户端:

@app.route("/")
async def index(request):
    async def stream_from_db(response):
        conn = await asyncpg.connect(database='test')
        async with conn.transaction():
            async for record in conn.cursor('SELECT generate_series(0, 10)'):
                response.write(record[0])

    return stream(stream_from_db)
基于类的视图
基于类的视图只是实现对请求的响应行为的类。它们提供了一种方法，将不同的HTTP请求类型划分到同一端点。与其定义和修饰三个不同的处理函数(每个端点支持的请求类型)，端点可以分配一个基于类的视图。

定义视图
基于类的视图应该子类化HTTPMethodView。然后，您可以为希望支持的每个HTTP请求类型实现类方法。如果接收到的请求没有定义的方法，则会生成一个405: Method not allowed 的响应。

要在端点上注册基于类的视图，将使用app.add_route方法。第一个参数应该是被调用的方法as_view的定义类，第二个参数应该是URL端点。

可用的方法是get、post、put、patch和delete。使用所有这些方法的类看起来如下所示。

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic('some_name')

class SimpleView(HTTPMethodView):

  def get(self, request):
      return text('I am get method')

  def post(self, request):
      return text('I am post method')

  def put(self, request):
      return text('I am put method')

  def patch(self, request):
      return text('I am patch method')

  def delete(self, request):
      return text('I am delete method')

app.add_route(SimpleView.as_view(), '/')
你还可以使用async 异步语法。

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic('some_name')

class SimpleAsyncView(HTTPMethodView):

  async def get(self, request):
      return text('I am async get method')

app.add_route(SimpleAsyncView.as_view(), '/')
URL参数
如果您需要任何URL参数，如路由指南中所讨论的，在方法定义中包含它们。

class NameView(HTTPMethodView):

  def get(self, request, name):
    return text('Hello {}'.format(name))

app.add_route(NameView.as_view(), '/<name>')
装饰器
如果您想在类中添加任何装饰器，可以设置decorator类变量。当调用as_view时，这些将被应用到类中。

class ViewWithDecorator(HTTPMethodView):
  decorators = [some_decorator_here]

  def get(self, request, name):
    return text('Hello I have a decorator')

app.add_route(ViewWithDecorator.as_view(), '/url')
URL构建
如果您希望为HTTPMethodView构建一个URL，请记住，类名将是您将传入url_for的端点。例如:

@app.route('/')
def index(request):
    url = app.url_for('SpecialClassView')
    return redirect(url)


class SpecialClassView(HTTPMethodView):
    def get(self, request):
        return text('Hello from the Special Class View!')


app.add_route(SpecialClassView.as_view(), '/special_class_view')
使用组合视图
Using CompositionView

作为HTTPMethodView的替代方法，您可以使用CompositionView将处理程序函数移到视图类之外。

每个支持的HTTP方法的处理函数都在源代码的其他地方定义，然后使用CompositionView.add方法添加到视图中。第一个参数是要处理的HTTP方法的列表(例如，['GET'， 'POST'])，第二个参数是处理函数。下面的示例显示了使用外部处理程序函数和内联lambda的CompositionView用法:

from sanic import Sanic
from sanic.views import CompositionView
from sanic.response import text

app = Sanic(__name__)

def get_handler(request):
    return text('I am a get method')

view = CompositionView()
view.add(['GET'], get_handler)
view.add(['POST', 'PUT'], lambda request: text('I am a post/put method'))

# Use the new view to handle requests to the base URL
app.add_route(view, '/')
Note: 当前您不能使用url_for为CompositionView构建一个URL。

自定义协议
注意:这是高级用法，大多数读者不需要这样的功能。

您可以通过指定自定义协议来更改Sanic协议的行为，该协议应该是asyncio.protocol的子类。然后，该协议可以作为sanic.run方法的关键字参数协议传递。

自定义协议类的构造函数接收来自Sanic的以下关键字参数。

loop: 一个异步兼容的事件循环。
connections: 用于存储协议对象的集合。当Sanic接收SIGINT或SIGTERM时，它执行protocol.close_if_idle关闭此集合中存储的所有协议对象。
signal: 带有stopped属性的sanic.server.Signal对象。当Sanic收到SIGINT或SIGTERM，signal.stopped分配True。
request_handler: 取一个sanic.request.Request对象和response回调作为参数的coroutine。
error_handler: 在抛出异常时调用的处理程序sanic.exceptions.Handler。
request_timeout: 请求超时前的秒数。
request_max_size: 指定请求的最大大小的整数，以字节为单位。
Example
如果处理函数不返回HTTPResponse对象，则默认协议中出现错误。

通过重写write_response协议方法，如果处理程序返回一个字符串，它将被转换为HTTPResponse对象。

from sanic import Sanic
from sanic.server import HttpProtocol
from sanic.response import text

app = Sanic(__name__)


class CustomHttpProtocol(HttpProtocol):

    def __init__(self, *, loop, request_handler, error_handler,
                 signal, connections, request_timeout, request_max_size):
        super().__init__(
            loop=loop, request_handler=request_handler,
            error_handler=error_handler, signal=signal,
            connections=connections, request_timeout=request_timeout,
            request_max_size=request_max_size)

    def write_response(self, response):
        if isinstance(response, str):
            response = text(response)
        self.transport.write(
            response.output(self.request.version)
        )
        self.transport.close()


@app.route('/')
async def string(request):
    return 'string'


@app.route('/1')
async def response(request):
    return text('response')

app.run(host='0.0.0.0', port=8000, protocol=CustomHttpProtocol)
SSL Example
可以传入SSLContext：

import ssl
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain("/path/to/cert", keyfile="/path/to/keyfile")

app.run(host="0.0.0.0", port=8443, ssl=context)
您还可以将证书和密钥的位置传递给字典:

ssl = {'cert': "/path/to/cert", 'key': "/path/to/keyfile"}
app.run(host="0.0.0.0", port=8443, ssl=ssl)
日志
Logging

Sanic允许您根据python3 logging API对请求进行不同类型的日志记录(访问日志、错误日志)。如果您想创建一个新的配置，您应该对python3 logging有一些基本的了解。

Quick Start
使用默认设置的一个简单示例如下:

from sanic import Sanic

app = Sanic('test')

@app.route('/')
async def test(request):
    return response.text('Hello World!')

if __name__ == "__main__":
  app.run(debug=True, access_log=True)
要使用自己的日志记录配置，只需使用logging.config.dictConfig，或在初始化Sanic应用时传递log_config：

app = Sanic('test', log_config=LOGGING_CONFIG)
要关闭日志，只需分配access_log=False:

if __name__ == "__main__":
  app.run(access_log=False)
这将跳过在处理请求时调用日志功能。你甚至可以做进一步的生产以获得额外的速度:

if __name__ == "__main__":
  # disable debug messages
  app.run(debug=False, access_log=False)
Configuration
默认情况下，log_config参数设置为使用sanic.log.LOGGING_CONFIG_DEFAULTS字典配置。

在sanic中使用了三个日志记录器loggers，如果您想创建自己的日志配置，则必须定义:

root: 用于记录内部消息。
sanic.error: 用于记录错误日志。

sanic.access: 用于记录访问日志。

Log format
除了python提供的默认参数(asctime、levelname、message)， Sanic还提供了用于访问日志记录器logger的其他参数:

host (str): request.ip
request (str): request.method + " " + request.url
status (int): response.status
byte (int): len(response.body)
默认的访问日志格式是：

%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d
测试
Testing

Sanic端点可以使用test_client对象在本地测试，这取决于附加的aiohttp库。

test_client公开get、post、put、delete、patch、head和options方法，以便与应用程序运行。一个简单的例子(使用pytest)如下:

# Import the Sanic app, usually created with Sanic(__name__)
from external_server import app

def test_index_returns_200():
    request, response = app.test_client.get('/')
    assert response.status == 200

def test_index_put_not_allowed():
    request, response = app.test_client.put('/')
    assert response.status == 405
在内部，每次调用test_client方法时，Sanic应用程序运行于127.0.0.1:42101，您的测试请求使用aiohttp执行。

test_client方法接受以下参数和关键字参数:

uri(default '/') 一个表示测试uri的字符串。
gather_request(default True) 一个布尔值，它决定原始请求是否由函数返回。如果设置为True，返回值是(request, response)的一个元组，如果False仅返回响应。

server_kwargs (default {}) 在测试请求运行之前传递给app.run的附加参数。

debug(default False)一个布尔值，它决定是否在调试模式下运行服务器。

该函数进一步接受了*request_args和**request_kwargs，它们直接传递给aiohttp ClientSession请求。

例如，为了向GET请求提供数据，您将执行以下操作:

def test_get_request_includes_data():
    params = {'key1': 'value1', 'key2': 'value2'}
    request, response = app.test_client.get('/', params=params)
    assert request.args.get('key1') == 'value1'
并向JSON POST请求提供数据:

def test_post_json_request_includes_data():
    data = {'key1': 'value1', 'key2': 'value2'}
    request, response = app.test_client.post('/', data=json.dumps(data))
    assert request.json.get('key1') == 'value1'
关于aiohttp的可用参数的更多信息可以在ClientSession的文档中找到。

pytest-sanic
pytest-sanic是一个pytest插件，它可以帮助您异步地测试您的代码。编写测试:

async def test_sanic_db_find_by_id(app):
    """
    Let's assume that, in db we have,
        {
            "id": "123",
            "name": "Kobe Bryant",
            "team": "Lakers",
        }
    """
    doc = await app.db["players"].find_by_id("123")
    assert doc.name == "Kobe Bryant"
    assert doc.team == "Lakers"
pytest-sanic还提供了一些有用的设备，如loop、unused_port、test_server、test_client。

@pytest.yield_fixture
def app():
    app = Sanic("test_sanic_app")

    @app.route("/test_get", methods=['GET'])
    async def test_get(request):
        return response.json({"GET": True})

    @app.route("/test_post", methods=['POST'])
    async def test_post(request):
        return response.json({"POST": True})

    yield app


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))


#########
# Tests #
#########

async def test_fixture_test_client_get(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/test_get')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"GET": True}

async def test_fixture_test_client_post(test_cli):
    """
    POST request
    """
    resp = await test_cli.post('/test_post')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"POST": True}
部署
Deploying

部署Sanic是由内置的webserver简化的。在定义了sanic.Sanic的实例之后。我们可以用以下关键字参数调用run方法:

host (default "127.0.0.1"): 地址来托管服务器。
port (default 8000): 开启服务器的端口。
debug (default False): 启用调试输出(减慢服务器)。
ssl (default None): ssl加密的SSLContext。
sock (default None): 用于服务器接受连接的套接字。
workers (default 1): 生成的工作进程数。
loop (default None): 一个asyncio兼容的事件循环。如果没有指定，Sanic将创建自己的事件循环。
protocol (default HttpProtocol): asyncio.protocol的子类。
进程
Workers

默认情况下，Sanic只使用一个CPU核心侦听主进程。To crank up the juice，只需在run参数中指定workers的数量。

app.run(host='0.0.0.0', port=1337, workers=4)
Sanic将会自动启动多个进程，并在它们之间路由流量。我们建议尽可能多的workers拥有可用的核心。

通过命令行运行
如果您喜欢使用命令行参数，则可以通过执行模块来启动Sanic服务器。例如，如果您在名为server.py的文件中初始化Sanic作为app，你可以这样运行服务器:

python -m sanic server.app --host=0.0.0.0 --port=1337 --workers=4

通过这种运行sanic的方式，无需在Python文件中调用app.run。如果这样做，请确保将其包装起来，以便它只在解释器直接运行时执行。

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, workers=4)
通过Gunicorn运行
Gunicorn ‘Green Unicorn’ 是UNIX的一个WSGI HTTP服务器。它是一个由Ruby的Unicorn项目移植的预fork worker模型。

为了使用Gunicorn运行Sanic应用程序，您需要为Gunicornworker-class 参数使用特殊的sanic.worker.GunicornWorker：

gunicorn myapp:app --bind 0.0.0.0:1337 --worker-class sanic.worker.GunicornWorker
如果您的应用程序遭受内存泄漏，您可以配置Gunicorn以优雅地重新启动一个worker，因为它处理了给定数量的请求。这可以方便地帮助限制内存泄漏的影响。

有关更多信息，请参见 Gunicorn 文档。

异步支持
Asynchronous support

如果您需要与其他应用程序共享sanic进程，特别是loop，这是合适的。但是，请注意，该方法不支持使用多进程，并且不是一般运行该应用程序的首选方式。

这里有一个不完整的示例(请参见run_asyn.py在一些更实用的例子中):

server = app.create_server(host="0.0.0.0", port=8000)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(server)
loop.run_forever()
扩展
Extensions

由社区创建的Sanic扩展列表。

Sanic-Plugins-Framework: 方便创建和使用Sanic插件的库。
Sessions: 对sessions的支持。允许使用redis、memcache或内存存储。
CORS: A port of flask-cors.
Compress: 允许您轻松地压缩Sanic响应。Flask-Compress的一个端口。
Jinja2: 支 持Jinja2模板。
JWT: JSON Web令牌(JWT)的身份验证扩展。
OpenAPI/Swagger: OpenAPI支持，外加Swagger UI。
Pagination: 简单的分页的支持。
Motor: Simple motor wrapper。
Sanic CRUD: 与peewee模型的CRUD REST API生成。
UserAgent: Add user_agent to request。
Limiter: sanic的速率限制。
Sanic EnvConfig: 将环境变量引入到Sanic配置中。
Babel: 在Babel库的帮助下向Sanic应用程序添加i18n/l10n支持。
Dispatch: 在werkzeug中由DispatcherMiddleware激发的调度程序。可以充当sanicto - wsgi适配器。
Sanic-OAuth: OAuth库，用于连接和创建您自己的令牌提供者。
Sanic-nginx-docker-example: 使用Sanic构建简单易用的骨架项目需要使用nginx，由docker-compose编排。
sanic-graphql: Graphico与Sanic集成。
sanic-prometheus: Sanic的Prometheus标准。
Sanic-RestPlus: A port of Flask-RestPlus for Sanic. Full-featured REST API with SwaggerUI generation。
sanic-transmute: 从python函数和类中生成api的Sanic扩展，并自动生成Swagger UI文档。
pytest-sanic: Sanic的一个pytest插件。它帮助您异步地测试代码。
jinja2-sanic: Sanic的jinja2模板渲染器。