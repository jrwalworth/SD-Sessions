from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Spot:
    db = 'sk8rmap'
    def __init__(self, data):
        self.id = data['id']
        self.skater_id = data['skater_id']
        self.name = data['name']
        self.spot_aka = data['spot_aka']
        self.descr = data['descr']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.lon = data['lon']
        self.lat = data['lat']
        self.type = data['type']
        self.photos = data['photos']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_spots(cls):
        query = "SELECT * FROM spot;"
        results = connectToMySQL(cls.db).query_db(query)
        spots=[]
        for s in results:
            spots.append( cls(s) )
        return spots
    
    @classmethod
    def get_all_streetspots(cls):
        query = "SELECT * FROM spot WHERE type='Street';"
        results = connectToMySQL(cls.db).query_db(query)
        streetspots=[]
        for s in results:
            streetspots.append( cls(s) )
        return streetspots
    
    @classmethod
    def get_all_skateparks(cls):
        query = "SELECT * FROM spot WHERE type='Skatepark';"
        results = connectToMySQL(cls.db).query_db(query)
        skateparks=[]
        for s in results:
            skateparks.append( cls(s) )
        return skateparks

    
    @classmethod
    def get_one_spot(cls, data):
        query = "SELECT * FROM spot WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_skater_from_spot(cls, data):
        query = "SELECT skater_id FROM spot where id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def insert_spot(cls, data):
        query = "INSERT INTO spot ( skater_id, name, spot_aka, descr, address, city, state, zip, \
            type, photos, rating, created_at, updated_at) VALUES (%(skater_id)s, %(name)s, \
            %(spot_aka)s, %(descr)s, %(address)s, %(city)s, %(state)s, %(zip)s, \
            %(type)s, %(photos)s, %(rating)s, NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_spot(cls, data):
        query = "UPDATE spot SET skater_id=%(skater_id)s, name=%(name)s, spot_aka=%(spot_aka)s, descr=%(descr)s, address=%(address)s,\
            city=%(city)s, state=%(state)s, zip=%(zip)s, type=%(type)s,\
            photos=%(photos)s, rating=%(rating)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_spot(cls, data):
        query = "DELETE FROM spot WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    #Skatespot addition - validations
    def validate_spot(spot):
        is_valid = True
        if len(spot['name']) < 1:
            is_valid = False
            flash('You must add a spot name.')
        #validate descr and instructions
        if len(spot['address']) < 2:
            flash('Your spot must have an address.')
            is_valid = False
        if len(spot['type']) < 2:
            flash('What good is a spot without a type? Add type before submitting your spot.')
            is_valid = False
        return is_valid