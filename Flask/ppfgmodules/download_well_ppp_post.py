import os
import pandas as pd

class PPPDownloadFile:
    
    def __init__(self):
        self.fmtNames = {
            'PP': 'PP',
            'FG': 'FG',
            'OBG': 'OBG',
            'MW': 'MW',
            'ECD': 'ECD',
            'casing': 'casing',
            'LOT': 'LOT',
            'PT': 'PT',
            'PPFG_marker': 'PPFG_marker',
        }
        self.fmtEmptyHeader = {
            'PP': ['PP_TVDSS_M', 'PP_SG'],
            'FG': ['FG_TVDSS_M', 'FG_SG'],
            'OBG': ['OBG_TVDSS_M', 'OBG_SG'],
            'MW': ['MW_TVDSS_M', 'MW_SG'],
            'ECD': ['ECD_TVDSS_M', 'ECD_SG'],
            'casing': ['CASING_SIZE_INCH', 'CASING_TVDSS_M'],
            'LOT': ['LOT_TVDSS_M', 'LOT_SG'],
            'PT': ['PT_TVDSS_M', 'PT_SG'],
            'PPFG_marker': ['PPFG_MARKER_NAME', 'PPFG_MARKER_TVDSS_M'],
        }
    
    def setOutputFolder(self, outputFolder):
        self._outputFolder = outputFolder
    
    def getOutputFolder(self):
        return self._outputFolder

    def setWellRootFolder(self, wellRootFolder):
        self._wellRootFolder = wellRootFolder

    def getWellRootFolder(self):
        return self._wellRootFolder

    def setPPPFolderName(self, pppFolder):
        self._pppFolderName = pppFolder

    def getPPPFolderName(self):
        return self._pppFolderName
    
    def readMarkerFile(self, markerFile):
        df = pd.read_csv(markerFile)
        self.setMarkerDF(df)
    
    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self, wellName=None):
        if wellName:
            wMarkerDF = self._markerDF[self._markerDF['SHORT_NAME']==wellName]
            wMarkerDF = wMarkerDF.sort_values(by='MARKER_TVDSS_M')
            return wMarkerDF
        else:
            return self._markerDF
    
    def readEventFile(self, eventFile):
        usedCols = ['SHORT_NAME', 'EVENT_PLOT_X', 'EVENT_PLOT_Y', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
        eventDF = pd.read_csv(eventFile, usecols=usedCols)
        self.setEventDF(eventDF)
    
    def setEventDF(self, eventDF):
        self._eventDF = eventDF
    
    def getEventDF(self, wellName):
        if wellName:
            wEventDF = self._eventDF[self._eventDF['SHORT_NAME']==wellName]
            return wEventDF
        else:
            return self._eventDF
    
    def getDF_Marker(self, wellName):
        markerDF = self.getMarkerDF().dropna()
        wellMarkerDF = markerDF[markerDF['SHORT_NAME']==wellName][['MARKER_NAME', 'MARKER_TVDSS_M']]
        wellMarkerDF = wellMarkerDF.sort_values(by='MARKER_TVDSS_M')
        wellMarkerDF = wellMarkerDF.reset_index(drop=True)
        return wellMarkerDF

    def getDF_PP(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        PP_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['PP']))
        try:
            df = pd.read_csv(PP_File).dropna()
        except Exception as err:
            print(err)
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['PP'])
            return emptyDF
        else:
            return df

    def getDF_FG(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        FG_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['FG']))
        try:
            df = pd.read_csv(FG_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['FG'])
            return emptyDF
        else:
            return df
    
    def getDF_OBG(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        OBG_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['OBG']))
        try:
            df = pd.read_csv(OBG_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['OBG'])
            return emptyDF
        else:
            return df

    def getDF_MW(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        MW_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['MW']))
        try:
            df = pd.read_csv(MW_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['MW'])
            return emptyDF
        else:
            return df

    def getDF_ECD(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        ECD_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['ECD']))
        try:
            df = pd.read_csv(ECD_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['ECD'])
            return emptyDF
        else:
            return df

    def getDF_LOT(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        LOT_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['LOT']))
        try:
            usedCols = ['LOT_TVDSS_M', 'LOT_SG']
            df = pd.read_csv(LOT_File, usecols=usedCols)
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['LOT'])
            return emptyDF
        else:
            return df

    def getDF_PT(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        LOT_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['PT']))
        try:
            usedCols = ['PT_TVDSS_M', 'PT_SG']
            df = pd.read_csv(LOT_File, usecols=usedCols)
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['PT'])
            return emptyDF
        else:
            return df

    def getDF_Casing(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        casing_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['casing']))
        try:
            df = pd.read_csv(casing_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['casing'])
            return emptyDF
        else:
            return df

    def getDF_PPFG_marker(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        PPFG_marker_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['PPFG_marker']))
        try:
            df = pd.read_csv(PPFG_marker_File).dropna()
        except Exception as err:
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['PPFG_marker'])
            return emptyDF
        else:
            return df

    def getDF_PPPPost(self, wellName):
        PP_DF = self.getDF_PP(wellName)
        FG_DF = self.getDF_FG(wellName)
        OBG_DF = self.getDF_OBG(wellName)
        MW_DF = self.getDF_MW(wellName)
        ECD_DF = self.getDF_ECD(wellName)
        LOT_DF = self.getDF_LOT(wellName)
        PT_DF = self.getDF_PT(wellName)
        casing_DF = self.getDF_Casing(wellName)
        marker_DF = self.getDF_Marker(wellName)
        PPFG_marker_DF = self.getDF_PPFG_marker(wellName)

        frames = [PP_DF, FG_DF, OBG_DF, MW_DF, ECD_DF, LOT_DF, PT_DF, casing_DF, marker_DF, PPFG_marker_DF]
        resultDF = pd.concat(frames, axis=1, join='outer')
        return resultDF
    
    def saveDF_PPPPost(self, wellName):
        outputFolder = self.getOutputFolder()
        if not os.path.exists(outputFolder):
            os.mkdir(outputFolder)
        pppPostDF = self.getDF_PPPPost(wellName)
        outputFile = os.path.join(outputFolder, '{}_ppppost.csv'.format(wellName))
        pppPostDF.to_csv(outputFile, index=False)