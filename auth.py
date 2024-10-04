from database import User
import hashlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def hash_password(password):
    logger.debug(f"Hashing password: {password}")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    logger.debug(f"Hashed password: {hashed}")
    return hashed

def login(username, password):
    logger.debug(f"Login attempt for user: {username}")
    user = User.get_by_username(username)
    if user:
        logger.debug(f"User found: {username}")
        logger.debug(f"Stored hashed password: {user['password']}")
        entered_hash = hash_password(password)
        logger.debug(f"Entered password hash: {entered_hash}")
        if user['password'] == entered_hash:
            logger.debug("Password match successful")
            return user
        else:
            logger.debug("Password match failed")
    else:
        logger.debug(f"User not found: {username}")
    return None

def register(username, password):
    logger.debug(f"Registration attempt for user: {username}")
    if User.get_by_username(username):
        logger.debug(f"Username already exists: {username}")
        return False
    hashed_password = hash_password(password)
    logger.debug(f"Hashed password for registration: {hashed_password}")
    User.create(username, hashed_password)  # Make sure this is passing the hashed password
    logger.debug(f"User created: {username}")
    return True

def check_login(session):
    return session.get('user') is not None

def logout(session):
    session['user'] = None