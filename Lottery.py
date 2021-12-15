import sqlite3
import random

def create_table():
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS warns (id INTEGER,name TEXT,number INTEGER)")
  conn.commit()
  conn.close()

def insert(id,name):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns")
    rows = cur.fetchall()
    try:
      length = rows[-1][2]
    except:
      length = 0
    length = length+1
    cur.execute(f"INSERT INTO warns VALUES(?,?,?)",(id,name,length))
    conn.commit()
    conn.close()
    return length

"""def add(id,name,number):
  conn = sqlite3.connect("lottery.db")
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
  conn = sqlite3.connect("lottery.db")
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
  return mylist"""
def view():
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns")
    rows = cur.fetchall()
    conn.close()
    return rows
def viewspl(id):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns WHERE id=?",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows
def viewnum(number):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns WHERE number=?",(number,))
    rows = cur.fetchall()
    conn.close()
    return rows
def delete(length):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM warns")

    rows = cur.fetchall()
    if rows == []:
      return -1
    for x in rows:
      if x[2] == length:
        break
      continue
    else:
      return -1
    cur.execute(f"DELETE FROM warns WHERE number=?",(x[2],))
    conn.commit()
    conn.close()

def clear():
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM warns")
  rows = cur.fetchall()
  for x in rows:
    value = x[2]
    cur.execute(f"DELETE FROM warns WHERE number=?",(value,))
    conn.commit()
  conn.close()
"""def update(name,amount,interest,final):
    conn = sqlite3.connect("warnings.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE warns SET name=?,length=? WHERE name={name}")
    conn.commit()
    conn.close()"""
create_table()


