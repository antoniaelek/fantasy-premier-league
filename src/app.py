from flask import Flask, render_template, request

from tornado.ioloop import IOLoop

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.server.server import Server

from plots import vpc

flask_app = Flask(__name__)

bokeh_app = Application(FunctionHandler(vpc.modify_doc))

io_loop = IOLoop.current()

server = Server({'/vpc': bokeh_app}, io_loop=io_loop, allow_websocket_origin=["localhost:5000"])
server.start()

# Index page, no args
@flask_app.route('/')
def index():
    vpc = server_document("http://localhost:5006/vpc")
    return render_template("index.html", vpc=vpc)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    # app.run(host='0.0.0.0')

    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from bokeh.util.browser import view

    print('Opening Flask app with embedded Bokeh application on http://localhost:8080/')

    # This uses Tornado to server the WSGI app that flask provides. Presumably the IOLoop
    # could also be started in a thread, and Flask could server its own app directly
    http_server = HTTPServer(WSGIContainer(flask_app))
    http_server.listen(5000)

    io_loop.add_callback(view, "http://localhost:5000/")
    io_loop.start()
