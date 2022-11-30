import os
import pandas as pd

class DeviationSurvey:

    def __init__(self):
        pass

    def readDeviationSurveyFile(self, deviationSurveyFile):
        devSurDF = pd.read_csv(deviationSurveyFile)
        self.setDeviationSurveyDF(devSurDF)
    
    def setDeviationSurveyDF(self, devSurDF):
        self._devSurDF = devSurDF
    
    def getDeviationSurveyDF(self):
        return self._devSurDF

    def getAllWellNames(self):
        devSurDF = self.getDeviationSurveyDF()
        wellNames = devSurDF['SHORT_NAME'].unique()
        return wellNames
        
    def getWellDeviationSurveyDF(self, wellName):
        devSurDF = self.getDeviationSurveyDF()
        wellDevSurDF = devSurDF[devSurDF['SHORT_NAME']==wellName]
        wellDevSurDF = wellDevSurDF.sort_values(by="TVDSS")
        return wellDevSurDF