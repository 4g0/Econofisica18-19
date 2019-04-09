#inputs from user

#number of cycles for the simulation
numberOfCycles = 1

#number of agents instance of the class Households
numberOfHouseholds = 100

#percentage of random agents
percentageOfNumbAgents = 50

#number of agents instance of the class Firms
numberOfFirms = 4

#seed for random value
seed = 0

#boolean variable for verbose
verbose = False

#boolean variable for network structure
network = False

#probability of connection in the network structure
probabilityOfConnection = 0.15

#unemployment
unemployment = False






#global variables

#name for the saved figure
nameForFigSaving = ""

#url for the schedule of a single day, see README for other info
urlOfTheDailySchedule = "ScheduleDailyVanilla.csv"
#url for the schedule of interest rates
urlOfInterestRateSchedule = "ScheduleInterestRates.csv"

#current interest rate
currentInterestRate = "Medium"
pastInterestRate = "Medium"

#initial threshold for the consumption of goods for all the agents Household
initialThresholdForConsumption = 0

#initial average previous price for all the agent Firms
firstAveragePreviousPriceForGoods = 100

#defining mean and variance for initial inner price of agent instance of the class Household
initialHouseholdMeanPriceForGoods = firstAveragePreviousPriceForGoods * 0.85
initialHouseholdStandardDeviationPriceForGoods = 0.05

#defining mean and variance for initial inner price of agent instance of the class Firm
initialFirmMeanPriceForGoods = firstAveragePreviousPriceForGoods * 1.15
initialFirmStandardDeviationPriceForGoods = 0.05

#ratio between Firms and Households
ratioFirmHouseholds = numberOfFirms/ numberOfHouseholds

#initial Price for bonds 
initialBondPrices = 100

#initial price for shares
initialSharePrices = 100


#scaling factor for the inner price for Goods of agent instance of the class Firm
if ratioFirmHouseholds < 1:
    scalingFactorForInnerFirmPriceForGoods = 0.2 *ratioFirmHouseholds
else:
    scalingFactorForInnerFirmPriceForGoods = 0.2 

#scaling factor for the inner price for Goods of agent instance of the class Household    
scalingFactorForInnerHouseholdPriceForGoods = 0.2 

#probability thresholds based on current interest rate
lowerProbabilityBoundBasedOnInterestRate = 0.2
mediumProbabilityBoundBasedOnInterestRate = 0.5
higherProbabilityBoundBasedOnInterestRate = 0.8

#probability moments for the household's preferences on stock market
preferenceVariation = 0.1 

#euphoria for the agent if win on the stock market
euphoriaIfWin = 1

#probability to consume if unemployed
unemploymentConsumptionProbability = 0.5

