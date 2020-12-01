from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.share import ShareModel
from datetime import datetime
import requests
from json import dumps

twelvedata_key = 'API KEY'

class Share(Resource):

    # Input format control
    parser = reqparse.RequestParser()
    parser.add_argument('Volumns',
        type = int,
        required = True,
        help = 'Every share needs a volumn!'
    )

    #@jwt_required()
    def get(self, symbol):
        share = ShareModel.find_by_symbol(symbol)
        if share:
            # return share.json()
            return {'Shares': [x.json() for x in share]}
        return {'message': 'The Symbol not found.'}, 404

    #@jwt_required()
    def post(self, symbol):

        # Generate purchase_time
        purchase_time = datetime.now().strftime("%m/%d/%Y_%H:%M:%S") # format: '11/26/2020, 19:08:35'

        # Generate units
        data = Share.parser.parse_args()

        # Get a real-time price
        price_url = "https://api.twelvedata.com/price?symbol={0}&apikey={1}".format(symbol, twelvedata_key)
        real_time_price = requests.get(price_url).json()['price']

        #  Generate a Incremental ID
        id_num = ShareModel.id_generate() +  1

        share = ShareModel(id_num, purchase_time, symbol, data['Volumns'], real_time_price)

        try:
            share.save_to_db()
        except:
            return {"message": "An error occurred inserting the share. (time: {0}, symbol: {1}, units: {2}, price: {3} .".format(share.trans_datetime, share.trans_symbol, share.trans_volumns, share.trans_price)}, 500 # internal server error

        return share.json(), 201 # 201: return a value

class ShareModify(Resource):
    #@jwt_required()
    def delete(self, symbol, id):
        share = ShareModel.find_by_symbol_id(id, symbol)
        if share:
            share.delete_from_db()

        return {'message': '{0}, {1} :share deleted'.format(id, symbol)}

    #@jwt_required()
    def put(self, symbol, id): # both create or update the item

        data = Share.parser.parse_args()
        share = ShareModel.find_by_symbol_id(id, symbol)

        share.trans_volumns = data['Volumns']
        share.save_to_db()

        return share.json()


class ShareList(Resource):
    def get(self):
        return {'Shares': [share.json() for share in ShareModel.query.all()]}
