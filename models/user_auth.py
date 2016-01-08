from werkzeug.security import generate_password_hash, \
     check_password_hash

class UserAuth(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
        
    
# TODO for sign up 
# 1. user = UserAuth('name','pwd')
# 2. store user.pw_hash in database along with user.username

# TODO for sign in
# find user by username
# 