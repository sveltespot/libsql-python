# PyLibSQL

This is a fork of the original [libsql-experimental-python](https://github.com/tursodatabase/libsql-experimental-python/) project.

> [!CAUTION]
> This is a work in progress and is not yet ready for production use.

## Installation

> [!NOTE]
> This package is not yet available on PyPI and must be installed from source.
> Easiest way to install is to clone the repository, source the virtual environment
> and run `maturin develop`.

```bash
git clone https://github.com/sveltespot/pylibsql.git
cd pylibsql
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install maturin
maturin develop
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
