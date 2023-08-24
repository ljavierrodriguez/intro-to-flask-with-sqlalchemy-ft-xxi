from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit() 