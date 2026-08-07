from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv('COGNODB_URI')
USERNAME = os.getenv('COGNODB_USERNAME')
PASSWORD = os.getenv('COGNODB_PASSWORD')

driver = GraphDatabase.driver(
    URL,
    auth=(USERNAME,PASSWORD)
)

try:
    driver.verify_connectivity()
    print('Connected to CognoDB successfully')
except Exception as e:
    print('Failed to connect to CognoDB')
    print(e)

def get_driver():
    return driver