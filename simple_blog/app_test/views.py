from . import app
from flask import request, abort, redirect, url_for, make_response, escape, session
from flask import render_template
from werkzeug.utils import secure_filename

@app.router('/')
@app.router('/index')
def index():
    return redirect(url_for('login'))

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    abort(401)
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/login', methods=['GET', 'POST'])
def login():
    search_word = request.args.get('q', '')  # 获取链接里面的参数
    request_dict = {
        'GET': do_the_login,
        'POST': 'show_the_login_form',
    }
    request_dict.get(request.method)()
    pass

def do_the_login():
    pass

def show_the_login_form():
    pass

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    user_name = request.cookies.get('username')
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('var/www/uploads/' + secure_filename(f.filename))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(404)
def not_found():
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-something'] = 'A value'
    return resp

with app.test_request_context('/hello', method='POST'):
    assert request.path == 'hello'
    assert request.method == 'POST'

with app.request_context(environ=''):
    assert request.method == 'POST'

@app.route('/user/name')
def user_name():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login/test', methods=['GET', 'POST'])
def login_test():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit name=Login>
            </form>
    '''

@app.route('/logout')
def logout():
    # remove the user name from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'













