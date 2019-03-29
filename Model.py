# coding: utf-8

import GlobalVariables as common

#user input of some of the variables
common.numberOfHouseholds = int(input("Insert the number of household to create: "))
common.percentageOfNumbAgents = int(input("Insert the percentage of numb agents (from 0 to 100):"))
common.numberOfFirms = int(input("Insert the number of firms to create: "))
common.numberOfCycles = 300 #int(input("Insert the number of cycles:"))
common.seed = int(input("Insert a seed for random values:"))
common.verbose = eval(input("Verbose (True or False):"))
common.network = eval(input("Do you want to create a network between the households (True or False):"))
if common.network: 
    common.probabilityOfConnection = float(input("Probability of connection in the network:"))
    
common.unemployment = eval(input("Do you want to introduce the unemployment modelling:"))


from Environment import *
from Firms import *
from Household import *
from Book import *

if common.unemployment:
    from ActionsU import *
else:
    from Actions import *


#setting the seed
np.random.seed(seed = common.seed)

# first, creating the environment
environment = Environment()


#then we create the Agents
environment.createAgent("Household", common.numberOfHouseholds)
environment.createAgent("Firm", common.numberOfFirms)
if common.verbose:
    print("Global interest rate for the next cycle is:", common.currentInterestRate)


#if there's a social network
if common.network:
    environment.createBaseGraph()
    #environment.drawBaseGraph(l = 55, h=34, pos = "circular")


#the scheduled actions are done
for cycle in range(common.numberOfCycles):
    environment.cycle( urlOfTheDailySchedule = common.urlOfTheDailySchedule)



#ir plot
environment.plotOfInterestRate()



#price for goods plot
environment.plotOfPriceForGoods()

#environment.PriceForGoodsHistogram()

#candlestick plot
environment.candlestickForShares()

