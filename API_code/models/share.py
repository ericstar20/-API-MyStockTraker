# Create a internal respresentation for item
from db import db
from sqlalchemy import func

class ShareModel(db.Model):

    # SQLAlchemy
    __tablename__ = 'shares'
    # Shares' Columns info
    trans_id       = db.Column(db.Integer, primary_key = True)
    trans_symbol   = db.Column(db.String(5), primary_key = True)
    trans_datetime = db.Column(db.String(20))
    trans_volumns  = db.Column(db.Integer)
    trans_price    = db.Column(db.Float(precision=5))

    def __init__(self, trans_id, trans_datetime, trans_symbol, trans_volumns, trans_price):
        self.trans_id       = trans_id
        self.trans_datetime = trans_datetime
        self.trans_symbol   = trans_symbol
        self.trans_volumns  = trans_volumns
        self.trans_price    = trans_price

    def json(self):
        return {
                'Transactioin ID'      : self.trans_id,
                'Transactioin DateTime': self.trans_datetime,
                'Transactioin Symbol'  : self.trans_symbol,
                'Transactioin Volumns' : self.trans_volumns,
                'Transactioin Price'   : self.trans_price
                }

    @classmethod
    def find_by_symbol_id(cls, trans_id, trans_symbol):
        return cls.query.filter_by(trans_symbol = trans_symbol,
                                   trans_id = trans_id).first()
        # Equal to -> SELECT * FROM shares WHERE trans_symbol = trans_symbol and trans_id = trans_id
        # Also return as ShareModel object

    @classmethod
    def find_by_symbol(cls, trans_symbol):
        return cls.query.filter_by(trans_symbol = trans_symbol).all()
        # Equal to -> SELECT * FROM shares WHERE trans_symbol = trans_symbol
        # Also return as ShareModel object

    def id_generate():
        # return cls.query.count()
        return db.session.query(db.func.max(ShareModel.trans_id)).scalar()

    def save_to_db(self):
        db.session.add(self) # session allow multiple insert
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
