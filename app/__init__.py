import os

from flask import Flask, request, render_template, jsonify, current_app

from flask_login import LoginManager
from .models import User, db_wrapper, Logger, Pos

DATABASE = {
    'name': 'ffws-ska.db',
    'engine': 'peewee.SqliteDatabase'
}

DEBUG = True
SECRET_KEY = 'kslaiedljdso'


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(user_id)
    except:
        return None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(__name__)
    
    login_manager.init_app(app)
    
    db_wrapper.init_app(app)
        
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/login')
    def login():
        if request.method == 'POST':
            pass
        return render_template('login.html')

    @app.route('/admin')
    def admin():
        db = get_db()
        poses = db.execute("SELECT * FROM pos ORDER BY nama")
        return render_template('admin/index.html')
    
    @app.route('/alert')
    def alert():
        return render_template('alert/index.html')
    
    @app.route('/map')
    def map():
        return render_template('map/index.html')
    
    @app.route('/about')
    def about():
        return render_template('about/index.html')
    
    @app.route('/')
    def index():
        eks_ch = open(os.path.join(app.instance_path,'ch.json')).read()
        eks_tma = open(os.path.join(app.instance_path,'tma.json')).read()
        our_poses = {
            'kedungbelang': Logger.get(pos_id=1),
            'gandekan': Logger.select(Logger.pos_id==2),
            'joyotakan': Logger.get(pos_id=3)
        }
        return render_template('index.html', ch=eks_ch, tma=eks_tma, poses=our_poses)
    
    return app    