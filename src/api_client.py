"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
import pymongo
import pickle
import numpy as np
import pandas as pd
from clean_data import clean_api_data
from model import MyModel


class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key='vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db=None,
                 interval=30):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        self.db = db
        self.interval = 30
        self.model = None

    def save_to_database(self, row):
        """Save a data row to the database."""
        print("Received data:\n" + repr(row) + "\n")  # replace this with your code

    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                for row in data:
                    self.save_to_database(row)
                    self.predict_fraud(row)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)
    
    def predict_fraud(self, row):
        cleaned_data = clean_api_data(row)
        prediction = self.model.predict(cleaned_data)[0]
        current_time = time.time()
        
        print("prediction: ", prediction)
        print("time :", current_time)
        print()
        
        
        
        
    def load_model(self, model):
        self.model = model
        


def main():
    """Collect events every 30 seconds."""
    with open('./model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    client = EventAPIClient()
    client.load_model(model)
    client.collect()


if __name__ == "__main__":
    main()
