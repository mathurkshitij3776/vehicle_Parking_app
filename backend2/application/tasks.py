import csv
from celery import shared_task
from .models import *
from jinja2 import Template
from .mail import send_email
from datetime import date, timedelta, datetime
import requests
from collections import defaultdict
from flask import render_template


@shared_task(ignore_results = False, name = "download_csv_report")
def csv_report():
    history = Reservations.query.all() # card details
    csv_file_name = f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:
        sr_no = 1
        card_csv = csv.writer(csvfile, delimiter = ',')
        card_csv.writerow(['Sr No.', 'spotid', 'user_id', 'parking_time', 'leaving_time', 'Revenue'])
        totalrevenue = 0
        for c in history:
            cost = c.leaving_cost
            if cost is not None:
                totalrevenue += cost  # Add to total only once, and only if not None
                cost_display = cost
            elif cost is None:
                cost_display = "Currently Occupied"  
            this_card = [sr_no, c.spot_id, c.user_id, c.parking_timestamp, c.leaving_timestamp, cost_display]    
            card_csv.writerow(this_card)
           
            sr_no += 1
    return csv_file_name
# @shared_task(ignore_results=False, name="download_csv_report")
# def csv_report():
#     try:
#         history = Reservations.query.all()
#         csv_file_name = f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
#         with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
#             sr_no = 1
#             card_csv = csv.writer(csvfile, delimiter=',')
#             card_csv.writerow(['Sr No.', 'Spot ID', 'User ID', 'Parking Time', 'Leaving Time', 'Revenue'])
            
#             totalrevenue = 0  # Initialize as integer to match your DB field type
            
#             for c in history:
#                 # Safe handling with explicit None checks
#                 leaving_cost_value = getattr(c, 'leaving_cost', None)
                
#                 if leaving_cost_value is not None:
#                     # Convert to int to match your DB field type, handle any conversion errors
#                     try:
#                         cost_value = int(leaving_cost_value)
#                         totalrevenue += cost_value
#                         cost_display = f"₹{cost_value}"
#                     except (ValueError, TypeError):
#                         cost_display = "Error in cost"
#                 else:
#                     cost_display = "Currently Occupied"
                
#                 # Safe handling of other fields
#                 spot_id = getattr(c, 'spot_id', 'N/A')
#                 user_id = getattr(c, 'user_id', 'N/A')
                
#                 # Handle datetime fields safely
#                 parking_time = c.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if c.parking_timestamp else 'N/A'
#                 leaving_time = c.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if c.leaving_timestamp else 'N/A'
                
#                 this_card = [sr_no, spot_id, user_id, parking_time, leaving_time, cost_display]
#                 card_csv.writerow(this_card)
#                 sr_no += 1
            
#             # Add summary row
#             card_csv.writerow(['', '', '', '', 'Total Revenue:', f'₹{totalrevenue}'])
#             print(f"CSV exported successfully: {csv_file_name}")
        
#         return csv_file_name
        
#     except Exception as e:
#         print(f"Error in csv_report: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise

# def csv_report():
#     history = Reservations.query.all()
#     csv_file_name = f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
#     with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
#         sr_no = 1
#         card_csv = csv.writer(csvfile, delimiter=',')
#         card_csv.writerow(['Sr No.', 'Spot ID', 'User ID', 'Parking Time', 'Leaving Time', 'Revenue'])
        
#         totalrevenue = 0
        
#         for c in history:
#             cost = c.leaving_cost
#             if cost is not None:
#                 totalrevenue += cost  # Add to total only once
#                 cost_display = cost
#             else:
#                 cost_display = "Currently Occupied"
            
#             this_card = [sr_no, c.spot_id, c.user_id, c.parking_timestamp, c.leaving_timestamp, cost_display]
#             card_csv.writerow(this_card)
#             # REMOVED: totalrevenue += c.leaving_cost  <- This line was the problem
#             sr_no += 1
        
#         # Add total row at the end
# #         card_csv.writerow(['', '', '', '', 'Total Revenue:', f'₹{totalrevenue}'])
    
#     return csv_file_name



# @shared_task(ignore_results = False, name = "monthly_report")
# def monthly_report():
#     users = User.query.all()
#     for user in users[1:]:
#         user_data = {}
#         user_data['name'] = user.name
#         user_data['username'] = user.username
#         user_data['lotid'] = {} 
#         details = []
#         Totalcost = 0
#         mostusedlot = 0
#         reservations = Reservations.query.filter_by(user_id = user.id) # Note: image shows "sta" being typed
#         for info in reservations:
#             info_dict = {}
#             lotid = (Parking_spot.query.filter_by(id = info.spot_id).first()).lotid
#             if lotid not in user_data['lotid']:
#                     user_data['lotid'][lotid] = 1 
#             else:
#                 user_data['lotid'][lotid] += 1  
#             info_dict['lotid'] = user_data['lotid'][lotid]
#             primelocation = (Parking_lot.query.filter_by(id = lotid).first()).primelocation
            
#             info_dict["location"] = primelocation
#             info_dict["parkingleavingtime"] = info.parking_timestamp
#             info_dict["leavingtime"] = info.leaving_timestamp
#             info_dict["vichel_number"] = info.vichel_number
#             raw = info.leaving_cost
#             cost = raw if (raw is not None and raw > 0) else 0.0
#             Totalcost += cost
            
#             if raw is not None and raw > 0:
#                 info_dict['leaving_cost'] = f"₹{raw}"
#             else:
#                 info_dict['leaving_cost'] = "Currently Occupied"

#             details.append(info_dict)
#         for lotd in details:
#              if mostusedlot < lotd['lotid']:
#                 mostusedlot = lotid
        
#         user_data['mostusedlot'] = mostusedlot
#         user_data['Totalcost'] = Totalcost    
#         user_data['details'] = details
#         mail_template = """
# <h3>Dear {{user_data.name}}</h3>
# <p>Please find the current status of your cards in the table below.</p>

# <p>Visit our ecard app at http://127.0.0.1:5173 for details.</p>

# <p>Most used parking lot: {{user_data.mostusedlot}} </p>
# <table>
#   <tr>
#     <th>Card Name</th>
#     <th>Status</th>
#   </tr>
#   {% for detail in user_data.details %}
#   <tr>
#     <td>{{detail.location}}</td>
#     <td>{{detail.parkingleavingtime}}</td>
#     <td>{{detail.leavingtime}}</td>
#     <td>{{detail.vichel_number}}</td>
#     <td>{{detail.leaving_cost}}</td>
#   </tr>
#   {% endfor %}
  
# </table>
# <p>Total cost of parking lot: {{user_data.Totalcost}} </p>
# <h5>Regards<br>
# E card V2<br>
# <h5>IITM BS Degree</h5>
# """
#         message = Template(mail_template).render(user_data = user_data)
#         send_email(user.email, subject = "Monthly reservation detail Report", message=message) 
#     return "Monthly reports sent"
# @shared_task(bind=True, ignore_results=False, name="monthly_report")
# def monthly_report(self):
#     """
#     Task: Send each user their parking activity report for the past month.
#     Guards against None costs and counts lot usage safely.
#     Retries once after 60s on any error.
#     """
#     today = date.today()
#     first_of_month = today.replace(day=1)
#     last_month_end = first_of_month - timedelta(days=1)
#     last_month_start = last_month_end.replace(day=1)
#     month_name = last_month_start.strftime('%B %Y')
#     # 2. Iterate users
#     for user in User.query.all():
#             # 3. Fetch user reservations in window
#             res_list = Reservations.query.filter(
#                 Reservations.user_id == user.id,
#                 Reservations.parking_timestamp.between(last_month_start, last_month_end)
#             ).all()
#             if not res_list:
#                 continue  # no activity last month

#             # 4. Summarize usage and cost
#             lot_count = defaultdict(int)
#             total_cost = 0.0
#             details = []

#             for r in res_list:
#                 # Count lot usage
#                 spot = Parking_spot.query.get(r.spot_id)
#                 lot_id = spot.lotid
#                 lot_count[lot_id] += 1
#                 location = Parking_lot.query.get(lot_id).primelocation

#                 # Safe cost handling
#                 raw_cost = r.leaving_cost
#                 cost = raw_cost if raw_cost is not None else 0.0
#                 total_cost += cost
#                 cost_display = f"₹{raw_cost}" if raw_cost is not None else "Currently Occupied"

#                 # Detail entry
#                 details.append({
#                     'location': location,
#                     'entry': r.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.parking_timestamp else 'N/A',
#                     'exit': r.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.leaving_timestamp else 'N/A',
#                     'vehicle': r.vichel_number or 'N/A',
#                     'cost': cost_display
#                 })

#             # 5. Determine most used lot
#             most_used_lot = max(lot_count, key=lot_count.get)

#             # 6. Render email
#             html = render_template(
#                 'monthly_report.html',
#                 name=user.name,
#                 month=month_name,
#                 total_cost=f"₹{total_cost:.2f}",
#                 most_used_lot=most_used_lot,
#                 details=details
#             )

#             # 7. Send email
#             send_email(
#                 to=user.email,
#                 subject=f"{month_name} Parking Activity Report",
#                 message=html,
#                 html=True
#             )

#     return "Monthly reports sent"

@shared_task(ignore_results = False, name = "monthly_report")
def monthly_report():
    users = User.query.all()
    for user in users[1:]:
        user_data = {}
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['lotid'] = {} 
        details = []
        Totalcost = 0 
        mostusedlot = 0
        reservations = Reservations.query.filter_by(user_id = user.id)
        for info in reservations:
            info_dict = {}
            lotid = (Parking_spot.query.filter_by(id = info.spot_id).first()).lotid
            if lotid not in user_data['lotid']:
                user_data['lotid'][lotid] = 1 
            else:
                user_data['lotid'][lotid] += 1  
            info_dict['lotid'] = user_data['lotid'][lotid]
            primelocation = (Parking_lot.query.filter_by(id = lotid).first()).primelocation
            
            info_dict["location"] = primelocation
            info_dict["parkingleavingtime"] = info.parking_timestamp
            info_dict["leavingtime"] = info.leaving_timestamp
            info_dict["vichel_number"] = info.vichel_number
            
            raw = info.leaving_cost
            if raw is not None and raw > 0:
                cost = int(raw) 
                info_dict['leaving_cost'] = f"₹{cost}"
                Totalcost += cost  
            else:
                cost = 0  
                info_dict['leaving_cost'] = "Currently Occupied"
               
            
            details.append(info_dict)
            
        # Find most used lot
        if details:  # Only if there are details
            for lotd in details:
                if mostusedlot < lotd['lotid']:
                    mostusedlot = lotd['lotid']
        
        user_data['mostusedlot'] = mostusedlot
        user_data['Totalcost'] = f"₹{Totalcost}"
        user_data['details'] = details
        
        mail_template = """
<h3>Dear {{user_data.name}}</h3>
<p>Please find the current status of your parking reservations in the table below.</p>

<p>Visit our ecard app at http://127.0.0.1:5173 for details.</p>

<p>Most used parking lot: {{user_data.mostusedlot}} </p>
<table border="1" style="border-collapse: collapse;">
  <tr>
    <th>Location</th>
    <th>Parking Time</th>
    <th>Leaving Time</th>
    <th>Vehicle Number</th>
    <th>Cost</th>
  </tr>
  {% for detail in user_data.details %}
  <tr>
    <td>{{detail.location}}</td>
    <td>{{detail.parkingleavingtime}}</td>
    <td>{{detail.leavingtime}}</td>
    <td>{{detail.vichel_number}}</td>
    <td>{{detail.leaving_cost}}</td>
  </tr>
  {% endfor %}
</table>
<p><strong>Total cost of parking: {{user_data.Totalcost}}</strong></p>
<h5>Regards<br>
E card V2<br>
IITM BS Degree</h5>
"""
        message = Template(mail_template).render(user_data = user_data)
        send_email(user.username, subject = "Monthly reservation detail Report", message=message) 
    return "Monthly reports sent"

@shared_task(ignore_results = False, name = "generate_msg")
def generate_msg():
    # today = date.today()
    # yesterday= today - timedelta(days=1)
    # r = Reservations.query.filter(
    #            Reservations.user_id == id, Reservations.parking_timestamp >= yesterday).first()
    # if not r:    
    #    name = (User.query.filter_by(id = id).first()).name
    #    text = f"Hi {name}, your You haven't booked parking since yesterday."
      
    #    response = requests.post("https://chat.googleapis.com/v1/spaces/AAQAfuXGDbE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_5FOszFyClOFsJWjXVl72Iri_4Wly5nfvKPTo6InC9g", json = {"text": text})
    #    print(response.status_code)
    #    return "The delivery is sent to user"

    text = f"Hi New Parking lot has been added."
    response = requests.post("https://chat.googleapis.com/v1/spaces/AAQAfuXGDbE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_5FOszFyClOFsJWjXVl72Iri_4Wly5nfvKPTo6InC9g", json = {"text": text})
    print(response.status_code)
    return "The delivery is sent to user"
