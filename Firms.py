
# coding: utf-8

# In[10]:


import import_ipynb

import GlobalVariables as common
import numpy as np


# In[27]:


class Firm:
    
    def __init__(self, averagePreviousPriceForGoods = 0, priceForGoods = 0, stockpile = 0, soldAmount = 0, nameOFTheFirm = ""):
        """
        Instance of the class Firm 
        
        parameters:
        averagePreviousPriceForGoods (float): the average price for goods on the previous cycle
        priceForGoods (float): the inner price for goods
        stockpile (int): the stockpile of the firm
        nameOFTheFirm (str): the name of the firm
        """
        self.averagePreviousPriceForGoods =  averagePreviousPriceForGoods
        self.priceForGoods = priceForGoods
        self.stockpile = stockpile
        self.requestedAmount = soldAmount + common.numberOfHouseholds/common.numberOfFirms
        self.nameOFTheFirm = nameOFTheFirm
        self.priceForGoodsInACycle = [] #stores the price for the goods in a cycle
        self.listOfAveragePreviousPrices = [averagePreviousPriceForGoods] #a list with the average previous prices
        if common.verbose == True:
            print("Firm", self.nameOFTheFirm, "created.")
            
    def __str__(self):
        return self.nameOFTheFirm
    
    def adaptPriceForGoods(self, direction):
        """
        Function that adapts the attribute priceForGoods based on the value of the variable direction the 
        global variable representing the interest rate, and the trend of the average previous price evaluated in
        the past two cycles
        
        parameters:
        direction (str): can be either "Up or Down"
        """
        keepPrice = False
        if len(self.listOfAveragePreviousPrices)>=2:
            if self.listOfAveragePreviousPrices[-1]>self.listOfAveragePreviousPrices[-2] and self.priceForGoods>self.listOfAveragePreviousPrices[-1]:
                keepPrice = True
        
        if direction == "Up":
            if common.verbose == True:
                print("\tIncreasing price for goods for", self.nameOFTheFirm, "with global interest rate", common.currentInterestRate)
                print("\t\tIt was", self.priceForGoods)
            self.priceForGoods *= np.random.uniform(1, 1+common.scalingFactorForInnerFirmPriceForGoods)
            if common.verbose == True:
                print("\t\tNow it is", self.priceForGoods)
        elif direction == "Down":
            randomValue = np.random.random()
            if common.currentInterestRate == "Low":
                # the firm adapts its price if and only if price is growing and with a probability of 33% 
                if keepPrice and randomValue < 0.33:
                    if common.verbose == True:
                        print("\tPrice is kept by", self.nameOFTheFirm )
                else:
                    if common.verbose == True:
                        print("\tDecreasing price for goods for", self.nameOFTheFirm, "with global interest rate", common.currentInterestRate)
                        print("\t\tIt was", self.priceForGoods)
                    self.priceForGoods /= np.random.uniform(1, 1 + common.scalingFactorForInnerFirmPriceForGoods)
                    if common.verbose == True:
                        print("\t\tNow it is", self.priceForGoods)
            elif common.currentInterestRate == "Medium":
                # the firm adapts its price if and only if price is growing and with a probability of 11%
                if keepPrice and randomValue < 0.11:
                    if common.verbose == True:
                        print("\tPrice is kept by", self.nameOFTheFirm )
                else:
                    if common.verbose == True:
                        print("\tDecreasing price for goods for", self.nameOFTheFirm, "with global interest rate", common.currentInterestRate)
                        print("\t\tIt was", self.priceForGoods)
                    self.priceForGoods /= np.random.uniform(1, 1 + common.scalingFactorForInnerFirmPriceForGoods)
                    if common.verbose == True:
                        print("\t\tNow it is", self.priceForGoods)

            elif common.currentInterestRate == "High":
                    if common.verbose == True:
                        print("\tDecreasing price for goods for", self.nameOFTheFirm, "with global interest rate", common.currentInterestRate)
                        print("\t\tIt was", self.priceForGoods)
                    self.priceForGoods /= np.random.uniform(1, 1 + common.scalingFactorForInnerFirmPriceForGoods)
                    if common.verbose == True:
                        print("\t\tNow it is", self.priceForGoods)
            

