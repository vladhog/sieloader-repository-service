import cherrypy
from cherrypy_dynpool import ThreadPoolMonitor
from flask_minify import Minify
from flask import Flask


from params import *
import api

app = Flask("SIERRA Repository")
Minify(app=app, go=False)

app.register_blueprint(routes)

cherrypy.tree.graft(app.wsgi_app, '/')
cherrypy.engine.threadpool_monitor = ThreadPoolMonitor(cherrypy.engine)
cherrypy.engine.threadpool_monitor.subscribe()
cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8060,
                        'engine.autoreload.on': True,
                        'server.thread_pool': 5,
                        'server.thread_pool_max': -1,
                        'server.thread_pool_minspare': 5,
                        'server.thread_pool_maxspare': 15,
                        'server.thread_pool_frequency': 2,
                        'server.thread_pool_log_frequency': 1,
                        'server.thread_pool_shrink_frequency': 5,
                        })
cherrypy.engine.start()
cherrypy.engine.threadpool_monitor.configure(
    thread_pool=cherrypy.server.httpserver.requests,
    logger=cherrypy.log
)