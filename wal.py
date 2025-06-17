import datetime as dt

'''
Write-Ahead Log (WAL) System for simpleDB
This module implements a simple write-ahead log system for a key-value database.
'''
class wal:
    
    '''
    Initialize the WAL system with a log file name and a custom WAL boolean to mark for custom WAL implementation.
        Args:
           log_file_name (str): The name of the log file to be used.
           custom_wal (bool): A flag indicating whether to use a custom WAL implementation.
    '''
    def __init__(self,log_file_name,custom_wal):
        self.log_file_name = log_file_name
        self.custom_wal = custom_wal
        self.open_log_file()
    
    
    '''
    Open the log file for writing. If the file does not exist, it will be created.
    If the file cannot be opened, an error message will be printed.
    '''
    def open_log_file(self):
        try:
            self.log_file = open(self.log_file_name, 'a+')
            print(f"[Timestamp: {dt.datetime.now()}] [init] Log file '{self.log_file_name}' opened successfully.")
        except IOError as e:
            print(f"[Timestamp: {dt.datetime.now()}] [Error] Error opening log file '{self.log_file_name}': {e}")
            self.log_file = None
    
    
    '''
    Write a log entry for a database operation.
        Args:
            operation (str): The operation being logged (e.g., "set", "delete").
            key (str): The key involved in the operation.
            value (str, optional): The value associated with the key, if applicable.
        Returns:
            bool: True if the log entry was written successfully, False otherwise.
    '''
    def write_log(self, operation, key, value=None, expiry=None,state="START") -> bool:
        operation = operation.upper()
        if self.log_file is None:
            print("Log file is not open. Cannot write log.")
            return False
        
        try:
            if self.custom_wal:
                if value is not None:
                    if expiry is not None:
                        log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] [{state}] {operation} {key} {value} with TTL {expiry} seconds\n"
                    else:
                        log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] [{state}] {operation} {key} {value}\n"
                else:
                    log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] [{state}] {operation} {key}\n"
            else:
                if value is not None:
                    if expiry is not None:
                        log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] {operation} {key} {value} with TTL {expiry} seconds\n"
                    else:
                        log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] {operation} {key} {value}\n"
                else:
                    log_entry = f"[Timestamp: {dt.datetime.now()}] [Task] {operation} {key}\n"
            self.log_file.write(log_entry)
            self.log_file.flush()
            print(f"Logged: {log_entry.strip()}")
            return True
        except IOError as e:
            print(f"[Timestamp: {dt.datetime.now()}] [Error] Error writing to log file '{self.log_file_name}': {e}")
            return False
    
    
    '''
    Read all log entries from the log file.
        Returns:
            list: A list of log entries, each entry as a string.
    '''
    def read_log(self):
        if self.log_file is None:
            print("Log file is not open. Cannot read log.")
            return []
        
        try:
            self.log_file.seek(0)
            log_entries = self.log_file.readlines()
            print(f"Read {len(log_entries)} log entries from '{self.log_file_name}'.")
            return [entry.strip() for entry in log_entries]
        except IOError as e:
            print(f"[Timestamp: {dt.datetime.now()}] [Error] Error reading from log file '{self.log_file_name}': {e}")
            return []
    
    
    '''
    Close the log file if it is open.
    If the file is already closed or was never opened, a message will be printed.
    '''
    def close_log_file(self):
        if self.log_file is not None:
            try:
                self.log_file.close()
                print(f"[Timestamp: {dt.datetime.now()}] [Close] Log file '{self.log_file_name}' closed successfully.")
            except IOError as e:
                print(f"[Timestamp: {dt.datetime.now()}] [Error] Error closing log file '{self.log_file_name}': {e}")
            self.log_file = None
        else:
            print("Log file is already closed or was never opened.")