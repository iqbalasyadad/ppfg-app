import os
import pandas as pd

class WellTrajectory:

    def __init__(self):
        pass
    
    def readGenFile(self, genFile):
        df = pd.read_csv(genFile)
        self.setGenDF(df)

    def setGenDF(self, genDF):
        self._genDF = genDF
    
    def getGenDF(self):
        return self._genDF
    
    def getWellNames(self):
        genDF = self.getGenDF()
        wellNamesDF = genDF[['SHORT_NAME']].drop_duplicates()
        wellNames = wellNamesDF['SHORT_NAME'].values
        return wellNames
    
    def setWellParentFolder(self, wellParentFolder):
        self._wellParentFolder = wellParentFolder
    
    def getWellParentFolder(self):
        return self._wellParentFolder
    
    def getWellTrajectoryDic(self, wellName):
        wellParentFolder = self.getWellParentFolder()
        trajectoryFilePath = os.path.join(*[wellParentFolder, wellName, wellName+'_position.csv'])
        
        xs = []
        ys = []
        if os.path.exists(trajectoryFilePath):
            wellTrajectoryDF = pd.read_csv(trajectoryFilePath)
            wellTrajectoryDF = wellTrajectoryDF.drop_duplicates()
            wellTrajectoryDF = wellTrajectoryDF.sort_values(by="Z")
            xs = wellTrajectoryDF['X'].values.tolist()
            ys = wellTrajectoryDF['Y'].values.tolist()

        trajectoryDic = {
            "SHORT_NAME": wellName,
            "X": xs,
            "Y": ys,
        }

        return trajectoryDic

    def getWellsTrajectoryRecords(self, wellNames):
        wellsTrajectoryRecords = []
        for wellName in wellNames:
            wellTrajectoryDic = self.getWellTrajectoryDic(wellName)
            wellsTrajectoryRecords.append(wellTrajectoryDic)
        return wellsTrajectoryRecords