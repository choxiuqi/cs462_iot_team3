from app import db 
import datetime 

class Sensor(db.Model): 
    __tablename__ = 'sensor' #database table name, optionally specified 
    
    id = db.Column(db.String(80), primary_key=True) 
    desc = db.Column(db.String(80), unique=False, nullable=False)
    type = db.Column(db.String(10), unique=False, nullable=False)   
    meeting_room_id = db.Column(db.String(10), db.ForeignKey('meeting_room.id'), unique=False, nullable=False) 

    # one-to-many model

    meeting_room = db.relationship('MeetingRoom', back_populates='sensors')
    uss_records = db.relationship('USSRecord', back_populates='sensor', cascade='all', lazy=True, uselist=True)
    latest_uss_records = db.relationship('LatestUSSRecord', back_populates='sensor', cascade='all', lazy=True, uselist=True)
    sensor_health =  db.relationship('SensorHealth', back_populates='sensor', cascade='all', lazy=True, uselist=True)
    pir_records = db.relationship('PIRRecord', back_populates='sensor', cascade='all', lazy=True, uselist=True)
    pir_records_debug = db.relationship('PIRRecordDebug', back_populates='sensor', cascade='all', lazy=True, uselist=True)



    def __init__(self, id, desc, meeting_room_id, uss_records=None, latest_uss_records=None, sensor_health=None, pir_records=None): 
        self.id = id 
        self.desc = desc 
        self.meeting_room_id = meeting_room_id
        uss_records = [] if uss_records is None else uss_records
        self.uss_records = uss_records
        latest_uss_records = [] if latest_uss_records is None else latest_uss_records
        self.latest_uss_records = latest_uss_records
        sensor_health = [] if sensor_health is None else sensor_health
        self.sensor_health = sensor_health
        pir_records = [] if pir_records is None else pir_records
        self.pir_records = pir_records

    
    def serialize(self): 
        return { 
            'id': self.id, 
            'desc': self.desc, 
            'meeting_room_id': self.meeting_room_id, 
            'uss_records': [r.serialize() for r in self.uss_records],
            'sensor_health': [s.serialize() for s in self.sensor_health],
            'pir_records': [p.serialize() for p in self.pir_records] 
        }

    def health(self):
        return {
            'id': self.id,
            'desc': self.desc,
            'meeting_room_id': self.meeting_room_id,
            'sensor_health': [s.serialize() for s in self.sensor_health],
            'pir_records': [p.health() for p in self.pir_records]
        }

class MeetingRoom(db.Model): 
    __tablename__ = 'meeting_room' 
    id = db.Column(db.String(10), primary_key=True) 
    capacity = db.Column(db.Integer, unique=False, nullable=True)

    # one-to-many relationship
    sensors = db.relationship('Sensor', back_populates='meeting_room', lazy=True, uselist=True)
    occupancy_records = db.relationship('Occupancy', back_populates='meeting_room', lazy=True, uselist=True)
    occupancy_records_debug = db.relationship('OccupancyDebug', back_populates='meeting_room', lazy=True, uselist=True)

    def __init__(self, id, capacity, sensors=None, occupancy_records=None): 
        self.id = id 
        self.capacity = capacity
        sensors = [] if sensors is None else sensors
        self.sensors = sensors
        occupancy_records = [] if occupancy_records is None else occupancy_records
        self.occupancy_records = occupancy_records

    def serialize(self):
        return {
            'meeting_room_id' : self.id,
            'capacity' : self.capacity,
            'sensors' : [s.serialize() for s in self.sensors],
            'occupancy_records' : [o.serialize() for o in self.occupancy_records]
        }

class USSRecord(db.Model): 
    __tablename__ = 'uss_record' #database table name, optionally specified 
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer, nullable=False) 
    timestamp = db.Column(db.DateTime, unique=False, nullable=False) 
    sensor_id = db.Column(db.String(80), db.ForeignKey('sensor.id'), unique=False, nullable=False)
    
    # one-to-many model
    sensor = db.relationship('Sensor', back_populates='uss_records', cascade='all', lazy=True)

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

class LatestUSSRecord(db.Model): 
    __tablename__ = 'latest_uss_record' #database table name, optionally specified 
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer, nullable=False) 
    timestamp = db.Column(db.DateTime, unique=False, nullable=False) 
    sensor_id = db.Column(db.String(80), db.ForeignKey('sensor.id'), unique=False, nullable=False)
    
    # one-to-many model
    sensor = db.relationship('Sensor', back_populates='latest_uss_records', cascade='all', lazy=True)

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

class Occupancy(db.Model): 
    __tablename__ = 'occupancy' 
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False) 
    meeting_room_id = db.Column(db.String(10), db.ForeignKey('meeting_room.id'), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=True)
    remarks = db.Column(db.String(120), unique=False, nullable=True)

    # one-to-many relationship
    meeting_room = db.relationship('MeetingRoom', back_populates='occupancy_records')

    def __init__(self, timestamp, meeting_room_id, value, remarks=None): 
        self.timestamp = timestamp
        self.meeting_room_id = meeting_room_id
        self.value = value
        self.remarks = remarks

    def serialize(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'meeting_room_id': self.meeting_room_id,
            'value' : self.value
        }

class OccupancyDebug(db.Model): 
    __tablename__ = 'occupancy_debug' 
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False) 
    meeting_room_id = db.Column(db.String(10), db.ForeignKey('meeting_room.id'), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=True)
    remarks = db.Column(db.String(120), unique=False, nullable=True)

    # one-to-many relationship
    meeting_room = db.relationship('MeetingRoom', back_populates='occupancy_records_debug')

    def __init__(self, timestamp, meeting_room_id, value, remarks=None): 
        self.timestamp = timestamp
        self.meeting_room_id = meeting_room_id
        self.value = value
        self.remarks = remarks

    def serialize(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'meeting_room_id': self.meeting_room_id,
            'value' : self.value
        }


class SensorHealth(db.Model): 
    __tablename__ = 'sensor_health' 
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(80), db.ForeignKey('sensor.id'), unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=True)
    timestamp = db.Column(db.DateTime, unique=False) 
    temperature = db.Column(db.Float, unique = False, nullable = True)

    # one-to-many relationship
    sensor = db.relationship('Sensor', back_populates='sensor_health')

    def __init__(self, timestamp, sensor_id, value, temperature=None): 
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.value = value
        self.temperature = temperature

    def serialize(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'sensor_id': self.sensor_id,
            'value' : self.value,
            'temperature': self.temperature
        }


class PIRRecord(db.Model): 
    __tablename__ = 'pir_record' 
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False) 
    sensor_id = db.Column(db.String(80), db.ForeignKey('sensor.id'), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=True)
    temperature = db.Column(db.Float, unique = False, nullable = True)

    # one-to-many relationship
    sensor = db.relationship('Sensor', back_populates='pir_records')

    def __init__(self, timestamp, sensor_id, value, temperature=None): 
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.value = value
        self.temperature = temperature

    def serialize(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'sensor_id': self.sensor_id,
            'value' : self.value
        }
    
    def health(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'sensor_id' : self.sensor_id,
            'temperature' : self.temperature,
            'value' : self.value
        }

class PIRRecordDebug(db.Model): 
    __tablename__ = 'pir_record_debug' 
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False) 
    sensor_id = db.Column(db.String(80), db.ForeignKey('sensor.id'), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=True)

    # one-to-many relationship
    sensor = db.relationship('Sensor', back_populates='pir_records_debug')

    def __init__(self, timestamp, sensor_id, value): 
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.value = value

    def serialize(self):
        return {
            'id' : self.id,
            'timestamp' : self.timestamp,
            'sensor_id': self.sensor_id,
            'value' : self.value
        }

class Upcoming(db.Model):
    __tablename__ = 'upcoming'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(80), unique=False, nullable=False)
    start = db.Column(db.DateTime, unique=False)
    end = db.Column(db.DateTime, unique=False)

    def __init__(self, creator, start, end):
        self.creator = creator
        self.start = start
        self.end = end

    def serialize(self):
        return {
            'id' : self.id,
            'creator' : self.creator,
            'start': self.start,
            'end' : self.end
        } 


class ManualCounter(db.Model):
    __tablename__ = 'manual_counter'
    id = db.Column(db.Integer, primary_key=True)
    movement = db.Column(db.String(10), unique=False, nullable=False)     # values are in/out
    timestamp = db.Column(db.DateTime, unique=False)
    occupancy = db.Column(db.Integer, unique=False)
    remarks = db.Column(db.String(120), unique=False, nullable=True)
    

    def __init__(self, movement, timestamp, occupancy, remarks=None):
        self.movement = movement
        self.timestamp = timestamp
        self.occupancy = occupancy
        self.remarks = remarks