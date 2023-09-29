from secret import MONGO_DB_ADMIN_PASSWORD

MONGO_DB_URL = f"mongodb+srv://admin:{MONGO_DB_ADMIN_PASSWORD}@chatapp.ktbl8my.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "ChatApp"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
