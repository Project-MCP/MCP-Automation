# src/utils.py

import json

class DataProcessor:
    def __init__(self, data_source):
        self.source = data_source
        self.data = None

    def load_data(self):
        try:
            with open(self.source, 'r') as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            return False

    def get_user_by_id(self, user_id):
        if not self.data:
            return None
        for user in self.data.get('users', []):
            if user.get('id') == user_id:
                return user
        return None

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
