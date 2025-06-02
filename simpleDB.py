class simpleDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.data = {}
        self.load()

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data.get(key, None)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save()

    def exists(self, key):
        return key in self.data

    def clear(self):
        self.data.clear()
        for key in list(self.data.keys()):
            del self.data[key]
        self.save()
        
    def save(self):
        with open(self.db_name, 'w') as f:
            for key, value in self.data.items():
                f.write(f"{key}:{value}\n")
    
    def load(self):
        try:
            with open(self.db_name, 'r') as f:
                for line in f:
                    key, value = line.strip().split(':', 1)
                    self.data[key] = value
        except FileNotFoundError:
            pass
    
    def drop(self):
        try:
            import os
            os.remove(self.db_name)
            self.data.clear()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error deleting database: {e}")
    