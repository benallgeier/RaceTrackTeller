""" raceClass.py

    A race has the following:
    a number (1 for the first race, 2 for the second race, ...),
    a number of horses
    bets on the race, SHOULD RACE HAVE BETS OR APP OR BOTH
    top 4 finishing horses,
    and the payouts for the various bets
"""

##### Questions: Include bets? require numberHorses at instantiation?

class Race(object):
  def __init__(self, numberRace, numberHorses):
    object.__init__(self)
    self.setNumberRace(numberRace)
    self.setNumberHorses(numberHorses)


  def setNumberRace(self, numberRace):
    self.__numberRace = numberRace

  def setNumberHorses(self, numberHorses):
    self.__numberHorses = numberHorses

  def getNumberRace(self):
    return self.__numberRace

  def getNumberHorses(self):
    return self.__numberHorses

  numberRace   = property(fset = setNumberRace,   fget = getNumberRace)
  numberHorses = property(fset = setNumberHorses, fget = getNumberHorses)

  # to check for winners, we will need the top 4 horses
  
  def setTop4Horses(self, top4):
    self.__top4Horses = top4

  def getTop4Horses(self):
    return self.__top4Horses

  top4Horses = property(fset = setTop4Horses, fget = getTop4Horses)


  # to determine winnings, we need the payouts for:
  # win, place, show, exacta, trifecta, and superfecta
  # payouts should be a dictionary
  # see winnings method in betClass
  def setPayouts(self, payouts):
    self.__payouts = payouts

  def getPayouts(self):
    return self.__payouts

  payouts = property(fset = setPayouts, fget = getPayouts)
    
