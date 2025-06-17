from SimpleDB import SimpleDB
import pickle,os

# Todo- implement serialization and deserialization from scratch
"""
    BinarySimpleDB is a subclass of SimpleDB that uses binary serialization for data storage.
    It inherits all methods from SimpleDB and overrides the save and load methods
    to use binary serialization.
"""
class BinarySimpleDB(SimpleDB):

    '''
        Save the database to a binary file.
    '''
    def save(self):
        with open(self.db_name + '.bin', 'wb') as f:
            pickle.dump(self.data, f)
        with open(self.db_name + '_expiry.bin', 'wb') as f:
            pickle.dump(self.expiry, f)


    '''
        Load the database from a binary file.
    '''
    def load(self):
    # Add Wal Support
        try:
            with open(self.db_name + '.bin', 'rb') as f:
                self.data = pickle.load(f)
            with open(self.db_name + '_expiry.bin', 'rb') as f:
                self.expiry = pickle.load(f)
        except FileNotFoundError:
            self.data = {}
            
    '''
        Drop the database by deleting the binary file.
    '''
    def drop(self):
        try:
            self.data.clear()
            self.wal.write_log("drop", self.db_name + '.bin')
            self.wal.close_log_file()
            os.remove(self.db_name + '.bin')
            os.remove(self.log_file_name)
            os.remove(self.db_name + '_expiry.bin')
        except FileNotFoundError:
            pass