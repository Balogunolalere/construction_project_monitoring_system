from database import User
import hashlib
import smtplib
from email.mime.text import MIMEText
import uuid

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    user = User.get_by_username(username)
    if user and user['password'] == hash_password(password):
        return user
    return None

def register(username, password):
    if User.get_by_username(username):
        return False
    hashed_password = hash_password(password)
    User.create(username, hashed_password)
    return True

def check_login(session):
    return session.get('user') is not None

def logout(session):
    session['user'] = None

# def send_reset_email(email, reset_token):
#     msg = MIMEText(f"Click the link to reset your password: http://localhost:8501/reset_password?token={reset_token}")
#     msg['Subject'] = 'Password Reset'
#     msg['From'] = 'no-reply@example.com'
#     msg['To'] = email

#     with smtplib.SMTP('smtp.example.com') as server:
#         server.login('username', 'password')
#         server.sendmail('no-reply@example.com', [email], msg.as_string())

# def reset_password(token, new_password):
#     user = User.get_by_reset_token(token)
#     if user:
#         hashed_password = hash_password(new_password)
#         User.update_password(user['username'], hashed_password)
#         return True
#     return False

# def generate_reset_token(username):
#     token = str(uuid.uuid4())
#     User.update(username, None, None, reset_token=token)
#     return token
