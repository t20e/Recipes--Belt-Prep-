from flask_app.config.mysqlconnection import connectToMySQL
import re 
from flask import flash
from flask_app.models import recipe

email_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
names_validators = re.compile("^[a-zA-Z]+$")
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
    
    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name,last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s,  %(password)s, NOW())"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results,'*******************2435')
        return results


    @classmethod
    def check_if_email_exists(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return True

    @classmethod
    def check_password_email_login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def check_registration_fields(data):
        is_valid = False
        if data['password'] != data['password_confirm']:
            is_valid = True
            flash('passwords do not match!')

        if len(data['password']) < 8:
            is_valid = True
            flash('passwords is to short!')

        if not email_pattern.match(data['email']):
            is_valid = True
            flash('Not a valid Email!')
        if not names_validators.match(data['first_name']):
            if len(data['first_name']) < 2:
                flash('first name needs to be at least 2 characters and all letters')
                is_valid = True
        if not names_validators.match(data['last_name']):
            if len(data['last_name']) < 2:
                flash('Last name needs to be at least 2 characters and all letters')
                is_valid = True

        email_holder = data['email'].split('@')
        if email_holder == data['email'].split('@'):
            if len(email_holder[0]) > 2:
                holder = User.check_if_email_exists(data)
                if holder != False:
                    flash("email already exists")
                    is_valid = True
            elif len(email_holder[0]) < 2:
                flash('email needs to be more then 2 charaters')
                is_valid = True
        return is_valid



    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipe ON user_id = users.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        instance = cls(results[0])
        for row in results:
            recipe_data = {
                'id' : row['recipe.id'],
                'name' : row['name'],
                'description' : row['description'],
                'instructions' : row['instructions'],
                'created_at' : row['recipe.created_at'],
                'updated_at' : row['recipe.updated_at'],
                'under_30' : row['under_30'],
                'user_id' : row['user_id']
            }
            instance.recipes.append(recipe.Recipe(recipe_data))
            print(instance.first_name)
        return instance

    # @classmethod
    # def get_all_recipes(cls,data):
    #     if not 
    #     query = "SELECT * FROM recipe LEFT JOIN users ON user_id = users.id WHERE users.id = %(user_id)s;"
    #     results = connectToMySQL('recipes').query_db(query,data)
    #     user_data = {
    #         'id' : results[0]['users.id'],
    #         'first_name' : results[0]['first_name'],
    #         'last_name' : results[0]['last_name'],
    #         'email' : results[0]['email'],
    #         'password' : results[0]['password'],
    #         'created_at' : results[0]['users.created_at'],
    #         'updated_at' : results[0]['users.updated_at'],
    #     }
    #     instance = cls(user_data)
    #     for row in results:
    #         instance.recipes.append(recipe.Recipe(row))
    #         print(instance.first_name)
    #     return instance

