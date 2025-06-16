from SimpleDB import SimpleDB
import json,os

# Todo- implement serialization and deserialization from scratch
"""
    JsonSimpleDB is a subclass of SimpleDB that uses JSON for data storage.
    It inherits all methods from SimpleDB and overrides the save and load methods
    to use JSON serialization.
"""
class JsonSimpleDB(SimpleDB):
    
    """
        Save the database to a JSON file.
    """
    def save(self): 
        with open(self.db_name + '.json', 'w') as f:
            json.dump(self.data, f)

    """
        Load the database from a JSON file.
    """
    def load(self):
    # Add Wal Support
        try:
            with open(self.db_name + '.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
       
    """
        Drop the database by deleting the JSON file.
    """       
    def drop(self):
        try:
            self.data.clear()
            self.wal.write_log("drop", self.db_name + '.json')
            self.wal.close_log_file()
            os.remove(self.db_name + '.json')
            os.remove(self.log_file_name)
        except FileNotFoundError:
            pass