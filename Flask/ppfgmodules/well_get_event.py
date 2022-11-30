import os
import pandas as pd

class WellEvent:

    def __init__(self):
        pass

    def readEventFile(self, eventFile):
        usedCols = ['SHORT_NAME', 'EVENT_PLOT_SG', 'EVENT_PLOT_TVDSS_M', 'EVENT_TVDSS_M', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
        eventDF = pd.read_csv(eventFile, usecols=usedCols)
        self.setEventDF(eventDF)
    
    def setEventDF(self, eventDF):
        self._eventDF = eventDF
    
    def getEventDF(self):
        return self._eventDF
    
    def getWellsEventDF(self, wellNames):
        eventDF = self.getEventDF()
        wellsEventDF = eventDF.loc[eventDF['SHORT_NAME'].isin(wellNames)]
        wellsEventDF = wellsEventDF.sort_values(by='SHORT_NAME')
        return wellsEventDF

    def getWellsEventRecords(self, wellNames):
        wellsEventDF = self.getWellsEventDF(wellNames)
        wellsEventDF = wellsEventDF.fillna("")
        wellsEventRecords = wellsEventDF.to_dict(orient='records')
        return wellsEventRecords