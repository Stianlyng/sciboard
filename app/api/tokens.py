from datetime import datetime, timedelta
import jwt

def createToken(user_id,secret):
    # Create an expirationdate
    today = datetime.utcnow()
    days = timedelta(days=2)
    expirationDate = today + days
    return jwt.encode({'user': user_id, 'expires': str(expirationDate)},secret, algorithm='HS256')

def checkToken(token,secret):
    # Create an expirationdate
    today = datetime.utcnow()

    # DEcode
    token = jwt.decode(token, secret, algorithms=["HS256"])

    if token["expires"] < str(today):
        return False
    else:
        return token["user"]
