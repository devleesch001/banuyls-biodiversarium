def init(db):
    class Role(db.Model):
        name=db.Column(db.String(50), primary_key=True)
        display_name=db.Column(db.String(50))

        def __init__(self, name, display_name):
            self.name = name
            self.display_name = display_name

    class Grant(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        user_id = db.Column(
            db.Integer, db.ForeignKey('user.id')
        )

        grant=db.Column(db.String(50), db.ForeignKey('role.name'))

        def __init__(self, user, name):
            self.user_id=user
            self.grant=name

        def toDict(self):
            return {
                "id":self.id,
                "user_id":self.user_id,
                "grant":self.grant
            }
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        username = db.Column(db.String(50))
        email=db.Column(db.String(50))
        password = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)

        def __init__(self, user, email, passw):
            self.username = user
            self.email = email
            self.password=passw

        def toDict(self):
            return {
                "id":self.id,
                "username":self.username,
                "active":self.is_active
            }
            
        def get_id(self):
            return self.id

        def check_password(self, password):
            return password == self.password

    return (User, Grant, Role)