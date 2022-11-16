def init(db):
    class Token(db.Model):
        user_id = db.Column(
            db.Integer, db.ForeignKey('user.id'), primary_key=True
        )

        access_token = db.Column(db.String(255), unique=True)
        expires = db.Column(db.DateTime)
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        username = db.Column(db.String(50))
        password = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)

        def __init__(self, user, passw):
            self.username = user
            self.password=passw
            
        def get_id(self):
            return self.id

        def check_password(self, password):
            return password == self.password

    return (User, Token)