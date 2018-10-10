from quart import Quart
from quart import session
from quart import render_template
from sqlite3 import dbapi2 as sqllite3
import os


app = Quart(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
@app.route('/')
async def index():
    return 'Hello Word!'

app.config.update({
    'DATABASE': os.path.join(app.root_path, 'blog.db')
})

def connect_db():
    engine = sqllite3.connect(app.config["DATABASE"])
    engine.row_factory = sqllite3.Row
    return engine

@app.cli.command()
def init_db():
    """Create an empty database"""
    db = connect_db()
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql')) as file_:
        db.cursor().executescript(file_.read())
    db.commit()

def get_db(g):
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/', methods=['GET'])
async def posts():
    db = get_db()
    cur = db.execute("""SELECT title, text FROM post ORDER BY id DESC""",)
    posts = cur.fetchall()
    return await render_template('post.html', posts=posts)

@app.route('/login')
def login():
    session['logged_in'] = True





































