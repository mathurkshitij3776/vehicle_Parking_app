from flask import current_app as app
from flask import jsonify, abort, request, send_from_directory
from .models import *
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from application.caching import cache
from celery.result import AsyncResult
from application.tasks import csv_report, monthly_report, generate_msg

def role_req(role):
    def wrapper(fun):
        @wraps(fun)
        @jwt_required()
        def decorator(*args, **kwargs):
             if current_user.role != role:
                 return jsonify(msg = "You are not authorised"), 403
             return fun(*args, **kwargs)
        return decorator
    return wrapper





@app.route("/api/login", methods = ['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"message":"Username or password is required"}),400
    user = User.query.filter_by(username = username).one_or_none()

    if not user or not check_password_hash(user.password, password):#user.password == password
        return jsonify({ "message": "either username or password is wrong"}), 401
    
    cuser = {
        "id" : user.id,
        "name" : user.name,
        "username" : user.username
     }
    access_token = create_access_token(identity = user)
    return jsonify(access_token = access_token, role = user.role, auser = cuser), 200



@app.route("/api/register", methods = ['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    fullname = request.json.get('fullname', None)
    hashpassword = generate_password_hash(password)
    user = User.query.filter_by(username = username).one_or_none()
    if user:
        return jsonify( message =  "user already registered"),409
    
    user = User(username = username, password = hashpassword, name = fullname)
    db.session.add(user)
    db.session.commit()
    return jsonify(message =  "user Registered successfully"), 201

#Get ALL Parking lot
@app.route("/api/Parkinglots", methods = ['GET'])
@role_req('admin')
def getparkinglots():
    parkinglots = Parking_lot.query.all()
    listparkinglots = []
    for parkinglot in parkinglots:
        occupied = Parking_spot.query.filter_by(lotid = parkinglot.id, status = 'O').all()
        listparkinglots.append( {
                "id": parkinglot.id,
                "prime_location": parkinglot.prime_location,
                "priceperhour": parkinglot.priceperhour,
                "address" : parkinglot.address,
                "pincode" : parkinglot.pincode,
                "maxspots" : parkinglot.maxspots,
                "number_of_spots" : len(parkinglot.number_of_spots()),
                "Occupied" : len(occupied)
            })
    return jsonify({"parkinglots" :listparkinglots}) 

#admin Dashobard
@app.route("/api/AdminDashboard")
@role_req('admin')
# @cache.cached(timeout= 60, key_prefix= 'admindash')
def admindashobard():
    cacheykey = 'admindash'
    cacheda = cache.get(cacheykey)
    if cacheda:
        return jsonify({"parkinglots":cacheda}), 200
    # cachedata = cache.get('admindash')
    # if cachedata:
    #     return cachedata
    Parkinglots = Parking_lot.query.all()
    listparkinglots = []
    # parking_lots = {}
    if Parkinglots:
        for parkinglot in Parkinglots:
             occupied = Parking_spot.query.filter_by(lotid = parkinglot.id, status = 'O').all()
             listparkinglots.append( {
                     "id": parkinglot.id,
                     "primelocation": parkinglot.primelocation,
                     "priceperhour": parkinglot.priceperhour,
                     "address" : parkinglot.address,
                     "pincode" : parkinglot.pincode,
                     "maxspots" : parkinglot.maxspots,
                    #  "number_of_spots" : len(parkinglot.number_of_spots()),
                     "Occupied" : len(occupied),
                     "spots":[{"id":s.id, "lotid":s.lotid, "status":s.status} for s in parkinglot.spots]
                 })
        # return jsonify({"parkinglots" :listparkinglots}),200
        # cachd = jsonify({"parkinglots" :listparkinglots})
        # cache.set('admindash', cachd, timeout = 60)
        # return cachd, 200
        cache.set(cacheykey, listparkinglots, timeout=10)  # 5 minutes
        return jsonify({"parkinglots": listparkinglots}), 200
    return jsonify({"message" : "NO PARKING LOT AVAILABLE"}), 404


#Create parking lot
@app.route("/api/createParkinglot", methods = ['POST'])
@role_req('admin')
def createparkinglot():
    primelocation = request.json.get("primelocationName", None)
    address = request.json.get("address", None)
    pincode = request.json.get("pincode", None)
    priceperhour = request.json.get("priceperhour", None)
    maxspots = request.json.get("maxspots", None)
    maxspots = int(maxspots)
    priceperhour = int(priceperhour)
    # if Parking_lot.query.filter_by(address = )
    if not priceperhour or not address or not primelocation or not maxspots or not pincode:
        return jsonify({"message": "reneter all the details"})
      
    newparkinglot = Parking_lot(primelocation = primelocation, 
                                address = address,
                                pincode = pincode, 
                                priceperhour = priceperhour, 
                                maxspots = maxspots)
    db.session.add(newparkinglot)
    db.session.commit()
    for _ in range(maxspots):
        newspot = Parking_spot(lotid = newparkinglot.id)
        db.session.add(newspot)
    db.session.commit()
    res  = generate_msg.delay()
    cache.delete('admindash')
    return jsonify({"message" : "Parkinglot success"}), 201

#edit parkinglot
@app.route("/api/editParkinglot/<int:id>", methods = ['GET','PUT', "POST"])
@role_req('admin')
def editparkinglot(id):
    if request.method == 'GET':
        plot=  Parking_lot.query.filter_by(id  = id).first()
        if not plot:
            return jsonify({"message": "No parking lot found"}), 404
        
        lot = {
            "id": plot.id,
            "primelocation" : plot.primelocation,
            "priceperhour" : plot.priceperhour,
            "address": plot.address,
            "pincode": plot.pincode,
            "maxspots": plot.maxspots
        }
        return jsonify(formdata = lot), 200
    
    else:
        parkinglot = Parking_lot.query.filter_by(id =id).first()
        parkinglot.primelocation = request.json.get("primelocation")
        parkinglot.address = request.json.get("address")
        parkinglot.priceperhour = request.json.get("priceperhour")
        spotsoldcount = parkinglot.maxspots
        newspotcount = request.json.get("maxspots")
        # parkinglot.maxspots = request.json.get("maxspots")
        parkinglot.pincode = request.json.get("pincode")
        
        spots = parkinglot.spots
        availspots = Parking_spot.query.filter_by(lotid = id, status = 'A').all()
        availablespots = len(availspots)
    
        if (newspotcount > spotsoldcount):
            parkinglot.maxspots= newspotcount
            for _ in range(newspotcount - spotsoldcount):
                newspot = Parking_spot(lotid = parkinglot.id)
                db.session.add(newspot),201
            db.session.commit()
            cache.delete('admindash')
            return jsonify({"message" : "Edited successfully"})
               
                
        elif (spotsoldcount - newspotcount) <= availablespots:
            parkinglot.maxspots = newspotcount
            for i in range((spotsoldcount - newspotcount)):
                db.session.delete(availspots[i]), 201

            db.session.commit()
            cache.delete('admindash') 
            return jsonify({"message" : "Edited successfully"})
        elif (spotsoldcount - newspotcount) > availablespots:
            return jsonify({"error" :"cannot reduct spots as they are filled"})
            
        
        


#Delete Parkinglot
@app.route("/api/deleteParkinglot/<int:id>", methods=  ['DELETE'])
@role_req('admin')
def deleteparkinglot(id):
    parkinglot = Parking_lot.query.filter_by(id= id).first()
    spots = parkinglot.spots
    for spot in spots:
        if spot.status == 'O':
            return jsonify({"message": "Cannot delete parking lot as it is occupied"})
    
    db.session.delete(parkinglot)
    db.session.commit()
    cache.delete('admindash')
    return jsonify({ "message" :"parking lot deleted"})


#View parking spot
@app.route("/api/viewparkingspot/<int:id>")
@role_req('admin')
def viewparkingspot(id):
    parkingspot = Parking_spot.query.filter_by(id= id).first()
    parkinglot = Parking_lot.query.filter_by(id = parkingspot.lotid).first()
    
    spotdetails = {
        "id" : parkingspot.id,
        "status" : parkingspot.status,
        "primelocation" : parkinglot.primelocation
    }
    return jsonify(spotdetails), 200



#view spot
@app.route('/api/spotdetails/<int:id>', methods=  ["GET"])
@role_req('admin')
def detials(id):
    if (Parking_spot.query.filter_by(id = id).first()).status =='A':
         return jsonify({"message":"The spot  is UNocuppied"}), 404
    else:
        reserved = Reservations.query.filter_by(spot_id = id).first()
        lotid = (Parking_spot.query.filter_by(id = id).first()).lotid
        rate = (Parking_lot.query.filter_by(id = lotid).first()).priceperhour
        now = datetime.now()
        past = reserved. parking_timestamp
        totalhours = (now - past).total_seconds()/ (60*60)
        cost = rate * totalhours
        spot = {
            "spotid" : reserved.spot_id,
            "userid" : reserved.user_id,
            "viheclenumber": reserved.vichel_number,
            "date": reserved.parking_timestamp.isoformat(),
            "cost": cost
        }
        return jsonify(spot = spot), 200
        


    
#delete parkingspot
@app.route("/api/deleteParkingspot/<int:id>", methods=  ['DELETE'])
@role_req('admin')
def deleteparkingspot(id):
    parkingspot = Parking_spot.query.filter_by(id = id).first()
    parkinglot = Parking_lot.query.filter_by(id = parkingspot.lotid).first()
    if parkingspot.status == 'A' and parkingspot:
        parkinglot.maxspots = parkinglot.maxspots - 1
        db.session.delete(parkingspot)
        db.session.commit()
        return jsonify({"mess": "spot deleted successfully"})
    else:
        return jsonify({"message": "Spot is Occupied"}), 400



@app.route('/history/reservation/<int:id>', methods= ['GET'])
@role_req('user')
def reservations(id):
    reservations = Reservations.query.filter_by(user_id = id).all()    
    if len(reservations)==0:
        return jsonify({"message": "user haven't booked any spot"}), 400
    reserved = []
    for reserve in reservations:
        lotid  = (Parking_spot.query.filter_by(id = reserve.spot_id).first()).lotid 
        location  = (Parking_lot.query.filter_by(id  = lotid).first()).primelocation

        reserved.append(    
            {
            "id" : reserve.id,
            "spotid" : reserve.spot_id,
            "lotid" : lotid,
            "user_id": reserve.user_id,
            "parkingtimestamp": reserve.parking_timestamp,
            "leavingtimestamp": reserve.leaving_timestamp,
            "totalcost": reserve.leaving_cost,
            "vichelnumber": reserve.vichel_number,
            "location" : location
            
        })
    return jsonify(reservations = reserved), 200


@app.route('/book/reservation', methods= ['POST'])
@role_req('user')
def bookreservations():
    lotid = request.json.get('lotid')
    
    userid = current_user.id
    spotid = request.json.get('spotid')
    vehiclenumber = int(request.json.get('vehiclenumber'))

    parkingtimestamp = datetime.now()
    parkinglot =Parking_lot.query.filter_by(id= lotid).first()
    for spot in parkinglot.spots:
        if spot.status == 'A':
            spot.status = 'O'
            reservation = Reservations(user_id= userid, 
                               spot_id= spotid, 
                               vichel_number = vehiclenumber,
                               parking_timestamp= parkingtimestamp,
                               )
            db.session.add(reservation)
            db.session.commit()
            return jsonify({"message": "SPot booked Successfully"}), 201
    
    
    return jsonify({"message":"spot unavailable"}), 404
    
    

#search-lotdetials
@app.route('/api/alllotdetails')
@role_req('user')
def alllots():
    t  = request.args.get('term', '')
    parkinglots = Parking_lot.query.filter(Parking_lot.primelocation.ilike(f"%{t}%")|
                                         Parking_lot.pincode.ilike(f"%{t}%")).all()
    
    result = []
    for lot in parkinglots:
        aval = Parking_spot.query.filter_by(lotid =lot.id, status = 'A').count()

        result.append( {
            "id": lot.id,
            "address": lot.address,
            "availability":aval
        } )
    return jsonify(result = result), 200    



#alluser
@app.route('/api/allusers')
@role_req('admin')
def allusers():
    allusers = User.query.all()
    users = []
    for user in allusers:
        if user.role != 'admin':
            spotid = (Reservations.query.filter_by(user_id = user.id).first()).spot_id
            lotid = (Parking_spot.query.filter_by(id = spotid).first()).lotid
            location = (Parking_lot.query.filter_by(id = lotid).first()).primelocation 
            pincode = (Parking_lot.query.filter_by(id = lotid).first()).pincode
            users.append({
                "id" : user.id,
                "username" : user.username,
                "fullname" : user.name,
                "location" : location,
                "pincode" : pincode
            })
    
            return jsonify(users = users), 200



#search for admin
@app.route('/api/search/admin')
@role_req('admin')
def adminsearch():
    category = request.args.get('category','')
    t  = request.args.get('term', '')
    
    if category == 'location':
        parkinglots = Parking_lot.query.filter(Parking_lot.primelocation.ilike(f"%{t}%")).all()
        listparkinglots = []
        if parkinglots:
            for lot in parkinglots:
             occupied = Parking_spot.query.filter_by(lotid = lot.id).all()
             listparkinglots.append( {
                     "id": lot.id,
                     "primelocation": lot.primelocation,
                     "priceperhour": lot.priceperhour,
                     "address" : lot.address,
                     "pincode" : lot.pincode,
                     "maxspots" : lot.maxspots,
                     "Occupied" : len(occupied),
                     "spots":[{"id":s.id, "lotid":s.lotid, "status":s.status} for s in lot.spots]
                 })
            return jsonify(info = listparkinglots),200
        return jsonify({"message" : "NO PARKING LOT AVAILABLE"}), 404
    

    elif category == 'pincode':
        parkinglots = Parking_lot.query.filter(Parking_lot.pincode.ilike(f"%{t}%")).all()
        listparkinglots = []
        if parkinglots:
            for lot in parkinglots:
             occupied = Parking_spot.query.filter_by(lotid = lot.id, status ='O').all()
             listparkinglots.append( {
                     "id": lot.id,
                     "primelocation": lot.primelocation,
                     "priceperhour": lot.priceperhour,
                     "address" : lot.address,
                     "pincode" : lot.pincode,
                     "maxspots" : lot.maxspots,
                     "Occupied" : len(occupied),
                     "spots":[{"id":s.id, "lotid":s.lotid, "status":s.status} for s in lot.spots]
                 })
            return jsonify(info = listparkinglots),200
        return jsonify({"message" : "no parking lot available currenlty at this place"}), 404
    

    elif category == 'userid':
        t = int(t)
        user= User.query.filter_by(id =t).first()
        if user.role != 'admin':
            spotid = (Reservations.query.filter_by(user_id = user.id).first()).spot_id
            lotid = (Parking_spot.query.filter_by(id = spotid).first()).lotid
            location = (Parking_lot.query.filter_by(id = lotid).first()).primelocation 
            pincode = (Parking_lot.query.filter_by(id = lotid).first()).pincode
            user={
                "id" : user.id,
                "category" : user.role,
                "username" : user.username,
                "fullname" : user.name,
                "location" : location,
                "pincode" : pincode
            }
    
            return jsonify(info = user),200
        return jsonify(info = "No Users"),404


    elif category == 'username':
            user =  User.query.filter_by(username =t).first()
            
            if user.role != 'admin':
                spotid = (Reservations.query.filter_by(user_id = user.id).first()).spot_id
                lotid = (Parking_spot.query.filter_by(id = spotid).first()).lotid
                location = (Parking_lot.query.filter_by(id = lotid).first()).primelocation 
                pincode = (Parking_lot.query.filter_by(id = lotid).first()).pincode
                user={
                    "id" : user.id,
                    "category" : user.role,
                    "username" : user.username,
                    "fullname" : user.name,
                    "location" : location,
                    "pincode" : pincode
                }
        
                return jsonify(info = user), 200
            return jsonify(info = "No Users"), 404


@app.route('/api/lotdetails/<int:id>')
@role_req('user')
def getlotdetails(id):
    
    spot = Parking_spot.query.filter_by(lotid = id, status= 'A').first()
    parkinglot = Parking_lot.query.filter_by(id = spot.lotid).first()
    rate = parkinglot.priceperhour
   
    if not spot:
        return jsonify({"message": "No spots Available"}),404
  
    result = {
    "lotid": id,
    "spotid":spot.id,
    "rate": rate,
    "userid" : current_user.id
          }
    return jsonify(result = result), 200
    
    
#release    
@app.route('/release/<int:id>', methods= ['GET','POST'])
@role_req('user')
def release(id):
    reserve= Reservations.query.filter_by(id =id).first()
    if request.method == "GET":
         reserve= Reservations.query.filter_by(id =id).first()
         spotid=  reserve.spot_id
         lotid = (Parking_spot.query.filter_by(id = spotid).first()).lotid
         rate = (Parking_lot.query.filter_by(id = lotid).first()).priceperhour
         now = datetime.now()
         past = reserve.parking_timestamp
         totalhours = (now - past).total_seconds()/ (60*60)
         cost = rate * totalhours
    
         if not reserve:
             return jsonify({"err": "reservation not found"}), 404
         spotdetails ={
             "id" : reserve.id,
             "spotid" : reserve.spot_id,
             "viheclenumber": reserve.vichel_number,
             "parkingstamp" : reserve.parking_timestamp,
             "leavingstamp" : now,
             "rate": rate,
             "cost": cost
         }
         return jsonify(spotdetails = spotdetails), 200
    elif request.method == "POST":
        cost = request.json.get('cost',None)
        time = datetime.now()
        reserve.leaving_cost = cost
        reserve.leaving_timestamp = time
        (Parking_spot.query.filter_by(id = reserve.spot_id).first()).status = 'A'
        db.session.commit()
        return jsonify(message = "The SPOT is released"), 201


#revenue from each lot
@app.route('/revenue', methods= ['GET'])
@role_req('admin')
def revenue():
    revenue = {}
    reservations = Reservations.query.filter(Reservations.leaving_cost != None).all()
    for reserve in reservations:
        spotid = reserve.spot_id
        lotid = (Parking_spot.query.filter_by(id = spotid).first()).lotid
        
        if lotid not in revenue:
              
              revenue[lotid] = reserve.leaving_cost
        else:
            revenue[lotid] += reserve.leaving_cost


    return jsonify(revenue = revenue), 200           


@app.route('/status')
@role_req('admin')
def status():
    lots = Parking_lot.query.all()
    status = {}
    for lot in lots:
        occupied = Parking_spot.query.filter_by(lotid = lot.id, status = 'O').count()
        available = Parking_spot.query.filter_by(lotid = lot.id, status = 'A').count()
        if lot.id not in status:
            status[lot.id] = {
                "occupied" : occupied,
                "available": available
            }

    return jsonify(status = status), 200        


@app.route('/history/reservations/<int:id>', methods= ['GET'])
@role_req('user')
def history(id):
    reservations = Reservations.query.filter_by(user_id = id).all()    
    if len(reservations)==0:
        return jsonify({"message": "user haven't booked any spot"}), 400
    reserved = {}
    for reserve in reservations:
        lotid  = (Parking_spot.query.filter_by(id = reserve.spot_id).first()).lotid 
        location  = (Parking_lot.query.filter_by(id  = lotid).first()).primelocation
        if location not in reserved:
            reserved[location] = 1
        else:
            reserved[location] += 1

    return jsonify(reserved = reserved), 200            
        

@app.route('/export_csv')
def export():
    result = csv_report.delay()
    return{
        "id" : result.id,
        "result" : result.result
    }    


@app.route('/csvresult/<id>')
def csvresult(id):
    res = AsyncResult(id)
    # return {
    #     "filename" : res.result
    # }
    return send_from_directory('static', res.result)


# @app.route('/sendmail')
# def sendmail():
#     res = monthly_report.delay()
#     return {
#         "message" : res.result
#     }    