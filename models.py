from app import db 
import datetime 

class PIRsensor(db.Model): 
    __tablename__ = 'pir_sensor' #database table name, optionally specified 
    
    id = db.Column(db.Integer, primary_key=True) 
    desc = db.Column(db.String(120), unique=False, nullable=False) 
    meeting_room_id = db.Column(db.Integer, unique=False, nullable=False) 

    # one-to-many model

    records = db.relationship('Record', back_populates='sensor', cascade='all', lazy=True, uselist=True) 
    meeting_room = db.relationship('MeetingRoom', back_populates='sensors', cascade='all', lazy=True)


    def __init__(self, id, desc, meeting_room_id): 
        self.id = id 
        self.desc = desc 
        self.meeting_room_id = meeting_room_id
    
    def serialize(self): 
        return { 
            'id': self.id, 
            'desc': self.desc, 
            'meeting_room_id' : self.meeting_room_id, 
            'records': [r.serialize() for r in self.records] 
        }


class Record(db.Model): 
    __tablename__ = 'record' #database table name, optionally specified 
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer, nullable=False) 
    timestamp = db.Column(db.DateTime, unique=False, nullable=False) 
    sensor_id = db.Column(db.Integer, db.ForeignKey('pir_sensor.id'), unique=False, nullable=False, )
    
    # one-to-many model
    sensor = db.relationship('PIRSensor', back_populates='records')

    def __init__(self, value, timestamp, sensor_id): 
        self.value = value
        self.timestamp = timestamp
        self.sensor_id = sensor_id

    def serialize(self):
        return {
            'record_id': self.id,
            'value': self.value,
            'timestamp':self.timestamp,
            'sensor_id':self.sensor_id
        }

class MeetingRoom(db.Model): 
    __tablename__ = 'meeting_room' 
    id = db.Column(db.Integer, primary_key=True) 
    current_occupancy = db.Column(db.Integer, unique=False, nullable=True) 
    
    sensors = db.relationship('PIRsensor', back_populates='meeting_room', lazy=True, uselist=True)

    def __init__(self, id, sensors, current_occupancy=None): 
        self.id = id 
        self.sensors = [] if sensors is None else sensors 
        self.sensors = sensors

    def serialize(self):
        return {
            'meeting_room_id' : self.id,
            'current_occupancy' : self.current_occupnacy,
            'sensors' : self.sensors
        }