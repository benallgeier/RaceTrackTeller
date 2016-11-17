""" raceTrackTeller.py

    Allows user to:
    
    enter bets on horse races,
    to enter the winning horses and payouts
    to cash out,
    to see all unpaid winning bets,
    and to see history of bets.
"""

from betClass import *
from raceClass import *
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

#################  Initialize number of races and horses in races ######

class getStarted(Tk):
  def __init__(self):
    Tk.__init__(self)
    self.title("RaceTrackTeller")
    self.btn = Button(self, text = "Get Started!", command = self.starterWindow,
           width = 18).grid()
 
   

  def starterWindow(self):
    self.numberRaces = simpledialog.askinteger("", "How many races are today?",
                                        initialvalue = 1)
    self.numberHorsesList = []
    
    if not self.numberRaces: # Cancel
      return
    for i in range(self.numberRaces):
      number = simpledialog.askinteger("", "How many horses are in race {}?".format(i+1),
                                       initialvalue = 1)
      if number is None: # Cancel
        return
      self.numberHorsesList.append(number)

    self.app = App(self.numberRaces, self.numberHorsesList)

 ##########################  Main app  #################################   

class App(Tk):
  def __init__(self, numberRaces, numberHorsesList):    
    Tk.__init__(self)

    # setting background to black
    self["bg"] = "#000"
    # could change the 3 to most recent bet!
    self.title("Come on 3!")
    # for debugging
    print("number of races: {}".format(numberRaces))
    print("number of horses in the races: {}".format(numberHorsesList))
    # initialize the number of races and the number of horses in races
    self.setNumberRaces(numberRaces)
    self.setNumberHorsesList(numberHorsesList)
    # for debugging
    print("number of races: {}".format(self.numberRaces))
    print("number of horses in the races: {}".format(self.numberHorsesList))

    # Wanted to initialize as a list with and then append new bettor
    # but couldn't deal with the initialization
    # efficient way to do this?
    self.setBettors()

    # create the races
    self.races = []
    for i in range(self.numberRaces):
      self.races.append(Race(i + 1, self.numberHorsesList[i]))
    #print(self.races[0].numberHorses, self.races[1].numberHorses)

    # we will keep track of bets
    self.bets = []
      

    # create the four main frames
    self.placeBetsFrame = PlaceBets(self)
    self.raceResultsFrame = RaceResults(self)
    self.cashOutFrame = CashOut(self)
    self.historyFrame = History(self)

    self.placeBetsFrame.grid(row = 1, columnspan = 6)

    # create the four main buttons
    self.placeBetsButton = Button(self, text = "Place Bets",
                                command = self.placeBetsSwitch)
    self.placeBetsButton.grid(row = 0, column = 0)

    self.raceResultsButton = Button(self, text = "Race Results",
                                    command = self.raceResultsSwitch)
    self.raceResultsButton.grid(row = 0, column = 1)

    self.cashOutButton = Button(self, text = "Cash Out",
                                command = self.cashOutSwitch)
    self.cashOutButton.grid(row = 0, column = 2)

    self.historyButton = Button(self, text = "History",
                                command = self.historySwitch)
    self.historyButton.grid(row = 0, column = 3)

 # create the functions for switching frames
    self.frames = (self.placeBetsFrame, self.raceResultsFrame,
                self.cashOutFrame, self.historyFrame)
    
  def placeBetsSwitch(self):
    for frame in self.frames:
      frame.grid_remove()
 #   self.tmplbl.grid_remove()
    self.placeBetsFrame.grid(row = 1, column = 0, columnspan = 4)

  def raceResultsSwitch(self):
    for frame in self.frames:
      frame.grid_remove()
    self.raceResultsFrame.grid(row = 1, column = 0, columnspan = 4)

  def cashOutSwitch(self):
    for frame in self.frames:
      frame.grid_remove()
      self.cashOutFrame.grid(row = 1, column = 0)

  def historySwitch(self):
    for frame in self.frames:
      frame.grid_remove()
    self.historyFrame.grid(row = 1, column = 0)
    

  # setters and getters for initiating app
  def setNumberRaces(self, numberRaces):
    self.__numberRaces = numberRaces
  def getNumberRaces(self):
    return self.__numberRaces
  numberRaces = property(fset = setNumberRaces, fget = getNumberRaces)

  def setNumberHorsesList(self, numberHorsesList):
    self.__numberHorsesList = numberHorsesList
  def getNumberHorsesList(self):
    return self.__numberHorsesList
  numberHorsesList = property(fset = setNumberHorsesList, fget = getNumberHorsesList)

  def setBettors(self):
    self.__bettors = ["Fake Bettor"]

  def getBettors(self):
    return self.__bettors

  bettors = property(fset = setBettors, fget = getBettors)
  

  def addBettor(self):
    bettor = self.placeBetsFrame.newBettorEntry.get()
    print("bettor", bettor)
    if bettor in self.bettors:
      messagebox.showinfo(title = "Bettor Clash", message = "Name already used.")
    else:
      self.bettors.append(bettor)
      print(self.bettors)
      self.placeBetsFrame.bettorsList.insert(END, bettor)
      
  ######## inconsistent use of curselection -- see getTotals -- got lucky here
  def addHorses(self):
    # if no race number is selected, we can't update horses
    if self.placeBetsFrame.raceList.curselection() == ():
      messagebox.showinfo(title = "Can't Update Horses", message = "Please select a race number")
    else:
      raceNumber = self.placeBetsFrame.raceList.curselection()[0]
      raceNumber = int(raceNumber)
      numberHorses = self.numberHorsesList[raceNumber]
      print("Number of Horses: {}".format(numberHorses))
      for list in (self.placeBetsFrame.horsesList,
                   self.placeBetsFrame.horsesList2, self.placeBetsFrame.horsesList3,
                   self.placeBetsFrame.horsesList4):
        list.delete(0, END)
        if numberHorses > 9:
          list["height"] = numberHorses
        for number in range(numberHorses):
          list.insert(END, number + 1)
      print("numberHorses: {}".format(numberHorses))


  def getTotals(self):
    # first we create a bet from the selected information
    # then we get the number of bets and the cost from the BetClass
    
    ###### add in dialog if any of the last 4 entries are empty
    ###### give dialog if entry is not a float

    bettorSelected = self.placeBetsFrame.bettorsList.curselection()
    bettor = self.placeBetsFrame.bettorsList.get(bettorSelected[0])
    print("bettor", bettor)
    

    raceNumber = self.placeBetsFrame.raceList.curselection()
    print("raceSelected", raceNumber)
    print("raceSelected[0]", raceNumber[0])
    print("type raceSelected[0]", type(raceNumber[0]))
    race = self.placeBetsFrame.raceList.get(int(raceNumber[0]))
    race = int(race)
    print("race", race)

    amount = self.placeBetsFrame.amountEntry.get()
    print(type(amount))
    amount = float(amount)
    print("amount", amount)

    betTypeSelected = self.placeBetsFrame.typeList.curselection()
    betType = self.placeBetsFrame.typeList.get(betTypeSelected[0])
    print("type", betType)

    horses = []
    # we only want horses from the first horse list -- we get a list
    if betType in (
      "Win", "Place", "Show", "Exacta Box", "Trifecta Box", "Superfecta Box"):
      horsesSelected = self.placeBetsFrame.horsesList.curselection()
      print("horsesSelected", horsesSelected)
      print("First horse", self.placeBetsFrame.horsesList.get(horsesSelected[0]))
      print("First horse type", type(self.placeBetsFrame.horsesList.get(horsesSelected[0])))
      for i in range(len(horsesSelected)):
        horses.append(self.placeBetsFrame.horsesList.get(horsesSelected[i]))
      print("horses", horses)

    elif betType == "Exacta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      # we need to form a list with two sublists
      firstList = []
      secondList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      print("horses", horses)

    elif betType == "Trifecta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      horsesSelected3 = self.placeBetsFrame.horsesList3.curselection()
    # we need to form a list with three sublists
      firstList = []
      secondList = []
      thirdList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      for third in range(len(horsesSelected3)):
        thirdList.append(self.placeBetsFrame.horsesList3.get(horsesSelected3[third]))
      horses.append(thirdList)
      print("horses", horses)

    elif betType == "Superfecta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      horsesSelected3 = self.placeBetsFrame.horsesList3.curselection()
      horsesSelected4 = self.placeBetsFrame.horsesList4.curselection()
    # we need to form a list with four sublists
      firstList = []
      secondList = []
      thirdList = []
      fourthList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      for third in range(len(horsesSelected3)):
        thirdList.append(self.placeBetsFrame.horsesList3.get(horsesSelected3[third]))
      horses.append(thirdList)
      for fourth in range(len(horsesSelected4)):
        fourthList.append(self.placeBetsFrame.horsesList4.get(horsesSelected4[fourth]))
      horses.append(fourthList)
      print("horses", horses)

    bet = Bet(bettor, raceNumber, amount, betType, horses)

    (bets, cost) = (bet.totalBets, bet.cost)
    print("bets" , bets)
    print("cost", cost)

    # add total bets to totalBetsEntry
    self.placeBetsFrame.totalBetsEntry.delete(6, END)
    self.placeBetsFrame.totalBetsEntry.insert(6, bet.getTotalBets())

    # add cost to costEntry
    self.placeBetsFrame.costEntry.delete(6, END)
    self.placeBetsFrame.costEntry.insert(6, bet.getCost())
    
  # unfortunately, I think I need to repeat most of the code
  # from getTotals
  def confirmBet(self):
    # first we create a bet from the selected information
    # then we add the bet to self.bets
    
    ###### add in dialog if any of the last 4 entries are empty
    ###### give dialog if entry is not a float

    bettorSelected = self.placeBetsFrame.bettorsList.curselection()
    bettor = self.placeBetsFrame.bettorsList.get(bettorSelected[0])
    print("bettor", bettor)
    

    raceNumber = self.placeBetsFrame.raceList.curselection()
    print("raceSelected", raceNumber)
    print("raceSelected[0]", raceNumber[0])
    print("type raceSelected[0]", type(raceNumber[0]))
    race = self.placeBetsFrame.raceList.get(int(raceNumber[0]))
    race = int(race)
    print("race", race)

    amount = self.placeBetsFrame.amountEntry.get()
    print(type(amount))
    amount = float(amount)
    print("amount", amount)

    betTypeSelected = self.placeBetsFrame.typeList.curselection()
    betType = self.placeBetsFrame.typeList.get(betTypeSelected[0])
    print("type", betType)

    horses = []
    # we only want horses from the first horse list -- we get a list
    if betType in (
      "Win", "Place", "Show", "Exacta Box", "Trifecta Box", "Superfecta Box"):
      horsesSelected = self.placeBetsFrame.horsesList.curselection()
      print("horsesSelected", horsesSelected)
      print("First horse", self.placeBetsFrame.horsesList.get(horsesSelected[0]))
      print("First horse type", type(self.placeBetsFrame.horsesList.get(horsesSelected[0])))
      for i in range(len(horsesSelected)):
        horses.append(self.placeBetsFrame.horsesList.get(horsesSelected[i]))
      print("horses", horses)

    elif betType == "Exacta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      # we need to form a list with two sublists
      firstList = []
      secondList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      print("horses", horses)

    elif betType == "Trifecta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      horsesSelected3 = self.placeBetsFrame.horsesList3.curselection()
    # we need to form a list with three sublists
      firstList = []
      secondList = []
      thirdList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      for third in range(len(horsesSelected3)):
        thirdList.append(self.placeBetsFrame.horsesList3.get(horsesSelected3[third]))
      horses.append(thirdList)
      print("horses", horses)

    elif betType == "Superfecta":
      horsesSelected1 = self.placeBetsFrame.horsesList.curselection()
      horsesSelected2 = self.placeBetsFrame.horsesList2.curselection()
      horsesSelected3 = self.placeBetsFrame.horsesList3.curselection()
      horsesSelected4 = self.placeBetsFrame.horsesList4.curselection()
    # we need to form a list with four sublists
      firstList = []
      secondList = []
      thirdList = []
      fourthList = []
      for first in range(len(horsesSelected1)):
        firstList.append(self.placeBetsFrame.horsesList.get(horsesSelected1[first]))
      horses.append(firstList)
      for second in range(len(horsesSelected2)):
        secondList.append(self.placeBetsFrame.horsesList2.get(horsesSelected2[second]))
      horses.append(secondList)
      for third in range(len(horsesSelected3)):
        thirdList.append(self.placeBetsFrame.horsesList3.get(horsesSelected3[third]))
      horses.append(thirdList)
      for fourth in range(len(horsesSelected4)):
        fourthList.append(self.placeBetsFrame.horsesList4.get(horsesSelected4[fourth]))
      horses.append(fourthList)
      print("horses", horses)

    bet = Bet(bettor, raceNumber, amount, betType, horses)
    self.bets.append(bet)
    print(self.bets)

  def addResults(self):
    pass
  

#####################   Place Bets Frame #############################


class PlaceBets(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self["bg"] = "#070"
    
    # add New Bettor row
    Label(self, text = "New Bettor: ").grid(row = 0, column = 0)
    self.newBettorEntry = Entry(self, width = 12)
    self.newBettorEntry.grid(row = 0, column = 1)
    self.addBettorButton = Button(self, text = "Add Bettor", command = parent.addBettor)
    self.addBettorButton.grid(row = 0, column = 2)

    # add components for putting in bet

    # Listbox of bettors
    Label(self, text = "Bettor").grid(row = 1, column = 0)    
    self.bettorsList = Listbox(self, height = 9, width = 12,
                               exportselection = False)
    self.bettorsList.grid(row = 2, column = 0)
    # insert "Fake Bettor", which is the only initial name in bettors
    # addBettor from App adds bettors when Add Bettor button is selected
    self.bettorsList.insert(END, parent.bettors[0])
    
    # Listbox of race numbers
    Label(self, text = "Race").grid(row = 1, column = 1)
    self.raceList = Listbox(self, height = 9, width = 5,
                            exportselection = False)
    self.raceList.grid(row = 2, column = 1)
    for i in range(parent.numberRaces):
      self.raceList.insert(END, i + 1)

    # Entry for amount of bet (not total cost of bet)
    Label(self, text = "Amount").grid(row = 1, column = 2)
    self.amountEntry = Entry(self, width = 5)
    self.amountEntry.grid(row = 2, column = 2)

    # Listbox for types of bets
    Label(self, text = "Type").grid(row = 1, column = 3)
    self.typeList = Listbox(self, height = 9, width = 12, exportselection = False)
    self.typeList.grid(row = 2, column = 3)
    for betType in ("Win", "Place", "Show", "Exacta", "Exacta Box",
                 "Trifecta", "Trifecta Box", "Superfecta", "Superfecta Box"):
      self.typeList.insert(END, betType)

    # We add four lists for horses
    #### I want to hide the last three unless they are needed
    #### Could Update Horses after Race number and type are selected
    #### then use bet type to determine which horse lists to hide or show
    Label(self, text = "Horses").grid(row = 1, column = 5, columnspan = 4)
    
    self.horsesList = Listbox(self, height = 9, selectmode = EXTENDED, width = 4,
                              exportselection = False)
    self.horsesList.grid(row = 2, column = 5)

    self.horsesList2 = Listbox(self, height = 9, selectmode = EXTENDED, width = 4,
                               exportselection = False)
    self.horsesList2.grid(row = 2, column = 6)

    self.horsesList3 = Listbox(self, height = 9, selectmode = EXTENDED, width = 4,
                               exportselection = False)
    self.horsesList3.grid(row = 2, column = 7)

    self.horsesList4 = Listbox(self, height = 9, selectmode = EXTENDED, width = 4,
                               exportselection = False)
    self.horsesList4.grid(row = 2, column = 8)

    # add button that will populate horse numbers in the horse listboxes
    self.updateHorsesButton = Button(self, text = "Update Horses",
                                     command = parent.addHorses)
    self.updateHorsesButton.grid(row = 3, column = 1)

    # add button so bettor can see number of bets and cost
    self.getTotalsButton = Button(self, text = "Get Totals",
                                  command = parent.getTotals)
    self.getTotalsButton.grid(row = 3, column = 3)
    
    # add button to actually place bet
    self.addToBetsButton = Button(self, text = "Make Bet", command = parent.confirmBet)
    self.addToBetsButton.grid(row = 3, column = 4)

    # we add entries for total bets and cost of bet

    # entry for total bets 
    self.totalBetsEntry = Entry(self, width = 9)
    self.totalBetsEntry.insert(0, "Bets: ")
    self.totalBetsEntry.grid(row = 4, column = 3)

    # entry for cost
    self.costEntry = Entry(self, width = 10)
    self.costEntry.insert(0, "Cost: ")
    self.costEntry.grid(row = 4, column = 4)
    

#####################   Race Results #############################
class RaceResults(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self["bg"] = "#070"

    # add the label for race -- user must pick a race
    # to enter information for
    Label(self, text = "Race").grid(row = 0, column = 0)

    # user picks race from radio buttons
    self.raceBtns = []
    self.raceRadVar = IntVar()
    for i in range(parent.numberRaces):
      self.raceBtns.append(
        Radiobutton(self, text = i + 1, variable = self.raceRadVar, value = i + 1))
      self.raceBtns[i].grid(row = i + 1, column = 0)

    # add Label to let user know to enter top 4 horses
    Label(self, text = "Top 4 horses").grid(row = 0, column = 1, columnspan = 4)

    # add label for 1st place horse in selected race
    Label(self, text = "1st").grid(row = 1, column = 1)
    # add Entry to enter first place horse
    self.firstEntry = Entry(self, width = 3)
    self.firstEntry.grid(row = 2, column = 1)

    # add label for 2nd place horse in selected race
    Label(self, text = "2nd").grid(row = 1, column = 2)
    # add Entry to enter second place horse
    self.secondEntry = Entry(self, width = 3)
    self.secondEntry.grid(row = 2, column = 2)

    # add label for 3rd place horse in selected race
    Label(self, text = "3rd").grid(row = 1, column = 3)
    self.thirdEntry = Entry(self, width = 3)
    self.thirdEntry.grid(row = 2, column = 3)

    # add label for 4th place horse in selected race
    Label(self, text = "4th").grid(row = 1, column = 4)
    self.fourthEntry = Entry(self, width = 3)
    self.fourthEntry.grid(row = 2, column = 4)

    # add labels to aid in entering payouts
    Label(self, text = "Payouts").grid(row = 0, column = 5, columnspan = 6)
    Label(self, text = "Win").grid(row = 1, column = 5)
    Label(self, text = "Place").grid(row = 1, column = 6)
    Label(self, text = "Show").grid(row = 1, column = 7)
    Label(self, text = "Exacta").grid(row = 1, column = 8)
    Label(self, text = "Trifecta").grid(row = 1, column = 9)
    Label(self, text = "Superfecta").grid(row = 1, column = 10)

    # add entries for these payouts
    self.firstWinEntry = Entry(self, width = 3)
    self.firstWinEntry.grid(row = 2, column = 5)

    self.firstPlaceEntry = Entry(self, width = 3)
    self.firstPlaceEntry.grid(row = 2, column = 6)

    self.firstShowEntry = Entry(self, width = 3)
    self.firstShowEntry.grid(row = 2, column = 7)

    self.secondPlaceEntry = Entry(self, width = 3)
    self.secondPlaceEntry.grid(row = 3, column = 6)

    self.secondShowEntry = Entry(self, width = 3)
    self.secondShowEntry.grid(row = 3, column = 7)

    self.thirdShowEntry = Entry(self, width = 3)
    self.thirdShowEntry.grid(row = 4, column = 7)

    self.exactaEntry = Entry(self, width = 3)
    self.exactaEntry.grid(row = 2, column = 8)

    self.trifectaEntry = Entry(self, width = 3)
    self.trifectaEntry.grid(row = 2, column = 9)

    self.superfectaEntry = Entry(self, width = 3)
    self.superfectaEntry.grid(row = 2, column = 10)

    # button to push in results
    ##### probably should allow for user to edit answers
    ##### same for bets -- for a later time

    self.raceResultsButton = Button(self, text = "Enter Results",
                                    command = parent.addResults)
    self.raceResultsButton.grid(row = 7, column = 6, columnspan = 3)
    

#####################   Cash Out #############################
class CashOut(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.lblOut = Label(self, text = "3")
    self.lblOut.grid(row = 1, column = 0)

#####################   History #############################
class History(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.lblOut = Label(self, text = "4")
    self.lblOut.grid(row = 1, column = 1)


a = getStarted()
a.mainloop()


## add in the main stuff and mainloop()







############## Building radio buttons for number of horse races
    

##    # need to immediately get the number of races
##    self.totalRaces = 12
##
##    Label(self, text = "Next Race").grid(row = 0, column = 0)
##
##    #### considered making race buttons go across top row
##    #### but I could not get text to appear below
##    #### and so it could cause some confusion when selecting buttons
##    self.raceBtns = []
##    self.raceRadVar = IntVar()
##    for i in range(self.totalRaces):
##      self.raceBtns.append(
##        Radiobutton(self, text = i + 1, variable = self.raceRadVar, value = i))
##      self.raceBtns[i].grid(row = i + 1, column = 0)
##
##    print("Race number: {}".format(self.raceRadVar.get()))
##
 

          
    

    

