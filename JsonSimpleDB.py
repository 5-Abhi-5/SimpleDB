from SimpleDB import SimpleDB
import json,os,datetime as dt

# Todo- implement serialization and deserialization from scratch
# Todo- Add support for Expiry of keys
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
            
        # ERROR in type of datetime not serializable (convert to str and use for serialization and vice versa [probable solution])
        # for key, value in self.expiry.items():
        #     if value:
        #         self.expiry[key] = None
        #     else:
        #         self.expiry[key] = value.isoformat() if isinstance(value, dt.datetime) else value
            
        # with open(self.db_name + '_expiry.json', 'w') as f:
        #     json.dump(self.expiry, f)


    """
        Load the database from a JSON file.
    """
    def load(self):
    # Add Wal Support
        try:
            with open(self.db_name + '.json', 'r') as f:
                self.data = json.load(f)
                
            # # ERROR in type of datetime not serializable (convert to str and use for serialization and vice versa [probable solution])
            # with open(self.db_name + '_expiry.json', 'r') as f:
            #     self.expiry = json.load(f) 
             
            # for key, value in self.expiry.items():
            #     self.expiry[key] = dt.datetime.fromisoformat(value) if isinstance(value, str) else value
            
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