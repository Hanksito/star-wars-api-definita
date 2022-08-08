from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

planetfavourites = db.Table('planetfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

peoplefavourites = db.Table('peoplefavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), nullable=False, primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planetfavourites = db.relationship('Planet',secondary=planetfavourites, lazy='subquery', backref=db.backref('user', lazy=True))
    peoplefavourites = db.relationship('People',secondary=peoplefavourites, lazy='subquery', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.Planet

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True ,nullable=False)
    name = db.Column(db.String(250))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color =  db.Column(db.String(250))
    gender = db.Column(db.String(250))
    
    def __repr__(self):
        return '<People %r>' % self.People

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            
        }