import os
import pandas as pd

class CombineTraceCommon:
    
    def __init__(self):
        pass
    
    def __init__(self):
        self.fmtNames = {
            'PP': 'PP',
            'FG': 'FG',
            'OBG': 'OBG',
            'MW': 'MW',
            'ECD': 'ECD',
            'casing': 'casing',
        }
        self.fmtEmptyHeader = {
            'PP': ['PP_TVDSS_M', 'PP_SG'],
            'FG': ['FG_TVDSS_M', 'FG_SG'],
            'OBG': ['OBG_TVDSS_M', 'OBG_SG'],
            'MW': ['MW_TVDSS_M', 'MW_SG'],
            'ECD': ['ECD_TVDSS_M', 'ECD_SG'],
            'casing': ['CASING_SIZE_INCH', 'CASING_TVDSS_M'],
        }

    def setWellRootFolder(self, wellRootFolder):
        self._wellRootFolder = wellRootFolder

    def getWellRootFolder(self):
        return self._wellRootFolder

    def setPPPFolderName(self, pppFolder):
        self._pppFolderName = pppFolder

    def getPPPFolderName(self):
        return self._pppFolderName

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

    def getDic_wellPPP(self, wellName):
        PP_Dic = self.getDF_PP(wellName).to_dict(orient='list')
        MW_Dic = self.getDF_MW(wellName).to_dict(orient='list')

        wellName_Dic = {"SHORT_NAME": wellName}
        wellPPP_Dic = {}
        for d in [PP_Dic, MW_Dic, wellName_Dic]:
            wellPPP_Dic.update(d)
        return wellPPP_Dic

    def getDic_wellsPPP(self, wellNames):
        wellsPPP_Dic = {}
        for i, wellName in enumerate(wellNames):
            wellsPPP_Dic[i] = self.getDic_wellPPP(wellName)
        return wellsPPP_Dic