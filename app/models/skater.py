from operator import truediv
from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Skater:
    db = 'sk8rmap'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.bio = data['bio']
        self.stance = data['stance']
        self.avatar = data['avatar']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM skater;"
        results = connectToMySQL(cls.db).query_db(query)
        skaters=[]
        for s in results:
            skaters.append( cls(s) )
        return skaters
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM skater WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM skater WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_username(cls, data):
        query = "SELECT * FROM skater WHERE username=%(username)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def add_skater_fav(cls,data):
        # For each spot user favorites, add to favorite list
        query = "INSERT INTO skater_fav_spot (skater_id, spot_id, created_at, updated_at) \
            VALUES(%(skater_id)s, %(spot_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_favs(cls, data):
        # Get skater favorites list
        query = "SELECT * FROM skater_fav_spot WHERE skater_id=%(id)s;"
        
        query2 = "SELECT sf.spot_id, s.name \
            FROM skater_fav_spot sf, spot s \
            WHERE sf.skater_id=%(id)s \
            AND sf.spot_id = s.id;"
            
        query3 = "SELECT sf.spot_id, s.name \
            FROM skater_fav_spot sf \
            WHERE sf.skater_id=%(id)s\
            LEFT JOIN spot s ON  sf.spot_id = s.id;"
        # TODO join in spot table to bring up spot details
        results = connectToMySQL(cls.db).query_db(query, data)
        results2 = connectToMySQL(cls.db).query_db(query2, data)
        results3 = connectToMySQL(cls.db).query_db(query3, data)
        
        print('results...', results)
        print('results2:', results2)
        print('results3...', results3)
        # for f in results:
        #     favs.append(cls(f))
        return results2
    
    
    #     @classmethod
    # def get_all_streetspots(cls):
    #     query = "SELECT * FROM spot WHERE type='Street';"
    #     results = connectToMySQL(cls.db).query_db(query)
    #     streetspots=[]
    #     for s in results:
    #         streetspots.append( cls(s) )
    #     return streetspots

    
    # @classmethod
    # def rate_spot(cls, data):
    #     # Allow user to rate specific spot out of 4 point rating scale.
    #     return True
    
    # @classmethod
    # def get_ratings(cls, data):
    #     # Get skater ratings for all spots they've rated.
    #     return True
    
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO skater (username, password, first_name, last_name, email, \
            created_at, updated_at) VALUES (%(username)s, %(password)s, %(first_name)s, \
                %(last_name)s, %(email)s, NOW(), NOW() );"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE skater SET username=%(username)s, password=%(password)s, \
            first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, \
            bio=%(bio)s, stance=%(stance)s, avatar=%(avatar)s, updated_at=NOW() \
            WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM skater WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    #user/skater registration validations
    def validate_registration(skater):
        is_valid = True
        query = 'SELECT * FROM skater WHERE email=%(email)s;'
        results = connectToMySQL(Skater.db).query_db(query, skater)
        #validate username
        if len(skater['username']) < 2:
            flash('Username must be at least two characters.')
            is_valid = False
        #validate password
        if len(skater['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters. Try again.")
        #confirm password
        if skater['password'] != skater['conf-password']:
            is_valid = False
            flash('Passwords must match.')
        #validate names
        if len(skater['first_name']) < 2:
            flash('First name must be at least two characters.')
            is_valid = False
        if len(skater['last_name']) < 2:
            flash('Last name must be at least two characters.')
            is_valid = False
        #validate email
        if len(skater['email']) < 1:
            is_valid = False
            flash('You must add an email address.')
        elif not EMAIL_REGEX.match(skater['email']):
            is_valid = False
            flash('Invalid email format.')
        if len(results) >= 1:
            is_valid = False
            flash('This email is already being used.')
        return is_valid

    def fullName(self):
        return (self.first_name, self.last_name)