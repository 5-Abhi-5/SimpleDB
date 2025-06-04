# 🪶 SimpleDB

**SimpleDB** is a lightweight key-value database written in Python. It provides persistent storage on disk and supports common operations like `SET`, `GET`, `DELETE`, `EXISTS`, `CLEAR`, and `DROP`. The database is accessible via a simple CLI with crash recovery using **Write-Ahead Logging (WAL)** (Implemented in two ways one memory efficient and other compute efficient).

---

## 🚀 Features

- ✅ Key-Value store architecture
- 💾 Persistent file storage on disk
- 🖥️ Simple CLI for executing commands
- ⚡ Fast in-memory access with file sync
- 🧾 Write-Ahead Logging (WAL) for crash recovery
- 🔐 Commands:
  - `SET <key> <value>` – Insert or update a key
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
