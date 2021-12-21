import sqlite3

def create_table():
  conn = sqlite3.connect("warnings.db")
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS warns (id INTEGER,name TEXT,amount INTEGER)")
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
  cur.execute(f"SELECT * FROM warns WHERE id={id}") 
  rows = cur.fetchall()
  if rows == []:
    return -1
  print(rows)
  oldvalue = rows[0]
  oldvalue = oldvalue[2]
  value = rows[0][2]+amount
  cur.execute(f"UPDATE warns SET amount=? WHERE id=?",(value,id))
  conn.commit()
  conn.close()
  mylist = [oldvalue,value,amount]
  return mylist

def remove(id,name,amount):
  conn = sqlite3.connect("warnings.db")
  cur = conn.cursor()
  cur.execute(f"SELECT * FROM warns WHERE id={id}") 
  rows = cur.fetchall()
  if rows == []:
    return -1
  print(rows)
  oldvalue = rows[0]
  oldvalue = oldvalue[2]
  value = rows[0][2]-amount
  if value < 0:
    return -2
  cur.execute(f"UPDATE warns SET amount=? WHERE id=?",(value,id))
  conn.commit()
  conn.close()
  mylist = [oldvalue,value,amount]
  return mylist
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


