# 
from flask import Flask
from application.config import LoadDevelopmentConfig
from application.security import jwt
from application.models import User
from application.database import db
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache
from application.caching import cache
from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.tasks import monthly_report, generate_msg

def create_app():
    app = Flask(__name__)
    app.config.from_object(LoadDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    cache.init_app(app)
    # Import routes INSIDE the function to avoid circular imports
    with app.app_context():
        from application import routes
    
    return app

app = create_app()

celery = celery_init_app(app)
celery.autodiscover_tasks()
@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
     sender.add_periodic_task(
          crontab(minute='*/2'),
          monthly_report.s(),
     )

# @celery.on_after_finalize.connect
# def setup_periodic_task(sender, **kwargs):
#      sender.add_periodic_task(
#           crontab(minute='*/2'),
#           generate_msg.s(),
#      )     

if __name__ == "__main__":
    
    
    # Perform setup tasks within the application context
    with app.app_context():
        db.create_all()
        if User.query.filter_by(role = 'admin').first():
                app.run(debug=True)

        else:        
             db.session.add(User( username= "mathurkshitij@3776", password = generate_password_hash("kshitij2001"), role = "admin", name = "kshitij"))
             db.session.add(User( username= "kshitij@3776", password = generate_password_hash("kshitij2001"), name = "mathur"))
             db.session.commit()
             app.run(debug=True)
        
        
        # Uncomment and modify as needed for initial data
        # if not User.query.filter_by(role='admin').first():
        #     admin_user = User(
        #         username="admin@example.com", 
        #         password="admin123",  # In production, hash this!
        #         role="admin"
        #     )
        #     db.session.add(admin_user)
        #     db.session.commit()
            
