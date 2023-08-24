from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


notes_categories = db.Table(
    'notes_categories',
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id', ondelete="CASCADE"), nullable=False, primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False, primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    
    profile = db.relationship('Profile', cascade="all, delete", backref='user', uselist=False)
    notes = db.relationship('Note', cascade="all, delete", backref='user')
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "biography": self.profile.biography,
            "notes": [note.serialize() for note in self.notes]
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit() 


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.String(200), default="")
    facebook = db.Column(db.String(200), default="")
    twitter = db.Column(db.String(200), default="")
    instagram = db.Column(db.String(200), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "biography": self.biography,
            "facebook": self.facebook,
            "twitter": self.twitter,
            "instagram": self.instagram,
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit() 
        

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    categories = db.relationship('Category', secondary=notes_categories)
    
    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "username": self.user.username,
            "categories": [category.serialize() for category in self.categories]
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit() 
        

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    notes = db.relationship('Note', secondary=notes_categories)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit() 
        
