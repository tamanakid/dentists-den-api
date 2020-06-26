from extensions import db, ma


# User Table

class User(db.Model):
    username = db.Column(db.String(16), primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    password = db.Column(db.String(32))

    def __init__(self, username, firstname, lastname, password):
        super(User, self).__init__()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password



# Product Schema
class UserSchema(ma.Schema):
	class Meta:
		fields = ("username", "firstname", "lastname", "password")

user_schema = UserSchema()
users_schema = UserSchema(many = True)
