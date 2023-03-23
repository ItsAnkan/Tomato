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
sample_data = {
    123456:[('64 Ed. Street, A-Zone, Durgapur-4',"['Black Tea', 'Latte', 'Americano', 'Hot chocolate']"),('20F , Apsara Building Complex, City Center, Durgapur -16',"['Mocha', 'Black Tea', 'Java Chip', 'Latte']"),('H45, Vikram Sarani, Asansol',"['Frappuccino', 'Mocha', 'Americano', 'Latte', 'Cappuccino']"),('10 ABC Colony, C-Zone, Durgapur-7',"['Mocha', 'Frappuccino', 'Hot chocolate']"),('29 D-Block, Sun Apartments, Bidhannagar, Durgapur-15',"['Cappuccino', 'Hot chocolate', 'Latte', 'Americano', 'Java Chip']")],
    123457:[('40 D-3 , Einstein Road, B-Zone, Durgapur - 5',"['Chicken Wings', 'Chicken Bucket', 'Krushers', 'Twisters', 'French Fries']"),('13 Golf Street, A-Zone, Durgapur-3',"['Hot Wings', 'French Fries', 'Krushers']"),('5 Sector C, Bidhannagar, Durgapur - 16',"['Chicken Wings', 'Krushers', 'Popcorn chicken', 'Chicken Nuggets']"),('46 B, 6th Street, Michael Faraday Road, Durgapur - 16',"['Chicken Bucket', 'Duo Bucket Meal']")],
    123458:[('64 Ed. Street, A-Zone, Durgapur-4',"['Chicken Exotica', 'Spiced Meat Balls', 'Double cheese pizza']"),('13/40 Chaffe Street, C-Zone, Durgapur - 6',"['Prawn Grande Pizza', 'Paneer Supreme Pizza', 'Garlic bread', 'Creamy Mushroom Pasta', 'Spiced Meat Balls', 'Veggie Lover Pizza']"),('54 School Road, A-Zone, Durgapur-4',"['Magnum Truffle', 'Prawn Grande Pizza', 'Paneer Supreme Pizza', 'Veggie Lover Pizza']"),('20/13 Chandidas Avenue, B-Zone, Durgapur - 5',"['Tandoori onion pizza', 'Double cheese pizza', 'Garlic bread', 'Prawn Grande Pizza']"),('80 ,Sukanta Bithi, Asansol',"['Chicken Exotica', 'Paneer Supreme Pizza', 'Magnum Truffle']")],
    123459:[('11/15 Nehru Street, A-Zone, Durgapur-4',"['Happy Meal', 'Maharaja McChicken', 'Mc Aloo Tikki', 'Mc Flurry', 'Soft serve ', 'Chicken Mcgrill']"),('2/40 JK Pal Lane, Benachity, Durgapur-13',"['Chicken Mcgrill', 'Happy Meal', 'Cheese Burger', 'Soft serve ', 'McSpicy paneer']"),('7/5 Sukumar Roy Path, C-Zone, Durgapur-9',"['Mc Flurry', 'Soft serve ', 'Cheese Burger']"),('15/4 Kashinath Road, B-Zone, Durgapur - 6',"['Happy Meal', 'Maharaja McChicken', 'Masala Grill Veg', 'Mc Flurry', 'Soft serve ', 'McMuffin']"),('4/5 Dayanad Road, A-Zone, Durgapur-4',"['Maharaja McChicken']"),('43, Mahalaxmi Park Street, Fuljhore, Durgapur - 6',"['Happy Meal', 'Soft serve ', 'McMuffin']")],
    123460:[('40 D-3 , Einstein Road, B-Zone, Durgapur - 5',"['Paneer Biryani', 'Veg Biryani']"),('12, 5th Ave, Sepco Twp, Durgapur-5',"['Kolkata Biryani', 'Chicken Biryani']"),('12/30, Tansen Road, B-Zone, Durgapur-2',"['Hydrabadi Biryani', 'Kolkata Biryani', 'Lucknowi Biryani']")],
    123461:[('1/19, Joydev Rd, B-Zone, Durgapur - 2',"[' Smoked Chicken Sub ', 'Roasted Chicken Sub', 'Chicken Ranch', 'Corn and Peas Sub']"),('18/18, Vivekananda Ave, A-Zone, Durgapur - 5',"['Veggie delight Sub', 'Ala Patty Sub', 'Corn and Peas Sub', 'Paneer Tikka Sub']")],
    123462:[('20/30, Nagarjun Extension, B-Zone, Durgapur - 205',"['Red Velvet Cake', 'Chocolate Chip Pastry', 'Chicken Patties', 'Paneer Patties']"),('25/6, Bengal Ambuja Housing Complex, City Center, Durgapur - 16',"['Crossiant', 'Hotdog', 'Chocolate Chip Pastry']"),('1D/8, Akbar Rd, A-Zone, Durgapur - 04',"['Red Velvet Cake', 'Black Forest Cake', 'Creamy Rose Cake', 'Mango Mania']")],
    123463:[('20/13 Chandidas Avenue, B-Zone, Durgapur - 5',"['Choco Lava Cake', 'Margarita Pizza', 'Cheesy Jalapeno Pasta', 'Peppy Paneer']"),('B1-200/13, Mamra, Durgapur - 10',"['Mexican Pizza', 'Choco Lava Cake', 'Peppy Paneer']"),('2/40 JK Pal Lane, Benachity, Durgapur-13',"['Krispy Chicken Strips', 'Barbeque Chicken', 'Taco Indiana', 'Mexican Pizza']"),('13th St, A-Zone, Durgapur - 5',"['Barbeque Chicken', 'Krispy Chicken Strips', 'Veg Extravaganza', 'Mexican Pizza', 'Double Cheese Sandwich']")],
}
# -----------------------------------------------------------------------------------
PENDING_DB = "Pendings"
for rid in sample_data:
    orders = sample_data[rid]
    if len(orders) > 0:
        info(f"Creating Demo Orders for RID : {rid}")
        for order in orders:
            cur.execute(f"INSERT INTO {PENDING_DB} VALUES ({rid},'{order[0]}',\"{order[1]}\")")
        success("Success !")
success("Sample Data Creating Successfull")

con.commit()
con.close()