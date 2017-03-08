'''    
Created on Jul 26, 2016

@author: cesar
'''
import numpy as np
import pandas as pd

def pandasTSfromBag(datetimeBag,date0=None,datef=None,pandasSeries=None):
    """
    creates a time series from a bag i.e. a list like 
    
    @param pandasSeries
    @param datetimeBag: [date0,date1,date2,...]
    
    @return pandasSeries
    """
    if pandasSeries == None:
        if date0 == None:
            date0 = min(datetimeBag)
        if datef == None:
            datef = max(datetimeBag)
        dateRange = pd.date_range(date0,datef)
        values = np.zeros(len(dateRange))
        pandasSeries = pd.Series(values,index=dateRange)
        
    missedVisits = 0
    N = len(pandasSeries)
    
    #important variables
    t0 = int(pandasSeries.index[0].strftime("%s"))
    dt = int(pandasSeries.index[1].strftime("%s")) - int(pandasSeries.index[0].strftime("%s"))
    
    for date in datetimeBag:
        #main operation
        index = int(np.floor((int(date.strftime("%s")) - t0)/dt))
        if(index < N and index > 0):
            #print "index: ",index
            #print ((int(dateTuple[0].strftime("%s")) - t0)/dt)
            pandasSeries[index] += 1
        else:
            missedVisits += 1
                    
    return (missedVisits,pandasSeries)

def pandasTSfromTupleBag(pandasSeries,datetimeBag):
    """
    creates a time series from a bag i.e. a list like 
    
    @param pandasSeries
    @param datetimeBag: [date0,date1,date2,...]
    
    @return pandasSeries
    """
    missedVisits = 0
    N = len(pandasSeries)
    
    #important variables
    t0 = int(pandasSeries.index[0].strftime("%s"))
    dt = int(pandasSeries.index[1].strftime("%s")) - int(pandasSeries.index[0].strftime("%s"))
    
    for date_tuple in datetimeBag:
        date = date_tuple[0]
        #main operation
        index = int(np.floor((int(date.strftime("%s")) - t0)/dt))
        if(index < N and index > 0):
            #print "index: ",index
            #print ((int(dateTuple[0].strftime("%s")) - t0)/dt)
            pandasSeries[index] += date_tuple[1]
        else:
            missedVisits += 1
                    
    return (missedVisits,pandasSeries)

def normalizeAndShowTogether(name1,ts1,name2,ts2,name3,ts3):
    """
    """
    M = max(ts1.values)
    ts1N = ts1/M
    M3 = max(ts3.values)
    ts3N = ts3/M3
    
    return pd.DataFrame({name1:ts1N,name2:ts2,name3:ts3N})
