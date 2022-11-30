import os
import re
import pandas as pd
import numpy as np

class PostMortemProfile:

    def __init__(self):
        self.headerTemplate = {
            'PP': ['PP_TVDSS_M', 'PP_SG'],
            'FG': ['FG_TVDSS_M', 'FG_SG'],
            'OBG': ['OBG_TVDSS_M', 'OBG_SG'],
            'MW': ['MW_TVDSS_M', 'MW_SG'],
            'ECD': ['ECD_TVDSS_M', 'ECD_SG'],
            'casing': ['CASING_SIZE_INCH', 'CASING_TVDSS_M', 'CASING_PLOT_SG'],
            'LOT': ['LOT_TVDSS_M', 'LOT_SG'],
            'PT': ['PT_TVDSS_M', 'PT_SG'],
            'log': ['MD', 'TVDSS', 'GR', 'NPHI', 'RHOB', 'RT', 'DT'],
            'PPFG_marker': ['PPFG_MARKER_NAME', 'PPFG_MARKER_TVDSS_M', 'PPFG_MARKER_PLOT_SG']
        }

    def setPostMortemAsciiFolder(self, folder):
        self._postMortemAsciiFolder = folder
        pmAsciiWellNames = [os.path.splitext(f)[0] for f in os.listdir(folder)]
        self.setPostMortemAsciiWellFileNames(pmAsciiWellNames)
    
    def getPostMortemAsciiFolder(self):
        return self._postMortemAsciiFolder

    def setPostMortemAsciiWellFileNames(self, fnames):
        self._postMortemWellFileNames = fnames
    
    def getPostMortemAsciiWellFileNames(self):
        return self._postMortemWellFileNames
    
    def readEventFile(self, eventFile):
        usedCols = ['SHORT_NAME', 'EVENT_PLOT_SG', 'EVENT_PLOT_TVDSS_M', 'EVENT_TYPE', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
        eventDF = pd.read_csv(eventFile, usecols=usedCols)
        self.setEventDF(eventDF)
    
    def setEventDF(self, eventDF):
        self._eventDF = eventDF
    
    def getRawEventDF(self, wellName):
        if wellName:
            wEventDF = self._eventDF[self._eventDF['SHORT_NAME']==wellName]
            return wEventDF
        else:
            return self._eventDF

    def getWellEvent_DF(self, wellName):
        usedCols = ['EVENT_PLOT_SG', 'EVENT_PLOT_TVDSS_M', 'EVENT_DETAIL', 'EVENT_TYPE','EVENT_DESCRIPTION']
        wEventDF = self.getRawEventDF(wellName)[usedCols]
        return wEventDF

    def readMarkerFile(self, markerFile):
        df = pd.read_csv(markerFile)
        self.setMarkerDF(df)
    
    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getRawMarkerDF(self, wellName=None):
        if wellName:
            wMarkerDF = self._markerDF[self._markerDF['SHORT_NAME']==wellName]
            wMarkerDF = wMarkerDF.sort_values(by='MARKER_TVDSS_M')
            return wMarkerDF
        else:
            return self._markerDF

    def getWellMarker_DF(self, wellName):
        markerDF = self.getRawMarkerDF()
        wellMarkerDF = markerDF[markerDF['SHORT_NAME']==wellName][['MARKER_NAME', 'MARKER_TVDSS_M']]
        wellMarkerDF = wellMarkerDF.dropna()
        wellMarkerDF = wellMarkerDF.sort_values(by='MARKER_TVDSS_M')
        wellMarkerDF['MARKER_PLOT_SG'] = 2.5
        return wellMarkerDF

    def setLogFolder(self, logFolder):
        self._logFolder = logFolder
    
    def getLogFolder(self):
        return self._logFolder

    def getWellLog_DF(self, wellName):
        logFolder = self.getLogFolder()
        logFilePath = os.path.join(logFolder, wellName+'.csv')
        if os.path.exists(logFilePath):
            logDF = pd.read_csv(logFilePath, skiprows=[1]).replace(-999.25, np.nan)
        else:
            logDF = pd.DataFrame(columns=self.headerTemplate['log'])
        return logDF

    def getWellAdjustedDT_DF(self, wellName):
        logDF = self.getWellLog_DF(wellName)
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
        
    def getWellAdjustedRT_DF(self, wellName):
        logDF = self.getWellLog_DF(wellName)
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

    def getPostMortemAsciiWellDF(self, wellName):
        pmAsciiFolder = self.getPostMortemAsciiFolder()
        pmAsciiWellFileNames = self.getPostMortemAsciiWellFileNames()
        wellNameLower = wellName.lower()
        for pmAsciiWellFileName in pmAsciiWellFileNames:
            pmAsciiWellFileNameSplitted = re.split('\s|_', pmAsciiWellFileName.lower())
            if wellNameLower in pmAsciiWellFileNameSplitted:
                pmAsciiWellFilePath = os.path.join(pmAsciiFolder, pmAsciiWellFileName + '.csv')
                pmAsciiWellDF = pd.read_csv(pmAsciiWellFilePath)
                return pmAsciiWellDF
        emptyDF = pd.DataFrame()
        return emptyDF
    
    def getPostMortemAsciiWellPropDF(self, wellName, columns):
        pmAsciiWellDF = self.getPostMortemAsciiWellDF(wellName)
        pmAsciiWellPropDF = pd.DataFrame()
        for column in columns:
            if column in pmAsciiWellDF.columns:
                pmAsciiWellPropDF = pd.concat([pmAsciiWellPropDF, pmAsciiWellDF[[column]]], axis=1)
            else:
                pmAsciiWellPropDF[column] = np.nan
        return pmAsciiWellPropDF
    
    def getWellPP_DF(self, wellName):
        pmAsciiWellPropPPDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['PP'])
        pmAsciiWellPropPPDF = pmAsciiWellPropPPDF.dropna(subset=['PP_TVDSS_M', 'PP_SG'])
        return pmAsciiWellPropPPDF
    
    def getWellFG_DF(self, wellName):
        pmAsciiWellPropFGDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['FG'])
        pmAsciiWellPropFGDF = pmAsciiWellPropFGDF.dropna(subset=['FG_TVDSS_M', 'FG_SG'])
        return pmAsciiWellPropFGDF

    def getWellOBG_DF(self, wellName):
        pmAsciiWellPropOBGDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['OBG'])
        pmAsciiWellPropOBGDF = pmAsciiWellPropOBGDF.dropna(subset=['OBG_TVDSS_M', 'OBG_SG'])
        return pmAsciiWellPropOBGDF

    def getWellMW_DF(self, wellName):
        pmAsciiWellPropMWDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['MW'])
        pmAsciiWellPropMWDF = pmAsciiWellPropMWDF.dropna(subset=['MW_TVDSS_M', 'MW_SG'])
        return pmAsciiWellPropMWDF

    def getWellECD_DF(self, wellName):
        pmAsciiWellPropECDDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['ECD'])
        pmAsciiWellPropECDDF = pmAsciiWellPropECDDF.dropna(subset=['ECD_TVDSS_M', 'ECD_SG'])
        return pmAsciiWellPropECDDF

    def getWellCasing_DF(self, wellName):
        pmAsciiWellPropCasingDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['casing'])
        pmAsciiWellPropCasingDF = pmAsciiWellPropCasingDF.dropna(subset=['CASING_SIZE_INCH', 'CASING_TVDSS_M'])
        pmAsciiWellPropCasingDF['CASING_PLOT_SG'] = 0
        return pmAsciiWellPropCasingDF

    def getWellPT_DF(self, wellName):
        pmAsciiWellPropPTDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['PT'])
        pmAsciiWellPropPTDF = pmAsciiWellPropPTDF.dropna(subset=['PT_TVDSS_M', 'PT_SG'])
        return pmAsciiWellPropPTDF

    def getWellLOT_DF(self, wellName):
        pmAsciiWellPropLOTDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['LOT'])
        pmAsciiWellPropLOTDF = pmAsciiWellPropLOTDF.dropna(subset=['LOT_TVDSS_M', 'LOT_SG'])
        return pmAsciiWellPropLOTDF
    
    def getWellPPFGMarker_DF(self, wellName):
        pmAsciiWellPropPPFGMarkerDF = self.getPostMortemAsciiWellPropDF(wellName, self.headerTemplate['PPFG_marker'])
        pmAsciiWellPropPPFGMarkerDF = pmAsciiWellPropPPFGMarkerDF.dropna(subset=['PPFG_MARKER_NAME', 'PPFG_MARKER_TVDSS_M'])
        pmAsciiWellPropPPFGMarkerDF['PPFG_MARKER_PLOT_SG'] = 2.5
        return pmAsciiWellPropPPFGMarkerDF
    
    def getWellPostMortemProfileDic(self, wellName):
        PP_Dic = {'PP': self.getWellPP_DF(wellName).to_dict(orient='list')}
        FG_Dic = {'FG': self.getWellFG_DF(wellName).to_dict(orient='list')}
        OBG_Dic = {'OBG': self.getWellOBG_DF(wellName).to_dict(orient='list')}
        MW_Dic = {'MW': self.getWellMW_DF(wellName).to_dict(orient='list')}
        ECD_Dic = {'ECD': self.getWellECD_DF(wellName).to_dict(orient='list')}
        marker_Dic = {'MARKER': self.getWellMarker_DF(wellName).to_dict(orient='list')}
        casing_Dic = {'CASING': self.getWellCasing_DF(wellName).to_dict(orient='list')}
        LOT_Dic = {'LOT': self.getWellLOT_DF(wellName).to_dict(orient='list')}
        PT_Dic = {'PT': self.getWellPT_DF(wellName).to_dict(orient='list')}
        event_Dic = {'EVENT': self.getWellEvent_DF(wellName).to_dict(orient='list')}
        DT_Dic = {'DT': self.getWellAdjustedDT_DF(wellName).to_dict(orient='list')}
        RT_Dic = {'RT': self.getWellAdjustedRT_DF(wellName).to_dict(orient='list')}
        PPFG_marker_Dic = {'PPFG_MARKER': self.getWellPPFGMarker_DF(wellName).to_dict(orient='list')}

        wellName_Dic = {"SHORT_NAME": wellName}

        wellPostMortem_Dic = {}
        for d in [wellName_Dic, PP_Dic, FG_Dic, OBG_Dic, MW_Dic, PPFG_marker_Dic,
                    ECD_Dic, marker_Dic, casing_Dic, LOT_Dic, PT_Dic, event_Dic, DT_Dic, RT_Dic]:
            wellPostMortem_Dic.update(d)
        return wellPostMortem_Dic

    def getWellsPostMortemProfileList(self, wellNames):
        wellsPostMortemList = []
        for wellName in wellNames:
            wellPPP_Dic = self.getWellPostMortemProfileDic(wellName)
            wellsPostMortemList.append(wellPPP_Dic)
        return wellsPostMortemList

    def getWellsPostMortemProfileDic(self, wellNames):
        wellsPostMortemList = self.getWellsPostMortemProfileList(wellNames)
        wellsPostMortemDic = {
            "postMortemProfileRecords": wellsPostMortemList,
        }
        return wellsPostMortemDic