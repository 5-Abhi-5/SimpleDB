from database.SimpleDB import SimpleDB
from database.JsonSimpleDB import JsonSimpleDB
from database.BinarySimpleDB import BinarySimpleDB


'''
Main function to interact with the simpleDB.
Prompts the user for commands to set, get, delete, check existence, clear, or drop the database.
'''
def main():
    print("\n\n\t\t\t\t\tWelcome to SimpleDB!\n\n")
    print("What kind of storage you need (txt/json/binary)?")
    storage_type = input("Enter 'json' for JSON storage or 'binary' for Binary storage (default is txt): ").strip().lower()
    if storage_type == "json":
        db_class = JsonSimpleDB
    elif storage_type == "binary":
        db_class = BinarySimpleDB
    else:
        db_class = SimpleDB
    db_name = input("Enter database name: ").strip()
    custom_wal = input("Use custom WAL(Compute Efficient)  (y/n)? ").strip().lower() == 'y'
    db = db_class(db_name,custom_wal)
    print(f"Database {db_name} initialized.")
    while True:
        command = input("Enter command (set/incr/get/delete/exists/clear/drop/exit): ").strip().lower()
        if command == "exit":
            print("\nExiting the database.\n")
            print("Database exited successfully.\n")
            break
        elif command.startswith("set "):
            _, key, value, *ttl = command.split(maxsplit=3)
            if ttl:
                db.set(key, value, ttl)
                print(f"Set {key} to {value} with TTL {ttl[0]}")
            else:   
                db.set(key, value)
                print(f"Set {key} to {value}")
        elif command.startswith("incr "):
            _, key = command.split(maxsplit=1)
            res = db.incr(key)
            if res:
                print(f"Incremented {key}")
            else:
                print(f"Key {key} does not exist, cannot increment")
        elif command.startswith("get "):
            _, key = command.split(maxsplit=1)
            value = db.get(key)
            print(f"{key} = {value}")
        elif command.startswith("delete "):
            _, key = command.split(maxsplit=1)
            res = db.delete(key)
            if res:
                print(f"Deleted {key}")
            else:
                print(f"Key {key} does not exist, cannot delete")
        elif command.startswith("exists "):
            _, key = command.split(maxsplit=1)
            res = db.exists(key)
            if res:
                print(f"{key} exists")
            else:
                print(f"{key} does not exist")
        elif command == "clear":
            db.clear()
            print("Database cleared")
        elif command == "drop":
            db.drop()
            print("\nExiting the database.\n")
            print("Database exited successfully.\n")
            print("Database deleted")
            break
        else:
            print("Unknown command")
 
      
'''Defines the main entry point for the script.'''
if __name__ == "__main__":
    main()     