from database.SimpleDB import SimpleDB
import json,os,datetime as dt

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
            
        # Overhead of copying dictionary for making data serializable (optimize later)
        temp=self.expiry.copy()
        for key, value in temp.items():
            if value:
                temp[key] = value.isoformat() 
            else:
                temp[key] = 'None'
                     
        with open(self.db_name + '_expiry.json', 'w') as f:
            json.dump(temp, f)
        
        temp.clear()


    """
        Load the database from a JSON file.
    """
    def load(self):
    # Add Wal Support
        try:
            with open(self.db_name + '.json', 'r') as f:
                self.data = json.load(f)
                
            with open(self.db_name + '_expiry.json', 'r') as f:
                self.expiry = json.load(f) 
             
            for key, value in self.expiry.items():
                if value == 'None':
                    self.expiry[key] = None
                else:
                    self.expiry[key] = dt.datetime.fromisoformat(str(value)) 
            
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
            os.remove(self.db_name + '_expiry.json')
        except FileNotFoundError:
            pass