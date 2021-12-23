import sqlite3

def create_table():
  conn = sqlite3.connect("currency.db")
  cur = conn.cursor()
  cur.execute(f"CREATE TABLE IF NOT EXISTS warns (id INTEGER,name TEXT,money INTEGER)")
  conn.commit()
  conn.close()

def delete(id,database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    try:
      cur.execute(f"DELETE FROM {database} WHERE id=?",(id,))
    except:
      return -1
    
    conn.commit()
    conn.close()


def insert(id,name,money,database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {database}")
    rows = cur.fetchall()
    
    cur.execute(f"INSERT INTO {database} VALUES(?,?,?)",(id,name,money))
    conn.commit()
    conn.close()

def update(id,name,money,boolean = True,database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    val = viewnum(id)
    if val == []:
      insert(id,name,0,500)
      val = viewnum(id)
      
    for x in val:
      myval = x[2]
    if boolean == True:
      money = myval + money 
    else:

      if myval -money < 0:
        money = 0 
      else:
        money = myval-money
    
    cur.execute(f"UPDATE {database} SET money=? WHERE id=?",(money,id))
    conn.commit()
    conn.close()


"""
def add(id,name,amount):
  conn = sqlite3.connect("currency.db")
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
  conn = sqlite3.connect("currency.db")
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

"""
def viewnum(id,database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {database} WHERE id=?",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def viewname(name,database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {database} WHERE name=?",(name,))
    rows = cur.fetchall()
    conn.close()
    return rows
def view(database="warns"):
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {database}")
    rows = cur.fetchall()
    conn.close()
    return rows


create_table()