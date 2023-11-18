import datetime
import peewee as pw
from bcrypt import checkpw, hashpw, gensalt
from playhouse.flask_utils import FlaskDB
from playhouse.shortcuts import model_to_dict
from flask_login import UserMixin


db_wrapper = FlaskDB()

class BaseModel(db_wrapper.Model):
    pass
        

class User(UserMixin, BaseModel):
    '''User Authentication'''
    username = pw.CharField(unique=True)
    password = pw.TextField()
    is_active = pw.BooleanField(default=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)

    def check_password(self, password):
        return checkpw(password.encode(), self.password.encode())
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt())
    
    
class Pos(BaseModel):
    '''Pos Pengamatan'''
    nama = pw.CharField(max_length=50)
    kab = pw.CharField(max_length=50, null=True)
    lonlat = pw.CharField(max_length=50, null=True)
    dpl = pw.IntegerField(default=0)
    sh = pw.FloatField(null=True)
    sk = pw.FloatField(null=True)
    sm = pw.FloatField(null=True)
    min_wlevel = pw.FloatField(default=0) # nilai minimum wlevel (cm)
    max_wlevel = pw.FloatField(default=1000) # dalam centimeter
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    
    def get_ch(self, tgl=datetime.datetime.now()):
        return tgl
    
    def get_tma(self, tgl=datetime.datetime.now()):
        return tgl
    
class Logger(BaseModel):
    sn = pw.CharField(max_length=12, unique=True)
    pos = pw.ForeignKeyField(Pos, null=True)
    tinggi_sonar = pw.IntegerField(default=1000)
    tipping_factor = pw.FloatField(default=0.2)
    latest_battery = pw.FloatField(null=True)
    latest_sampling = pw.DateTimeField(null=True)
    latest_up = pw.DateTimeField(null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    
    
class Hourly(BaseModel):
    pos = pw.ForeignKeyField(Pos, index=True)
    logger = pw.ForeignKeyField(Logger, index=True)
    sampling = pw.DateTimeField()
    num_data = pw.IntegerField(default=0)
    rain = pw.FloatField(null=True)
    tick = pw.IntegerField(null=True)
    wlevel = pw.FloatField(null=True)
    distance = pw.IntegerField(null=True)
    num_alarm = pw.IntegerField(null=True)
    
    class Meta:
        indexes = (
            (('pos', 'logger', 'sampling'), True),
        )
    
class AlertLog(BaseModel):
    pos = pw.ForeignKeyField(Pos, backref='alerts', index=True)
    sampling = pw.DateTimeField()
    content = pw.TextField(null=True)
    
    class Meta:
        indexes = (
            (('pos', 'sampling'), True),
        )
    

class Note(BaseModel):
    obj = pw.CharField(max_length=50, index=True)
    waktu = pw.DateTimeField(default=datetime.datetime.now())
    username = pw.CharField()
    body = pw.TextField()
    

class Raw(BaseModel):
    content = pw.TextField()
    received = pw.DateTimeField(default=datetime.datetime.now())
    sn = pw.CharField(max_length=10, null=True)