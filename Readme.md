# 🪶 SimpleDB

**SimpleDB** is a lightweight key-value database written in Python from scratch. It provides persistent storage on disk and supports common operations like `SET`, `INCR`, `GET`, `DELETE`, `EXISTS`, `CLEAR`, and `DROP`. The database is accessible via a simple CLI and supports optional TTL key expiry, Write-Ahead Logging (WAL), and pluggable storage formats: `JSON` , `Binary` and `Txt` (Default).

---

## 🚀 Features

- ✅ Key-Value store architecture
- 💾 Persistent file storage on disk
- 🖥️ Simple CLI for executing commands
- ⚡ Fast in-memory access with file sync
- 🧾 Write-Ahead Logging (WAL) for crash recovery
- ⏳ TTL (Time-To-Live) for expiring keys 
- 🧮 Storage format support:
  - `json`: human-readable
  - `binary`: compact and fast
  - `txt`: default
- 🔐 Commands:
  - `SET <key> <value> <seconds>(optional)`  – Insert or update a key with optional expiry time(TTL)
  - `INCR <key>` – Increments value of key by one
  - `GET <key>` – Retrieve a value by key
  - `DELETE <key>` – Remove a key-value pair
  - `EXISTS <key>` – Check if a key exists
  - `CLEAR` – Remove all data
  - `DROP` – Delete the database file permanently
  - `EXIT` – Exit the CLI

---

## 🧑‍💻 Usage

### ▶️ Start the CLI

```bash
python db.py
```

# More features coming soon...
