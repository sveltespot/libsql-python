# PyLibSQL

This is a fork of the original libsql-experimental-python project.

> [!CAUTION]
> This is a work in progress and is not yet ready for production use.**

## Installation

```bash
pip install pylibsql
```

## Usage

```python
import pylibsql

con = pylibsql.connect("hello.db", sync_url="http://localhost:8080", auth_token="")

con.sync()

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, email TEXT);")
cur.execute("INSERT INTO users VALUES (1, 'penberg@iki.fi')")

print(cur.execute("SELECT * FROM users").fetchone())
```

## Development

### Dependencies

  - Python 3.7+ with pip and venv (Install python-dev package for your distribution)
  - Rust toolchain
  - maturin (install with `pip install maturin`)

### Building
  
  ```bash
  maturin develop
  ```
