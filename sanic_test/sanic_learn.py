from sanic.response import text, redirect, json
from sanic import Sanic
from sanic import Blueprint, response
from sanic.exceptions import NotFound

bp = Blueprint('my_blueprint')


async def handler1(request):
    return text('ok')


async def handler2(request, name):
    return text('Folder - {}'.format(name))


async def person_handler2(request, name):
    return text('Person - {}'.format(name))

app = Sanic(__name__)
app.blueprint(bp)


# add earch handler function as a router
app.add_route(handler1, '/test')
app.add_route(handler2, 'folder/<name>')
app.add_route(person_handler2, '/person/<name:[A-z]>', methods=['GET'])


@app.route('/')
async def index(request):
    # generate a URL for the endPoint 'post_handler'
    url = app.url_for('post_handler', post_id=5)
    return redirect(url)


@app.route('/post/<post_id>')
async def post_handler(request, post_id):
    return text('Post-{}'.format(post_id))

url = app.url_for('post_handler', post_id=5, arg_one='one', arg_two='two')
# /posts/5?arg_one=one&arg_two=two

# 支持多值参数
url = app.url_for('post_handler', post_id=5, arg_one=['one', 'two'])
# /posts/5?arg_one=one&arg_one=two


@bp.middleware
async def print_one_request(request):
    print('I am a spy')


@bp.middleware('request')
async def halt_request(request):
    return text('I halted the request')


@bp.middleware('response')
async def halt_reponse(request, response):
    return text('I halted the response')


@app.route('/json')
async def post_json(request):
    return json({'received': True, 'message': request.json})


@bp.exception(NotFound)
def ignore_404s(request, exception):
    return text('Yep')


bp.static('/folder/to/serve', '/web/path')


@app.route('/')
async def root(request):
    url = app.url_for('v1.post_handler', post_id=5)
    return redirect(url)


@app.route('/post/<post_id>')
async def post_handler(request, post_id):
    return text('Post {} in Blueprint v1'.format(post_id))


@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        response.write('foo')
        response.write('bar')
    return response.stream(streaming_fn, content_type='text/plain')


@app.route('/json')
def handle_request(request):
    return response.json({'message': 'Hello world!'},
                         headers={'X-Server-By':'sanic'},
                         status=200)


app = Sanic('myapp')
app.config.DB_NAME = 'appdb'
app.config.DU_USER = 'appuser'

"""


import myapp.default_setting
app = Sanic('myapp')
app.config.from_object(myapp.default_setting)


"""




