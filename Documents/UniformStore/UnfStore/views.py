from UnfStore import app,db
from flask import redirect, url_for, render_template, flash, session,request
from flask_login import login_user, logout_user, login_required, current_user
from UnfStore.models import User, Outfits, Cart, Orders
from sqlalchemy import or_, and_
import re
import time

@app.route('/')
@app.route('/login_page', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_welcome'))
         else:
            flash(f'Login successful', category='success')
            time.sleep(2)
            return redirect(url_for('boys_page'))
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
               time
               return redirect(url_for('boys_page'))     
         except:
            flash('an error occured', category='danger')

      return render_template('signup.html')
   else:
      return render_template('signup.html')

""" @app.route('/Admin_welcome_page')
def admin_welcome():
   return render_template('includes/welcome_adm.html')

@app.route('/Admin_page', methods=['GET' , 'POST'])
@login_required
def admin_page():   
   # '|' , or_ - represents 'or' logical operator
   # check for users with roles other than 1 and null roles and pass them to query for display
   # users = User.query.filter((User.user_role != 1) | (User.user_role == None)).all()
   query_items = (
      User.query.filter(or_(User.user_role != 1 , User.user_role == None)).all(),
      Cart.query.all(), 
      Orders.query.all(), 
      Outfits.query.all()
   )

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

   return render_template('admin.html', query_items = query_items )

@app.route('/Admbook_page', methods=['GET' , 'POST'])
@login_required
def admin_page2():    
   return render_template('adm_book.html') """

""" @app.route('/splash_page')
def splash_page():
   return render_template('includes/splash.html') """

""" @app.route('/AddVehicle_page', methods=['GET' , 'POST'])
def add_vehicle_page():
   if request.method == 'POST':
      items = [
         request.form['price'], request.form['description'],
         request.form['model'], request.form['type'], request.form['link'], 
         request.form['units'], request.form['year']
      ]
      print(items[5])
      print(0>int(items[5]))

      if items:
         reg_exp = '^\d{4}$'
         try:
            if (not(re.search(reg_exp, items[6]))):
               flash('invalid year or car units!',category='danger')
               return(redirect(url_for('add_vehicle_page')))
            else:
               new_vehicle = Outfits(
                  price=items[0], description=items[1],
                  model=items[2], car_type=items[3], 
                  image_link=items[4], vehicle_units=items[5], 
                  year=items[6]
               ) 
               db.session.add(new_vehicle)
               db.session.commit()
               return redirect(url_for('admin_page'))
         except:
            flash('An error occurred!', category='danger')
   else:
      return render_template('includes/addVeh.html') """

@app.route('/Boys_page', methods=['GET', 'POST'])
@login_required
def boys_page():
   fits = ['Male', 'Female']

   # Using dictionary comprehension to store the results for each car type
   outfit_by_gender = {gfit: Outfits.query.filter_by(gender=gfit).all() for gfit in fits}
   print(outfit_by_gender)
   
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

   return render_template('includes/boyswear.html', outfit_by_gender=outfit_by_gender)

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
         total_price = 0
         # Add the details of the outfit to the list
         cart_fit_details.append({
            'id': outfit.id,
            'price': outfit.price,
            'gender': outfit.gender,
            'description': outfit.description,            
            'outfit_image': outfit.image_link
         })

         total_price += outfit.price
         print(total_price)

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

   return render_template('includes/cart.html', cart_fit_details=cart_fit_details)

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