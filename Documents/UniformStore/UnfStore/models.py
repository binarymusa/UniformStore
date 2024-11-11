
from UnfStore import db,login_manager
from UnfStore import bcrypt
from flask_login import UserMixin
from flask import flash

# tells Flask-Login that the function (load_user) should be used to retrieve a user object when a user is logged in and their session needs to be managed.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# data fetched from the user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True) # primary-key column
    user_role = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    username = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000000) # default budget money
    
    role = db.relationship('Roles', backref='users')
    cart_rltship = db.relationship('Cart', backref='users', lazy=True)
    order_rltship = db.relationship('Orders', backref='users', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:            
            return f'{self.budget:,d}'
        else:
            return f"{self.budget}"
    @property
    def password(self):
        return self.password
    
    @password.setter
    # hashes the password using bcrypt and stores the hashed value in the "password_hash" column.
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    # check if a provided plain-text password matches the hashed password stored in the "password_hash" column
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    """ def can_purchase(self, vehicle_obj):
        return self.budget >= vehicle_obj.price
    
    def can_sell(self, vehicle_obj):
        return vehicle_obj in self.vehicle """
    
    # method to set the admin budget to 0
    # static methods don't have access to the instance (self) or class (cls) objects.
    @staticmethod
    def Admin_budget():
        users = User.query.filter_by(user_role=1).all()
        
        if users:
            for user in users:
                user.budget = 0
            db.session.commit()
            return f"Budget of users with role's 1 has been set to zero."
        else:
            return 'No users found with the specified role.'

    # method to dissasociate a user with a car, then deleting them
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        
        if user :
            # Subquery to select vehicle IDs owned by the user
            # A subquery is simply a nested query. can be used in another query
            subquery = db.session.query(Cart.id).filter_by(user_id=user_id).union(
                db.session.query(Orders.id).filter_by(user_id=user_id)
            ).subquery()
            
            # Delete related records from Cart and Orders tables and disassociate vehicles
            Cart.query.filter(Cart.id.in_(subquery)).delete(synchronize_session=False)
            Orders.query.filter(Orders.id.in_(subquery)).delete(synchronize_session=False)

            # Now you can safely delete the user
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False

# User roles database
class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(length=30), nullable=False, unique=True)

class Outfits(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    gender = db.Column(db.String(length=60), nullable=False, unique=False)
    category = db.Column(db.String(length=60), nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=False) 
    description = db.Column(db.String(length=1024), nullable=False)
    image_link = db.Column(db.String(length=1024), nullable =True, unique= False)

    cart_rltship = db.relationship('Cart', backref='outfit', lazy=True)
    orders_rltship = db.relationship('Orders', backref='outfit', lazy=True)
  
    # def __repr__(self):
    #     return f'Item {self.model}'

    def add_to_cart(self, user):
        cart_item = Cart(user_id=user.id, outfit_id=self.id)        
        # self.vehicle_units -= 1 
        db.session.add(cart_item)
        db.session.commit()
 
    def add_to_order(self, user):
        order_item = Orders(user_id=user.id, outfit_id=self.id)
        # self.owner = user.id
        # user.budget -= self.price
        # self.vehicle_units -= 1
        db.session.add(order_item)
        db.session.commit()
    
    def delete_outtfit(self):
        db.session.delete(self)
        db.session.commit()
    
class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    outfit_id = db.Column(db.Integer(), db.ForeignKey('outfits.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @staticmethod
    def count_user_items(user_id):
        pass

    def remove_from_cart(self):
        db.session.delete(self)
        db.session.commit()

class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    outfit_id = db.Column(db.Integer(), db.ForeignKey('outfits.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def remove_from_orders(self):
        db.session.delete(self)
        db.session.commit()
    # @staticmethod
    # def clear_purchased_items(user_id): 
    #     user = User.query.get(user_id)

    #     if user:
    #         items = Orders.query.filter_by(user_id=user_id).all()
    #         db.session.delete(items)
    #         db.session.commit()
    
    