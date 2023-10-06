import motor.motor_asyncio


MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.pf

users_collection = database.users
metrics_collection = database.metrics
user_metrics_collection = database.user_metrics
sections_collection = database.sections
