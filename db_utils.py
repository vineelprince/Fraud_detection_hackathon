import pymongo
import streamlit as st

# =====================================================
# MongoDB Connection (Centralized Utility)
# =====================================================
@st.cache_resource
def get_database():
    """
    Creates a secure MongoDB connection.
    This function is cached so Streamlit does not reconnect repeatedly.
    """

    # 🔴 REPLACE WITH YOUR ACTUAL MONGODB ATLAS URI
    uri = "mongodb+srv://student_app_user:lenti003@studentcompanioncluster.xsd2riq.mongodb.net/?appName=StudentCompanionCluster"

    client = pymongo.MongoClient(uri)

    return client["fraud_detection_db"]


# =====================================================
# Database & Collections
# =====================================================
db = get_database()

# Trusted emails collection
authorized_emails = db["authorized_emails"]

# Email fraud logs
email_logs = db["email_logs"]

# Optional: customer transaction history
customer_transactions = db["customer_transactions"]

