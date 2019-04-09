
# coding: utf-8

import import_ipynb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import seaborn as sns
import networkx as nx

import GlobalVariables as commons
from Household import * 
from Firms import *     
from Book import *

if common.unemployment:
    from ActionsU import *
else:
    from Actions import *
    
import math


class Environment:
    
    def __init__(self):
        """
        An instance of the class Environment
        """
        if common.verbose:
            print("The environment has been created")
        self.time = 0
        self.householdList = []
        self.firmList = []
        self.bookList = []
        
        
        self.unemploymentList = []
        
        self.G = nx.DiGraph()
        self.H = nx.DiGraph()
        self.listOfAllConnections = []
        self.connectionsInATurn = []
        self.influenceInATurnDic = {}
        
        self.completed = 0
        self.step = ( common.numberOfCycles // 100 ) * 5
        self.number_of_steps = common.numberOfCycles // self.step
        
    def tick(self):
        """
        Make the environment clock do one tick
        """
        self.time += 1
        if common.verbose:
            print("TICK = ", self.time+1)
            
    def computeUnemployment(self):
        """
        Compute the unemployment in the tick
        """
        unpl = 0
        for h in self.householdList:
            if h.employed == False:
                unpl += 1
            h.employed = False
        self.unemploymentList.append(unpl)
        
    def createAgent(self, agentType, numberOfAgents):
        """
        create numberOfAgents agents, instances of the class indicated by agentType
        str agentType: can be either Firm, Household, Book
        int numberOfAgents: number of the agents
        """
        for iterator in range(numberOfAgents):
            if agentType == "Household":
                randomNumber = np.random.randint(0,100)
                if randomNumber < common.percentageOfNumbAgents:
                    anAgent = Household(typeOfAgent = "Numb",
                                    priceForGoods=np.random.normal(common.initialHouseholdMeanPriceForGoods, common.initialHouseholdStandardDeviationPriceForGoods),
                                    thresholdForConsumpition = common.initialThresholdForConsumption,
                                    nameOfTheAgent= "Household_" + str(iterator + 1)
                                   )
                else:
                    anAgent = Household(typeOfAgent = "Trend",
                                    priceForGoods=np.random.normal(common.initialHouseholdMeanPriceForGoods, common.initialHouseholdStandardDeviationPriceForGoods),
                                    thresholdForConsumpition = common.initialThresholdForConsumption,
                                    nameOfTheAgent= "Household_" + str(iterator + 1)
                                   )
                self.householdList.append(anAgent)
            elif agentType == "Firm":
                anAgent = Firm(averagePreviousPriceForGoods = common.firstAveragePreviousPriceForGoods, 
                               priceForGoods = np.random.normal(common.initialFirmMeanPriceForGoods, common.initialFirmStandardDeviationPriceForGoods), 
                               nameOFTheFirm = "Firm_" + str(iterator + 1)
                              )
                aBook = Book(anAgent.nameOFTheFirm)
                self.firmList.append(anAgent)
                self.bookList.append(aBook)
        
    def PriceForGoodsGraph(self):
        """
        A function that plots the price averaged on all the firms
        """
        aaa = np.array([firm.listOfAveragePreviousPrices for firm in self.firmList])
        avg = [sum(day)/len(day) for day in aaa.T]
        del aaa

        plt.figure(figsize=(13, 8))
        plt.title("Average Price")
        plt.xlabel("Cycle")
        plt.ylabel("Price")
        plt.plot(range(len(avg)) , avg)
        plt.show()
    
    def PriceForGoodsHistogram(self):
        """
        A function that plots the histogram for the price of goods
        """
        plt.figure(figsize=(13, 8))
        plt.title("Histogram of prices for Goods")
        plt.xlabel("Price")
        for firm in self.firmList:
            sns.distplot(firm.listOfAveragePreviousPrices)
        plt.show()
    
    def PriceForSharesGraph(self):
        """
        A function that plots a candlestick representing the shares of a firm
        """
        for book in self.bookList:
            fig, ax = plt.subplots()
            ohlc_values = []

            for tick in range(common.numberOfCycles):
                # time, open, high, low, close
                if book.historicList[tick][0] == None:
                    high = 0
                else:
                    high = book.historicList[tick][0]
                if book.historicList[tick][1] == None:
                    low = 0
                else:
                    low = book.historicList[tick][1]
                opn = book.historicList[tick][2]
                cls = book.historicList[tick][3]
                ohlc_values.append([tick, opn, high, low , cls])

            #candlestick_ohlc(ax, ohlc_values, width=1, colorup='blue', colordown='red')
            plt.show()
        return None
        
    def InterestRateGraph(self):
        """
        A function that plot the global interest rate
        """
        interestRateSchedule = pd.read_csv(common.urlOfInterestRateSchedule)
        interestRateList = []
        
        for tick in range(common.numberOfCycles):
            stopping = False
            for timeIndex in range(len(interestRateSchedule)):
                tickThreshold = interestRateSchedule.iloc[timeIndex]["Tick"]
                if tick < tickThreshold and stopping == False:
                    scheduledInterestRate = interestRateSchedule.iloc[timeIndex]["Rate"]
                    if scheduledInterestRate == "High":
                        IntRate = 3
                    elif scheduledInterestRate == "Medium":
                        IntRate = 2
                    elif scheduledInterestRate == "Low":
                        IntRate = 1
                    interestRateList.append(IntRate)
                    stopping = True
                    
        plt.figure(figsize=(13, 8))
        plt.title("Interest Rate")
        plt.xlabel("Cycle")
        plt.ylabel("Interest Rate")
        plt.plot(range(common.numberOfCycles) , interestRateList)
        plt.show()
        return None
        
    
    def cycle(self, urlOfTheDailySchedule = "ScheduleDaily.csv"):
        """
        a cycle for the environment, in which the actions contained in the scheduled are preformed
        
        parameters:
        urlOfTheDailySchedule (str): url for a csv file containing columns [Agent, Action]
        
        """
        if common.network:
            #create the graph for the cycle
            self.createSubgraphForACycle()
            self.createDictOfInfluencesInACycle()
            #get those influences going
            self.getInfluenced()
        
        dailyActions = pd.read_csv(urlOfTheDailySchedule)

        for actionIndex in range(len(dailyActions)):
            agent = dailyActions.iloc[actionIndex]["Agent"]
            action = dailyActions.iloc[actionIndex]["Action"]
            
            if agent == "Households":
                if common.verbose:
                    print(agent,"will do", action)
                askAllTheAgent(self.householdList, globals()[action], self.firmList, self.bookList)
            elif agent == "Firms":
                if common.verbose:
                    print(agent,"will do", action)
                askAllTheAgent(self.firmList, globals()[action], self.householdList, self.bookList)
        
        #at the end of the cycle, the scheduled interest rate is applied
        computeInterestRate(currentTickNumber = self.time, 
                            urlOfInterestRateSchedule = common.urlOfInterestRateSchedule)
        
        #at the end of the cycle, the books records
        booksRecordHighAndLow(self.bookList)
        
        #the weights on the graph are updated
        if common.network:
            self.updateWeights()
            
        #compute the unemployment
        if common.unemployment:
            self.computeUnemployment()
            
        if self.time % self.step == 0:
            if self.time == 0: print("Simulation started")
            print("\t\t["+ " * "*self.completed +  " - "*(self.number_of_steps-self.completed) +"]")
            self.completed += 1
        if self.time + 1 == common.numberOfCycles:
            print("\t\t["+ " * "*(self.completed) +"]")
            print("Simulation completed.")
            
        #a tick
        self.tick()
        
        
        
    #####Network section
    def createAllConnections(self):
        """
        returns a list with all the directed connections between the Households
        """
        listOfAllConnections = []
        for i in range(len(self.householdList)):
            for j in range(len(self.householdList)):
                if i != j:
                    listOfAllConnections.append((self.householdList[i], self.householdList[j]))
        return listOfAllConnections


    def createBaseGraph(self):
        """
        create a complete digraph, with weights on links generated by a N(0.5,0.05) distribution
        """
        self.listOfAllConnections = self.createAllConnections()
        self.G.add_nodes_from(self.householdList)
        self.G.add_edges_from(self.listOfAllConnections)
        #bi implicazione
        for anHousehold in self.householdList:
            self.G.node[anHousehold]["Obj"] = anHousehold
        #aggiungo dei pesi alle connessioni del grafo
        #inizializzo i pesi casualmente 
        mean = 0.5
        variance = 0.05
        for anHousehold in self.householdList:
            for anotherHousehold in self.householdList:
                if [anHousehold,anotherHousehold] in self.G.edges:
                    randomWeigh = np.random.normal(loc = mean, scale=abs(np.sqrt(variance)))
                    self.G.edges[anHousehold, anotherHousehold]["Weight"] = randomWeigh

                    
    def drawBaseGraph(self, l, h, pos = "circular"):
        """
        plots the graph with all the connections
        """
        #plot del grafo con layout circolare
        labels = {edge: round(self.G.get_edge_data(edge[0], edge[1])["Weight"],3) for edge in self.G.edges()}
        if pos == "circular":
            circPos = nx.circular_layout(self.G)
            plt.figure(figsize = (13,8))
            nx.draw_networkx_nodes(self.G, circPos)
            nx.draw_networkx_labels(self.G,circPos)
            nx.draw_networkx_edges(self.G,circPos, alpha = 0.1)
            #nx.draw_networkx_edge_labels(G, circPos, edge_labels=labels)
            plt.axis("off")
            plt.show()   
        if pos == "spring":
            springPos = nx.spring_layout(self.G)
            plt.figure(figsize = (13,8))
            nx.draw_networkx_nodes(self.G, springPos)
            nx.draw_networkx_labels(self.G,springPos)
            nx.draw_networkx_edges(self.G, springPos, alpha = 0.1)
            #nx.draw_networkx_edge_labels(G, circPos, edge_labels=labels)
            plt.axis("off")
            plt.show()
            
    def drawGraphOfTheCycle(self):
        """
        plots the connection graph used in a cycle
        """
        labels2 = {edge: round(self.H.get_edge_data(edge[0], edge[1])["Weight"],3) for edge in self.H.edges()}
        circPos = nx.circular_layout(self.G)
        circPos2 = nx.circular_layout(self.H)

        plt.figure(figsize = (13,8))
        nx.draw_networkx_nodes(self.G, circPos)
        nx.draw_networkx_labels(self.G,circPos)
        nx.draw_networkx_nodes(self.H, circPos)
        nx.draw_networkx_edges(self.G,circPos, alpha = 0.1)
        nx.draw_networkx_edges(self.H,circPos, alpha = 1)
        #nx.draw_networkx_edge_labels(H, circPos, edge_labels=labels2)
        plt.axis("off")
        plt.show()
            
    def pickConnectionForACycle(self, probabilityOfConnection):
        """
        returns a list of the connections for the creation of the subgraph used in a cycle
        """
        listOfConnectionsInATurn = []
        #ogni giorno pesca dalla comunità persone con una data probabilità
        for connection in self.listOfAllConnections:
            if np.random.uniform() < probabilityOfConnection:
                listOfConnectionsInATurn.append(connection)
        return listOfConnectionsInATurn
    
    def createSubgraphForACycle(self):
        """
        create a subrgraph for the influences in a cycle
        """
        del self.connectionsInATurn
        self.connectionsInATurn = self.pickConnectionForACycle(common.probabilityOfConnection)
        self.H = self.G.edge_subgraph(self.connectionsInATurn).copy() 
        
    def createDictOfInfluencesInACycle(self):
        """
        create a dictionary with all the possible influences in a cycle
        """
        for anHousehold in self.householdList:
            self.influenceInATurnDic[anHousehold] = {}

        for edge in self.connectionsInATurn:
            influencer, influenced = edge
            self.influenceInATurnDic[influenced][influencer] =  []
            
            
            
    def getInfluenced(self):
        """
        Selects the influences in a cycles and change of the action performed by the household
        """

        for influenced, v in self.influenceInATurnDic.items():
    
            dictOfAdvices = {}
    
            for book in self.bookList:
                dictOfAdvices[book] = {}
                dictOfAdvices[book]["Ask"] = 0
                dictOfAdvices[book]["Bid"] = 0
                dictOfAdvices[book]["Hold"] = 0
                dictOfAdvices[book]["W"] = 0
                dictOfAdvices[book]["Infl"] = []
        
            if common.verbose:
                print(influenced, "is the influenced")
    
            for influencer, v2 in v.items():
                connectionWeight = self.G.get_edge_data(influencer, influenced)["Weight"]  
                if common.verbose:
                    print("\t",influencer, "is the influencer")
                pref = list(influencer.preferencesForFirmInStockMarket.copy())
                actions = influencer.actionWithSharesOfFirm.copy()
                for i in range(common.numberOfFirms):
                    book = self.bookList[i]
                    preferenceValue = pref[i]
                    action = actions[i]
                    dictOfAdvices[book][action] += 1
                    dictOfAdvices[book]["W"] += preferenceValue * connectionWeight
                    dictOfAdvices[book]["Infl"].append([influencer,book, action])
        
            for k, dic2 in dictOfAdvices.items():
                
                copy_pref_list = influenced.preferencesForFirmInStockMarket.copy()
                ind = 0
                for i, b in enumerate(self.bookList):
                    if b == k:
                        ind = i
                        
                        
                thold = copy_pref_list[ind] * 2
                
                if dic2["W"]>thold:
                    temporaryListOfActions = ["Ask", "Bid", "Hold"]
                    temporaryListOfValues = [0]*len(temporaryListOfActions)
                    for k2, val in dic2.items():
                        if k2 == "Ask":
                            temporaryListOfValues[0] = dic2[k2]
                        if k2 == "Bid":
                            temporaryListOfValues[1] = dic2[k2]
                        if k2 == "Hold":
                            temporaryListOfValues[2] = dic2[k2]
                    max_index = temporaryListOfValues.index(max(temporaryListOfValues))
                    if temporaryListOfValues[0] == temporaryListOfValues[1] == temporaryListOfValues[2]:
                        max_index = np.random.randint(3)
                    winningAction = temporaryListOfActions[max_index]
                    if common.verbose:
                        print("\t Advices for",k, [(temporaryListOfActions[i],temporaryListOfValues[i]) for i in range(3)])
                        print("\t Winning action:", winningAction)
                    for adviser, book, action in dic2["Infl"]:
                        if action == winningAction:
                            if common.verbose:
                                print("\t", adviser, "adviced the action")
                            self.influenceInATurnDic[influenced][adviser].append([book, action])
                else:
                    if common.verbose:
                        print("\t Advices for", k, "Not over threshold")
            del dictOfAdvices
            if common.verbose:print()
            
            
    def updateWeights(self):
        """
        updates the weights on the underlying graph based on the effectiveness of the advices
        """
        
        for influenced, dic2 in self.influenceInATurnDic.items():
            if common.verbose:
                print(influenced, "is influenced")
            for influencer, vals in dic2.items():
                if common.verbose:
                    print("\t", influencer, "is influencer")
                for book, suggestedAction in vals:
                    if common.verbose:
                        print("\t with", action, "for", book)

                    for i, b in enumerate(self.bookList):
                        if b == book:
                            index = i

                    historicalOfBook = book.historicList.copy()
                    if len(historicalOfBook) > 1:

                        reversedHistoricalOfBook = historicalOfBook[::-1]
                        currentSharesOfFirm = influenced.stockForSharesOfFirms[index] 

                        if currentSharesOfFirm:
                            if reversedHistoricalOfBook[0][:2] != [None,None] and reversedHistoricalOfBook[1][:2]!= [None,None]:
                                #azione sale
                                if np.mean(reversedHistoricalOfBook[0][:2]) > np.mean(reversedHistoricalOfBook[1][:2]):
                                    if suggestedAction == "Ask": #il soggetto vende 
                                        if common.verbose:
                                            print("\t\tLost having listened to advices. Decreasing strength of connection.")
                                        decrement = 0.8
                                        self.G.edges[influencer, influenced]["Weight"] *= decrement
                                    elif suggestedAction == "Bid" or suggestedAction == "Hold":
                                        if common.verbose:
                                            print("\t\tWon having listened to advices. Increasing strength of connection.")
                                        increment = 1.15
                                        self.G.edges[influencer, influenced]["Weight"] *= increment
                                #azione scende
                                else:
                                    if suggestedAction == "Ask":
                                        if common.verbose:
                                            print("\t\tWon having listened to advices. Increasing strength of connection.")
                                        increment = 1.15 
                                        self.G.edges[influencer, influenced]["Weight"] *= increment
                                    elif suggestedAction == "Bid" or suggestedAction == "Hold":
                                        if common.verbose:
                                            print("\t\tLost having listened to advices. Decreasing strength of connection.")
                                        decrement = 0.8
                                        self.G.edges[influencer, influenced]["Weight"] *= decrement
                        else:
                            if common.verbose:
                                print("\t\tNot enough data to analyze for the agent")
                    else:
                        if common.verbose:
                            print("\t\tNot enough data to analyze for the agent")        


        
    def resetAllVariablesForTheNetwork(self):
        """
        reset all the variables used by the network in a cycle
        """
        del self.H
        del self.connectionsInATurn
        del self.influenceInATurnDic
        self.H = nx.DiGraph()
        self.connectionsInATurn = []
        self.influenceInATurnDic = {}


    def candlestickForShares(self):
        """
        plot of the price for the shares of all the firms in the cycles
        """
        numberOfBooks = len(self.bookList)
        plt.figure(figsize = (21,13*numberOfBooks/3))
        

        for index in range(numberOfBooks): 
            plt.subplot(math.ceil(numberOfBooks/2),2,index+1)

            ohlc_values = []
            plt.title(self.bookList[index])
            plt.xlabel('tick')
            plt.ylabel('Price')

            for tick in range(common.numberOfCycles):

                # time, open, high, low, close
                if self.bookList[index].historicList[tick][0] == None:
                    high = 0
                else:
                    high = self.bookList[index].historicList[tick][0]
                if self.bookList[index].historicList[tick][1] == None:
                    low = 0
                else:
                    low = self.bookList[index].historicList[tick][1]
                opn = self.bookList[index].historicList[tick][2]
                cls = self.bookList[index].historicList[tick][3]
                ohlc_values.append([tick, opn, high, low , cls])

            candlestick_ohlc(plt.subplot(math.ceil(numberOfBooks/2), 2 ,index+1), ohlc_values, width=1, colorup='b', colordown='r')
        plt.savefig("shares_" + str(common.nameForFigSaving))
        plt.show()

    def plotOfPriceForGoods(self):
        """
        plot of the price for goods for all the firms in the cycles
        """
        plt.figure(figsize = (13,8))
        plt.title("Price for goods")
        for f in self.firmList:
            plt.plot(f.listOfAveragePreviousPrices, alpha = 0.4)
            plt.legend(self.firmList)
        aaa = np.array([firm.listOfAveragePreviousPrices for firm in self.firmList])
        avg = [sum(day)/len(day) for day in aaa.T]
        plt.plot(range(len(avg)) , avg, "r")
        plt.xlabel("Tick")
        plt.ylabel("Unit")
        plt.savefig("price_"+ str(common.nameForFigSaving))
        plt.show()
        
    def plotOfInterestRate(self):
        """
        plot of the global interest rate in the cycles
        """
        interestRateSchedule = pd.read_csv(common.urlOfInterestRateSchedule)
        interestRateList = []
        for tick in range(common.numberOfCycles):
            stopping = False
            for timeIndex in range(len(interestRateSchedule)):
                tickThreshold = interestRateSchedule.iloc[timeIndex]["Tick"]
                if tick < tickThreshold and stopping == False:
                    scheduledInterestRate = interestRateSchedule.iloc[timeIndex]["Rate"]
                    if scheduledInterestRate == "High":
                        IntRate = 3
                    elif scheduledInterestRate == "Medium":
                        IntRate = 2
                    elif scheduledInterestRate == "Low":
                        IntRate = 1
                    interestRateList.append(IntRate)
                    stopping = True

        plt.figure(figsize=(13, 8))
        plt.title("Interest Rate")
        plt.xlabel("Tick")
        plt.ylabel("Interest Rate")
        plt.plot(range(common.numberOfCycles) , interestRateList)
        plt.savefig("interestRate_" + str(common.nameForFigSaving))
        plt.show()