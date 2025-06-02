from simpleDB import simpleDB
def main():
    print
    db_name = input("Enter database name: ").strip()
    db = simpleDB(db_name)
    print(f"Database {db_name} initialized.")
    while True:
        command = input("Enter command (set/get/delete/exists/clear/exit/deleteDatabase): ").strip().lower()
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
        elif command == "deletedatabase":
            db.deleteDatabase()
            print("Database deleted")
            print("\nExiting the database.\n")
            print("Database exited successfully.\n")
            break
        else:
            print("Unknown command")
            
if __name__ == "__main__":
    main()     