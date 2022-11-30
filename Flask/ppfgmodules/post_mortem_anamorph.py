import os
import pandas as pd
import numpy as np
from ppfgmodules.well_post_mortem import PostMortemProfile

class PostMortemProfileCombineAnamorph(PostMortemProfile):

    def setPWellName(self, pWellName):
        self._pWellName = pWellName
    
    def getPWellName(self):
        return self._pWellName

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

    def getWellPPAnamorphDF(self, sWellName, pWellName):
        sPPDF = self.getWellPP_DF(sWellName)
        sMarkerDF = self.getWellMarker_DF(sWellName)
        pMarkerDF = self.getWellMarker_DF(pWellName)

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

    def getWellPTAnamorphDF(self, sWellName, pWellName):
        sPTDF = self.getWellPT_DF(sWellName)
        sMarkerDF = self.getWellMarker_DF(sWellName)
        pMarkerDF = self.getWellMarker_DF(pWellName)

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

    def getWellEventAnamorphDF(self, sWellName, pWellName):
        sEventDF = self.getWellEvent_DF(sWellName)
        sMarkerDF = self.getWellMarker_DF(sWellName)
        pMarkerDF = self.getWellMarker_DF(pWellName)

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
            sEventDF_Anm['EVENT_PLOT_TVDSS_M'] = tDepthsAnm
        else:

            sEventDF_Anm = pd.DataFrame({
                'EVENT_PLOT_SG': [],
                'EVENT_PLOT_TVDSS_M': [],
                'EVENT_DETAIL': [],
                'EVENT_DESCRIPTION': []
            })
        return sEventDF_Anm

    def getWellAnamorphDic(self, sWellName, pWellName):
        PP_Dic = self.getWellPPAnamorphDF(sWellName, pWellName).to_dict(orient='list')
        PT_Dic = self.getWellPTAnamorphDF(sWellName, pWellName).to_dict(orient='list')
        event_Dic = self.getWellEventAnamorphDF(sWellName, pWellName).to_dict(orient='list')

        wellName_Dic = {"SHORT_NAME": sWellName}

        wellPPP_Dic = {}
        for d in [wellName_Dic, PP_Dic, PT_Dic, event_Dic]:
            wellPPP_Dic.update(d)
        return wellPPP_Dic

    def getWellsAnamorphDic(self, sWellNames):
        pWellName = self.getPWellName()
        wellsPPP_Dic = {}
        for i, sWellName in enumerate(sWellNames):
            wellsPPP_Dic[i] = self.getWellAnamorphDic(sWellName, pWellName)
        pMarkerDF = self.getWellMarker_DF(self.getPWellName())
        pMarkerDF['MARKER_PLOT_X'] = 2.5
        pMarkerDic = pMarkerDF.to_dict(orient="list")
        wellsAnm_Dic = {
            "pppAnm": wellsPPP_Dic,
            "pMarker": pMarkerDic
        }
        return wellsAnm_Dic