from routes.home import home_route
from routes.deputado import deputado_route

def configure_all(app):
    configure_routes(app)

def configure_routes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(deputado_route)

def configure_db():
    pass

