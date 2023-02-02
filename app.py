from flask import Flask, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

CORS(app, support_credentials=True)

db = SQLAlchemy()

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tp.db'

db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from Models.models import *
from Controllers.loginController import *
from Controllers.annonceController import *
from Controllers.messagingController import *
from Controllers.photoController import *

migrate = Migrate(app, db)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route("/")
def index():
    return 'Hello, World!'


@app.route('/test')
def test():
    data = session['user']
    id = dict(session)['user']
    return f'Hello, you are logge in as user#{id}!  {data}'


@app.post('/login')
@cross_origin(supports_credentials=True)
def login():
    return loginFunction(db, request, Utilisateur)



@app.post('/logout')
@login_required
def logout():
    return user_logout()



@app.route('/users')
@login_required
def get_users():
    users = Utilisateur.query.all()
    return [user.toJSON() for user in users]



@app.post('/user/<int:id>')
@login_required
def user_account(id):
    user = Utilisateur.query.get(id)
    if(user):
        return user.toJSON()
    else:
        return {
            'message': 'user not found'
        }


@app.post('/user/<int:id>/depot_annonce')
def depot_annonce(id):
    return depotAnnonce(db, request, Utilisateur, Contact, Annonce, Localisation, id)
    

@app.post('/user/<int:id>/recherche_annonce')
def recherche_annonce(id):
    annonces = rechercheAnnonce(request, Annonce)
    return[annonce.toJSON() for annonce in annonces]



@app.post('/annonces')
def annonce_list():
    annonces = Annonce.query.all()
    return [annonce.toJSON() for annonce in annonces]


@app.post('/annonces/<int:id>')
def details_annonce(id):
    return detailsAnnonce(id, Annonce)

@app.post('/user/<int:id>/annonces')
def annonces_deposees(id):
    return annoncesDeposees(id, Annonce)

@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/delete/')
def supprimer_annonce(user_id, annonce_id):
    return supprimerAnnonce(db, user_id, annonce_id, Annonce)


@app.post('/user/<int:id>/messages')
def messages_recus(id):
    return viewMessages(db, id, Message)


@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/message')
def envoyer_offre(user_id, annonce_id):
    return sendMessage(db, request, user_id, annonce_id, Message, Annonce)


@app.route('/annonces/<int:annonce_id>/add_photo')
def imageAdd(annonce_id):
    return f"<form action = '/upload_image' method = 'post' enctype='multipart/form-data'><input type='file' name='file' /><input type='hidden' name='annonce_id' value={annonce_id}><input type = 'submit' value='Upload'></form>"


@app.post('/upload_photo')
def uploadImage():
    return photoAdded(db, request.form['annonce_id'], Photo)


@app.post('photos/<int:id>/delete_photo')
def deletePhoto(id):
    return id


if __name__=='__main__':
    app.run(Debug=True)