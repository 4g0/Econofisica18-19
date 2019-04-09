INTRODUCTION
The purpose of this model is to study, through agent-based simulation:

 - the evolution of prices depending on the interest rate;

 - the reciprocal influence among agents through the methodology of networks aimed at behavior in the stock market.

HOW TO SET
It is possible to choose the schedules of the interest rate and of the actions executed by agents. For the interest rate schedule, you can set the interest rate (Low, Medium, High) and how many cycles it should remain (i.e. 50 cycles). For the actions schedule, you can set the actions that will execute the agents and their order of execution, specifying the type of agent and the action.

HOW TO USE
You can start the execution of the model with the Model.ipynb file. 

It is possible to decide:
- the number of households
- the percentage of households that will act like numbs (randomly choosing the action to do, just depending on the current interest rate) in the stock market
- the number of firms, that will also be the number of titles in the stock market
- the number of cycles to run
- the seed for the random function
- the "verbose", that permits to have a comment and the results of every action done by the agents
- if the network for reciprocal influences should be enabled (and, in case, the probability of a connection between agents)
- if the unemployment should be implemented

If none of these parameters is chosen, it is possible to use the default ones.

WHAT HAPPENS
After the model has performed as requested, it will provide as results all the graphs necessary to understand what happened during the entire period: interest rate, price in the goods market, prices in the stock market, unemployment rate.
