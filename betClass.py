""" betClass.py

    We build the Bet class.

    We will record the bettor.
    
    When you place a bet,
    you should to give the
    race number, amount, type of bet, and horses,
    in that order.
    
    We will compute the
    total number of bets and total cost of bet from
    the type, amount, and horses selected.
    If the bet wins, we will determine the winnings
    from the amount of bet and the payouts for the race.
"""


class Bet(object):
  def __init__(self, bettor, raceNumber, amount, betType, horses):
    object.__init__(self)
    self.setBettor(bettor)
    self.setRaceNumber(raceNumber)
    self.setAmount(amount)
    self.setBetType(betType)
    self.setHorses(horses)
    # we compute all individual bets
    self.setAllBets()
    self.setWinnersRace("TBD")
    self.setPayouts("TBD")
    self.setCashedOut("N/A")


  # First we treat attributes that are passed in at instantiation


  # create our setters
  def setBettor(self, bettor):
    self.__bettor = bettor

  def setRaceNumber(self, raceNumber):
    self.__raceNumber = raceNumber

  def setAmount(self, amount):
    self.__amount = amount

  def setBetType(self, betType):
    self.__betType = betType

  def setHorses(self, horses):
    self.__horses = horses
    

  # create our getters
  def getBettor(self):
    return self.__bettor

  def getRaceNumber(self):
    return self.__raceNumber

  def getAmount(self):
    return self.__amount

  def getBetType(self):
    return self.__betType

  def getHorses(self):
    return self.__horses
  

  # create our properties
  bettor     = property(fget = getBettor, fset = setBettor)
  raceNumber = property(fget = getRaceNumber, fset = setRaceNumber)
  amount     = property(fget = getAmount, fset = setAmount)
  betType    = property(fget = getBetType, fset = setBetType)
  horses     = property(fget = getHorses, fset = setHorses)
  

  # Now we break down the bet into individual bets
  # we will use AllBets to check for a winner
  # with some thought, maybe this can be simplified
  # but I don't need to go beyond superfecta
  def setAllBets(self):
    bets = []
    
    # we consider the various betTypes to set bets
    
    # straight bets
    if self.betType in ("Win", "Place", "Show"):
      # we just add the number to the list bets
      for numbers in self.horses:
        bets.append(numbers)

    # Exacta typ bets
    elif self.betType in ("Exacta", "Exacta Box"):
      if self.betType == "Exacta":
        # we copy the two lists in self.horses
        firstPicks = self.horses[0]
        secondPicks = self.horses[1]
      elif self.betType == "Exacta Box":
        # self.horses is just a list
        # and we copy that list
        firstPicks = self.horses
        secondPicks = self.horses
      for first in firstPicks:
        for second in secondPicks:
          # we check for duplicates -- those are really bad bets
          # this takes care of not checking for bad bets from user
          # (such as picking 3 and 3 only in an exacta)
          if first != second:
            # we add a tuple to bets
            bets.append((first, second))

    # trifecta type bets
    elif self.betType in ("Trifecta, Trifecta Box"):
      if self.betType == "Trifecta":
        # we copy the three lists
        (firstPicks, secondPicks, thirdPicks) = (self.horses[0],
                                                 self.horses[1], self.horses[2])
      elif self.betType == "Trifecta Box":
        # we copy the list three times
        (firstPicks, secondPicks, thirdPicks) = (self.horses,
                                                 self.horses, self.horses)
      for first in firstPicks:
        for second in secondPicks:
          if first != second:
            for third in thirdPicks:
              if third not in (first, second):
                bets.append((first, second, third))

    # superfecta type bets
    elif self.betType in ("Superfecta, Superfecta Box"):
      if self.betType == "Superfecta":
        # we copy the four lists
        (firstPicks, secondPicks, thirdPicks, fourthPicks) = (self.horses[0],
                                                 self.horses[1], self.horses[2], self.horses[3])
      elif self.betType == "Superfecta Box":
        # we copy the list four times
        (firstPicks, secondPicks, thirdPicks, fourthPicks) = (self.horses,
                                                              self.horses, self.horses, self.horses)
      for first in firstPicks:
        for second in secondPicks:
          if first != second:
            for third in thirdPicks:
              if (first != third) and (second != third):
                for fourth in fourthPicks:
                  if fourth not in (first, second, third):
                    bets.append((first, second, third, fourth))             


    # we return bets      
    self.__allBets = bets


  def getAllBets(self):
    return self.__allBets

  allBets = property(fget = getAllBets, fset = setAllBets)


  # we count the number of individual bets
  def getTotalBets(self):
    return len(self.allBets)

  totalBets  = property(fget = getTotalBets)
  

  # we calculate the cost of the entire bet
  def getCost(self):
    return self.amount * self.totalBets

  cost = property(fget = getCost)
  

  # get top 4 horses after race is over
  # so when the app gets updated with the
  # results of the race, this method needs
  # to be called
  ##### This seems inefficient because we are keeping this
  ##### data for each race already -- did this so
  ##### that we can have a method for determining
  ##### if the bet is a winner without any parameters
  ##### Consider the trade-offs
  def setWinnersRace(self, top4):
      self.__winnersRace = top4

  def getWinnersRace(self):
    return self.__winnersRace

  winnersRace = property(fset = setWinnersRace, fget = getWinnersRace)

  
  def winnerQ(self):
    if self.winnersRace == "TBD":
      return "TBD"
    top4 = self.winnersRace
    if self.betType in ("Win", "Place", "Show"):
      horses = self.allBets
      
      if self.betType == "Win":
        chances = 1
      if self.betType == "Place":
        chances = 2
      elif self.betType == "Show":
        chances = 3

      for number in horses:  
        if number in top4[0:chances]:
          return True
        else:
          return False

    else:
      # now we consider non-straight bets
      winners = []
      if self.betType in ("Exacta", "Exacta Box"):
        winners.append(top4[0:2])
      elif self.betType in ("Trifecta", "Trifecta Box"):
        winners.append(top4[0:3])
      elif self.betType in ("Superfecta", "Superfecta Box"):
        winners.append(top4[0:4])
       # we now check to see if the needed winners are one of the bets   
      if winners[0] in self.allBets:
        return True
      else:
        return False
      
  ### see comments for winnersRace -- similar comments apply here
  def setPayouts(self, payouts):
    self.__payouts = payouts

  def getPayouts(self):
    return self.__payouts

  payouts = property(fset = setPayouts, fget = getPayouts)

  def winnings(self):
    if self.payouts == "TBD":
      return "TBD"

    if not self.winnerQ():
      return 0
    # Each type of bet has a standard units used in payouts

    # win, place, and show bets are reported for $2 bets
    if self.betType in ("Win", "Place", "Show"):
      # we need to test if the Place and Show bets
      # are sharp -- for example, if your place
      # horse comes in first, you still win.
      # The payouts dictionary will have three values for "Win",
      # two values for "Place", and one value for "Show".
      # So we need more than just knowing the betType
      # and if it is a winner or not.
      
      if self.betType == "Win":
        # then your pick finished first
        payout = self.payouts["Win"][0]

      elif self.betType == "Place":
        # first lets assume your pick finished first
        if self.horses == self.winnersRace[0]:
          payout = self.payouts["Win"][1]
        # so we can now assume your pick did finish second
        else:
          payout = self.payouts["Place"][0]

      elif self.betType == "Show":
        # first assume your pick finished first
        if self.horses == self.winnersRace[0]:
          payout = self.payouts["Win"][2]
        # now assume your pick finished second
        elif self.horses == self.winnersRace[1]:
          payout = self.payouts["Place"][1]
        # so now we can assume your pick did finish third
        else:
          payout = self.payouts["Show"] # just a number in payouts["Show"]
      
      return (self.amount / 2) * payout

    # Exactas winnings are reported for $1 bets
    elif self.betType in ("Exacta", "Exacta Box"):
      payout = self.payouts["Exacta"]
      return (self.amount * payout)

    # Trifecta winnings are reported for $1 bets
    elif self.betType in ("Trifecta", "Trifecta Box"):
      payout = self.payouts["Trifecta"]
      return (self.amount * payout)

    #Superfecta winnings are reported for $0.10 bets
    elif self.betType in ("Superfecta", "Superfecta Box"):
      payout = self.payouts["Superfecta"]
      return (self.amount / 0.1) * payout

  

   # we will default cashedOut to "N/A"
   # we will only change it if the bet wins
  def setCashedOut(self, yesOrNo):
    self.__cashedOut = yesOrNo
    
  def getCashedOut(self):
    return self.__cashedOut

  cashedOut = property(fset = setCashedOut, fget = getCashedOut)
    
    

    

