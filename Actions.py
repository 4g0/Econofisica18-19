# coding: utf-8

import numpy as np
import pandas as pd
import GlobalVariables as common

def workAndProduce(anHousehold, *argv):
    """
    An Household increases his disposable income by the average previous price of a Firm choosen randomly.
    The Firm increases its stockpile by one.
    
    parameters:
    anHousehold (Household): an instance of the class Household
    """
    
    firmList = argv[0]
    aFirm = np.random.choice(firmList)
    if common.verbose:
        print("\t", anHousehold, "is working and producing for", aFirm, "whose average previous price is",
              aFirm.averagePreviousPriceForGoods)
    anHousehold.disposableIncome += aFirm.averagePreviousPriceForGoods
    if common.verbose:
        print("\t", aFirm, "stockpile was", aFirm.stockpile, "and now is ", aFirm.stockpile + 1)
    aFirm.stockpile += 1 
    return None
    #OK

def evaluatePastConsumption(anHousehold, *argv):
    """
    An Household increases his own price for goods if he hasn't bought any goods 
    in the past three cycles.
    
    parameters:
    anHousehold: the instance of the class Household who's subject of the action
    """
    if anHousehold.pastCyclesWithoutBuyingGoods >= 3:
        if common.verbose:
            print("\t", anHousehold, "has not bought for 3 cycles. He is increasing his price for goods.")
        anHousehold.adaptPriceForGoods("Up")
    else:
        if common.verbose:
            print("\t", anHousehold, "has bought something in the last 3 cycles.")
            
    #OK    
    
def buyGood(anHousehold, *argv):
    """
    An Household, try to buy goods from a Firm choosen andomly, based on some constraints 
    (disposable income, enough stockpile), with an adaptment of the inner price for goods.
    
    parameters:
    anHousehold (Household): an instance of the class Household
    """
    firmList = argv[0]
    aFirm = np.random.choice(firmList)
    if common.verbose:
        print("\t", anHousehold, "is trying to buy goods from", aFirm)
    if anHousehold.priceForGoods >= aFirm.priceForGoods:
        if anHousehold.disposableIncome >= aFirm.priceForGoods:
            if aFirm.stockpile > 0:
                if common.verbose:
                    print("\tSold")
                    print("\t", aFirm, "stockpile was", aFirm.stockpile)
                aFirm.stockpile -= 1 #1 is the quantity sold
                if common.verbose:
                    print("\tNow it is", aFirm.stockpile)
                    print("\t", anHousehold, "disposable income was",anHousehold.disposableIncome )
                anHousehold.disposableIncome -= aFirm.priceForGoods
                if common.verbose:
                    print("\tNow it is", aFirm.stockpile)
                    print("\tNow it is",anHousehold.disposableIncome )
                aFirm.priceForGoodsInACycle.append(aFirm.priceForGoods)
                aFirm.adaptPriceForGoods("Up")
                anHousehold.adaptPriceForGoods("Down")
                anHousehold.pastCyclesWithoutBuyingGoods = 0
            else:
                if common.verbose:
                    print("\t\tNot enough stockpile.")
                anHousehold.adaptPriceForGoods("Up")
                anHousehold.pastCyclesWithoutBuyingGoods += 1
        else:
            if common.verbose:
                print("\t\tNot enough disposable income.")
            aFirm.adaptPriceForGoods("Down")
            anHousehold.pastCyclesWithoutBuyingGoods += 1
    else:
        if common.verbose:
            print("\t\tThe prices don't match.")
        aFirm.adaptPriceForGoods("Down")
        anHousehold.adaptPriceForGoods("Up")
        anHousehold.pastCyclesWithoutBuyingGoods += 1
        
    return None
    #OK

def buyBond(anHousehold, *argv):
    """
    An Household buy bonds in a probabilistic way basing the actions on some constraints (his disposable income)
    and the global interest rate.

    parameters:
    anHousehold (Household): an instance of the class Household
    """
    if common.verbose:
        print("\t", anHousehold, "is trying to buy Bonds")
    randomValue = np.random.random()
    if anHousehold.disposableIncome >= common.initialBondPrices:
        if common.currentInterestRate == "Low":
            if randomValue < common.lowerProbabilityBoundBasedOnInterestRate:
                if common.verbose:
                    print("\t\tBought")
                    print("\t\tHis euphoria for goods was", anHousehold.euphoriaForGoods)
                anHousehold.euphoriaForGoods = common.euphoriaIfWin*0.11
                if common.verbose:
                    print("\t\tand now is ", anHousehold.euphoriaForGoods)
                    print("\t\tHis disposable income was", anHousehold.disposableIncome)
                anHousehold.disposableIncome -= common.initialBondPrices
                anHousehold.bondAmount +=1
                if common.verbose:
                    print("\t\tand now is ", anHousehold.disposableIncome)
            else:
                if common.verbose:
                    print("\t\tFailed attempt")
                pass #more propension toward stocks
        elif common.currentInterestRate == "Medium":
            if randomValue < common.mediumProbabilityBoundBasedOnInterestRate:
                if common.verbose:
                    print("\t\tBought")
                    print("\t\tHis euphoria for goods was", anHousehold.euphoriaForGoods)
                anHousehold.euphoriaForGoods = common.euphoriaIfWin*0.22
                if common.verbose:
                    print("\t\tand now is ", anHousehold.euphoriaForGoods)
                    print("\t\tHis disposable income was", anHousehold.disposableIncome)
                anHousehold.disposableIncome -= common.initialBondPrices
                anHousehold.bondAmount +=1
                if common.verbose:   
                    print("\t\tand now is ", anHousehold.disposableIncome)
            else:
                if common.verbose:
                    print("\t\tFailed attempt")
                pass #more propension toward stocks
        elif common.currentInterestRate == "High":
            if randomValue < common.higherProbabilityBoundBasedOnInterestRate:
                if common.verbose:
                    print("\t\tBought")
                    print("\t\tHis euphoria for goods was", anHousehold.euphoriaForGoods)
                anHousehold.euphoriaForGoods = common.euphoriaIfWin*0.33
                if common.verbose:
                    print("\t\tand now is ", anHousehold.euphoriaForGoods)
                    print("\t\tHis disposable income was", anHousehold.disposableIncome)
                anHousehold.disposableIncome -= common.initialBondPrices
                anHousehold.bondAmount +=1
                if common.verbose:
                    print("\t\tand now is ", anHousehold.disposableIncome)
            else:
                if common.verbose:
                    print("\t\tFailed attempt")
                pass #more propension toward stocks
    return None
    #OK

def interactWithStockMarket(anHousehold, *argv):
    
    """
    An Household invests on stock market, based on an inner preference list for the choice of the firm 
    (attribute preferencesForFirmInStockMarket), and a designed action (attribute actionWithSharesOfFirm).

    parameters:
    anHousehold (Household): an instance of the class Household
    """
    
    if common.verbose:
        print("\t", anHousehold, "is trying to interact with the stock market")
    
    #change his actions for the next cycle
    if common.verbose:
        print("\t", anHousehold, "is a ",anHousehold.typeOfAgent,"agent")
    if anHousehold.typeOfAgent == "Trend":
        #controlla il trend
        bookList = argv[1].copy()
        for index in range(common.numberOfFirms):
            historicalOfBook = bookList[index].historicList
            reversedHistoricalOfBook = historicalOfBook[::-1]
            if len(historicalOfBook) > 1:
                if reversedHistoricalOfBook[0][:2] != [None,None] and reversedHistoricalOfBook[1][:2]!= [None,None]:
                    if np.mean(reversedHistoricalOfBook[0][:2]) > np.mean(reversedHistoricalOfBook[1][:2]):
                        #anHousehold.actionWithSharesOfFirm[index] = "Ask"
                        actionProbability = [0.6,0.3,0.1]
                        anHousehold.actionWithSharesOfFirm[index] = np.random.choice(["Ask", "Bid", "Hold"], p=actionProbability)
                        if common.verbose:
                            print("\tHas changed his action to Ask for the firm", common.numberOfFirms[index])
                    else:
                        #anHousehold.actionWithSharesOfFirm[index] = "Bid"
                        actionProbability = [0.3,0.6,0.1]
                        anHousehold.actionWithSharesOfFirm[index] = np.random.choice(["Ask", "Bid", "Hold"], p=actionProbability)
                        if common.verbose:
                            print("\tHas changed his action to Bid for the firm", common.numberOfFirms[index])
                else:
                    if common.verbose:
                        print("\tHasn't changed his action because of not enough data")
                    actionProbability = [0.5,0.5,0]
                    anHousehold.actionWithSharesOfFirm[index] = np.random.choice(["Ask", "Bid", "Hold"], p=actionProbability)
                    pass #he doesn't change her actions because of his trending nature
            else:
                if common.verbose:
                    print("\t\tNot enough data to analyze for the agent")
                actionProbability = [0.5,0.5,0]
                anHousehold.actionWithSharesOfFirm[index] = np.random.choice(["Ask", "Bid", "Hold"], p=actionProbability)
    if anHousehold.typeOfAgent == "Numb":
        
        if common.currentInterestRate == "Low":
            actionProbability = [0.2,0.3,0.5]
        if common.currentInterestRate == "Medium":
            actionProbability = [0.3,0.3,0.4]
        if common.currentInterestRate == "High":
            actionProbability = [0.3,0.2,0.5]   
            
        a1 = "Ask"
        a2 = "Bid"
        a3 = "Hold"
        anHousehold.actionWithSharesOfFirm = np.random.choice([a1,a2,a3], p=actionProbability, size = common.numberOfFirms, replace = True)
        
        if common.verbose:
            bookList = argv[1].copy()
            for index in range(common.numberOfFirms):
                print("\tHas changed his action to",anHousehold.actionWithSharesOfFirm[index] ,"for the firm", common.numberOfFirms[index])
    
    """
    An Household invests on stock market, based on an inner preference list for the choice of the firm 
    (attribute preferencesForFirmInStockMarket), and a designed action (attribute actionWithSharesOfFirm).

    parameters:
    anHousehold (Household): an instance of the class Household
    """
    bookList = argv[1].copy()
    arrayOfPreferences = anHousehold.preferencesForFirmInStockMarket
    booksByPreference = [book for _,book in sorted(zip(arrayOfPreferences, bookList))]
    actionsByPreference = [action for _,action in sorted(zip(arrayOfPreferences, anHousehold.actionWithSharesOfFirm))]
    indexByPreference = [index for _, index in sorted(zip(arrayOfPreferences, range(len(arrayOfPreferences))))]

    for i in range(len(booksByPreference)):
        action = actionsByPreference[i]
        indexOfCurrentInteraction = indexByPreference[i]
        # the price that the agent propose is from a Normal distribution
        lastPrice = booksByPreference[i].last
        variance = (len(booksByPreference[i].askList) - len(booksByPreference[i].bidList))*0.005
        price = np.random.normal(loc = lastPrice, scale = np.sqrt(abs(variance)))
        if action == "Ask" and anHousehold.stockForSharesOfFirms[indexOfCurrentInteraction] > 0:
            if common.verbose:
                print("\t", anHousehold, "is doing action Ask with price", price, "for shares of the firm", booksByPreference[i])
            matched, interactingHouseholdAndPrice = booksByPreference[i].collectOffer(anHousehold, price, action) 
            
            if matched:
                #the interaction
                interactingHousehold = interactingHouseholdAndPrice[0]
                interactingPrice = interactingHouseholdAndPrice[1]
                if common.verbose:
                    print("\t\tMatched with ", interactingHousehold, "at", interactingPrice)
                    print("\t\t", interactingHousehold, "disposable income was",interactingHousehold.disposableIncome)
                interactingHousehold.disposableIncome -= interactingPrice
                if common.verbose:
                    print("\t\tNow it is ",interactingHousehold.disposableIncome)
                    print("\t\t", anHousehold, "disposable income was",anHousehold.disposableIncome)
                anHousehold.disposableIncome += interactingPrice
                if common.verbose:
                    print("\t\tNow it is ",anHousehold.disposableIncome)
                interactingHousehold.stockForSharesOfFirms[indexOfCurrentInteraction] += 1
                anHousehold.stockForSharesOfFirms[indexOfCurrentInteraction] -= 1
                if common.verbose:
                    print("\t\t", interactingHousehold, "now has", 
                          interactingHousehold.stockForSharesOfFirms[indexOfCurrentInteraction], "shares.")
                    print("\t\t", anHousehold, "now has", 
                          anHousehold.stockForSharesOfFirms[indexOfCurrentInteraction], "shares.")
            if not matched:
                pass
            
        if action == "Bid" and anHousehold.disposableIncome>price:
            if common.verbose:
                print("\t", anHousehold, "is doing action Bid with price", price,"for shares of the firm", booksByPreference[i])
            matched, interactingHouseholdAndPrice = booksByPreference[i].collectOffer(anHousehold, price, action)
            
            if matched:
                interactingHousehold = interactingHouseholdAndPrice[0]
                interactingPrice = interactingHouseholdAndPrice[1]
                if common.verbose:
                    print("\t\tMatched with ", interactingHousehold, "at", interactingPrice)
                    print("\t\t", interactingHousehold, "disposable income was",interactingHousehold.disposableIncome)
                interactingHousehold.disposableIncome += interactingPrice
                if common.verbose:
                    print("\t\tNow it is ",interactingHousehold.disposableIncome)
                    print("\t\t", anHousehold, "disposable income was",anHousehold.disposableIncome)
                anHousehold.disposableIncome -= interactingPrice
                if common.verbose:
                    print("\t\tNow it is ",anHousehold.disposableIncome)
                interactingHousehold.stockForSharesOfFirms[indexOfCurrentInteraction] -= 1
                anHousehold.stockForSharesOfFirms[indexOfCurrentInteraction] += 1
                if common.verbose:
                    print("\t\t", interactingHousehold, "now has", 
                          interactingHousehold.stockForSharesOfFirms[indexOfCurrentInteraction], "shares.")
                    print("\t\t", anHousehold, "now has", 
                          anHousehold.stockForSharesOfFirms[indexOfCurrentInteraction], "shares.")
            if not matched:
                pass
        
        if action == "Hold":
            if common.verbose:
                print("\t\tNot matched")
            pass
            
    return None

def evaluateEuphoria(anHousehold, *argv):
    """
    An household modifies his euphoria and propension for the shares of a firm.
    The household, independently of her nature, check if he has won on the stock market in this cycle: 
    if he has, he'll increase his euphoria and propension for the shares of the firm.
    The household, based on her nature, change her actions for the next cycle.
    If the household has enough euphoria, he'll buy another good.
    
    parameters:
    anHousehold (Household): an instance of the class Household
    """
    
    #check if he has won on the stock market
    if common.verbose:
        print("\t", anHousehold, "is checking if he's won in the stock market. ")
    bookList = argv[1].copy()
    for index in range(common.numberOfFirms):
        historicalOfBook = bookList[index].historicList
        if len(historicalOfBook) > 1:
            reversedHistoricalOfBook = historicalOfBook[::-1]
            currentSharesOfFirm = anHousehold.stockForSharesOfFirms[index]
            if currentSharesOfFirm:
                if reversedHistoricalOfBook[0][:2] != [None,None] and reversedHistoricalOfBook[1][:2]!= [None,None]:
                    if np.mean(reversedHistoricalOfBook[0][:2]) > np.mean(reversedHistoricalOfBook[1][:2]):
                        if common.verbose:
                            print("\tWon. Adapting his euphoria from ",anHousehold.euphoriaForGoods)
                        anHousehold.euphoriaForGoods = common.euphoriaIfWin #if he wins, he feels richer
                        if common.verbose:
                            print("\tTo", anHousehold.euphoriaForGoods)
                            print("\tAdapting his preference for the firm from ",anHousehold.preferencesForFirmInStockMarket[index])
                        anHousehold.preferencesForFirmInStockMarket[index] *= np.random.uniform(1, 1+common.preferenceVariation) 
                        if common.verbose:
                            print("\tTo", anHousehold.preferencesForFirmInStockMarket[index])
                    else:
                        if common.verbose:
                            print("\tNot won.\nAdapting his preference for the gitm from ",anHousehold.preferencesForFirmInStockMarket[index])
                        anHousehold.preferencesForFirmInStockMarket[index] *= np.random.uniform(1-common.preferenceVariation, 1)
                        if common.verbose:
                            print("\tTo", anHousehold.preferencesForFirmInStockMarket[index])
                else:
                    if common.verbose:
                        print("\t\tNot enough data to analyze for the agent")
                    
        else:
            if common.verbose:
                print("\t\tNot enough data to analyze for the agent")
                
    
    #if he has enough euphoria, he'll buy another good
    if common.verbose:
        print("\t",anHousehold, "has euphoria for goods", anHousehold.euphoriaForGoods)
    randomValue = np.random.random()
    if randomValue < anHousehold.euphoriaForGoods: #only wants to buy other goods
        if common.verbose:
            print(anHousehold, "is willing to buy another good")
        firmList = argv[0]
        aFirm = np.random.choice(firmList)
        if aFirm.stockpile > 0:
            if common.verbose:
                print("\t\tbuying another good from", aFirm)
                print("\t\t", aFirm, "stockpile was", aFirm.stockpile)
            aFirm.stockpile -= 1 #1 is the quantity sold
            if common.verbose:
                print("\t\tNow it is", aFirm.stockpile)
            aFirm.priceForGoodsInACycle.append(aFirm.priceForGoods)
            #aFirm.adaptPriceForGoods("Up")
            anHousehold.pastCyclesWithoutBuyingGoods = 0
            anHousehold.euphoriaForGoods *= 0.25 
            if common.verbose:
                print("\t",anHousehold, "now has euphoria for goods", anHousehold.euphoriaForGoods)
        else:
            if common.verbose:
                print("\tNot enough stockpile")
            pass
    else:
        if common.verbose:
            print("\t\tNot enough euphoria to buy another good.")
        pass
    return None

def checkBondPriceAndConvert(anHousehold, *argv):
    bookList = argv[1].copy()
    arrayOfPreferences = anHousehold.preferencesForFirmInStockMarket
    booksByPreference = [book for _,book in sorted(zip(arrayOfPreferences, bookList))]
    actionsByPreference = [action for _,action in sorted(zip(arrayOfPreferences, anHousehold.actionWithSharesOfFirm))]
    indexByPreference = [index for _, index in sorted(zip(arrayOfPreferences, range(len(arrayOfPreferences))))]
    #inverting
    booksByPreference = booksByPreference[::-1]
    actionsByPreference = actionsByPreference[::-1]
    indexByPreference = indexByPreference[::-1]
    
    if (common.pastInterestRate == "Low" and common.currentInterestRate != "Low") or (common.pastInterestRate == "Medium" and common.currentInterestRate == "High"):
        anHousehold.euphoriaForGoods = 1
        index = indexByPreference[-1]
        action = "Ask"
        
        if anHousehold.stockForSharesOfFirms[index] > 0:
            
            for s in range(anHousehold.stockForSharesOfFirms[index]):
                if common.verbose:
                    print("\t", anHousehold, "is doing action Ask with price", price, "for shares of the firm", booksByPreference[index])
                    
                # the price that the agent propose is from a Normal distribution
                lastPrice = booksByPreference[index].last
                variance = (len(booksByPreference[index].askList) - len(booksByPreference[index].bidList))*0.005
                price = np.random.normal(loc = lastPrice, scale = np.sqrt(abs(variance)))
                
                matched, interactingHouseholdAndPrice = booksByPreference[index].collectOffer(anHousehold, price, action) 

                if matched:
                    #the interaction
                    interactingHousehold = interactingHouseholdAndPrice[0]
                    interactingPrice = interactingHouseholdAndPrice[1]
                    if common.verbose:
                        print("\t\tMatched with ", interactingHousehold, "at", interactingPrice)
                        print("\t\t", interactingHousehold, "disposable saving was",interactingHousehold.disposableSavings)
                    interactingHousehold.disposableSavings -= interactingPrice
                    if common.verbose:
                        print("\t\tNow it is ",interactingHousehold.disposableSavings)
                        print("\t\t", anHousehold, "disposable bonds were",anHousehold.bondAmount)
                    anHousehold.bondAmount += 1
                    if common.verbose:
                        print("\t\tNow it is ",anHousehold.disposableSavings)
                    interactingHousehold.stockForSharesOfFirms[index] += 1
                    anHousehold.stockForSharesOfFirms[index] -= 1
                    if common.verbose:
                        print("\t\t", interactingHousehold, "now has", 
                              interactingHousehold.stockForSharesOfFirms[index], "shares.")
                        print("\t\t", anHousehold, "now has", 
                              anHousehold.stockForSharesOfFirms[index], "shares.")
                if not matched:
                    pass

    if (common.pastInterestRate == "High" and common.currentInterestRate != "High") or (common.pastInterestRate == "Medium" and common.currentInterestRate == "Low"):
        index = indexByPreference[0]
        action = "Bid"
        
        if anHousehold.bondAmount > 0:
            
            for s in range(anHousehold.bondAmount):
                if common.verbose:
                    print("\t", anHousehold, "is doing action Bid with price", price, "for shares of the firm", booksByPreference[index])
                    
                # the price that the agent propose is from a Normal distribution
                lastPrice = booksByPreference[index].last
                variance = (len(booksByPreference[index].askList) - len(booksByPreference[index].bidList))*0.005
                price = np.random.normal(loc = lastPrice, scale = np.sqrt(abs(variance)))
                
                matched, interactingHouseholdAndPrice = booksByPreference[index].collectOffer(anHousehold, price, action) 

                if matched:
                    #the interaction
                    interactingHousehold = interactingHouseholdAndPrice[0]
                    interactingPrice = interactingHouseholdAndPrice[1]
                    if common.verbose:
                        print("\t\tMatched with ", interactingHousehold, "at", interactingPrice)
                        print("\t\t", interactingHousehold, "disposable saving was",interactingHousehold.disposableSavings)
                    interactingHousehold.disposableSavings += interactingPrice
                    if common.verbose:
                        print("\t\tNow it is ",interactingHousehold.disposableSavings)
                        print("\t\t", anHousehold, "disposable bonds were",anHousehold.bondAmount)
                    anHousehold.bondAmount -= 1
                    if common.verbose:
                        print("\t\tNow it is ",anHousehold.disposableSavings)
                    interactingHousehold.stockForSharesOfFirms[index] -= 1
                    anHousehold.stockForSharesOfFirms[index] += 1
                    if common.verbose:
                        print("\t\t", interactingHousehold, "now has", 
                              interactingHousehold.stockForSharesOfFirms[index], "shares.")
                        print("\t\t", anHousehold, "now has", 
                              anHousehold.stockForSharesOfFirms[index], "shares.")
                if not matched:
                    pass


def modifyPriceBasedOnInterest(aFirm, *argv):
    """
    A firm adapts its price based on the global interest rate.
    
    parameters:
    aFirm (Firm): an instance of the class Firm
    """
    randomValue = np.random.random()
    if common.verbose:
        print("\t", aFirm, "is modifying it price based on the global interest rate, which is ", common.currentInterestRate)
    if common.currentInterestRate == "Low":
        if randomValue < common.lowerProbabilityBoundBasedOnInterestRate:
            if common.verbose:
                print("\t\tIt was", aFirm.priceForGoods)
            aFirm.priceForGoods *= np.random.uniform(1, 1 + common.scalingFactorForInnerFirmPriceForGoods)
            if common.verbose:
                print("\t\tNow it is", aFirm.priceForGoods)
        else:
            pass
    elif common.currentInterestRate == "Medium":
        if common.verbose:
            print("\t\tNot modified.")
        #the firm does nothing if the interest rate is medium
        pass
    elif common.currentInterestRate == "High":
        if randomValue < common.higherProbabilityBoundBasedOnInterestRate:
            if common.verbose:
                print("\t\tIt was", aFirm.priceForGoods)
            aFirm.priceForGoods /= np.random.uniform(1, 1 + common.scalingFactorForInnerFirmPriceForGoods)
            if common.verbose:
                print("\t\tNow it is", aFirm.priceForGoods)
        else:
            pass
    return None

def evaluateAveragePreviousPrice(aFirm, *argv):
    """
    A firm sets its average previous price as the mean of all the selling prices in a cycles, and keeps 
    track of this price in its attribute listOfAveragePreviousPrices.
    
    parameters:
    aFirm (Firm): an instance of the class Firm
    """
    if common.verbose:
        print("\t", aFirm, "is evaluating the average previous price")
        print("\t\tIt was", aFirm.averagePreviousPriceForGoods)
    if len(aFirm.priceForGoodsInACycle) > 0:
        averagePrice = np.mean(aFirm.priceForGoodsInACycle)
    else:
        averagePrice = aFirm.priceForGoods
    aFirm.listOfAveragePreviousPrices.append(averagePrice)
    aFirm.averagePreviousPriceForGoods = averagePrice
    aFirm.priceForGoodsInACycle = [] #in the next cycle the list will be initially empty
    if common.verbose:
        print("\t\tNow it is", aFirm.averagePreviousPriceForGoods)
    return None

def askAllTheAgent(agentList, method, *argv):
    """
    Given a list of subjects and a method representing an action, all the subjects perform the action 
    in a random order.
    
    parameters:
    agentList (list): a list of instances of the class who is subject of the action
    method (function): the action itself
    """
    copyOfAgentList = agentList.copy()
    np.random.shuffle(copyOfAgentList)
    for anAgent in copyOfAgentList: method(anAgent, *argv)

def computeInterestRate(currentTickNumber, urlOfInterestRateSchedule = "ScheduleInterestRates.csv"):
    """
    Based on the number of cycles performed, the global variable representing the interest rate is 
    modified according to a schedule
    
    parameters:
    currentTickNumber (int): representing the current number of cycles performed
    urlOfInterestRateSchedule (str): the url for the CSV file containing the interest rate schedule
    """
    interestRateSchedule = pd.read_csv(urlOfInterestRateSchedule)
    stopping = False
    for timeIndex in range(len(interestRateSchedule)):
        tickThreshold = interestRateSchedule.iloc[timeIndex]["Tick"]
        if currentTickNumber < tickThreshold and stopping == False:
            scheduledInterestRate = interestRateSchedule.iloc[timeIndex]["Rate"]
            common.pastInterestRate = common.currentInterestRate
            common.currentInterestRate = scheduledInterestRate
            stopping = True
    if common.verbose:
        print("Setting the global interest rate as",common.currentInterestRate)
        print()
            
def booksRecordHighAndLow(listOfBooks):
    """
    Given the list of all the books, each one of them records its highest and lowest price of the cycle.
    
    parameters:
    listOfBooks (list): list with instances of the class Book
    """
    for book in listOfBooks:
        book.recordHighAndLow()

