'''
Module containing class for taking care of all the sql stuff
'''

import mysql.connector

RESTAURANT_DB = "RestaurantTable"
PENDING_DB = "Pendings"

class SqlHandler:
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(host="localhost",user="root",passwd="",database="Tomato")
        self.cursor  = self.conn.cursor()

    def login(self,uid,pwd):
        query = f"SELECT Name,Password from {RESTAURANT_DB} where RID = '{uid}'"
        self.cursor.execute(query)
        dat = self.cursor.fetchall()
        if dat == []:
            return -1,None
        else:
            dat = dat[0]
            if pwd == dat[1]:
                return 1,dat[0]
            else:
                return 0,None

    def get_restaurants(self) -> list:
        query = f"SELECT Name from {RESTAURANT_DB} where State = 'Open'"
        self.cursor.execute(query)
        return [i[0] for i in self.cursor.fetchall()]

    def get_items(self,restaurant: str) -> dict:
        query = f"SELECT Items from {RESTAURANT_DB} where Name = '{restaurant}'"
        self.cursor.execute(query)
        return eval(self.cursor.fetchall()[0][0])

    def place_order(self,restaurant: str,addr: str,items: list) -> None:
        query = f"INSERT INTO {PENDING_DB} VALUES ((SELECT RID FROM {RESTAURANT_DB} WHERE Name = '{restaurant}'),'{addr}',\"{str(items)}\")"
        self.cursor.execute(query)
        self.conn.commit()

    def set_restaurant_state(self,restaurant: str,state: str) -> None:
        query = f"UPDATE {RESTAURANT_DB} SET State = '{state}' where Name = '{restaurant}'"
        self.cursor.execute(query)
        self.conn.commit()
    
    def get_restaurant_state(self,restaurant: str):
        query = f"SELECT State FROM {RESTAURANT_DB} where Name = '{restaurant}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    def get_pendings(self,restaurant: str) -> list:
        query = f"SELECT Address,Items FROM {PENDING_DB} WHERE RID=(SELECT RID FROM {RESTAURANT_DB} WHERE Name='{restaurant}')"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def complete_pending_order(self,restaurant: str,addr: str) -> None:
        query = f"DELETE FROM {PENDING_DB} WHERE RID=(SELECT RID FROM {RESTAURANT_DB} WHERE Name='{restaurant}') AND Address = '{addr}' LIMIT 1"
        self.cursor.execute(query)
        self.conn.commit()