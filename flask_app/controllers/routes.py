from flask import render_template, redirect, request,session, url_for
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)  



@app.route('/')
def home():
    return render_template('index.html')

# dashbaord

@app.route('/dashboard')
def dash():
    data = {
        'user_id' : session['id']
    }
    
    user = User.get_all_recipes(data)

    return render_template('dashboard.html', user = user)


@app.route('/view_instructions<recipe_items>', methods=['GET'])
def view_instructions(recipe_items):
    if 'id' not in session:
        flash('please log in')
        return redirect('/')
    data ={
        'recipe_id' : recipe_items
    }
    get_recipe = Recipe.get_recipe_data(data)
    return render_template('show_recipe.html', get_recipe=get_recipe)

@app.route('/create')
def create_recipe():
    if 'id' not in session:
        flash('please log in')
        return redirect('/')
    return render_template('create_recipe.html')

# edit 
@app.route('/edit<items_id>')
def edit(items_id):
    if 'id' not in session:
        flash('please log in')
        return redirect('/')
    data ={
        'recipe_id' : items_id
    }
    get_recipe = Recipe.get_recipe_data(data)
    return render_template('edit.html', get_recipe =get_recipe, items_id = items_id)

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    data = {
        'recipe_id' : request.form['recipe_id'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'created_at' : request.form['date_made_on'],
        'under_30' : request.form['under_30']
    }
    check = Recipe.check_registration_fields(data)
    if check == False:
        update_recipe = Recipe.update_recipe(data)
        return redirect('/dashboard')
    return redirect(url_for('.edit', items_id = data['recipe_id']))

@app.route('/delete<recipe_id>')
def delete_recipe(recipe_id):
    data = {
        'recipe_id' : recipe_id
    }
    delete = Recipe.delete_recipe(data)
    return redirect('/dashboard')


@app.route('/reg_user', methods=['POST'])
def reg_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'password_confirm' : request.form['confirm_password']
    }
    if not User.check_registration_fields(data):
        print('red flag')
    else:
        return redirect('/')
    holder = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = holder
    create = User.create_user(data)
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']
    session['id'] = create
    print(create,'+++++++++++++++++')
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login_in():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password'],
    }
    holder = User.check_password_email_login(data) 
    if not holder:
        flash("invalid password/email")
        return redirect('/')
    if not bcrypt.check_password_hash(holder.password, request.form['password']):
        flash('invalid password/email')
        return redirect('/')
    session['first_name'] = holder.first_name
    session['last_name'] = holder.last_name
    session['email'] = holder.email
    session['id'] = holder.id
    return redirect('/dashboard')

@app.route('/add_recipe', methods=['GET','POST'])
def adding_recipe():
    if 'id' not in session:
        flash('please log in to create recipes')
        return redirect('/')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'created_at' : request.form['date_made_on'],
        'user_id' : request.form['user_id'],
        'under_30' : request.form['under_30']
    }
    if not Recipe.check_registration_fields(data):
        create_recipe = Recipe.create_recipe(data)
        return redirect('/dashboard')
    else:
        return redirect('/create')


