from database.SimpleDB import SimpleDB
from utilities.parser.JsonParser import JsonParser as parser
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
        
        json_parser = parser()
        
        # with open(self.db_name + '.json', 'w') as f:
            # json.dump(self.data, f)
        json_parser.dump_data(self.data,self.db_name + '.json')
            
        # Overhead of copying dictionary for making data serializable (optimize later)
        # temp=self.expiry.copy()
        # for key, value in temp.items():
        #     if value:
        #         temp[key] = value.isoformat() 
        #     else:
        #         temp[key] = 'None'
                     
        # # with open(self.db_name + '_expiry.json', 'w') as f:
        #     # json.dump(temp, f)
        #     # json_parser.dump_data(temp, f)
        # json_parser.dump_data(temp, self.db_name + '_expiry.json')
            
        
        # temp.clear()


    """
        Load the database from a JSON file.
    """
    def load(self):

    # Add Wal Support
        json_parser = parser()
        try:
            # with open(self.db_name + '.json', 'r') as f:
                # self.data = json.load(f)
            self.data = json_parser.load_data(self.db_name + '.json')
                
            # with open(self.db_name + '_expiry.json', 'r') as f:
                # self.expiry = json.load(f) 
                # self.expiry = json_parser.load_data(f)
            # self.expiry=json_parser.load_data(self.db_name + '_expiry.json')

             
            # for key, value in self.expiry.items():
            #     if value == 'None':
            #         self.expiry[key] = None
            #     else:
            #         self.expiry[key] = dt.datetime.fromisoformat(str(value)) 
            
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