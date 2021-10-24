import sqlite3

def create_table():
  conn = sqlite3.connect("warnings.db")
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS warns (id INTEGER,name TEXT,amount REAL)")
  conn.commit()
  conn.close()

def insert(id,name,amount):
    conn = sqlite3.connect("warnings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns")
    rows = cur.fetchall()
    for x in rows:
      if x[1] == name:
        return -1
        break
      else:
        continue
    cur.execute(f"INSERT INTO warns VALUES(?,?,?)",(id,name,amount))
    conn.commit()
    conn.close()

def add(id,name,amount):
  conn = sqlite3.connect("warnings.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM warns")
  rows = cur.fetchall()
  if id not in rows:
      return -1
  for x in rows:
    if x[0] == id:
      y = x
      break
    else:
      continue
  oldvalue = y[2] 
  value = y[2]+amount
  cur.execute(f"UPDATE warns SET amount={value}, WHERE id={id}")
  conn.commit()
  conn.close()
  mylist = [oldvalue,value,amount]
  return value

def remove(id,name,amount):
  conn = sqlite3.connect("warnings.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM warns")
  rows = cur.fetchall()
  if id not in rows:
      return -1
  for x in rows:
    if x[0] == id:
      y = x
      break
    else:
      continue
  value = y[2]-amount
  cur.execute(f"UPDATE warns SET amount={value}, WHERE id={id}")
  conn.commit()
  conn.close()
  return value
def view(id,name):
    conn = sqlite3.connect("warnings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns")
    rows = cur.fetchall()
    conn.close()
    return rows
"""def delete(name):
    conn = sqlite3.connect("warnings.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM warns WHERE name=?",(name,))
    conn.commit()
    conn.close()"""
"""def update(name,amount,interest,final):
    conn = sqlite3.connect("warnings.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE warns SET amount={amount},interest={interest},final={final} WHERE name={name}")
    conn.commit()
    conn.close()"""
create_table()


