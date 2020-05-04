
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
        return('Added to database')
    else:
        update_quantity(name,q)
        return('Updated quantity')


def show_stock():
    with conn:
        c.execute("SELECT * FROM manufrStock")
    return c.fetchall()


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


def inc_manu_quantity(name, val):
     # check to see if item is in stock
    with conn:
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]+val
            c.execute("""UPDATE manufrStock SET quantity = :quantity
                            WHERE name = :name""",
                        {'name': name, 'quantity': newQauntity})
            return('Quantity has been added')


def dec_manu_quantity(name, val):
    # check to see if item is in stock
    with conn:
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]-val  # new quantity = old quantity + (-value passed)
            if newQauntity < 0:
                return('Value exceeds quantity stock')
            c.execute("""UPDATE manufrStock SET quantity = :quantity
                        WHERE name = :name""",
                    {'name': name, 'quantity': newQauntity})
            return('Quantity has been reduced')


def remove_stock(name):
    # check to see if item is in stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("DELETE from manufrStock WHERE name = :name",
                    {'name': name})
        return('Item has been deleted')

""" Dealership database/commands """
# Car dealerships need new software to order new cars from the car manufacturer.
# Repair shops, auto stores, and dealerships need to be able to order 
# parts from the car manufacturer to keep their stock from running out
def show_dealer_stock():
    with conn:
        c.execute("SELECT * FROM dealerStock")

    return c.fetchall() 


def insert_dealer_prod(name,q):
    # check to see if item is in Manufacturer stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name':name})
            check = c.fetchone()
        if check is None:
            with conn:
                c.execute("SELECT cost FROM manufrStock WHERE name = :name",{'name':name})
                z = c.fetchone()
                cost = z[0]
                c.execute("INSERT INTO dealerStock VALUES (:name, :quantity, :cost)", {'name': name, 'quantity': q, 'cost': cost})
                del_shop_stock(name,-(q))
            return('Item has been added')
        else:
            del_shop_stock(name,-(q))
            inc_dealer_quantity(name, q)
            return('Updated quantity')

# def update_dealer_cost(name, cost):
#     with conn:
#         c.execute("""UPDATE dealerStock SET cost = :cost
#                     WHERE name = :name""",
#                   {'name': name, 'cost': cost})


def inc_dealer_quantity(name, val):
 
     # check to see if item is in dealerstock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM dealerStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]+val
            c.execute("""UPDATE dealerStock SET quantity = :quantity
                            WHERE name = :name""",
                        {'name': name, 'quantity': newQauntity})
            return('Quantity has been added')


def dec_dealer_quantity(name, val):
    # check to see if item is in dealerstock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM dealerStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]-val  # new quantity = old quantity + (-value passed)
            if newQauntity < 0:
                return('Value exceeds quantity stock')
            c.execute("""UPDATE dealerStock SET quantity = :quantity
                        WHERE name = :name""",
                    {'name': name, 'quantity': newQauntity})
            return('Quantity has been reduced')


def remove_dealer_stock(name):
    # check to see if item is in dealerstock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM dealerStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Not in stock')
    else:
        with conn:
            c.execute("DELETE from dealerStock WHERE name = :name",
                    {'name': name})
        return('Item has been deleted')

""" Repairshop database/commands """
# Repair shops, auto stores, and dealerships need to be able to order 
# parts from the car manufacturer to keep their stock from running out 

def show_shop_stock():
    with conn:
        c.execute("SELECT * FROM shopPartStock")
    return c.fetchall()

def show_manu_order_stock():
     # get the parts stock from Manufacturer
    with conn:
        c.execute("SELECT name, quantity, cost FROM manufrStock WHERE name NOT LIKE '%model%'")
    return c.fetchall() 

def del_shop_stock(name,val):    # remove part stock from manufacturer

    # check to see if part is in manufacturer stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return
    else:
        with conn:
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]+val  # new quantity = old quantity + (-value passed)
            if newQauntity < 0:
                return  # error string output is in add_car_stock
            c.execute("""UPDATE manufrStock SET quantity = :quantity
                        WHERE name = :name""",
                    {'name': name, 'quantity': newQauntity})


def add_shop_stock(name,val):    # add part stock to repairshop
     # check to see if part is in manufacturer stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Invalid input')
    else:
        with conn:
            # check to see if order is more than the manufacturer quantity amount
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]-val
            if newQauntity < 0:
                return('Quantity exceeds Manufacturer stock')
            else:
                c.execute("SELECT quantity FROM shopPartStock WHERE name = :name",{'name': name})
                z = c.fetchone()
                newQauntity = z[0]+val
                c.execute("""UPDATE shopPartStock SET quantity = :quantity
                            WHERE name = :name""",
                        {'name': name, 'quantity': newQauntity})
                return('Part has been ordered')


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

    # check to see if car is in manufacturer stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return
    else:
        with conn:
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]+val  # new quantity = old quantity + (-value passed)
            if newQauntity < 0:
                return  # error string output is in add_car_stock
            c.execute("""UPDATE manufrStock SET quantity = :quantity
                        WHERE name = :name""",
                    {'name': name, 'quantity': newQauntity})


def add_car_stock(name,val):    # add car stock to dealership

    # check to see if car is in manufacturer stock
    with conn:
        #c.execute("SELECT name FROM manufrStock WHERE name = :name LIKE '%car%'", {'name':name})
        c.execute("SELECT name FROM manufrStock WHERE name = :name",{'name':name})
        check = c.fetchone()

    if check is None:
        return('Invalid input')
    else:
        with conn:
            # check to see if order is more than the manufacturer quantity amount
            c.execute("SELECT quantity FROM manufrStock WHERE name = :name",{'name': name})
            z = c.fetchone()
            newQauntity = z[0]-val
            if newQauntity < 0:
                return('Quantity exceeds car stock')
            else:
                c.execute("SELECT quantity FROM dealerStock WHERE name = :name",{'name': name})
                z = c.fetchone()
                newQauntity = z[0]+val
                c.execute("""UPDATE dealerStock SET quantity = :quantity
                            WHERE name = :name""",
                        {'name': name, 'quantity': newQauntity})
                return('Car sent to dealership.')

#conn.close()