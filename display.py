from tkinter import *
from tkinter.font import Font

class Window:
    '''
    An instance of tomato™ window
    A sql process instance is passed to handle all sql query calls
    '''
    def __init__(self,sql_process) -> None:
        # Called when new window is intializes using 'Window()', here we set
        # some of the class attributes that have been accessed later
        self.handler = sql_process
        self.active_widgets = []
        self.window = Tk()
        self.icon = PhotoImage(file=".\\Assets\\icon.png")
        self.background = PhotoImage(file=".\\Assets\\background.png")
        self.fonts = {"large":Font(size=14),"title":Font(size=18),"medium":Font(size=12),"small":Font(size=10)}

    def del_running_widgets(self) -> None:
        # Called after each change in frame/page. It destroys the
        # widgets for the previous page(thus helping in transitioning
        # from one page to another and frees up some memory 
        try:
            for i in self.active_widgets:
                try:
                    i.destroy()
                except Exception:
                    pass
        except Exception:
            pass


    def main_frame(self,defrid="",defpwd="",err="") -> None:
        # The first page
        self.del_running_widgets()

        def auth_user():
            _rid = rid.get()
            _pwd = pwd.get()
            if len(_rid) == 0:
                self.main_frame(rid.get(),pwd.get(),"RID Field Cannot be Empty")
            else:
                if len(_pwd) == 0:
                    self.main_frame(rid.get(),pwd.get(),"Password Field Cannot be Empty")
                else:
                    s, r = self.handler.login(_rid,_pwd)
                    if s == 1:
                        self.restaurant_login_frame(r)
                    elif s == 0:
                        self.main_frame(rid.get(),pwd.get(),"Wrong Password")
                    elif s == -1:
                        self.main_frame(rid.get(),pwd.get(),"Wrong RID")

        errMsg = StringVar(value=err)

        main_frame = Label(self.window,height=720,width=1200,image=self.background)
        main_frame.pack_propagate(0)

        err_Lbl = Label(main_frame,textvariable=errMsg,font=Font(size=18,weight='bold'))
        err_Lbl.after(5000,func=lambda : self.main_frame(rid.get(),pwd.get()) if errMsg.get() != "" else lambda : None)
        err_Lbl.pack(side=TOP,pady=50)

        container = Canvas(main_frame,highlightthickness=0)
        container.create_image((305,-224),image=self.background)
        orderBtn = Button(container,text="Order Food",height=2,width=25,command=self.order_frame,relief=RAISED,font=self.fonts['large'])
        loginBtn = Button(container,text="Restaurant Login",height=2,width=25,command=auth_user,relief=RAISED,font=self.fonts['large'])
        uidLbl = Label(container,text="RID",font=self.fonts['medium'])
        pwdLbl = Label(container,text="Pwd",font=self.fonts['medium'])
        rid = Entry(container,background="#5fe868",font=self.fonts['medium'])
        rid.insert(0,defrid)
        rid.focus()
        pwd = Entry(container,background="#5fe868",show="*",font=self.fonts['medium'])
        pwd.insert(0,defpwd)
        
        orderBtn.grid(column=1,row=1,rowspan=2,columnspan=3,padx=10)
        loginBtn.grid(column=4,row=1,rowspan=2,columnspan=3,padx=10)
        uidLbl.grid(column=5,row=3)
        rid.grid(column=6,row=3)
        pwdLbl.grid(column=5,row=4)
        pwd.grid(column=6,row=4)
        container.pack(pady=25,side=BOTTOM,anchor="s")
        main_frame.pack()

        self.active_widgets = [rid,pwd,orderBtn,loginBtn,uidLbl,pwdLbl,container,main_frame]


    def order_frame(self,deferr="") -> None:
        # Order food page
        self.del_running_widgets()
        available = self.handler.get_restaurants()
        menu_items = {}             # Dictionary containing the button objects of the menu items
        restaurant_buttons = {}     # Dictionary containing the button objects of the restaurants
        selected_restaurant = ""    # The current restaurant selected by the user
        selected_items = []         # List containing the menu items selected for ordering
        items = {}                  # Dictionary containing the menu items of a restaurant
        total_price = IntVar(value=0)
        addr = StringVar(value="")
        err = StringVar(value=deferr)

        def deselect_restaurant_buttons():
            # Function for deselecting all the buttons when another button is pressed
            nonlocal menu_items
            for j in menu_items:
                try:
                    menu_items[j].destroy()
                except:
                    pass
            menu_items = {}
            for i in restaurant_buttons:
                restaurant_buttons[i].configure(state=NORMAL,relief=RAISED)
            total_price.set(0)
        
        def restaurant_on_button(evt):
            # Function called when A restaurant is selected
            nonlocal selected_restaurant
            nonlocal selected_items
            nonlocal items
            deselect_restaurant_buttons()
            selected_items = []
            selected_restaurant = evt.widget['text'].replace(" ","_")
            evt.widget.configure(state=DISABLED,relief=SUNKEN)
            items = self.handler.get_items(evt.widget.extra)
            make_food_list(items.keys())
        
        def menu_on_button(evt):
            # Called when a button from the menu side is pressed
            # This handles the "Pressing" and "Releasing" animation
            nonlocal selected_items
            w = evt.widget
            if w['state'] == NORMAL:
                w.config(relief=SUNKEN,state=DISABLED)
                selected_items.append(w["text"])
                total_price.set(total_price.get()+int(items[w["text"]]))
            else:
                w.config(relief=RAISED,state=NORMAL)
                selected_items.remove(w["text"])
                total_price.set(total_price.get()-int(items[w["text"]]))

        def place_order():
            # Called when Place order button is clicked
            nonlocal selected_restaurant
            if addr.get() != "":
                self.handler.place_order(selected_restaurant,addr.get(),selected_items)
                tot = total_price.get()
                deselect_restaurant_buttons() 
                self.payment(selected_restaurant,addr,items,selected_items,tot)
            else:
                deselect_restaurant_buttons()
                self.order_frame("Address field cannot be empty")
            selected_restaurant = ""

        order_frame = Label(self.window,height=720,width=1200,image=self.background)
        order_frame.pack_propagate(0)

        # 'restaurant' side widgets
        restaurants_side_frame = Canvas(order_frame,height=720,width=400,highlightthickness=0)
        restaurants_side_frame.pack_propagate(0)
        restaurants_side_frame.create_image((578,358),image=self.background)
        restaurant_label = Label(restaurants_side_frame,text = "Available Restaurants :",font=self.fonts['title'])
        restaurant_label.pack(side=TOP,pady=5)

        for item in available:
            restaurant_buttons[item] = Button(restaurants_side_frame,text=item,width=300,height=2,font=self.fonts['large'])
            restaurant_buttons[item].bind('<Button-1>',restaurant_on_button)
            restaurant_buttons[item].extra = item
            restaurant_buttons[item].pack(side=TOP,pady=2)
        
        # 'menu' side widgets
        menu_side_frame = Canvas(order_frame,height=720,width=600,highlightthickness=0)
        menu_side_frame.pack_propagate(0)
        menu_side_frame.create_image((22,358),image=self.background)

        addr_segment = Frame(menu_side_frame)
        addr_segment.pack(side=TOP,anchor="nw",pady=10)
        addr_label = Label(addr_segment,text="Address : ",height=1,font=self.fonts["title"])
        addr_input = Entry(addr_segment,font=self.fonts["title"],textvariable=addr,width=50)
        addr_input.focus()
        addr_label.pack(side=LEFT)
        addr_input.pack(side=LEFT)

        bottom_segment = Frame(menu_side_frame)
        bottom_segment.pack(side=BOTTOM)

        pay_button = Button(bottom_segment,text="Place Order",command=place_order,font=self.fonts['large'])
        pay_button.pack(side=LEFT)

        price_segment = Frame(bottom_segment)
        price_segment.pack(side=RIGHT)
        price_label = Label(price_segment,text="Price :",font=self.fonts['large'])
        price_label.pack(side=LEFT)
        price_display = Label(price_segment,textvariable=total_price,font=self.fonts['large'])
        price_display.pack(side=RIGHT)

        errLabel = Label(menu_side_frame,textvariable=err,font=Font(size=14,weight='bold'))
        errLabel.after(1200,func= lambda : self.order_frame() if err.get() != "" else lambda : None)
        errLabel.pack(side=BOTTOM,pady=5)

        def make_food_list(foodlist: list):
            # Called when a new restaurant is selected, this makes the food list in the
            # right side of the screen
            nonlocal menu_items
            for i in foodlist:
                menu_items[i] = Button(menu_side_frame,text=i,width=580,height=2,font=self.fonts['medium'])
                menu_items[i].bind('<Button-1>',menu_on_button)
                menu_items[i].pack(side=TOP,anchor="w",pady=1) 

        restaurants_side_frame.pack(side=LEFT,padx=20)
        menu_side_frame.pack(side=RIGHT,padx=20)

        back = Button(restaurants_side_frame,text="Back",command=self.main_frame,font=self.fonts['medium'])
        back.pack(side=BOTTOM,anchor='sw')

        order_frame.pack(side=LEFT)
        self.active_widgets = [restaurant_label,order_frame]


    def restaurant_login_frame(self,restaurant) -> None:
        # Restaurant login page
        self.del_running_widgets()
        order_buttons = {}      # Dictionary containing the button objects of the pending orders
        state = StringVar(value="Restaurant is "+self.handler.get_restaurant_state(restaurant))
        orders = self.handler.get_pendings(restaurant)
        selected_addr = []      # List containing the addresses selected to be completed

        def set_open():
            self.handler.set_restaurant_state(restaurant,"Open")
            state.set("Restaurant is "+self.handler.get_restaurant_state(restaurant))

        def set_close():
            self.handler.set_restaurant_state(restaurant,"Closed")
            state.set("Restaurant is "+self.handler.get_restaurant_state(restaurant))

        def pendings_list_handler() -> None:
            nonlocal orders
            nonlocal selected_addr
            nonlocal order_buttons
            for i in selected_addr:
                for j in orders:
                    if j[0] == i:
                        orders.remove(j)
            for i in selected_addr:
                self.handler.complete_pending_order(restaurant,i)
            selected_addr = []
            for button in order_buttons.values():
                button.destroy()
            order_buttons = {}
            pending_buttons(orders)

        def bSelect(event: Event):
            w = event.widget
            if w['state'] == NORMAL:
                w.config(relief=SUNKEN,state=DISABLED)
                selected_addr.append(w.extra)
            else:
                w.config(relief=RAISED,state=NORMAL)
                selected_addr.remove(w.extra)

        restaurant_frame = Label(self.window,height=720,width=1200,image=self.background)
        restaurant_frame.pack_propagate(0)

        buttons = Canvas(restaurant_frame,height=720,width=200,highlightthickness=0)
        buttons.create_image((593,358),image=self.background)
        buttons.pack_propagate(0)
        pendings = Canvas(restaurant_frame,height=720,width=900,highlightthickness=0)
        pendings.create_image((307,358),image=self.background)
        pendings.pack_propagate(0)

        # 'buttons' widgets 
        rest_name = Label(buttons,text=restaurant,font=Font(size=20,weight='bold',underline=1))
        state_label = Label(buttons,textvariable=state,font=Font(size=15,weight='bold'))
        bOpen = Button(buttons,text = "Open",command=set_open,font=Font(size=13))
        bClose = Button(buttons,text = "Close",command=set_close,font=Font(size=13))
        bLogout = Button(buttons,text="Logout",command=self.main_frame,font=Font(size=15))

        # 'pendings' widgets
        label = Label(pendings,text="Pending orders :",font=Font(size=16,weight='bold'))
        label.pack(side=TOP)

        bUpdate = Button(pendings,text="Update Pendings List",command=pendings_list_handler,font=Font(size=12))

        def pending_buttons(orders):
            # Funtion for creating the buttons for the pending orders
            nonlocal order_buttons
            for i in range(len(orders)):
                order_buttons[i+1] = Button(pendings,height=3,width=200,text=",".join(eval(orders[i][1]))+f" @ {orders[i][0]}",font=self.fonts["small"])
                order_buttons[i+1].bind('<Button-1>',bSelect)
                order_buttons[i+1].extra = orders[i][0]

            for b in order_buttons:
                order_buttons[b].pack(side=TOP,pady=3)

        bUpdate.pack(side=BOTTOM,anchor=E,padx=10,pady=5)

        rest_name.pack(side=TOP)
        state_label.pack(side=TOP,pady=5)
        bOpen.pack(side=TOP,pady=3)
        bClose.pack(side=TOP,pady=3)
        bLogout.pack(side=BOTTOM,pady=3)

        buttons.pack(side=LEFT,padx=5)
        pendings.pack(side=RIGHT,padx=5)
        restaurant_frame.pack()

        pendings_list_handler()

        self.active_widgets = [bOpen,bClose,bLogout,pendings,buttons,restaurant_frame]


    def payment(self,restaurant,addr,items,ordered,total):
        # Called when Payment is made
        def format(addr):
            if len(addr) > 25:
                lno = 0
                addr = addr.split()
                lines = []
                s = ""
                for i in addr:
                    if lno > 0:
                        if len(s) < 35:
                            s+= i + " "
                        else:
                            lines.append(s)
                            s = i + " "
                    else:
                        if len(s) < 25:
                            s+= i + " "
                        else:
                            lines.append(s)
                            lno = 1
                            s = i + " "
                lines.append(s)
                return "Delivery Address : " + lines[0] + "\n" + "\n          ".join([i for i in lines[1:]])
            else:
                return "Delivery Address : " + addr

        window = Toplevel()
        window.iconphoto(False,self.icon)
        window.resizable(0,0)

        success_label = Label(window,text="Payment Successfull !",font=Font(size=15))
        cheque_label = Label(window,text="Receipt",font=Font(size=20,weight="bold",underline=1))
        success_label.pack(side=TOP,pady=5)
        cheque_label.pack(side=TOP,pady=3)

        details_frame = Frame(window)
        details_frame.pack(side=TOP)
        restaurant_label = Label(details_frame,text="Restaurant Name : "+restaurant.replace("_"," "),font=Font(size=13,weight="bold"))
        addr_label = Label(details_frame,text=format(addr.get()),font=Font(size=13))
        addr.set("")
        restaurant_label.pack(side=TOP,pady=2,anchor=NW,padx=5)
        addr_label.pack(side=TOP,anchor=NW,pady=2,padx=5)

        items_frame = Frame(window)
        items_frame.pack(side=TOP,pady=(10,5))
        Label(items_frame,text="Item",font=Font(size=13,weight='bold',underline=1)).grid(column=1,row=1,padx=5)
        Label(items_frame,text="Price",font=Font(size=13,weight='bold',underline=1)).grid(column=2,row=1,padx=10,sticky="e")
        for i in range(len(ordered)):
            Label(items_frame,text=ordered[i],font=Font(size=12),justify=LEFT).grid(column=1,row=i+2,padx=5,sticky="w")
            Label(items_frame,text="₹"+items[ordered[i]],font=Font(size=12,slant='italic')).grid(column=2,row=i+2,padx=10,sticky="e")
        Label(items_frame,width=10,text="Total = ₹"+str(total),font=Font(size=13,weight='bold')).grid(column=2,row=i+3,padx=10,sticky="e")

        bottom_frame = Frame(window,width=100)
        bottom_frame.pack(pady=10)
        ok_btn = Button(bottom_frame,text="OK!",command=window.destroy,font=Font(size=13))
        ok_btn.pack()

        window.after(15000,window.destroy)

        window.mainloop()


    def start(self) -> None:
        # Called to start the window, used for setting up some things
        # and running the first page.
        self.window.title("tomato™")
        self.window.geometry('1200x720')
        self.window.resizable(0,0)
        self.window.iconphoto(False,self.icon)
        self.main_frame()
        self.window.mainloop()