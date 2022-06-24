from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favoritos = db.relationship('Favs', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favoritos": self.favoritos
        }


class Characters (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50))
    eyesColor = db.Column(db.String(50))
    hairColor = db.Column(db.String(50))
    height = db.Column(db.Integer)
    skinColor = db.Column(db.String(50), nullable=False)
    favoritos = db.relationship('Favs', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favoritos": self.favoritos,
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eyesColor": self.eyesColor,
            "hairColor": self.hairColor,
            "height": self.height,
            "skinColor": self.skinColor,
            "favoritos": self.favoritos
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.String(250))
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(100))
    orbitalPeriod = db.Column(db.String(100))
    rotationPeriod = db.Column(db.String(100))
    diameter = db.Column(db.String(100))
    favoritos = db.relationship('Favs', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "orbitalPeriod": self.orbitalPeriod,
            "rotationPeriod": self.rotationPeriod,
            "diameter": self.diameter,
            "favoritos": self.favoritos
        }


class Favs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))


    def to_dict(self):
        return {}

    def __repr__(self):
        return '<Favs %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "character_id": self.character_id,
            "planets_id": self.planets_id
        }