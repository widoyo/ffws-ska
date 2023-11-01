import os

from flask import Flask, request, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ffws-ska.db')
    )
    
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
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/.git', methods=['POST'])
    def git():
        return request.get_json()
    
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
        return render_template('index.html')
    
    return app    