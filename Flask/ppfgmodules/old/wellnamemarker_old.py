import pandas as pd
import numpy as np

class CWellMarker:

    def __init__(self):
        pass

    def setMarkerFile(self, f):
        df =  pd.read_csv(f)
        df = df.drop_duplicates()
        self.setMarkerDF(df)

    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self):
        return self._markerDF
    
    def getAllMarkerDict(self):
        markersDF = self.getMarkerDF()
        markerNamesList = markersDF['MARKER_NAME'].unique().tolist()
        markerNamesDF = pd.DataFrame({"MARKER_NAME": markerNamesList})
        return markerNamesDF.to_dict(orient='records')
    
    def getWellsXY(self, markerName):
        markersDF = self.getMarkerDF()
        markerDF = markersDF[markersDF['MARKER_NAME']==markerName]
        wellNames = markerDF['SHORT_NAME'].values.tolist()
        wellXs = markerDF['MARKER_X_M'].values.tolist()
        wellYs = markerDF['MARKER_Y_M'].values.tolist()
        return {
            "SHORT_NAME": wellNames,
            "X": wellXs,
            "Y": wellYs
        }

class CWellName:

    def __init__(self):
        pass

    def readGenFile(self, summFile):
        genDF = pd.read_csv(summFile)
        self.setGenDF(genDF)
    
    def setGenDF(self, genDF):
        self._genDF = genDF
    
    def getGenDF(self):
        return self._genDF
    
    def readMarkerFile(self, markerFile):
        markerDF =  pd.read_csv(markerFile)
        markerDF = markerDF.drop_duplicates()
        self.setMarkerDF(markerDF)

    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self):
        return self._markerDF
    
    def getAllWellNameDict(self):
        genDF = self.getGenDF()
        markerDF = self.getMarkerDF()
        wellNamesGenList = np.sort(genDF['SHORT_NAME'].unique().tolist())
        wellNamesMarkerList = np.sort(markerDF['SHORT_NAME'].unique().tolist())
        wellNamesList = np.intersect1d(wellNamesGenList, wellNamesMarkerList)
        wellNamesDF = pd.DataFrame({"SHORT_NAME": wellNamesList})
        return wellNamesDF.to_dict(orient='records')