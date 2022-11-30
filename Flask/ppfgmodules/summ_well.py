import os
import numpy as np
import pandas as pd
import re

class SummWellRecord:

    def __init__(self):
        self._kmtom = 1000

    def setMapMarker(self, markerName):
        self._mapMarker = markerName
    
    def getMapMarker(self):
        return self._mapMarker

    def setPropWell(self, propWell):
        self._propWell = propWell
    
    def getPropWell(self):
        return self._propWell

    # def setWellRootFolder(self, wellFolder):
    #     self._wellRootFolder = wellFolder
    
    # def getWellRootFolder(self):
    #     return self._wellRootFolder
    
    def setLogFolder(self, logFolder):
        self._logFolder = logFolder
    
    def getLogFolder(self):
        return self._logFolder
    
    # def setPPFGFolder(self, PPFG_Folder):
    #     self._PPFGFolder = PPFG_Folder
    
    # def getPPFGFolder(self):
    #     return self._PPFGFolder

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
        
    def readWellAddInfo(self, wellAddInfoFile):
        wellAddInfoDF = pd.read_csv(wellAddInfoFile)
        self.setWellAddInfoDF(wellAddInfoDF)
    
    def setWellAddInfoDF(self, wellAddInfoDF):
        self._wellAddInfoDF = wellAddInfoDF
    
    def getWellAddInfoDF(self):
        return self._wellAddInfoDF
    
    def getWTDSectionDic(self, wellName):
        wellsAddInfoDF = self.getWellAddInfoDF()
        wTDSectionDF = wellsAddInfoDF[wellsAddInfoDF['SHORT_NAME']==wellName]
        if wTDSectionDF.empty:
            resultwTDSection = ''
        else:
            resultwTDSection = wTDSectionDF['TD_SECTION_INCH'].values[0]
        wTDSectionDic = {
            'TD_SECTION_INCH': resultwTDSection,
        }
        return wTDSectionDic

    def readGenFile(self, genFile):
        genDF = pd.read_csv(genFile)
        self.setGenDF(genDF)
    
    def setGenDF(self, genDF):
        self._genDF = genDF
    
    def getGenDF(self):
        return self._genDF

    def getWGenDF(self, wellName):
        usedCols = ['SHORT_NAME', 'DRILLER_BOTTOM_X', 'DRILLER_BOTTOM_Y', 'TVDSS_DRILLER', 'SPUD_DATE']
        genDF = self.getGenDF()
        wellGenDF = genDF[genDF['SHORT_NAME']==wellName][usedCols]
        if wellGenDF.empty:
            wellGenDF['SHORT_NAME'] = [wellName]
        wellGenDF = wellGenDF.rename(columns={
            'DRILLER_BOTTOM_X': 'TD_X_M',
            'DRILLER_BOTTOM_Y': 'TD_Y_M',
            'TVDSS_DRILLER': 'TD_TVDSS_M',
            })
        return wellGenDF

    def getWGenDic(self, wellName):
        wGenDic = {
            'TD_X_M': '',
            'TD_Y_M': '',
            'TD_TVDSS_M': '',
            'TD_SECTION_INCH': '',
            'SPUD_DATE': ''
        }
        wGenDF = self.getWGenDF(wellName)
        if wGenDF.empty:
            return wGenDic
        else:
            wGenDic['TD_X_M'] = int(wGenDF['TD_X_M'].values[0])
            wGenDic['TD_Y_M'] = int(wGenDF['TD_Y_M'].values[0])
            wGenDic['TD_TVDSS_M'] = int(wGenDF['TD_TVDSS_M'].values[0])
            wGenDic['SPUD_DATE'] = wGenDF['SPUD_DATE'].values[0]
            return wGenDic

    def getTDXYZ(self, wellName):
        # genDF = self.getGenDF()
        # wgenDF = genDF[genDF['SHORT_NAME']==wellName]
        wgenDF = self.getWGenDF(wellName)
        tdx = int(wgenDF['TD_X_M'].values[0])
        tdy = int(wgenDF['TD_Y_M'].values[0])
        tdz = int(wgenDF['TD_TVDSS_M'].values[0])
        return tdx, tdy, tdz

    def getDepthMarker(self, wellName, depth):
        wMarkerDF = self.getMarkerDF(wellName)
        wLastMarkerDF = wMarkerDF[wMarkerDF['MARKER_TVDSS_M']<=depth].iloc[[-1]]
        markerName = wLastMarkerDF['MARKER_NAME'].values[0]
        markerDepth = int(wLastMarkerDF['MARKER_TVDSS_M'].values[0])
        markerPlus = round(depth - markerDepth, 1)
        return markerName, markerDepth, markerPlus
    
    def setSurrWellNames(self, surrWellNames):
        self._surrWellNames = surrWellNames
    
    def getSurrWellNames(self):
        return self._surrWellNames

    def setSurrWellPosDic(self, surrWellPos):
        self._surrWellPosDic = surrWellPos
    
    def getSurrWellPosDic(self):
        return self._surrWellPosDic
        
    def calcDist(self, pos1, pos2, mode):
        if mode=='3d':
            dist = np.sqrt((pos2['x']-pos1['x'])**2 + (pos2['y']-pos1['y'])**2 + (pos2['z']-pos1['z'])**2)
        elif mode=='2d':
            dist = np.sqrt((pos2['x']-pos1['x'])**2 + (pos2['y']-pos1['y'])**2)
        return dist
        
    def calcSurrWellPos(self, x, y, radius):
        mapMarkerName = self.getMapMarker()
        markerDF = self.getMarkerDF()
        markerOnMapDF = markerDF[markerDF['MARKER_NAME']==mapMarkerName]

        allWellNames = markerOnMapDF['SHORT_NAME'].values
        surrWellsName = []
        surrWellPosDic = {}
        for wellName in allWellNames:
            wMarkerDF = markerOnMapDF[markerOnMapDF['SHORT_NAME']==wellName]
            posPWell = {
                'x': x,
                'y': y }
            posSurrWell = {
                'x': int(wMarkerDF['X'].values[0]),
                'y': int(wMarkerDF['Y'].values[0]),
                'z': int(wMarkerDF['MARKER_TVDSS_M'].values[0])
            }
            dist2d = self.calcDist(posPWell, posSurrWell, mode='2d')

            if dist2d <= radius:
                surrWellsName.append(wellName)

                surrWellPosDic[wellName] = {
                    'x': posSurrWell['x'],
                    'y': posSurrWell['y'],
                    'dist': round(dist2d/self._kmtom, 2)
                }
        self.setSurrWellNames(surrWellsName)
        
        self.setSurrWellPosDic(surrWellPosDic)

    def readEventFile(self, eventFile):
        usedCols = ['SHORT_NAME', 'EVENT_DETAIL', 'EVENT_TVDSS_M']
        eventDF = pd.read_csv(eventFile, usecols=usedCols)
        self.setEventDF(eventDF)
    
    def setEventDF(self, eventDF):
        self._eventDF = eventDF
    
    def getEventDF(self, wellName=None):
        if wellName:
            wEventDF = self._eventDF[self._eventDF['SHORT_NAME']==wellName]
            return wEventDF
        else:
            return self._eventDF
    
    def getWEventSummDic(self, wellName):
        '''
        return df of well event flag and short desc
        '''
        wEventDF = self.getEventDF(wellName)
        eventFlag = ''
        eventShortDesc = ''
        wEventSummDic = {
            'EVENT_FLAG': eventFlag,
            'EVENT_SHORT_DESC': eventShortDesc
        }
        if wEventDF.empty:
            eventFlag = 'N'
            eventShortDesc = ''
        else:
            eventFlag = 'Y'
            eventTVDSSList = wEventDF['EVENT_TVDSS_M'].values
            eventDescList = wEventDF['EVENT_DETAIL'].values
            for i, eventDesc in enumerate(eventDescList):
                markerName, markerDepth, markerPlus = self.getDepthMarker(wellName, eventTVDSSList[i])
                eventShortDesc += '{} ({} +{})'.format(eventDesc, markerName, markerPlus)
                if i !=len(eventDescList)-1: 
                    eventShortDesc += ', '
                
        wEventSummDic['EVENT_FLAG'] = eventFlag
        wEventSummDic['EVENT_SHORT_DESC'] = eventShortDesc

        return wEventSummDic

    # def getMW(self, wellName, TVDSS):
    #     ''' 
    #     Get MW at well at TVDSS
    #     return: closest TVDSS, MW
    #     '''
    #     wfrFolder = self.getWellRootFolder()
    #     wellFolder = os.path.join(wfrFolder, wellName)
    #     ppfgFolder = self.getPPFGFolder()
    #     mwFolder = os.path.join(wellFolder, ppfgFolder)
    #     MWFileName = wellName+'_MW.csv'
    #     MWFilePath = os.path.join(mwFolder, MWFileName)
    #     MWTVDSS = np.nan
    #     MWVal = np.nan
    #     if os.path.exists(MWFilePath):
    #         MWDF = pd.read_csv(MWFilePath).dropna()
    #         if not MWDF.empty:
    #             MWDepthRanges = MWDF['MW_TVDSS_M'].values
    #             if TVDSS < min(MWDepthRanges) or TVDSS > max(MWDepthRanges) + 5:
    #                 return MWTVDSS, MWVal
    #             elif TVDSS in MWDepthRanges:
    #                 resultMWDF = MWDF[MWDF['MW_TVDSS_M']==TVDSS]
    #                 MWVal = resultMWDF['MW_SG'].values[0]
    #                 MWTVDSS = resultMWDF['MW_TVDSS_M'].values[0]
    #                 MWTVDSS = round(MWTVDSS)
    #                 MWVal = round(MWVal, 2)
    #             else:
    #                 resultMWDF = MWDF[MWDF['MW_TVDSS_M']<TVDSS]
    #                 MWVal = resultMWDF['MW_SG'].values[-1]
    #                 # MWTVDSS = resultMWDF['MW_TVDSS_M'].values[-1]
    #                 if TVDSS < max(MWDepthRanges) + 5:
    #                     MWTVDSS = TVDSS
    #                 else:
    #                     MWTVDSS = max(MWDepthRanges)
    #                 MWTVDSS = round(MWTVDSS)
    #                 MWVal = round(MWVal, 2)
    #         else:
    #             pass
    #     else:
    #         pass
    #     return MWTVDSS, MWVal

    def getMW(self, wellName, TVDSS):
        ''' 
        Get MW at well at TVDSS
        return: closest TVDSS, MW
        '''
        pmAsciiWellDF = self.getPostMortemAsciiWellDF(wellName)
        MWTVDSS = np.nan
        MWVal = np.nan

        if pmAsciiWellDF.empty:
            return MWTVDSS, MWVal

        if not set(['MW_TVDSS_M', 'MW_SG']).issubset(pmAsciiWellDF.columns):
            return MWTVDSS, MWVal

        MWDF = pmAsciiWellDF[['MW_TVDSS_M', 'MW_SG']]
        MWDepthRanges = MWDF['MW_TVDSS_M'].values
        if TVDSS < min(MWDepthRanges) or TVDSS > max(MWDepthRanges) + 5:
            return MWTVDSS, MWVal
        elif TVDSS in MWDepthRanges:
            resultMWDF = MWDF[MWDF['MW_TVDSS_M']==TVDSS]
            MWVal = resultMWDF['MW_SG'].values[0]
            MWTVDSS = resultMWDF['MW_TVDSS_M'].values[0]
            MWTVDSS = round(MWTVDSS)
            MWVal = round(MWVal, 2)
        else:
            resultMWDF = MWDF[MWDF['MW_TVDSS_M']<TVDSS]
            MWVal = resultMWDF['MW_SG'].values[-1]
            # MWTVDSS = resultMWDF['MW_TVDSS_M'].values[-1]
            if TVDSS < max(MWDepthRanges) + 5:
                MWTVDSS = TVDSS
            else:
                MWTVDSS = max(MWDepthRanges)
            MWTVDSS = round(MWTVDSS)
            MWVal = round(MWVal, 2)
        return MWTVDSS, MWVal

    def getTDMarkerDic(self, wellName):
        wGenDF = self.getWGenDF(wellName)
        if not wGenDF.empty:
            wTD = int(wGenDF['TD_TVDSS_M'].values[0])
            markerName, markerDepth, markerPlus = self.getDepthMarker(wellName, wTD)
            markerStr = "{} (+{})".format(markerName, int(markerPlus))
        else:
            markerStr = np.nan
        TDMarkerDic = { "TD_MARKER": markerStr }
        return TDMarkerDic

    def getTDMWDic(self, wellName):
        wGenDF = self.getWGenDF(wellName)
        if not wGenDF.empty:
            TD_TVDSS = int(wGenDF['TD_TVDSS_M'].values[0])
            MWTVDSS, MWVal = self.getMW(wellName, TD_TVDSS)
            if np.isnan(MWTVDSS): MWTVDSS=''
            if np.isnan(MWVal): MWVal=''
            # td_mw = "{} ({})".format(MWVal, MWTVDSS)
            td_mw = MWVal
        else:
            td_mw = np.nan
        TD_MW_Dic = { "TD_MW_SG": td_mw }
        return TD_MW_Dic

    def getWpONsDic(self, wellName):

        resultDic = {
            'PS_TD_MARKER': '',
            'PS_TD_TVDSS_M': '',
            'PS_TD_MW_SG': '',
            'PS_SHALLOWER_FLAG': ''
        }

        shallowerFlag = False
        pMarkerName = self.getPropWell()['TD']['marker_name']
        pMarkerPlus = self.getPropWell()['TD']['marker_plus']
  
        wMarkerDF = self.getMarkerDF(wellName)
        if wMarkerDF.empty:
            return resultDic
        else:
            wMarkerDF = wMarkerDF.sort_values(by='MARKER_TVDSS_M')

        pMarkerWellDF = wMarkerDF[wMarkerDF['MARKER_NAME']==pMarkerName]
        
        if pMarkerWellDF.empty:
            # surr well marker does not have proposed marker
            pOnsMarkerName = wMarkerDF['MARKER_NAME'].values[-1]
            pOnsMarkerTVDSS = wMarkerDF['MARKER_TVDSS_M'].values[-1]
            shallowerFlag = True
            pOnsMarkerPlus = '?'
        else:
            pOnsMarkerName = pMarkerWellDF['MARKER_NAME'].values[0]
            pOnsMarkerTVDSS = int(pMarkerWellDF['MARKER_TVDSS_M'].values[0])
            pOnsMarkerPlus = pMarkerPlus
        
        # get well td
        sTD_DF = self.getWGenDF(wellName)
        if sTD_DF.empty:
            shallowerFlag = True
        else:
            sTD_TVDSS = int(sTD_DF['TD_TVDSS_M'].values[0])
        
        if not shallowerFlag:
            pOns_TD_TVDSS = pOnsMarkerTVDSS + pOnsMarkerPlus
            if sTD_TVDSS < pOns_TD_TVDSS:
                shallowerFlag=True

        if not shallowerFlag:
            pOnsTD_MW_TVDSS, pOnsTD_MW_SG = self.getMW(wellName, pOns_TD_TVDSS)
            if np.isnan(pOnsTD_MW_TVDSS):
                pOnsTD_MW_TVDSS = ''
            if np.isnan(pOnsTD_MW_SG):
                pOnsTD_MW_SG = ''
        
        if shallowerFlag:
            resultTDMarker = 'shallower'
            resultTDTVDSS = 'shallower'
            resultTDMW = ''
            shallowerFlagText = 'Y'

        else:
            resultTDMarker = "{} (+{})".format(pOnsMarkerName, pOnsMarkerPlus)
            resultTDTVDSS = pOns_TD_TVDSS
            if pOnsTD_MW_SG == '' and pOnsTD_MW_TVDSS == '' :
                resultTDMW = ''
            else:
                resultTDMW = "{} ({})".format(pOnsTD_MW_SG, pOnsTD_MW_TVDSS)
            shallowerFlagText = 'N'
        
        resultDic['PS_TD_TVDSS_M'] = resultTDTVDSS
        resultDic['PS_TD_MARKER'] = resultTDMarker
        resultDic['PS_TD_MW_SG'] = resultTDMW
        resultDic['PS_SHALLOWER_FLAG'] = shallowerFlagText
        return resultDic


    # def getSonicFlagDicOld(self, wellName):
    #     wfrFolder = self.getWellRootFolder()
    #     wellFolder = os.path.join(wfrFolder, wellName)
    #     logFileName = wellName + "_log.csv"
    #     logFile = os.path.join(wellFolder, logFileName)
    #     sonicColName = 'DT'
    #     sonicFlagText = ''
    #     if os.path.exists(logFile):
    #         logDF = pd.read_csv(logFile, skiprows=[1])
    #         logDF = logDF.replace(-999.25, np.nan)
    #         if sonicColName in logDF.columns:
    #             sonicDF = logDF[[sonicColName]].dropna()
    #             if sonicDF.empty:
    #                 sonicFlagText = 'N'
    #             else:
    #                 sonicFlagText = 'Y'
    #         else:
    #             sonicFlagText = 'N'
    #     else:
    #         sonicFlagText = '?'
    #     sonicFlagDic = {
    #         'SONIC_FLAG': sonicFlagText
    #     }
    #     return sonicFlagDic
    
    def getSonicFlagDic(self, wellName):
        logFolder = self.getLogFolder()
        logFilePath = os.path.join(logFolder,  wellName+'.csv')
        sonicColName = 'DT'
        sonicFlagText = ''
        if os.path.exists(logFilePath):
            logDF = pd.read_csv(logFilePath, skiprows=[1])
            logDF = logDF.replace(-999.25, np.nan)
            if sonicColName in logDF.columns:
                sonicDF = logDF[[sonicColName]].dropna()
                if sonicDF.empty:
                    sonicFlagText = 'N'
                else:
                    sonicFlagText = 'Y'
            else:
                sonicFlagText = 'N'
        else:
            sonicFlagText = '?'
        sonicFlagDic = {
            'SONIC_FLAG': sonicFlagText
        }
        return sonicFlagDic
    
    # def getPostMortemFlagOld(self, wellName):
    #     wfrFolder = self.getWellRootFolder()
    #     wellFolder = os.path.join(wfrFolder, wellName)
    #     postMortemFolder = os.path.join(wellFolder, self.getPPFGFolder())
    #     ppPostMortemFileName = wellName + '_pp.csv'
    #     ppPostMortemFile = os.path.join(postMortemFolder, ppPostMortemFileName)
    #     if os.path.exists(ppPostMortemFile):
    #         ppDF = pd.read_csv(ppPostMortemFile).dropna()
    #         if ppDF.empty:
    #             postMortemFlag = 'N'
    #         else:
    #             postMortemFlag = 'Y'
    #     else:
    #         postMortemFlag = 'N'
    #     postMortemFlagDic = {
    #         'POST_MORTEM_FLAG': postMortemFlag
    #     }
    #     return postMortemFlagDic

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

    def getPostMortemFlag(self, wellName):
        pmAsciiWellDF = self.getPostMortemAsciiWellDF(wellName)
        # pmAsciiWellPPDF = pmAsciiWellDF[['PP_TVDSS_M', 'PP_SG']]

        if {'PP_TVDSS_M', 'PP_SG'}.issubset(pmAsciiWellDF.columns):
            pmAsciiWellPPDF = pmAsciiWellDF[['PP_TVDSS_M', 'PP_SG']]
            if pmAsciiWellPPDF.empty:
                postMortemFlag = 'N'
            else:
                postMortemFlag = 'Y'

        else:
            postMortemFlag = 'N'
        postMortemFlagDic = {
            'POST_MORTEM_FLAG': postMortemFlag
        }
        return postMortemFlagDic

    def getSummByXYDF(self, wellName):
        wGenDic = self.getWGenDic(wellName)
        wPosDic = self.getSurrWellPosDic()[wellName]
        TDMarkerDic = self.getTDMarkerDic(wellName)
        TDMWDic = self.getTDMWDic(wellName)
        sonicFlagDic = self.getSonicFlagDic(wellName)
        eventDic = self.getWEventSummDic(wellName)
        postMortemFlagDic = self.getPostMortemFlag(wellName)

        summWDic = pd.DataFrame ({
            'SHORT_NAME': [wellName],
            'TD_SECTION_INCH': [wGenDic['TD_SECTION_INCH']],
            'TD_X_M': [wGenDic['TD_X_M']],
            'TD_Y_M': [wGenDic['TD_Y_M']],
            'TD_TVDSS_M': [wGenDic['TD_TVDSS_M']],
            'SPUD_DATE': [wGenDic['SPUD_DATE']],
            'TD_MARKER': [TDMarkerDic['TD_MARKER']],
            'TD_MW_SG': [TDMWDic['TD_MW_SG']],
            'WELL_X_M': [wPosDic['x']],
            'WELL_Y_M': [wPosDic['y']],
            'DIST_KM': [wPosDic['dist']],
            'SONIC_FLAG': [sonicFlagDic['SONIC_FLAG']],
            'EVENT_FLAG': [eventDic['EVENT_FLAG']],
            'EVENT_SHORT_DESC': [eventDic['EVENT_SHORT_DESC']],
            'POST_MORTEM_FLAG': [postMortemFlagDic['POST_MORTEM_FLAG']]
        })
        return summWDic

    def getSummByWellDF(self, wellName):
        wTDSectionDic = self.getWTDSectionDic(wellName)
        wGenDic = self.getWGenDic(wellName)
        wPosDic = self.getSurrWellPosDic()[wellName]
        TDMarkerDic = self.getTDMarkerDic(wellName)
        TDMWDic = self.getTDMWDic(wellName)
        pOnsDic = self.getWpONsDic(wellName)
        sonicFlagDic = self.getSonicFlagDic(wellName)
        eventDic = self.getWEventSummDic(wellName)
        postMortemFlagDic = self.getPostMortemFlag(wellName)
        summWDic = pd.DataFrame ({
            'SHORT_NAME': [wellName],
            'TD_SECTION_INCH': [wTDSectionDic['TD_SECTION_INCH']],
            'TD_X_M': [wGenDic['TD_X_M']],
            'TD_Y_M': [wGenDic['TD_Y_M']],
            'TD_TVDSS_M': [wGenDic['TD_TVDSS_M']],
            'SPUD_DATE': [wGenDic['SPUD_DATE']],
            'TD_MARKER': [TDMarkerDic['TD_MARKER']],
            'TD_MW_SG': [TDMWDic['TD_MW_SG']],
            'WELL_X_M': [wPosDic['x']],
            'WELL_Y_M': [wPosDic['y']],
            'DIST_KM': [wPosDic['dist']],
            'PS_TD_MARKER': [pOnsDic['PS_TD_MARKER']],
            'PS_TD_TVDSS_M': [pOnsDic['PS_TD_TVDSS_M']],
            'PS_TD_MW_SG': [pOnsDic['PS_TD_MW_SG']],
            'PS_SHALLOWER_FLAG': [pOnsDic['PS_SHALLOWER_FLAG']],
            'SONIC_FLAG': [sonicFlagDic['SONIC_FLAG']],
            'EVENT_FLAG': [eventDic['EVENT_FLAG']],
            'EVENT_SHORT_DESC': [eventDic['EVENT_SHORT_DESC']],
            'POST_MORTEM_FLAG': [postMortemFlagDic['POST_MORTEM_FLAG']]
        })
        return summWDic

    def getSummWellsDF(self, mode, wellNames):

        if len(wellNames)<1:
            return []

        frames = []
        if mode == "point":
            for wellName in wellNames:
                summWell = self.getSummByXYDF(wellName)
                frames.append(summWell)
        if mode == "well":
            for wellName in wellNames:
                summWell = self.getSummByWellDF(wellName)
                frames.append(summWell)
        resultDF = pd.concat(frames, ignore_index=True)
        resultDF = resultDF.fillna("")
        return resultDF

    def getSummWellsRecords(self, mode, wellNames):
        summWellsDF = self.getSummWellsDF(mode, wellNames)
        summWellRecords = summWellsDF.to_dict(orient="records")
        return summWellRecords