from flask import Flask
from flask_restful import Api, Resource, reqparse
import hashlib

app = Flask(__name__)
api = Api(app)


class CreatePassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=str, required=True, help='Phone number is required')
        parser.add_argument('password_hash', type=str, required=True, help='Password hash is required')
        args = parser.parse_args()
        
        phone_number = args.phone_number
        password_hash = args.password_hash

        salt = 'my_secret_salt'  
        # Combine password with salt
        combined_string = f'{password_hash}{salt}'.encode('utf-8')
        # Hash the combined string with SHA-256 algorithm
        hashed_string = hashlib.sha256(combined_string).hexdigest()
        
        return {"phone_number": phone_number}

api.add_resource(CreatePassword, '/create_password')


class VerifyPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_or_email', type=str, required=True, help='Phone number or email is required')
        parser.add_argument('password_hash', type=str, required=True, help='Password hash is required')
        args = parser.parse_args()

        phone_or_email = args.phone_or_email
        password_hash = args.password_hash

        # check if phone_or_email exists in users
        if phone_or_email in users:
            user = users[phone_or_email]
           
            combined_string = f'{password_hash}my_secret_salt'.encode('utf-8')
            hashed_string = hashlib.sha256(combined_string).hexdigest()
            
            # check if password hash matches
            if hashed_string == user['password_hash']:
                return {"status": "success"}
            else:
                return {"status": "failure", "message": "Password does not match"}
        else:
            return {"status": "failure", "message": "User does not exist"}

api.add_resource(VerifyPassword, '/verify_password')



if __name__ == '__main__':
    app.run()
