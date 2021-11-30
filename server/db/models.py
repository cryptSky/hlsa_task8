from . import db

class User(db.Model):
    id = db.Column(db.Integer, 
                          primary_key=True)
    name = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'birthdate': self.birthdate.strftime("%Y-%m-%d")
        }