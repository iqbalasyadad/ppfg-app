import os
import pandas as pd
import numpy as np

class PPPPost:
    
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
            'log': 'log',
            'PPFG_marker': 'PPFG_marker'
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
            'log': ['MD', 'TVDSS', 'GR', 'NPHI', 'RHOB', 'RT', 'DT'],
            'PPFG_marker': ['PPFG_MARKER_NAME', 'PPFG_MARKER_TVDSS_M', 'PPFG_MARKER_PLOT_X']
        }

    def setWellRootFolder(self, wellRootFolder):
        self._wellRootFolder = wellRootFolder

    def getWellRootFolder(self):
        return self._wellRootFolder
    
    def setLogFolder(self, logFolder):
        self._logFolder = logFolder
    
    def getLogFolder(self):
        return self._logFolder

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
        wellMarkerDF['MARKER_PLOT_X'] = 2.5
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
            df['PPFG_MARKER_PLOT_X'] = 2.5
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
            df['CASING_PLOT_X'] = 0
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

    def getDF_Event(self, wellName):
        usedCols = ['EVENT_PLOT_X', 'EVENT_PLOT_Y', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
        wEventDF = self.getEventDF(wellName)[usedCols]
        return wEventDF

    def getDF_log(self, wellName):
        logFolder = self.getLogFolder()
        logFilePath = os.path.join(logFolder, wellName+'.csv')
        if os.path.exists(logFilePath):
            logDF = pd.read_csv(logFilePath, skiprows=[1]).replace(-999.25, np.nan)
        else:
            logDF = pd.DataFrame(columns=self.fmtEmptyHeader['log'])
        return logDF
    
    def normalizeArr(self, arr):
        arrMin = min(arr)
        arrMax = max(arr)

        arrNorm = [] 
        for val in arr:
            valNorm = (val-arrMin)/(arrMax-arrMin)
            arrNorm.append(valNorm)
        return arrNorm

    def getDF_NormalizedDT(self, wellName):
        logDF = self.getDF_log(wellName)
        usedCols = ['TVDSS', 'DT']
        if set(usedCols).issubset(logDF.columns):
            DT_DF = logDF[usedCols].dropna()
        else:
            DT_DF = pd.DataFrame(columns=usedCols)
        
        DT_DF = DT_DF.rename(columns={'TVDSS': 'DT_TVDSS_M', 'DT': 'DT_USF'})     
        if DT_DF.empty:
            return DT_DF
        else:
            DTVals = DT_DF['DT_USF'].values
            # DTValsNorm = np.array(self.normalizeArr(DTVals))
            DTValsNorm = DTVals/100
            DTNorm_DF = pd.DataFrame({
                'DT_TVDSS_M': DT_DF['DT_TVDSS_M'].values,
                'DT_USF': DTValsNorm
            })
            return DTNorm_DF

    def getDF_NormalizedRT(self, wellName):
        logDF = self.getDF_log(wellName)
        usedCols = ['TVDSS', 'RT']
        if set(usedCols).issubset(logDF.columns):
            RT_DF = logDF[usedCols].dropna()
        else:
            RT_DF = pd.DataFrame(columns=usedCols)
        
        RT_DF = RT_DF.rename(columns={'TVDSS': 'RT_TVDSS_M', 'RT': 'RT_OHMM'})     
        if RT_DF.empty:
            return RT_DF
        else:
            RTVals = RT_DF['RT_OHMM'].values
            # RTValsNorm = np.array(self.normalizeArr(RTVals))
            RTValsNorm = RTVals/20
            RTNorm_DF = pd.DataFrame({
                'RT_TVDSS_M': RT_DF['RT_TVDSS_M'].values,
                'RT_OHMM': RTValsNorm
            })
            return RTNorm_DF    

    def getDic_wellPPP(self, wellName):
        PP_Dic = {'PP': self.getDF_PP(wellName).to_dict(orient='list')}
        FG_Dic = {'FG': self.getDF_FG(wellName).to_dict(orient='list')}
        OBG_Dic = {'OBG': self.getDF_OBG(wellName).to_dict(orient='list')}
        MW_Dic = {'MW': self.getDF_MW(wellName).to_dict(orient='list')}
        ECD_Dic = {'ECD': self.getDF_ECD(wellName).to_dict(orient='list')}
        marker_Dic = {'MARKER': self.getDF_Marker(wellName).to_dict(orient='list')}
        casing_Dic = {'CASING': self.getDF_Casing(wellName).to_dict(orient='list')}
        LOT_Dic = {'LOT': self.getDF_LOT(wellName).to_dict(orient='list')}
        PT_Dic = {'PT': self.getDF_PT(wellName).to_dict(orient='list')}
        event_Dic = {'EVENT': self.getDF_Event(wellName).to_dict(orient='list')}
        DT_Dic = {'DT': self.getDF_NormalizedDT(wellName).to_dict(orient='list')}
        RT_Dic = {'RT': self.getDF_NormalizedRT(wellName).to_dict(orient='list')}
        PPFG_marker_Dic = {'PPFG_MARKER': self.getDF_PPFG_marker(wellName).to_dict(orient='list')}

        wellName_Dic = {"SHORT_NAME": wellName}

        wellPPP_Dic = {}
        for d in [wellName_Dic, PP_Dic, FG_Dic, OBG_Dic, MW_Dic, PPFG_marker_Dic,
                    ECD_Dic, marker_Dic, casing_Dic, LOT_Dic, PT_Dic, event_Dic, DT_Dic, RT_Dic]:
            wellPPP_Dic.update(d)
        return wellPPP_Dic

    def getList_wellsPPP(self, wellNames):
        wellsPPP_List = []
        for wellName in wellNames:
            wellPPP_Dic = self.getDic_wellPPP(wellName)
            wellsPPP_List.append(wellPPP_Dic)
        return wellsPPP_List

    def getDic_wellsPPP(self, sWellNames):
        wellsPPP_List = self.getList_wellsPPP(sWellNames)
        wellsAnm_Dic = {
            "pppPost": wellsPPP_List,
            "someVal": 'some_val'
        }
        return wellsAnm_Dic