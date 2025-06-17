import datetime as dt,os
from wal import wal


''' 
A simple key-value database class that uses a Write-Ahead Logging (WAL) mechanism for durability.
This class allows setting, getting, deleting, checking existence, clearing, and dropping the database.
it uses a log file to record operations, ensuring that changes are durable and can be recovered in case of a crash.
'''
class SimpleDB:
    
    '''
    Initialize the simpleDB with a database name and an optional custom WAL flag.
        Args:
            db_name (str): The name of the database file.
            custom_wal (bool): A flag indicating whether to use a custom WAL implementation.
    ''' 
    def __init__(self, db_name,custom_wal=False):
        self.db_name = db_name
        self.data = {}
        self.expiry={}
        self.log_file_name = f"{db_name}.log"
        self.wal = wal(self.log_file_name,custom_wal)
        self.wal.write_log("init", db_name)
        self.load()


    '''
    Set a key-value pair in the database.
        Args:
            key (str): The key to set.
            value (str): The value to associate with the key.
    If the operation is successful, the data is saved to the database file and a log entry is written.
    If the operation fails, an error message is printed.
    '''
    def set(self, key, value, ttl=None):
        if self.wal.write_log( "set", key, value, ttl[0] if ttl else None):
            self.data[key] = value
            if ttl:
                expiry_time = dt.datetime.now() + dt.timedelta(seconds=int(ttl[0]))
                self.expiry[key] = expiry_time
            else:
                self.expiry[key] = None
            self.save()
            if self.wal.custom_wal:
                self.wal.write_log("set", key, value, ttl[0] if ttl else None, state="SUCCESS")
        else:
            print("operation failed")
    
    
    '''
    Increment the value associated with a key in the database.
        Args:
            key (str): The key to increment.
        Returns:
            bool: True if the key exists and was incremented, False otherwise.
    If the key exists, it's value is incremented by 1.
    If the operation is successful, the data is saved to the database file and a log entry is written.
    If the operation fails, an error message is printed.
    '''
    def incr(self,key):
        self.expire_keys()
        if key in self.data:
            try:
                self.wal.write_log("incr", key, self.data[key])
                self.data[key] = int(self.data[key]) + 1
                self.save() 
                if self.wal.custom_wal:
                    self.wal.write_log("incr", key, self.data[key]-1, state="SUCCESS")
                return True
            except ValueError:
                print(f"Value for key '{key}' is not an integer.")
        return False
    

    '''
    Get the value associated with a key in the database.
        Args:
            key (str): The key to retrieve.
        Returns:
            str: The value associated with the key, or None if the key does not exist.
    '''
    def get(self, key):
        self.expire_keys()
        return self.data.get(key, None)
 
 
    '''    
    Delete a key from the database.
        Args:   
            key (str): The key to delete.
    If the operation is successful, the key is removed from the data dictionary and the database file is updated and a log entry is written.
    If the operation fails, an error message is printed.        
    '''
    def delete(self, key):
        if key in self.data:
            self.wal.write_log("delete", key)
            del self.data[key]
            if key in self.expiry:
                del self.expiry[key]
            self.save()
            if self.wal.custom_wal:
                self.wal.write_log("delete", key, state="SUCCESS")
        else:
            print("operation failed")
        
        
    ''' 
    Check if a key exists in the database.
        Args:   
            key (str): The key to check for existence.
        Returns:
            bool: True if the key exists, False otherwise.
    '''
    def exists(self, key):
        self.expire_keys()
        return key in self.data
    
    
    ''' 
    Clear all entries in the database.
    This method removes all keys from the data dictionary and updates the database file.    
    If the operation is successful, a log entry is written.
    If the operation fails, an error message is printed.
    '''
    def clear(self):
        for key in list(self.data.keys()):
            self.delete(key)
        
        
    '''
    Save the current state of the database to the database file.
    This method writes all key-value pairs in the data dictionary to the database file.
    '''
    def save(self):
        with open(self.db_name + '.txt','w') as f:
            for key, value in self.data.items():
                f.write(f"{key}:{value}\n")
        with open(self.db_name + '_expiry.txt', 'w') as f:
            for key, value in self.expiry.items():
                f.write(f"{key}:{value.isoformat() if value else 'None'}\n")
    
    
    '''
        This method checks for keys that have expired based on their TTL (Time To Live).
        If a key has a TTL and the current time exceeds the TTL, the key is deleted from the database.
    '''
    def expire_keys(self):
        current_time = dt.datetime.now()
        keys_to_delete = []
        for key, value in self.expiry.items():
            if value and value <= current_time:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            if key in self.data:
                self.delete(key)  
                print(f"Key '{key}' has expired and has been deleted.")
        self.save()  
    
    '''
    Load the database from the log file.
    This method reads the log file and processes each entry to update the data dictionary.
    If the log file does not exist, it is ignored.
    If an error occurs while reading the log file, an error message is printed.
    '''
    '''
    custom_wal==True
        This block is used to load the database from log file in Compute Efficient way.
        This only performs data operation only if it failed to persist in database file and existed in log file (maintains durability and atomacity).
    
    custom_wal==False
        This block is used to load the database from log file in Memory Efficient way.
        This processes each log entry and updates the database accordingly.
        It is memory efficient as the log file maintains a single log of operations rather than storing the success of operations also.
    '''
    def load(self):
        
        print("Loading database...")
        
        ops=[]
        
        self.load_expiry() 
        if self.wal.custom_wal:
            self.load_database() #Think on this (Compute Overhead)
            self.save() 
            return
        
        try:
            with open(self.log_file_name, 'r') as f:
                for line in f:
                    if self.wal.custom_wal:
                        _, _, _, _, state, operation, key, *extra = line.strip().split(" ")
                    else:
                        _, _, _, state, operation, key, *extra = line.strip().split(" ")
                    operation = operation.lower()
                    state = state.lower()
                    state = state.replace("[", "").replace("]", "")
                    # print(state,operation,key,value)
                    value=extra[0] if extra else None
                    value = ' '.join(value) if value else None
                    print(f"Processing log entry: {line.strip()}")
                    if self.wal.custom_wal:
                        if state == "start" and operation != "init":
                            ops.append((operation, key, value))
                        elif state == "success" and len(ops)>0:
                             ops.pop()
                    elif state == "task" and operation != "init":
                        ops.append((operation, key, value))
        except FileNotFoundError:
            pass
                    
        for operation, key, value in ops:
            if operation == "set":
                self.data[key] = ' '.join(value)
            elif operation == "delete":
                del self.data[key]
            elif operation == "clear":
                for k in list(self.data.keys()):
                    del self.data[k]
            elif operation == "incr":
                self.data[key] = int(value)+1
            elif operation == "drop":
                self.drop()
                
        self.save()
        ops.clear()
        self.expire_keys() 
        
    
    '''
    Drop the database and remove the log file.
    This method clears the data dictionary, closes the log file, and removes both the log file and the database file.
    If an error occurs during deletion, an error message is printed.
    '''
    def drop(self):
        try:
            self.data.clear()
            self.wal.write_log("drop", self.db_name + '.txt')
            self.wal.close_log_file()
            os.remove(self.log_file_name) #order matters (don't know why but first remove log file then database file) maybe because after init if no entry is there, then database file is not created at first place so how can we remove it
            os.remove(self.db_name+ '.txt')
            os.remove(self.db_name + '_expiry.txt')
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error deleting database: {e}")
    
    
    '''
    It is used to load the data from database file.
    '''
    def load_database(self):
        try:
            with open(self.db_name + '.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split(':', 1)
                    self.data[key] = value
        except FileNotFoundError:
            pass
    
    
    '''
    It is used to load the expiry time from database_expiry file.
    '''
    def load_expiry(self):
        try:
            with open(self.db_name + '_expiry.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split(':', 1)
                    if value == 'None':
                        self.expiry[key] = None
                    else:
                        self.expiry[key] = dt.datetime.fromisoformat(value)
        except FileNotFoundError:
            pass
        
    
