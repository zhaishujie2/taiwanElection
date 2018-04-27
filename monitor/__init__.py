# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import *
import logging

app = Flask(__name__)
app.config.from_object('config')
CORS(app, supports_credentials=True)
handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
# Create modules
# app.register_blueprint(articleModule)
# app.register_blueprint(detectModule)
# app.register_blueprint(flightModule)
# app.register_blueprint(travelerModule)
# app.register_blueprint(screenModule)
# app.register_blueprint(public_opinionModule)
# Enable the toolbar?
app.config['DEBUG_TB_ENABLED'] = app.debug
# Should intercept redirects?
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# Enable the profiler on all requests, default to false
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
# Enable the template editor, default to false
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
# debug toolbar
# toolbar = DebugToolbarExtension(app)
# the debug toolbar is only enabled in debug mode
app.config['DEBUG'] = True
app.config['ADMINS'] = frozenset(['17789624306@163.com'])
app.config['SECRET_KEY'] = '123456'
from .main import  userModule
app.register_blueprint(userModule)
