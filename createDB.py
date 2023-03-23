import mysql.connector
import time

# Print Functions
def now():
    return time.strftime("[%H:%M:%S] ",time.localtime(time.time()))

def success(s):
    print(f"{now()} [SUCCESS] {s}")

def info(s):
    print(f"{now()} [INFO] {s}")

def warning(s):
    print(f"{now()} [WARNING] {s}")

def error(s):
    print(f"{now()} [ERROR] {s}")

# -----------------------------------------------------------------------------------
info("Creating Database \"Tomato\" ...")

try:
    con = mysql.connector.connect(host="localhost",user="root",passwd="")
    con.cursor().execute("CREATE DATABASE Tomato")
    con.close()
    success("Database Created Successfully")
except mysql.connector.errors.InterfaceError:
    error("Can't connect to MySql server, try reconnecting")
    exit()
except:
    warning("Database already exists")
con.close()

# -----------------------------------------------------------------------------------
time.sleep(1)
info("Connecting to database ...")

try:
    con = mysql.connector.connect(host="localhost",user="root",passwd="",database="Tomato")
    if con.is_connected():
        success("Successfully Connected")
    else:
        error("Couldn't Connect")
except Exception as e:
    error(e)
    exit()
cur = con.cursor()

# -----------------------------------------------------------------------------------
RESTAURANT_DB = "RestaurantTable"

try:
    sql = f"CREATE TABLE {RESTAURANT_DB} (RID INT(6) PRIMARY KEY, Name VARCHAR(20), Password VARCHAR(30), Items VARCHAR(500), State VARCHAR(5))"
    cur.execute(sql)
except:...

# Data
mtable = [
    {"rid":123456,"name":"StarTucks","password":"startucks2022","items":'{"Cappuccino":"215","Latte":"125","Americano":"240","Mocha":"959","Dragon Fruit refresher":"500","Frappuccino":"959","Black Tea":"150","Java Chip":"299","Parfait":"455","Hot chocolate":"190"}',"state":"Open"},
    {"rid":123457,"name":"TFC","password":"tfc2022","items":'{"Chicken Wings":"150","Chicken Bucket":"649","Chicken Nuggets":"150","Hot Wings":"150","Krushers":"70","Popcorn chicken":"499","Burger Combo":"235","French Fries":"95","Duo Bucket Meal":"469","Twisters":"349"}',"state":"Open"},
    {"rid":123458,"name":"Pizza Tut","password":"pizzatut2022","items":'{"Tandoori onion pizza":"150","Paneer Supreme Pizza":"649","Prawn Grande Pizza":"150","Chicken Exotica":"150","Spiced Meat Balls":"70","Creamy Mushroom Pasta":"499","Magnum Truffle":"235","Garlic bread":"95","Double cheese pizza":"469","Veggie Lover Pizza":"349"}',"state":"Open"},
    {"rid":123459,"name":"McTonald","password":"mctonald2022","items":'{"Happy Meal":"150","Chicken Mcgrill":"649","Maharaja McChicken":"150","Masala Grill Veg":"150","McSpicy paneer":"70","Mc Aloo Tikki":"499","Mc Flurry":"235","Soft serve ":"95","Cheese Burger":"469","McMuffin":"349"}',"state":"Open"},
    {"rid":123460,"name":"Taji Biryani","password":"tajibiryani2022","items":'{"Keema Biryani":"150","Mutton Biryani":"649","Hydrabadi Biryani":"150","Kolkata Biryani":"150","Lucknowi Biryani":"70","Veg Biryani":"499","Paneer Biryani":"235","Callicut Biryani":"95","Chicken Biryani":"469","Chicken Dum Biryani":"349"}',"state":"Open"},
    {"rid":123461,"name":"Tubway","password":"tubway2022","items":'{"Egg And Cheese Sub":"150","Tuna Sub":"649"," Smoked Chicken Sub ":"150","Roasted Chicken Sub":"150","Veggie delight Sub":"70","Ala Patty Sub":"499","Chicken Ranch":"235","Corn and Peas Sub":"95","Paneer Tikka Sub":"469","Mexican Bean Sub":"349"}',"state":"Open"},
    {"rid":123462,"name":"Taramount","password":"taramount2022","items":'{"Mango Mania":"150","Creamy Rose Cake":"649","Chicken Patties":"150","Paneer Patties":"150","Crossiant":"70","Hotdog":"499","Chocolate Chip Pastry":"235","Black Forest Cake":"95","Red Velvet Cake":"469","Mousse":"349"}',"state":"Open"},
    {"rid":123463,"name":"Tominoes","password":"tominoes2022","items":'{"Taco Indiana":"150","Margarita Pizza":"649","Mexican Pizza":"150","Veg Extravaganza":"150","Krispy Chicken Strips":"70","Choco Lava Cake":"499","Barbeque Chicken":"235","Peppy Paneer":"95","Double Cheese Sandwich":"469","Cheesy Jalapeno Pasta":"349"}',"state":"Open"}
]

restaurants = ["StarTucks","TFC","Pizza_Tut","McTonald","Taji_Biryani","Tubway","Taramount","Tominoes"]
# DB Funtions

def insert_main_table(rid,name,password,items,state="Open"):
    sql = "INSERT INTO {} VALUES ({},'{}','{}','{}','{}')".format(RESTAURANT_DB,rid,name,password,items,state)
    info(f"Inserting Field for {name}")
    try:
        cur.execute(sql)
    except Exception as e:
        error(e)
    else:
        success("Inserted successfully")
        con.commit()

info("Starting inserting values to database")

for i in mtable:
    info(f"Inserting data for {i['name']}")
    insert_main_table(**i)

info("Creating Pendings Table")
try:
    cur.execute("CREATE TABLE Pendings (RID INT(6), Address varchar(75), Items varchar(500))")
    success("Successfully created Pendings Table")
except Exception as e:
    error(e)

con.close()