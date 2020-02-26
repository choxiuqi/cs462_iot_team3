from app import db 
import datetime 

class Sensor(db.Model): 
    __tablename__ = 'pir_sensor' #database table name, optionally specified 
    
    id = db.Column(db.Integer, primary_key=True) 
    desc = db.Column(db.String(80), unique=False, nullable=False)
    type = db.Column(db.String(10), unique=False, nullable=False)   
    meeting_room_id = db.Column(db.Integer, db.ForeignKey('meeting_room.id'), unique=False, nullable=False) 

    # one-to-many model

    meeting_room = db.relationship('MeetingRoom', back_populates='sensors')
    records = db.relationship('Record', back_populates='sensor', cascade='all', lazy=True, uselist=True) 


    def __init__(self, id, desc, meeting_room_id, records=None): 
        self.id = id 
        self.desc = desc 
        self.meeting_room_id = meeting_room_id
        records = [] if records is None else records
        self.records = records

    
    def serialize(self): 
        return { 
            'id': self.id, 
            'desc': self.desc, 
            'meeting_room_id': self.meeting_room_id, 
            'records': [r.serialize() for r in self.records] 
        }

class MeetingRoom(db.Model): 
    __tablename__ = 'meeting_room' 
    id = db.Column(db.Integer, primary_key=True) 
    current_occupancy = db.Column(db.Integer, unique=False, nullable=True) 
    
    # one-to-many relationship
    sensors = db.relationship('Sensor', back_populates='meeting_room', lazy=True, uselist=True)

    def __init__(self, id, sensors=None, current_occupancy=None): 
        self.id = id 
        sensors = [] if sensors is None else sensors
        self.sensors = sensors
        self.current_occupancy = current_occupancy

    def serialize(self):
        return {
            'meeting_room_id' : self.id,
            'current_occupancy' : self.current_occupancy,
            'sensors' : [s.serialize() for s in self.sensors]
        }

class Record(db.Model): 
    __tablename__ = 'record' #database table name, optionally specified 
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer, nullable=False) 
    timestamp = db.Column(db.DateTime, unique=False, nullable=False) 
    sensor_id = db.Column(db.Integer, db.ForeignKey('pir_sensor.id'), unique=False, nullable=False)
    
    # one-to-many model
    sensor = db.relationship('Sensor', back_populates='records', cascade='all', lazy=True)

    def __init__(self, value, timestamp, sensor_id): 
        self.value = value
        self.timestamp = timestamp
        self.sensor_id = sensor_id

        # self.sensor = None

    def serialize(self):
        return {
            'record_id': self.id,
            'value': self.value,
            'timestamp':self.timestamp,
            'sensor_id':self.sensor_id
        }