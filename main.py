from tkinter import *
from os import walk

window = Tk()
window.geometry("875x500")


class ItemClass:
    def __init__(self, name, cost):
        self.name = name
        self.cost = int(float(cost))
        self.quantity = Entry(window)
        self.quantity.place(x=X_loc + 550, y=Y_loc + 35)

    def printItem(self):
        print(' name: {} , cost {} '.format(self.name, self.cost))

    def getName(self):
        return str(self.name)

    def getCost(self):
        return str(self.cost)

    def getQuantity(self):
        if self.quantity.get() == "":
            return 0;
        return self.quantity.get()

    def resetQuantity(self):
        self.quantity.delete(0, "end")


class MenuCard:
    obj = []

    def __init__(self, heading):
        self.heading = heading
        self.itemDetails = {}
        self.X_loc = 50
        self.Y_loc = 110
        self.quantity = 0
        self.myBillpath = "BILLS"
        self.label_head = Label(window, text=self.heading, font="Times 32 bold")
        self.label_head.place(x=420, y=30, anchor="center")

        self.subMenu = Label(window, text="MENU", font="Times 28 bold")
        self.subMenu.place(x=50, y=60)

        self.BillNo = 1000

    def getLastBillNo(self):
        for i in walk(self.myBillpath):
            for file in i[2]:
                if file.split("_")[0] == "BILL":
                    if int(float(file.split("_")[1].strip(".txt"))) > int(self.BillNo):
                        self.BillNo = int(float(file.split("_")[1].strip(".txt")))
        return self.BillNo;

    def getNextBillNo(self):
        return self.getLastBillNo() + 1

    def getNextBillName(self):
        return '{}\\BILL_{}.txt'.format(self.myBillpath, self.getNextBillNo())

    def UpdateLocation(self, x, y):
        self.X_loc = x
        self.Y_loc = y

    def getLocation(self):
        return self.X_loc, self.Y_loc

    def addItems(self, ItemClass):
        MenuCard.obj.append(ItemClass)
        text2fill = '{:.<30}'.format(ItemClass.getName()) + "Rs." + '{:5}'.format(ItemClass.getCost())
        label = Label(window, text=text2fill, font="Courier 18 ")
        label.place(x=self.X_loc, y=self.Y_loc + 30)
        self.UpdateLocation(self.X_loc, self.Y_loc + 30)

    def resetItemQuantity(self):
        for item in MenuCard.obj:
            item.resetQuantity()
            self.clearSummary()
            obj = []

    def clearSummary(self):
        xxx = 550
        yyy = 300
        for clear_loc in range(yyy, 500, 10):
            label = Label(window, text="                                   ", font="Courier 12 ")
            label.place(x=xxx, y=clear_loc)

    def Summary(self):
        xxx = 550
        yyy = 300
        label = Label(window, text='Bill NO: {}'.format(self.getNextBillNo()), font="Courier 12 ")
        label.place(x=xxx, y=yyy)
        yyy = yyy + 30
        sumof_each = []
        for i in MenuCard.obj:
            sumof_each.append(int(i.getQuantity()) * int(i.getCost()))
            text2fillAgain = '{} {} x Rs.{} = Rs.{} '.format(str(i.getName()), int(i.getQuantity()), int(i.getCost()),
                                                             int(i.getQuantity()) * int(i.getCost()))
            label = Label(window, text=text2fillAgain, font="Courier 12 ")
            label.place(x=xxx, y=yyy)
            yyy = yyy + 20

        label = Label(window, text="---------------------", font="Courier 12 ")
        label.place(x=xxx, y=yyy)
        yyy = yyy + 20
        label = Label(window, text='Total      Rs.{}'.format(str(sum(sumof_each))), font="Courier 12 ")
        label.place(x=xxx, y=yyy)
        yyy = yyy + 20
        label = Label(window, text="---------------------", font="Courier 12 ")
        label.place(x=xxx, y=yyy)


# ==========================
##=== main starts here=====
# ==========================


print("Starting..")
listofitems = []

# heading
a = MenuCard("MY BILLING TOOL")

# --------------------
# reading file
# --------------------
val = []
filename = "CONFIG/config.csv"
# open the file for reading
filehandle = open(filename, 'r')

while True:
    # read a single line
    line = filehandle.readline()

    if not line:
        break
    a1, b1 = line.split(",")
    # val.append(str(a1))
    # val.append(b1.rstrip())

    val.append([a1, b1.strip()])

# close the pointer to that file
filehandle.close()
# --------------------


# --------------------
# creating objects in Menu
# --------------------
for i in val:
    print(i[0])
    X_loc, Y_loc = a.getLocation()
    listofitems.append(ItemClass(i[0].strip('"'), i[1].strip('"')))
    a.addItems(ItemClass(i[0].strip('"'), i[1].strip('"')))
# --------------------


print(MenuCard.obj)

for i in listofitems:
    i.printItem()

def cleanExit():
    window.destroy()

def createBill():
    sumofEach = []
    q_in_list=sum([int(i.getQuantity()) for i in MenuCard.obj])
    if q_in_list>0:
        curr_file = a.getNextBillName()
        with open(curr_file, "x") as writer:
            writer.write("BILL NO:" + str(a.getNextBillNo() - 1) + "\n");
            for i in MenuCard.obj:
                sumofEach.append(int(i.getQuantity()) * int(i.getCost()));
                text2fillAgain = '{} {} x Rs.{} = Rs.{}  {}'.format(str(i.getName()), int(i.getQuantity()),
                                                                    int(i.getCost()),
                                                                    int(i.getQuantity()) * int(i.getCost()), "\n");
                writer.write(text2fillAgain);
            writer.write("---------------------\n");
            text = 'Total      {} {}'.format(str(sum(sumofEach)), "\n");
            writer.write(text);
            writer.write("---------------------\n");
        print("Bill written {}".format(curr_file));
        a.resetItemQuantity();
    else:
        print("Nothing to Bill")






b1 = Button(window, text="biil", width=20, command=createBill)
b1.place(x=100, y=350)

b2 = Button(window, text="Summary", width=20, command=a.Summary)
b2.place(x=100, y=400)

b3 = Button(window, text="Exit", width=20, command=cleanExit)
b3.place(x=100, y=450)

window.mainloop()
