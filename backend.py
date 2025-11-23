# Install dependencies if needed:
# pip install pymongo twilio python-dotenv

from pymongo.mongo_client import MongoClient
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file (do NOT commit this file!)
load_dotenv()

# MongoDB Atlas credentials (keep in .env)
mongo_uri = os.environ.get("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["myka"]
contacts_collection = db["contacts"]
logs_collection = db["logs"]

# Twilio credentials (keep in .env)
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_client = TwilioClient(account_sid, auth_token)
twilio_whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")  # whatsapp:+14155238886

# Example: Add a contact (uncomment to use)
# contact = {"name": "ADIBiber", "number": "+919XXXXXXXXXX"}
# contacts_collection.insert_one(contact)

# Fetch all contacts
contacts = list(contacts_collection.find({}, {"_id": 0}))
print("All contacts:", contacts)

# Send a WhatsApp message
recipient_number = "+919742320225"  # Use a joined/verified WhatsApp number
message_body = "Hey! This is a test. (Sent from Twilio trial account)"
message = twilio_client.messages.create(
    body=message_body,
    from_=twilio_whatsapp_number,
    to="whatsapp:" + recipient_number
)
print("Message SID:", message.sid)

# Log message in the database
log = {
    "to": recipient_number,
    "body": message_body,
    "status": "sent",
    "sid": message.sid
}
logs_collection.insert_one(log)

# Fetch and print message logs
logs = list(logs_collection.find({}, {"_id": 0}))
print("Message logs:", logs)
