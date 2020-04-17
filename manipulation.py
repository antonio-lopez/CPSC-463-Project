
import sqlite3

conn = sqlite3.connect('inventory.db')

c = conn.cursor()

""" Manufacturer database/commands """
# The manufacturing facilities are losing track of parts and materials and need a software 
# tool to track all the car parts and materials (e.g. glass, bolts, chairs, steel) 
# that have been purchased and received from suppliers. They may have over 100 different suppliers.

def insert_prod(name,q,cost):
    with conn:
        c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        with conn:
            c.execute("INSERT INTO manufrStock VALUES (:name, :quantity, :cost)", {'name': name, 'quantity': q, 'cost': cost})
        return 'Inserted the stock in DataBase'
    else:
        return 'Stock with same name already present.'

def show_stock():
    with conn:
        c.execute("SELECT * FROM manufrStock")
    return c.fetchall()


def update_cost(name, cost,date):
    with conn:
        c.execute("""UPDATE manufrStock SET cost = :cost
                    WHERE name = :name""",
                  {'name': name, 'cost': cost})


def update_quantity(name, val):
    with conn:
        c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE manufrStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})


def remove_stock(name):
    with conn:
        c.execute("DELETE from manufrStock WHERE name = :name",
                  {'name': name})
        conn.commit()

""" Dealership database/commands """
# Car dealerships need new software to order new cars from the car manufacturer.
# Repair shops, auto stores, and dealerships need to be able to order 
# parts from the car manufacturer to keep their stock from running out
def show_dealer_stock():
    with conn:
        c.execute("SELECT * FROM dealerStock")

    return c.fetchall() 


def insert_dealer_prod(name,q,cost):
    with conn:
        c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        with conn:
            c.execute("INSERT INTO dealerStock VALUES (:name, :quantity, :cost)", {'name': name, 'quantity': q, 'cost': cost})
        return 'Inserted the stock in DataBase'
    else:
        return 'Stock with same name already present.'

def update_dealer_cost(name, cost):
    with conn:
        c.execute("""UPDATE dealerStock SET cost = :cost
                    WHERE name = :name""",
                  {'name': name, 'cost': cost})


def update_dealer_quantity(name, val):
    with conn:
        c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE dealerStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})


def remove_dealer_stock(name):
    with conn:
        c.execute("DELETE from dealerStock WHERE name = :name",
                  {'name': name})
        conn.commit()

""" Repairshop database/commands """
# Repair shops, auto stores, and dealerships need to be able to order 
# parts from the car manufacturer to keep their stock from running out 

def show_shop_stock():
    with conn:
        c.execute("SELECT * FROM shopPartStock")
    return c.fetchall()

def del_shop_stock(name,val):    # remove car stock from manufacturer
    # todo - exception handling to check if car is in stock
    with conn:
        c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE manufrStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})

def add_shop_stock(name,val):    # add car stock to dealership
    # todo - exception handling to check if car is in stock
    with conn:
        c.execute("SELECT quantity FROM shopPartStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE shopPartStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})


""" Customer database/commands """
# Customers need a way to order new and used cars directly from the 
# car manufacturer that can then be picked up at a local dealership
# Solution - no need for customer database, remove car inventory from
# Manufacturer table and add to Dealership car inventory table  

def show_car_stock():
    # get the car stock from Manufacturer
    with conn:
        c.execute("SELECT name, quantity, cost FROM manufrStock WHERE name LIKE '%model%'")

    return c.fetchall() 

def del_car_stock(name,val):    # remove car stock from manufacturer
    # todo - exception handling to check if car is in stock
    with conn:
        c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE manufrStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})

def add_car_stock(name,val):    # add car stock to dealership
    # todo - exception handling to check if car is in stock
    with conn:
        c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE dealerStock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})

#conn.close()