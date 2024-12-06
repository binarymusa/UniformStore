from UnfStore import app,db,api
from flask import redirect, url_for, render_template, flash, session,request, jsonify, Blueprint
from flask_restful import Resource,abort
from flask_login import login_user, logout_user, login_required, current_user
from UnfStore.models import User, Outfits, Cart, Orders
from sqlalchemy import or_, and_
# from intasend import APIService - -  -
import re
import time

views_blueprint = Blueprint('views', __name__)
def fits_by_gender():
   fits = ['Male', 'Female', 'Unisex']
   # Using dictionary comprehension to store the results for each fit type
   outfit_by_gender = {gfit: Outfits.query.filter_by(gender=gfit).all() for gfit in fits}
   return outfit_by_gender

@app.route('/')
@app.route('/login_page', methods=['GET', 'POST'])
# @views_blueprint.route('/login_page', methods=['GET', 'POST'])
def login_page():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      check_user = User.query.filter_by(username=username).first()

      if check_user and check_user.check_password_correction(attempted_password=password):
         login_user(check_user) 

         #  Access the associated role object via the role relationship
         if check_user.role and check_user.role.role_name == 'Admin':
            flash(f'Admin Login successful', category='success')
            return redirect(url_for('admin_page'))
         else:
            flash(f'Login successful', category='success')
            time.sleep(2)
            return redirect(url_for('views.boys_page'))
      else:
         flash(f'Incorrect username or Password', category='danger')
         return redirect(url_for('login_page'))
   else:
      return render_template('login.html')

@app.route('/sign_up_page' , methods=['GET', 'POST'])
def signup_page():
   if request.method == 'POST':
      # Get data from the form
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
         
      existing_user = User.query.filter(and_(User.username == username , User.email_address == email)).first()
      
      if existing_user:
         flash(f'User already exists. Try different credentials', category='danger')
         return redirect(url_for('signup_page'))
      else:
         #checks if the email given matches the expression 
         reg_exp = '^\S+(\@gmail\.com$|\@hotmail\.com$|\@yahoo\.com$)$'
         try:
            if (not(re.search(reg_exp, email))):
               flash('Invalid email address!', category='danger')
               return redirect(url_for('signup_page'))
            else:
               # return True
               print(email)           
               # Add the new user to database
               new_user = User(username=username, email_address=email, password=password)
               db.session.add(new_user)
               db.session.commit()

               login_user(new_user)
               flash(f'signup successful', category='success')  
               return redirect(url_for('boys_page'))     
         except:
            flash('an error occured', category='danger')

      return render_template('signup.html')
   else:
      return render_template('signup.html')


@app.route('/Admin_page', methods=['GET' , 'POST'])
@login_required
def admin_page():   
   if request.method == 'GET':
      # '|' , or_ - represents 'or' logical operator
      # check for users with roles other than 1 and null roles and pass them to query for display
      # users = User.query.filter((User.user_role != 1) | (User.user_role == None)).all()
      query_items = (
         User.query.filter(or_(User.user_role != 1 , User.user_role == None)).all(),
         Cart.query.all(), 
         Orders.query.all(), 
         Outfits.query.all()
      )
      fits_by_gender()

   if request.method == 'POST':
      user_to_delete = request.form.get('user_delete')
      vehicle_to_delete = request.form.get('vehicle_delete')

      if user_to_delete:
        User.delete_user(user_to_delete)

        flash('user deletion confirmed', category='danger')
        return redirect(url_for('admin_page'))  
           
      elif vehicle_to_delete:
         selected_fit = Outfits.query.filter_by(id=vehicle_to_delete).first()

         if selected_fit:
            selected_fit.delete_vehicle()
            flash('outfit deletion succesful', category='danger')
            return redirect(url_for('admin_page'))
         else:
            flash('deletion unsuccesful', category='danger')

   return render_template('includes/admin.html', query_items = query_items, outfit_by_gender=fits_by_gender())

# @app.route('/Boys_page', methods=['GET', 'POST'])
@views_blueprint.route('/Boys_page', methods=['GET', 'POST'])
@login_required
def boys_page():
   fits_by_gender() 
   if request.method == 'POST':
      item = request.form.get('added_fit') 
      item2 = request.form.get('order_fit') 
                  
      if item:         
         selected_item = Outfits.query.filter_by(id=item).first() 
         if selected_item:
            selected_item.add_to_cart(current_user)
            flash('Item added to cart', category='success')
            return redirect(url_for('cart_page'))
         else:
            flash('error occurred', category='danger')
         
      elif item2:
         selected_item = Outfits.query.filter_by(id=item2).first()       
         if selected_item:
            # Add item to the cart based on method in its model
            selected_item.add_to_order(current_user)            
            flash('Order added', category='success')
            return redirect(url_for('my_orders'))
         else:
            flash('Order not added', category='danger')

   return render_template('includes/boyswear.html', outfit_by_gender=fits_by_gender())

# API resource
class OutfitResource(Resource):
   def get(self, outfit_id=None):
      if outfit_id:
         outfit = Outfits.query.filter_by(id=outfit_id).first()
         if outfit:
            return jsonify({
               'id': outfit.id,
               'name': outfit.category,
               'gender': outfit.gender,
               'price': outfit.price,
            })
         return jsonify({'message': 'Outfit not found'}), 404
      else:
         outfits = Outfits.query.all()
         return jsonify([
            {'id': outfit.id, 'name': outfit.category, 'gender': outfit.gender, 'price': outfit.price}
            for outfit in outfits
         ])

   def post(self):
      data = request.get_json()      
      if 'category' not in data or 'gender' not in data or 'price' not in data:
         return jsonify({'message': 'Missing data'}), 400
      
      new_outfit = Outfits(
         category=data['category'],
         gender=data['gender'],
         price=data['price'],
         description=data['description'],
         image_link=data['image_link']
      )
      try:
         db.session.add(new_outfit)
         db.session.commit()
         return jsonify({'message': 'Outfit added successfully'}), 201
      except Exception as e:
        print(f"Error adding outfit: {str(e)}")
        return jsonify({'message': 'An error occurred while adding the outfit'}), 500
   
   def put(self, outfit_id=None):
      if outfit_id:
         outfit = Outfits.query.filter_by(id=outfit_id).first()
         if outfit:
            data = request.get_json()
            # Update outfit properties based on the received JSON data
            outfit.category = data.get('category', outfit.category)
            outfit.gender = data.get('gender', outfit.gender)
            outfit.price = data.get('price', outfit.price)
            outfit.description = data.get('description', outfit.description)
            outfit.image_link = data.get('image_link', outfit.image_link)
            
            try:
               db.session.commit()
               return jsonify({'message': 'Outfit updated successfully'}), 200
            except Exception as e:
               print(f'error: {e}')               
         else:
            return jsonify({'message': 'Outfit not found'}), 404
      else:
         return jsonify({'message': 'Invalid request'}), 400
   
   def patch(self, outfit_id=None):
      if outfit_id:
         outfit = Outfits.query.filter_by(id=outfit_id).first()
         if outfit:
            data = request.get_json()
            outfit.category = data.get('category', outfit.category)
            outfit.gender = data.get('gender', outfit.gender)
            outfit.price = data.get('price', outfit.price)
            outfit.description = data.get('description', outfit.description)
            outfit.image_link = data.get('image_link', outfit.image_link)

            db.session.commit()
            return jsonify({'message': 'Outfit updated successfully'})
         else:
            return jsonify({'error': 'Outfit not found'}), 404
      else:
         return jsonify({'error': 'Outfit ID is required'}), 400
   
   def delete(self, outfit_id=None):
      if outfit_id:
         outfit = Outfits.query.filter_by(id=outfit_id).first()
         if outfit:
            db.session.delete(outfit)
            db.session.commit()
            return jsonify({'message': 'Outfit deleted successfully'})
         else:
               return jsonify({'error': 'Outfit not found'}), 404
      else:
         return jsonify({'error': 'Outfit ID is required'}), 400


# Register the API resources
api.add_resource(OutfitResource, '/api/outfits', '/api/outfits/<int:outfit_id>')

@app.route('/Girls_page', methods=['GET', 'POST'])
@login_required
def girls_page():
   fits = ['Male', 'Female', 'Unisex']

   outfit_by_gender = {gfit: Outfits.query.filter_by(gender=gfit).all() for gfit in fits}
   print(outfit_by_gender)

   if request.method == 'POST':
      pass
   return render_template('includes/girlswear.html', outfit_by_gender=outfit_by_gender)

@app.route('/mycart_page', methods=['GET', 'POST'])
@login_required
def cart_page():   
   cart_fit_details = []
   if request.method == 'GET':
      my_cart = Cart.query.filter_by(user_id=current_user.id).all()
      
      # Initialize a list to store the details of each outfit in the cart
      
      for item in my_cart:         
         outfit = item.outfit  # Access the associated outfit object via the relationship
         # Add the details of the outfit to the list
         cart_fit_details.append({
            'id': outfit.id,
            'price': outfit.price,
            'gender': outfit.gender,
            'description': outfit.description,            
            'outfit_image': outfit.image_link
         })
      Subtotals = sum(item.get('price', 0) for item in cart_fit_details)

   if request.method == 'POST':
      item = request.form.get('remove_added_fit')
      # item2 = request.form.get('order_added_fits')

      if item:   
         selected_outfit = Cart.query.filter_by(outfit_id=item, user_id=current_user.id).first()
         if selected_outfit:
            selected_outfit.remove_from_cart()
            flash('item removed from cart', category='success')
            return redirect(url_for('cart_page'))
         else:
            flash('an error occured', category='danger')
   
      # elif item2:
         # pass
         """ selected_fit = Cart.query.filter_by(vehicle_id=item).first()
         
         if selected_fit and current_user.can_purchase(selected_fit.outfit):
            selected_fit.outfit.buy(current_user)

            flash('Purchase was successful', category='success')
            # After purchasing, remove the item from the cart
            cart_item = Cart.query.filter_by(vehicle_id=item, user_id=current_user.id).first()
            
            db.session.delete(cart_item)
            db.session.commit()
            return redirect(url_for('purchases_page'))
         else:
            flash('Not enough money to purchase', category='danger')
            return redirect(url_for('cart_page')) """

   return render_template('includes/cart.html', cart_fit_details=cart_fit_details, Subtotals=Subtotals)


@app.route('/my_orders', methods=['GET', 'POST'])
@login_required
def my_orders():
   if request.method == 'GET':
      my_order = Orders.query.filter_by(user_id=current_user.id).all()
      
      ordered_fit_details = []
      for item in my_order:
         outfit = item.outfit
         ordered_fit_details.append({
            'id': outfit.id,
            'price': outfit.price,
            'category': outfit.category,
            'description': outfit.description,            
            'fit_image': outfit.image_link
         })
      print(ordered_fit_details)
   
   if request.method == 'POST':
      item = request.form.get('remove_order')

      if item:
         selected_fit = Orders.query.filter_by(outfit_id=item, user_id=current_user.id).first()
         if selected_fit:
            selected_fit.remove_from_orders()
            flash('Order removed successfully', category='success')
            return redirect(url_for('my_orders'))
         else:
            flash('Item not removed', category='danger')

   return render_template('orders.html', ordered_fit_details=ordered_fit_details)

@app.route('/logout')
def logout_page():
   logout_user()
   flash(" logged out succesfully!", category='info')
   return redirect(url_for('login_page'))