import os
import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Note, User, Profile, Category
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')

db.init_app(app)
Migrate(app, db) # flask db init, flask db migrate, flask db upgrade, flask db downgrade
CORS(app)

@app.route('/')
def main():
    return jsonify({ "status": "OK"}), 200

@app.route('/api/notes', methods=['GET'])
def list_notes():
    notes = Note.query.all() # [<Note 1>, <Note 2>] # SELECT * FROM notes;
    #notes = list(map(lambda note: note.serialize(), notes))
    notes = [note.serialize() for note in notes]
    return jsonify(notes), 200

@app.route('/api/notes/<int:id>', methods=['GET'])
def read_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({ "msg": f"Note with id {id} not found!"}), 404 
    
    return jsonify(note.serialize()), 200       

@app.route('/api/notes', methods=['POST'])
def create_note():
    
    body = request.json.get("body")
    categories = request.json.get("categories")
    
    if not body:
        return jsonify({"msg": "Body is required!"}), 400
    
    note = Note()
    note.body = body
    note.user_id = 1
    
    for category_id in categories:
        category = Category.query.get(category_id)
        
        if not category in note.categories:
            note.categories.append(category)
    
    
    note.save() # llamamos a la funcion save para crear el nuevo objeto note
    
    #db.session.add(note)
    #db.session.commit() 
    
    return jsonify(note.serialize()), 201
    
@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    
    body = request.json.get("body")
    categories = request.json.get("categories")
    
    if not body:
        return jsonify({"msg": "Body is required!"}), 400
    
    note = Note.query.get(id)
    if not note:
        return jsonify({ "msg": f"Note with id {id} not found!"}), 404 
    
    note.body = body
    
    for category_id in categories:
        category = Category.query.get(category_id)
        
        if not category in note.categories:
            note.categories.append(category)
    
    
    note.update() # llamamos a la funcion update para guardar los cambios del objeto note
    
    #db.session.commit() 
    
    return jsonify(note.serialize()), 200

@app.route('/api/notes', methods=['DELETE'])
@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id = None):
    
    if id is not None:
        note = Note.query.get(id)
        if not note:
            return jsonify({ "msg": f"Note with id {id} not found!"}), 404
        note.delete() # llamamos a la function delete del objeto note para eliminar
        
    else:
        #notes = Note.query.all()
        notes = Note.query.filter_by(user_id=1)
        for note in notes:
            note.delete()

    return jsonify({ "success": "Note deleted!"}), 200

@app.route('/api/notes/search', methods=['GET'])
def search_notes():
    
    search = request.args.get('s')
    start = request.args.get('start')    
    end = request.args.get('end')
        
    if not search:
        return jsonify({ "msg": "Please, insert words to search"}), 400
    
    #notes = Note.query.filter_by(body=search)
    
    #notes = Note.query.filter(Note.body.ilike(f"%{search}%")) # "%and%", "%and", "and%"
    
    notes = Note.query.filter(Note.body.ilike(f"%{search}%") & (Note.created_at.between(start, end)))
     
    notes = [note.serialize() for note in notes]
    
    return jsonify({ "search": search, "results": notes }), 200

@app.route('/api/test')
def test_models():
    
    user = User()
    user.username = "lrodriguez@4geeks.co"
    
    """
    user.save()
    profile = Profile()
    profile.user_id = user.id
    profile.save()
    """
    profile = Profile()
    user.profile = profile
    #user.save()
    
    
    #user = User.query.get(4)
    #user.profile.biography = "Soy profesor"
    #user.profile.twitter = "luisjrodriguezo"
    #user.update()
    
    #user = User.query.get(3)
    #user.profile.delete()
    #user.delete()
    
    for i in range(11):
        note = Note()
        note.body = f"This is my note {i+1}"
        #note.user_id = user.id 
        #note.save()
        user.notes.append(note)
    
    user.save()
    
    return jsonify({"message": "check the database!"}), 200
    

@app.route('/api/test/categories')
def load_categories():
    
    
    categories = ["Technologies", "Health", "Nationals", "Internationals", "World"]
    
    for cat in categories:
        category = Category()
        category.name = cat
        category.save()
        
    return jsonify({"message": "Categories loaded!"}), 200

@app.route('/api/user/<int:id>')
def read_user_by_id(id):
    
    user = User.query.get(id)
    
    if not user:
        return jsonify({ "msg": f"User with id {id} not found!"}), 404 
    
    return jsonify(user.serialize()), 200

if __name__ == '__main__':
    app.run()
