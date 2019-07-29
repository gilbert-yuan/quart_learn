from datetime import datetime
from sanic import Sanic, response
from sanic_wtf import SanicForm, FileAllowed, FileRequired, SanicForm
from wtforms import PasswordField, StringField, SubmitField, TextField, FileField
from wtforms.validators import DataRequired, Length
from sanic import response, request
from pathlib import Path
app = Sanic(__name__)

class LoginForm(SanicForm):
    name = StringField('Name', validators=[DataRequired])
    password = PasswordField('Passord', validators=[DataRequired])
    submit = SubmitField('Sign In')

class FeedbackForm(SanicForm):
    note = TextField('Note', validators=[DataRequired(), Length(max=40)])
    submit = SubmitField('Submit')

app.config['WTF_CSRF_SECRET_KEY'] = 'top secret!'

app.config['SECRET_EKY'] = 'top secret!!!'
app.config['UPLOAD_DIR'] = './uploaded.tmp'

"""
Configuration 
WTF_CSRF_ENABLED        default True
WTF_CSRF_FIELD_NAME     default sref_token
WTF_CSRF_SECRET_KEY     default 
WTF_CSRF_TIME_LIMIT     default 1800

"""


@app.middleware('request')
async def add_session_to_request(request):
    pass

app.static('/img', app.config.UPLOAD_DIR)

@app.listener('after_server_start')
async def make_upload_dir(app, loop):
    Path(app.config.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


session = {}

@app.middleware('request')
async def add_session(request):
    request['session'] = session



class UploadForm(SanicForm):
    image = FileField('Image', validators=[
        FileRequired(), FileAllowed('bmp gif jpg jpeg png'.split())])
    description = StringField('Description', validators=[Length(max=20)])
    submit = SubmitField('Upload')
    


@app.route('/', methods=['GET', 'POST'])
async def index(request):
    form = UploadForm(request)
    if form.validate_on_submit():
        image = form.image.data
        # NOTE: trusting user submitted file names here, the name should be
        # sanitized in production.
        uploaded_file = Path(request.app.config.UPLOAD_DIR) / image.name
        uploaded_file.write_bytes(image.body)
        description = form.description.data or 'no description'
        session.setdefault('files', []).append((image.name, description))
        return response.redirect('/')
    img = '<section><img src="/img/{}"><p>{}</p><hr></section>'
    images = ''.join(img.format(i, d) for i, d in session.get('files', []))
    content = f"""
    <h1>Sanic-WTF file field validators example</h1>
    {images}
    <form action="" method="POST" enctype="multipart/form-data">
      {'<br>'.join(form.csrf_token.errors)}
      {form.csrf_token}
      {'<br>'.join(form.image.errors)}
      {'<br>'.join(form.description.errors)}
      <br> {form.image.label}
      <br> {form.image}
      <br> {form.description.label}
      <br> {form.description(size=20, placeholder="description")}
      <br> {form.submit}
    </form>
    """
    return response.html(content)

# @app.route('/', methods=['GET', 'POST'])
# async def index(request):
#     form = FeedbackForm(request)
#     if request.method == 'POST' and form.validate():
#         note = form.note.data
#         msg = '{}-{}'.format(datetime.now(), note)
#         session.setdefault('fb', []).append(msg)
#         # name = form.name.data
#         # password = form.password.data
#         return response.redirect('/fail')
#     feedback = ''.join('<p>{}</p>'.format(m) for m in session.get('fb', []))
#     content = f"""
#     <h1>Form with CSRF Validation</h1>
#     <p>Try <a href="/fail">form</a> that fails CSRF validation</p>
#     {feedback}
#     <form action="" method="POST">
#       {'<br>'.join(form.csrf_token.errors)}
#       {form.csrf_token}
#       {'<br>'.join(form.note.errors)}
#       <br>
#       {form.note(size=40, placeholder="say something..")}
#       {form.submit}
#     </form>
#     """
#     # return response.html(await render_template('index.html', form=form))
#     return response.html(content)


@app.route('fail', methods=['GET', 'POST'])
async def fail(request):
    form = FeedbackForm(request)
    if request.method == 'POST' and form.validate():
        note = form.note.data
        msg = '{}-{}'.format(datetime.now(), note)
        session.setdefault('fb', []).append(msg)
        return response.redirect('/fail')
    feedback = ''.join('<p>{}</p>'.format() for m in session.get('fb', []))

    content = f"""
        <h1>Form which fails CSRF Validation</h1>
        <p>This is the same as this <a href="/">form</a> except that CSRF
        validation always fail because we did not render the hidden csrf token</p>
        {feedback}
        <form action="" method="POST">
        {'<br>'.join(form.csrf_token.errors)}
        {'<br>'.join(form.note.errors)}
        <br>
        {form.note(size=40, placeholder="say something..")}
        {form.submit}
        </form>
        """
    return response.html(content)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)