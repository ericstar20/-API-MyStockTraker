#------------------------------------------------------------------------------------------------------------------------#
# Connect to venv:
# 1. pip freeze: observe how many libraries you install
# 2. virtualenv venv --python=python3 (or any version you want to execute in the virtual env): create virtual enviroment
# 3. source venv/bin/activate : activate the virtual env
# 4. deactivate : exit the virtual env
# http://127.0.0.1:5000
#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#
# Section 5 note:
# 1. Run the app.py on the section 5 folder level.
#    This is because we need to use db data and db is on the section 5 folder.
#    cmd: python code/app.py
#    pwd: Users/shih-tien/SW_PRO/Personal Projects/API/section_5
#------------------------------------------------------------------------------------------------------------------------#
import os

from flask import Flask
from flask_restful import Api  # we are no longer need jsonify because flask_restful did for us
from flask_jwt import JWT

from security import authenticate, identity
from resources.share import Share, ShareList, ShareModify
from resources.user import UserRegister
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///user.db') # sqlite can be replace by mysql, postgresql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'eric' # In the real life, this key should be hide, complex.
api = Api(app)

# SQLAlchemy can create db automatically without using create_table.py
@app.before_first_request
def create_table():
    db.create_all()

# authenticate part
jwt = JWT(app, authenticate, identity) # create a new path /auth

api.add_resource(Share, '/shares/<string:symbol>')
api.add_resource(ShareModify, '/shares/<string:symbol>/<int:id>')
api.add_resource(ShareList, '/shares')
api.add_resource(UserRegister, '/register') # allow new user sign in


if __name__ == '__main__':
# avoid execute by import to other .py file
# __main__ means code is implement directly at app.py
    db.init_app(app)
    app.run(port=5000, debug=True)
