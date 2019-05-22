from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    data = users[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype = 'application/json')


@app.route('/create_user', methods = ['GET'])
def create_user():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", username="1234", password="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id==id)
    for user in users:
        js=json.dumps(user,cls=connector.AlchemyEncoder)
        return Response(js,status=200, mimetype='application/json')

    message={'status':404,'message':'Not found'}
    return Response(message, status=404,mimetype='application/json')




if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('0.0.0.0'))
