
# coding: utf-8

# In[1]:


import import_ipynb
import GlobalVariables as common
import numpy as np


# In[2]:


class Household:
    
    def __init__(self, typeOfAgent = "", priceForGoods = 0, thresholdForConsumpition = 0.5, nameOfTheAgent = "", disposableIncome = 400):
        """
        Instance of the class Household
        
        parameters:
        tyeOfAgent (str): can be either "Trend" or "Numb"
        priceForGoods (float): the inner price for goods
        thresh                        #################
        nameOfTheAgent (str): the name of the agent
        disposableIncome (float): the disposable income of the agent
        """
        
        self.typeOfAgent = typeOfAgent
        self.priceForGoods = priceForGoods 
        self.thresholdForConsumpition = thresholdForConsumpition #inner threshold for modelling a risk propension
        self.nameOfTheAgent = nameOfTheAgent
        self.disposableIncome = disposableIncome #disposable income
        self.disposableSavings = disposableIncome
        self.bondAmount = 0 
        self.employed = False
        self.pastCyclesWithoutBuyingGoods = 0 #number of cycles without buying goods
        self.euphoriaForGoods = common.initialThresholdForConsumption #initial euphoria 
        self.preferencesForFirmInStockMarket = np.random.random(size = common.numberOfFirms) #there's no network propagation
        self.stockForSharesOfFirms = [20 for i in range(common.numberOfFirms)]
        self.actionWithSharesOfFirm = [np.random.choice(["Ask", "Bid", "Hold"]) for i in range(common.numberOfFirms)]
        if common.verbose == True:
            print("Agent", self.nameOfTheAgent, "created. He's a", self.typeOfAgent, "agent.")
        #OK
    
    def __str__(self):
        return self.nameOfTheAgent
        #OK
    
    def adaptPriceForGoods(self, direction):
        """
        Function that adapts the attribute priceForGoods based on the value of the variable direction 
        
        parameters:
        direction (str): can be either "Up or Down"
        """
        if direction == "Up":
            if common.verbose == True:
                print("\tIncreasing price for goods for", self.nameOfTheAgent)
                print("\t\tIt was", self.priceForGoods)
            self.priceForGoods *= np.random.uniform(1, 1+common.scalingFactorForInnerHouseholdPriceForGoods)
            if common.verbose == True:
                print("\t\tNow it is", self.priceForGoods)
        elif direction == "Down":
            if common.verbose == True:
                print("\tDecreasing price for goods for", self.nameOfTheAgent)
                print("\t\tIt was", self.priceForGoods)
            self.priceForGoods /= np.random.uniform(1, 1+common.scalingFactorForInnerHouseholdPriceForGoods)
            if common.verbose == True:
                print("\t\tNow it is", self.priceForGoods)
         #OK

