from time import sleep
from display import Window
from sqlHandler import SqlHandler

sqlprocess = SqlHandler()
root = Window(sqlprocess)
root.start()