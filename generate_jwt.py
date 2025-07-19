import jwt
import datetime

secret_key = "8ef3a1492c75495eb10b556ab3a3a61c"
user_id = "1"  # sample user id

payload = {
    "sub": user_id,
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

token = jwt.encode(payload, secret_key, algorithm="HS256")
print(token)
