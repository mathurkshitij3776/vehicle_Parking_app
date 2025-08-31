from flask_jwt_extended import JWTManager

from application.models import User

jwt = JWTManager()


@jwt.user_identity_loader                
def load(user):                          
    return user.username                  

@jwt.user_lookup_loader                 
def lookup_user(_jwt_header, jwt_data): 
    identity = jwt_data["sub"]               
    return (                             
        User.query.filter_by(username=identity).one_or_none()                
    )
