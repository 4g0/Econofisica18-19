# coding: utf-8

import GlobalVariables as common
import numpy as np

class Book:
    
    def __init__(self, owner):
        """
        Instance of the class book.
        
        parameters:
        owner (str): the name of the firm who owns this book
        """
        if common.verbose:
            print("Book for the firm", owner, "created")
        self.owner = owner
        self.askList = [] #matrix of sellers, with agent, price as columns
        self.bidList = [] #matrix of buyers, with agent, price as columns
        self.high = 0 #initial high
        self.low = 1000000  #initial low
        self.open = common.initialSharePrices
        self.close = 0
        self.last = common.initialSharePrices # last transaction
        self.historicList = [] 
        #OK
        
    
    def checkMatch(self, agent, price, typeOfInsert):
        """
        Boolean Function that based on the offered\required price and the type of insertion of an Household
        returns the status of a possible transaction, True meaning there's a possibility for a transaction, 
        False meaning there's not
        
        parameters:
        agent (Household): an instance of the class Household 
        price (float): The price that the agent wants on order to end the transaction
        typeOfInsert (str): Can be either "Ask" or "Bid"
        """
        result = False
        if typeOfInsert == "Ask":
            # check in bid list
            temporaryList = self.bidList.copy()
            temporaryList = temporaryList[::-1]
            stop = False

            if len(temporaryList)>0:
                for i in range(len(temporaryList)):
                    if stop == False:
                        if price <= temporaryList[i][1]:
                            result = True
                            stop = True
            else:
                result = False
            del temporaryList
            
        if typeOfInsert == "Bid":
            # check in ask list
            temporaryList = self.askList.copy()
            stop = False
            if len(temporaryList)>0:
                for i in range(len(temporaryList)):
                    if stop == False:
                        if price >= temporaryList[i][1]:
                            result = True
                            stop = True
            else:
                result = False
            del temporaryList
            
        return result
    
    def __str__(self):
        return self.owner
            
    
    def match(self, agent, price, typeOfInsert):
        """
        A function that, based on the price and the type of insert of an Household,
        returns [(Household),(float)], result of a matched interaction.
        
        parameters:
        agent (Household): an instance of the class Household 
        price (float): The price that the agent wants on order to end the transaction
        typeOfInsert (str): Can be either "Ask" or "Bid"
        """
        if typeOfInsert == "Ask":
            temporaryAgentAndPrice = self.bidList[-1]
            self.bidList.pop(-1)
        if typeOfInsert == "Bid":
            temporaryAgentAndPrice = self.askList[0]
            self.askList.pop(0)
            
        if temporaryAgentAndPrice[1] > self.high: 
            self.high = temporaryAgentAndPrice[1]
        if temporaryAgentAndPrice[1] < self.low:
            self.low = temporaryAgentAndPrice[1]
        self.last = temporaryAgentAndPrice[1]
        
        if self.open == 0:
            self.open = temporaryAgentAndPrice[1]
        self.close = temporaryAgentAndPrice[1]
        
        return temporaryAgentAndPrice
    
    def insert(self, agent, price, typeOfInsert):
        """
        A function that inserts [agent, price] in the attribute askList or bidList based on the typeOfInsert.
        The insert is ordered based on the price.
        
        parameters:
        agent (Household): an instance of the class Household 
        price (float): The price that the agent wants on order to end the transaction
        typeOfInsert (str): Can be either "Ask" or "Bid"
        """
        if typeOfInsert == "Ask":
            temporaryList = self.askList.copy()
            stop = False
            if len(temporaryList)>0:
                for i in range(len(temporaryList)):
                    if stop == False:
                        if price<=temporaryList[i][1]:
                            self.askList.insert(i,[agent, price])
                            stop = True
                if price > temporaryList[-1][1]:
                    self.askList.insert(len(temporaryList)+1,[agent, price])
            else:
                self.askList.insert(0,[agent, price])
            del temporaryList
        if typeOfInsert == "Bid":
            temporaryList = self.bidList.copy()
            stop = False
            if len(temporaryList)>0:
                for i in range(len(temporaryList)):
                    if stop == False:
                        if price<=temporaryList[i][1]:
                            self.bidList.insert(i,[agent, price])
                            stop = True
                if price > temporaryList[-1][1]:
                    self.bidList.insert(len(temporaryList)+1,[agent, price])
            else:
                self.bidList.insert(0,[agent, price])
            del temporaryList
        return None
    
    def collectOffer(self, agent, price, typeOfInsert):
        """
        A function that checks if there can be a transaction for an Household based on the offered\required price 
        and the type of the action with the auxiliary function checkMatch.
        Returns a tuple [(bool), (Household), (float)] with status of the action, household to interact with, 
        price of the interaction.
        
        parameters:
        agent (Household): an instance of the class Household 
        price (float): The price that the agent wants on order to end the transaction
        typeOfInsert (str): Can be either "Ask" or "Bid"
        """
        if common.verbose:
            print("\t\tthe offer by", agent, "is ", price, ",", typeOfInsert)
        if self.checkMatch(agent,price,typeOfInsert):
            if common.verbose:
                print("\t\tMatched")
            return [True, self.match(agent,price,typeOfInsert)]
        else:
            if common.verbose:
                print("\t\tNot matched, offer registered")
            self.insert(agent,price,typeOfInsert)
            return [False, []] 
            
    
    def recordHighAndLow(self):
        """
        Function that records the highest and the lowest price of the day in the attribute historicList.
        If in this cycle there hasn't been any trade, it records None as both highest and lowest.
        """
        if self.high == 0 and self.low == 1000000:
            self.high, self.low = None, None
        if common.verbose:
            print("Book of ", self.owner, "is recording to his historical [", self.high,",",self.low,
                  ",",self.open,",",self.close,"]")
        self.historicList.append([self.high,self.low, self.open, self.close])
        self.bidList = []
        self.askList = []
        self.high = 0 #initial high
        self.low = 1000000  #initial low
        self.open = 0
        self.close = 0

