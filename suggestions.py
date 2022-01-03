import sqlite3
import random

def create_table():
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS suggestions (id INTEGER,context TEXT,entry INTEGER,response TEXT,msgid INTEGER,reason TEXT)")
  conn.commit()
  conn.close()

def delete_table():
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS suggestions")
  conn.commit()
  conn.close()

def insert(id,message,messageid):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM suggestions")
    rows = cur.fetchall()
    try:
      length = rows[-1][2]
    except:
      length = 0
    length = length+1
    response = "Not Answered"
    cur.execute(f"INSERT INTO suggestions VALUES(?,?,?,?,?,?)",(id,message,length,response,messageid,""))
    conn.commit()
    conn.close()
    return length

"""def add(id,name,number):
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM suggestions")
  rows = cur.fetchall()
  cur.execute(f"SELECT * FROM suggestions WHERE id={id}") 
  rows = cur.fetchall()
  if rows == []:
    return -1
  print(rows)
  oldvalue = rows[0]
  oldvalue = oldvalue[2]
  value = rows[0][2]+amount
  cur.execute(f"UPDATE suggestions SET amount=? WHERE id=?",(value,id))
  conn.commit()
  conn.close()
  mylist = [oldvalue,value,amount]
  return mylist

def remove(id,name,amount):
  conn = sqlite3.connect("lottery.db")
  cur = conn.cursor()
  cur.execute(f"SELECT * FROM suggestions WHERE id={id}") 
  rows = cur.fetchall()
  if rows == []:
    return -1
  print(rows)
  oldvalue = rows[0]
  oldvalue = oldvalue[2]
  value = rows[0][2]-amount
  if value < 0:
    return -2
  cur.execute(f"UPDATE suggestions SET amount=? WHERE id=?",(value,id))
  conn.commit()
  conn.close()
  mylist = [oldvalue,value,amount]
  return mylist"""
def view():
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM suggestions")
    rows = cur.fetchall()
    conn.close()
    return rows
def viewspl(entry):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM suggestions WHERE entry=?",(entry,))
    rows = cur.fetchall()
    conn.close()
    return rows
def delete(length):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM suggestions")

    rows = cur.fetchall()
    if rows == []:
      return -1
    for x in rows:
      if x[2] == length:
        break
      continue
    else:
      return -1
    cur.execute(f"DELETE FROM suggestions WHERE number=?",(x[2],))
    conn.commit()
    conn.close()

def addmsg(number,messageid):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE suggestions SET msgid=? WHERE entry=?",(messageid,number))
    conn.commit()
    conn.close()


def update(number,reason,response):
    conn = sqlite3.connect("lottery.db")
    cur = conn.cursor()
    cur.execute(f"UPDATE suggestions SET response=? ,reason=? WHERE entry=?",(response,reason,number))
    conn.commit()
    conn.close()
create_table()


