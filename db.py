from simpleDB import simpleDB

'''
Main function to interact with the simpleDB.
Prompts the user for commands to set, get, delete, check existence, clear, or drop the database.
'''
def main():
    print("\n\nWelcome to simpleDB!\n\n")
    db_name = input("Enter database name: ").strip()
    custom_wal = input("Use custom WAL(Compute Efficient)  (y/n)? ").strip().lower() == 'y'
    db = simpleDB(db_name,custom_wal)
    print(f"Database {db_name} initialized.")
    while True:
        command = input("Enter command (set/get/delete/exists/clear/drop/exit): ").strip().lower()
        if command == "exit":
            print("\nExiting the database.\n")
            print("Database exited successfully.\n")
            break
        elif command.startswith("set "):
            _, key, value = command.split(maxsplit=2)
            db.set(key, value)
            print(f"Set {key} to {value}")
        elif command.startswith("get "):
            _, key = command.split(maxsplit=1)
            value = db.get(key)
            print(f"{key} = {value}")
        elif command.startswith("delete "):
            _, key = command.split(maxsplit=1)
            db.delete(key)
            print(f"Deleted {key}")
        elif command.startswith("exists "):
            _, key = command.split(maxsplit=1)
            exists = db.exists(key)
            print(f"{key} exists: {exists}")
        elif command == "clear":
            db.clear()
            print("Database cleared")
        elif command == "drop":
            db.drop()
            print("Database deleted")
            print("\nExiting the database.\n")
            print("Database exited successfully.\n")
            break
        else:
            print("Unknown command")
      
            
if __name__ == "__main__":
    main()     