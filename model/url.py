import datetime
import qrcode
from io import BytesIO
from db import db
from random import choice
import string
from datetime import datetime
from urllib.parse import urlsplit
from flask import request


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer(), primary_key=True)
    org_url = db.Column(db.Text, nullable=False)
    short_id = db.Column(db.String(6), unique=False)
    qr_code = db.Column(db.LargeBinary)
    clicks = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    # user = db.relationship('User', back_populates='urls', lazy=True )
    created = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_id = self.gen_short_id()
        self.qr_code = self.generateqr()
    

    def __repr__(self):
        return f'<Url {self.short_id}>'
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def gen_short_id(self):
            chars = string.ascii_letters + string.digits
            length = 6
            short_id = ''.join(choice(chars) for x in range(length))
            # exist_url= self.query.filter_by(short_id=short_id).first()
            # if exist_url:
            #     return self.gen_short_id() #recursion 
            return short_id

    def generateqr(self):
        buffer = BytesIO()
        qr = qrcode.QRCode(
            version=None,
            box_size=5,
            border=2)
        qr.add_data(f'{request.host_url}{self.short_id}')  #- comment this when running a unit test 
        # qr.add_data(self.short_id) #- uncomment this when running a unit test 
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(buffer, 'JPEG', quality=70)
        buffer.seek(0)
        qr_code = buffer.getvalue()
        print(self,'im printing')
        return qr_code
        
        

#    Validating Url
def is_valid_url(url):
    split_url = urlsplit(url)
    return bool(split_url.scheme and split_url.netloc)




