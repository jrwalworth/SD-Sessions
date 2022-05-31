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
    def insert(cls, data):
        query = "INSERT INTO skater (username, password, first_name, last_name, email, \
            bio, stance, avatar, created_at, updated_at) VALUES (%(username)s, %(password)s, \
            %(first_name)s, %(last_name)s, %(email)s, %(bio)s, %(stance)s, %(avatar)s, \
            NOW(), NOW() );"
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