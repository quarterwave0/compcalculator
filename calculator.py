import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

simLength = 6 #years
inflationRate = 0.034 #percent 12mo inflation
taxationCoeff = 0.63 #CA and national income tax

baseSalary = 250 #,000 $
bonusCoeff = 0.15 #what percent of salary for yearly bonus?
yearlyRaise = 1.04 #percent yearly raise

signingBonus = 40 #,000 $
initialStockGrant = 250 #,000 $
vestingPeriod = 0.25 # % vested per year
refresherCoeff = 0.8 # what percent of last year's salary is given as refreshers?
stockAppreciation = 1.15 #how much does the stock value appreciate per year

currentTC = 200 #,000 $
currentRent = 5*12 #,000 $ yearly after tax
currentOtherExpenses = 10 #,000 $ yearly after tax

targetRent = 5*12 #,000 $ yearly after tax
targetOtherExpenses = 10 #,000 $ yearly after tax
targetStockLiquidation = 0.2 #percent of stock to liquidate yearly after tax
retirementContrib = 10 #,000 $ yearly before taxes

yearlyRaise = yearlyRaise - inflationRate
stockAppreciation = stockAppreciation - inflationRate
vestingYears = int(vestingPeriod**-1)

def calculateIncome():
    salary = np.ones(simLength) * baseSalary
    stock = np.zeros((simLength, simLength))
    stockHeld = np.zeros((simLength))
    stockSold = np.zeros((simLength))

    for i in range(simLength):

        if i==0:
            stock[i][i:i+vestingYears] = initialStockGrant*vestingPeriod
        else:
            salary[i] = salary[i-1]*yearlyRaise
            stock[i][i:i+vestingYears] = (salary[i-1]*refresherCoeff)*vestingPeriod

        for k in range(vestingYears):
            if(i+k<simLength):
                stock[i][i+k] = stock[i][i+k] * stockAppreciation ** k

    totalVesting = np.sum(stock, axis=0)
    newHeldStock = totalVesting * (1-targetStockLiquidation)
    stockSold = totalVesting * targetStockLiquidation

    for j in range(simLength):
        if j >= 1:
            stockHeld[j] = newHeldStock[j] + stockHeld[j-1]*stockAppreciation
        else:
            stockHeld[j] = newHeldStock[j]

    bonus = salary * bonusCoeff
    bonus[0] = bonus[0] + signingBonus

    return salary, bonus, stockSold, stockHeld

def calculateChartValues(salary, bonus, stockSold):
    withoutStock = np.sum((salary, bonus), axis=0)
    TC = np.sum((withoutStock, stockSold), axis=0)
    addl = (((TC-currentTC) - retirementContrib) * taxationCoeff - ((targetRent-currentRent)+(targetOtherExpenses-currentOtherExpenses)))/12

    return TC, addl

salary, bonus, stockSold, stockHeld = calculateIncome()

TC, additionalIncome = calculateChartValues(salary, bonus, stockSold)

fig, axs = plt.subplots((3), sharex=True)
axs[0].plot(TC*1000, ls='-', marker='o')
axs[0].set_title("Total Compensation")
axs[0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
axs[0].minorticks_on()
axs[0].grid(True, axis='x', which='major')
axs[0].grid(True, axis='y', which='major')

axs[1].plot(additionalIncome*1000, ls='-', marker='o')
axs[1].set_title("Additional Income Per Month")
axs[1].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
axs[1].minorticks_on()
axs[1].grid(True, axis='x', which='major')
axs[1].grid(True, axis='y', which='major')

axs[2].plot(stockHeld*1000, ls='-', color='orange', marker='o')
axs[2].set_title("Accrued Stock")
axs[2].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
axs[2].set_xlabel("Years")
axs[2].minorticks_on()
axs[2].grid(True, axis='x', which='major')
axs[2].grid(True, axis='y', which='major')

plt.show()