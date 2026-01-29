from flask import Flask
from config import Config
from models import db
from routes.tickets import tickets_bp
from routes.usuarios import usuarios_bp
from routes.setores import setores_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()
app.register_blueprint(tickets_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(setores_bp)


@app.route('/api/health')
def health():
    return {
        'status': 'ok',
        'aplicacao': 'Service Desk API'
    }


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )