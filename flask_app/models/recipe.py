from flask_app.config.mysqlconnection import connectToMySQL
import re 
from flask import flash

names_validators = re.compile("^[a-zA-Z]+$")

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
    
    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipe (name, description, instructions, created_at, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s,  %(created_at)s,  %(under_30)s, %(user_id)s)"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def get_recipe_data(cls,data):
        query = "SELECT * FROM recipe WHERE id = %(recipe_id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results,'recipe')
        return results
    
    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipe SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, created_at = %(created_at)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(recipe_id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results,'recipe')
        return print('update')
    
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipe WHERE id = %(recipe_id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results,'recipe')
        return print('DELETE')

    @staticmethod
    def check_registration_fields(data):
        is_valid = False 
        if len(data['name']) < 3:
            is_valid = True
            flash('name is to short!')
        if len(data['description']) < 3:
            is_valid = True
            flash('description is to short!')
        if len(data['instructions']) < 3:
            is_valid = True
            flash('instructions is to short!')
        
        if data['created_at'] == '':
            is_valid = True
            flash('select a date!')
        
        if data['under_30'] == '':
            is_valid = True
            flash('please select an option for under 30!')
        return is_valid
