#!/usr/bin/env python3

import sqlite3
import pylibsql
import pytest


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_execute(provider):
    conn = connect(provider, ":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    res = conn.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_cursor_execute(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_executemany(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    data = [(1, "alice@example.com"), (2, "bob@example.com")]
    conn.executemany("INSERT INTO users VALUES (?, ?)", data)
    res = cur.execute("SELECT * FROM users")
    assert [(1, "alice@example.com"), (2, "bob@example.com")] == res.fetchall()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_cursor_fetchone(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    data = [(1, "alice@example.com"), (2, "bob@example.com")]
    cur.executemany("INSERT INTO users VALUES (?, ?)", data)
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_cursor_fetchmany(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    data = [
        (1, "alice@example.com"),
        (2, "bob@example.com"),
        (3, "carol@example.com"),
        (4, "dave@example.com"),
        (5, "erin@example.com"),
    ]
    cur.executemany("INSERT INTO users VALUES (?, ?)", data)
    res = cur.execute("SELECT * FROM users")
    assert [(1, "alice@example.com"), (2, "bob@example.com")] == res.fetchmany(2)
    assert [(3, "carol@example.com"), (4, "dave@example.com")] == res.fetchmany(2)
    assert [(5, "erin@example.com")] == res.fetchmany(2)
    assert [] == res.fetchmany(2)


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_cursor_executemany(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    data = [(1, "alice@example.com"), (2, "bob@example.com")]
    cur.executemany("INSERT INTO users VALUES (?, ?)", data)
    res = cur.execute("SELECT * FROM users")
    assert [(1, "alice@example.com"), (2, "bob@example.com")] == res.fetchall()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_lastrowid(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    assert cur.lastrowid is None
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    assert cur.lastrowid == 0
    cur.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    assert cur.lastrowid == 1
    cur.execute("INSERT INTO users VALUES (?, ?)", (2, "bob@example.com"))
    assert cur.lastrowid == 2


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_basic(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    res = cur.execute("SELECT * FROM users")
    assert (
        ("id", None, None, None, None, None, None),
        ("email", None, None, None, None, None, None),
    ) == res.description


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_commit_and_rollback(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    conn.commit()
    cur.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()
    conn.rollback()
    res = cur.execute("SELECT * FROM users")
    assert res.fetchone() is None


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_autocommit(provider):
    conn = connect(provider, ":memory:", None)
    assert conn.isolation_level == None
    assert conn.in_transaction == False
    cur = conn.cursor()
    assert conn.in_transaction == False
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (?, ?)", (1, "alice@example.com"))
    assert conn.in_transaction == False
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()
    conn.rollback()
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_params(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (?, ?)", (1, "alice@example.com"))
    res = cur.execute("SELECT * FROM users")
    assert (1, "alice@example.com") == res.fetchone()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_fetchmany(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (?, ?)", (1, "alice@example.com"))
    cur.execute("INSERT INTO users VALUES (?, ?)", (2, "bob@example.com"))
    res = cur.execute("SELECT * FROM users")
    assert [(1, "alice@example.com"), (2, "bob@example.com")] == res.fetchall()


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_in_transaction(provider):
    conn = connect(provider, ":memory:")
    assert conn.in_transaction == False
    cur = conn.cursor()
    assert conn.in_transaction == False
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (?, ?)", (1, "alice@example.com"))
    cur.execute("INSERT INTO users VALUES (?, ?)", (2, "bob@example.com"))
    assert conn.in_transaction == True


@pytest.mark.parametrize("provider", ["libsql-remote", "libsql", "sqlite"])
def test_fetch_expression(provider):
    conn = connect(provider, ":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, email TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'alice@example.com')")
    res = cur.execute("SELECT QUOTE(email) FROM users")
    assert [("'alice@example.com'",)] == res.fetchall()


def connect(provider, database, isolation_level="DEFERRED"):
    if provider == "libsql-remote":
        from urllib import request
        import os

        sqld_host = os.getenv("SQLD_HOST", "localhost")
        sqld_port = os.getenv("SQLD_PORT", "8080")
        sqld_admin_port = os.getenv("SQLD_ADMIN_PORT", "9090")
        sqld_namespace = os.getenv("SQLD_NAMESPACE", "default")

        sqld_url = f"http://{sqld_host}:{sqld_port}"
        sqld_admin_url = f"http://{sqld_host}:{sqld_admin_port}"
        sqld_namespace_url = f"{sqld_admin_url}/v1/namespaces/{sqld_namespace}"

        # Note: libsql-remote tests requires libsql-server to be running on localhost:8080
        #    and the admin listener enabled and listening on localhost:9090.
        #    The server can be started with the following command:
        #    `sqld --admin-listen-addr 127.0.0.1:9090`

        try:
            res = request.urlopen(f"{sqld_url}/v2")
        except Exception as _:
            pytest.skip("libsql-remote server is not running")
        if res.status != 200:
            pytest.skip("libsql-remote server is not running")

        try:
            # Check if the namespace is created.
            res = request.urlopen(f"{sqld_namespace_url}/stats")
        except Exception as _:
            pytest.skip("libsql-remote admin listener is not enabled")
        if res.status != 200:
            pytest.skip(f"libsql-remote `{sqld_namespace}` namespace is not created")

        # Delete the `default` namespace and the associated database.
        delete_req = request.Request(
            f"{sqld_namespace_url}",
            method="DELETE",
        )
        request.urlopen(delete_req)
        create_req = request.Request(
            f"{sqld_namespace_url}/create",
            method="POST",
            data=b"{}",
        )
        create_req.add_header("Content-Type", "application/json")
        request.urlopen(create_req)

        # ignore the database parameter as ":memory:" is not supported by libsql-remote
        database = "/tmp/test.db"
        if os.path.exists(database):
            os.remove(database)
        return pylibsql.connect(
            database,
            sync_url=f"{sqld_url}",
            auth_token="",
            isolation_level=isolation_level,
        )
    if provider == "libsql":
        return pylibsql.connect(database, isolation_level=isolation_level)
    if provider == "sqlite":
        return sqlite3.connect(database, isolation_level=isolation_level)
    raise Exception(f"Provider `{provider}` is not supported")
