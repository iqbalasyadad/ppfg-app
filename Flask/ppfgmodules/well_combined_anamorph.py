import os
import pandas as pd
import numpy as np

class CombineAnamorphPP:

    def __init__(self):
        self.fmtNames = {
            'PP': 'PP',
            'FG': 'FG',
            'OBG': 'OBG',
            'MW': 'MW',
            'ECD': 'ECD',
            'casing': 'casing',
            'LOT': 'LOT',
            'PT': 'PT'
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
        }
    
    def setPWellName(self, pWellName):
        self._pWellName = pWellName
    
    def getPWellName(self):
        return self._pWellName

    def setWellRootFolder(self, wellRootFolder):
        self._wellRootFolder = wellRootFolder

    def getWellRootFolder(self):
        return self._wellRootFolder

    def setPPPFolderName(self, pppFolder):
        self._pppFolderName = pppFolder

    def getPPPFolderName(self):
        return self._pppFolderName
    
    def readMarkerFile(self, markerFile):
        usedCols = ['SHORT_NAME', 'MARKER_NAME', 'MARKER_TVDSS_M']
        df = pd.read_csv(markerFile, usecols=usedCols)
        self.setMarkerDF(df)
    
    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self, wellName=None):
        if wellName:
            wMarkerDF = self._markerDF[self._markerDF['SHORT_NAME']==wellName]
            wMarkerDF = wMarkerDF.sort_values(by='MARKER_TVDSS_M')
            return wMarkerDF[['MARKER_NAME', 'MARKER_TVDSS_M']]
        else:
            return self._markerDF
    
    def readEventFile(self, eventFile):
        usedCols = ['SHORT_NAME', 'EVENT_PLOT_SG', 'EVENT_PLOT_TVDSS_M', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
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

    def getValPos(self, val, arr):
        if val<arr[0]:
            return -1
        elif val>arr[-1]:
            return -2
        else:
            nArr = len(arr)
            for i in range(nArr-1):
                if arr[i]<=val and arr[i+1]>=val:
                    return i

    def anamorphDepths(self, tDepths, sDepths, pDepths):
        if len(tDepths)<1 or len(sDepths)<1 or len(pDepths)<0:
            return [], []
        n_pDepths = len(pDepths)
        compArr = np.zeros(n_pDepths-1)
        for i in range(n_pDepths-1):
            sDelta = sDepths[i+1] - sDepths[i]
            pDelta = pDepths[i+1] - pDepths[i]
            compArr[i] = pDelta/sDelta

        tDepthsAnm = np.zeros(len(tDepths))
        tDepthsMask = np.zeros(len(tDepths), dtype=int)
        for i_tDepth, tDepth in enumerate(tDepths):
            valPos = self.getValPos(tDepth, sDepths)
            if valPos ==-1:
                valAnm = (tDepth - sDepths[0]) * 1 + pDepths[0]
                tDepthsMask[i_tDepth] = 0
            elif valPos == -2:
                valAnm = (tDepth - sDepths[-1]) * 1 + pDepths[-1]
                tDepthsMask[i_tDepth] = 0     
            else:
                valAnm = (tDepth - sDepths[valPos]) * compArr[valPos] + pDepths[valPos]
                tDepthsMask[i_tDepth] = 1
            tDepthsAnm[i_tDepth] = valAnm
        return tDepthsAnm, tDepthsMask

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

    def getDF_PT(self, wellName):
        wellFolder = os.path.join(self.getWellRootFolder(), wellName)
        ppfgFolder = os.path.join(wellFolder, self.getPPPFolderName())
        PT_File = os.path.join(ppfgFolder, "{}_{}.csv".format(wellName, self.fmtNames['PT']))
        try:
            df = pd.read_csv(PT_File)
        except Exception as err:
            print(err)
            emptyDF = pd.DataFrame(columns=self.fmtEmptyHeader['PT'])
            return emptyDF
        else:
            return df

    def getDF_Event(self, wellName):
        usedCols = ['EVENT_PLOT_SG', 'EVENT_PLOT_TVDSS_M', 'EVENT_DETAIL', 'EVENT_DESCRIPTION']
        wEventDF = self.getEventDF(wellName)[usedCols]
        return wEventDF

    def getDF_PPAnamorph(self, sWellName, pWellName):
        sPPDF = self.getDF_PP(sWellName)
        sMarkerDF = self.getMarkerDF(sWellName)
        pMarkerDF = self.getMarkerDF(pWellName)

        sameMarkerArr = np.intersect1d(sMarkerDF['MARKER_NAME'].values, pMarkerDF['MARKER_NAME'].values)
        sMarkerDF_Same = sMarkerDF.loc[sMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]
        pMarkerDF_Same = pMarkerDF.loc[pMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]

        sPPVals_PP = sPPDF['PP_SG'].values
        sPPVals_Depth = sPPDF['PP_TVDSS_M'].values
        sMarkerDF_Depth = sMarkerDF_Same['MARKER_TVDSS_M'].values
        pMarkerDF_Depth = pMarkerDF_Same['MARKER_TVDSS_M'].values

        tDepthsAnm, tDepthsMask = self.anamorphDepths(sPPVals_Depth, sMarkerDF_Depth, pMarkerDF_Depth)

        # tDepthsAnmMaskTrue = tDepthsAnm[tDepthsMask.astype(bool)]
        # tPPsAnmMaskTrue = sPPVals_PP[tDepthsMask.astype(bool)]

        if len(tDepthsAnm)==len(sPPVals_Depth):
            sPPDF_Anm = pd.DataFrame({'PP_SG': sPPVals_PP, 'PP_TVDSS_M': tDepthsAnm})
        else:
            sPPDF_Anm = pd.DataFrame({'PP_SG': [], 'PP_TVDSS_M': []})
        return sPPDF_Anm

    def getDF_PTAnamorph(self, sWellName, pWellName):
        sPTDF = self.getDF_PT(sWellName)
        sMarkerDF = self.getMarkerDF(sWellName)
        pMarkerDF = self.getMarkerDF(pWellName)

        sameMarkerArr = np.intersect1d(sMarkerDF['MARKER_NAME'].values, pMarkerDF['MARKER_NAME'].values)
        sMarkerDF_Same = sMarkerDF.loc[sMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]
        pMarkerDF_Same = pMarkerDF.loc[pMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]

        sPTVals_SG = sPTDF['PT_SG'].values
        sPTVals_TVDSS = sPTDF['PT_TVDSS_M'].values
        sMarkerDF_Depth = sMarkerDF_Same['MARKER_TVDSS_M'].values
        pMarkerDF_Depth = pMarkerDF_Same['MARKER_TVDSS_M'].values

        tDepthsAnm, tDepthsMask = self.anamorphDepths(sPTVals_TVDSS, sMarkerDF_Depth, pMarkerDF_Depth)

        if len(tDepthsAnm)==len(sPTVals_TVDSS):
            sPTDF_Anm = pd.DataFrame({'PT_SG': sPTVals_SG, 'PT_TVDSS_M': tDepthsAnm})
        else:
            sPTDF_Anm = pd.DataFrame({'PT_SG': [], 'PT_TVDSS_M': []})
        return sPTDF_Anm

    def getDF_EventAnamorph(self, sWellName, pWellName):
        sEventDF = self.getDF_Event(sWellName)
        sMarkerDF = self.getMarkerDF(sWellName)
        pMarkerDF = self.getMarkerDF(pWellName)

        sameMarkerArr = np.intersect1d(sMarkerDF['MARKER_NAME'].values, pMarkerDF['MARKER_NAME'].values)
        sMarkerDF_Same = sMarkerDF.loc[sMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]
        pMarkerDF_Same = pMarkerDF.loc[pMarkerDF['MARKER_NAME'].isin(sameMarkerArr)]

        sEventVals_X = sEventDF['EVENT_PLOT_SG'].values
        sEventVals_Y = sEventDF['EVENT_PLOT_TVDSS_M'].values
        sMarkerDF_Depth = sMarkerDF_Same['MARKER_TVDSS_M'].values
        pMarkerDF_Depth = pMarkerDF_Same['MARKER_TVDSS_M'].values

        tDepthsAnm, tDepthsMask = self.anamorphDepths(sEventVals_Y, sMarkerDF_Depth, pMarkerDF_Depth)

        if len(tDepthsAnm)==len(sEventVals_Y):
            sEventDF_Anm = sEventDF.copy()
            sEventDF_Anm['EVENT_PLOT_Y'] = tDepthsAnm
        else:

            sEventDF_Anm = pd.DataFrame({
                'EVENT_PLOT_SG': [],
                'EVENT_PLOT_TVDSS_M': [],
                'EVENT_DETAIL': [],
                'EVENT_DESCRIPTION': []
            })
        return sEventDF_Anm
    
    def getDic_wellPPP(self, sWellName, pWellName):
        PP_Dic = self.getDF_PPAnamorph(sWellName, pWellName).to_dict(orient='list')
        PT_Dic = self.getDF_PTAnamorph(sWellName, pWellName).to_dict(orient='list')
        event_Dic = self.getDF_EventAnamorph(sWellName, pWellName).to_dict(orient='list')

        wellName_Dic = {"SHORT_NAME": sWellName}

        wellPPP_Dic = {}
        for d in [wellName_Dic, PP_Dic, PT_Dic, event_Dic]:
            wellPPP_Dic.update(d)
        return wellPPP_Dic

    def getDic_wellsPPP(self, sWellNames):
        pWellName = self.getPWellName()
        wellsPPP_Dic = {}
        for i, sWellName in enumerate(sWellNames):
            wellsPPP_Dic[i] = self.getDic_wellPPP(sWellName, pWellName)
        pMarkerDF = self.getMarkerDF(self.getPWellName())
        pMarkerDF['MARKER_PLOT_X'] = 2.5
        pMarkerDic = pMarkerDF.to_dict(orient="list")
        wellsAnm_Dic = {
            "pppAnm": wellsPPP_Dic,
            "pMarker": pMarkerDic
        }
        return wellsAnm_Dic