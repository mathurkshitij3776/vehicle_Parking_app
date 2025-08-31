from .database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(), nullable = False)
    username  = db.Column(db.String(), nullable = False)
    password =  db.Column(db.String(), nullable = False)
    role =  db.Column(db.String(), nullable = False, default = 'user')
    

class Parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    primelocation  = db.Column(db.String(), nullable = False, unique = True)
    priceperhour =  db.Column(db.Integer, nullable = False)
    address =  db.Column(db.String(), nullable = False)
    pincode = db.Column(db.String())
    maxspots =  db.Column(db.Integer, nullable = False)
    spots = db.relationship('Parking_spot', cascade = "all,delete" , backref = 'parking_lot', lazy = True)

class Parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    lotid =  db.Column(db.Integer, db.ForeignKey('parking_lot.id') , nullable = False)
    status =   db.Column(db.String(), nullable = False, default = 'A')
    

class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable = False)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id') , nullable = False)
    parking_timestamp =  db.Column(db.DateTime, nullable = False)
    leaving_timestamp =  db.Column(db.DateTime, default = None)
    leaving_cost =  db.Column(db.Integer, default = None)
    vichel_number = db.Column(db.Integer, nullable = False)
    



   