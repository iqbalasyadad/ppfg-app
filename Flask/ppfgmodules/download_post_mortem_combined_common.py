from ppfgmodules.well_post_mortem import PostMortemProfile
import pandas as pd
from zipfile import ZipFile
import io

class DownloadPostMortemCombinedCommon(PostMortemProfile):

    def getDF_PPPPost(self, wellName):
        PP_DF = self.getWellPP_DF(wellName)
        FG_DF = self.getWellFG_DF(wellName)
        OBG_DF = self.getWellOBG_DF(wellName)
        MW_DF = self.getWellMW_DF(wellName)
        ECD_DF = self.getWellECD_DF(wellName)
        LOT_DF = self.getWellLOT_DF(wellName)
        PT_DF = self.getWellPT_DF(wellName)
        casing_DF = self.getWellCasing_DF(wellName)
        marker_DF = self.getWellMarker_DF(wellName)
        PPFG_marker_DF = self.getWellPPFGMarker_DF(wellName)

        frames = [PP_DF, FG_DF, OBG_DF, MW_DF, ECD_DF, LOT_DF, PT_DF, casing_DF, marker_DF, PPFG_marker_DF]
        resultDF = pd.concat(frames, axis=1, join='outer')
        return resultDF

    def getExcel_wellsCombinedCommon(self, wellNames):
        output = io.BytesIO()
        if len(wellNames)<1:
            return output
        with pd.ExcelWriter(output, engine="openpyxl") as writer:              
            for wellName in wellNames:
                wellCombinedDF = self.getDF_PPPPost(wellName)
                wellCombinedDF.to_excel(writer, sheet_name=wellName, index=False)
        return output

    def getZip_wellsCombinedCommon(self, wellNames):
        stream = io.BytesIO()
        if len(wellNames)<1:
            return stream
        with ZipFile(stream, 'w') as zf:
            for wellName in wellNames:
                wellCombinedDF = self.getDF_PPPPost(wellName)
                csvFile = wellCombinedDF.to_csv(index=False)
                zf.writestr(wellName+'_post_mortem_ASCII.csv', csvFile)
        return stream