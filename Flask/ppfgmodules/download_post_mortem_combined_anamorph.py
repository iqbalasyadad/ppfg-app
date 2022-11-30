from ppfgmodules.post_mortem_anamorph import PostMortemProfileCombineAnamorph
import pandas as pd
from zipfile import ZipFile
import io

class DownloadPostMortemCombinedAnamorph(PostMortemProfileCombineAnamorph):
        # PP_Dic = self.getWellPPAnamorphDF(sWellName, pWellName).to_dict(orient='list')
        # PT_Dic = self.getWellPTAnamorphDF(sWellName, pWellName).to_dict(orient='list')
        # event_Dic = self.getWellEventAnamorphDF(sWellName, pWellName).to_dict(orient='list')

    def getAnamorphDF(self, sWellName):
        pWellName = self.getPWellName()
        PP_DF = self.getWellPPAnamorphDF(sWellName, pWellName)
        PT_DF = self.getWellPTAnamorphDF(sWellName, pWellName)
        event_DF = self.getWellEventAnamorphDF(sWellName, pWellName)
        frames = [PP_DF, PT_DF, event_DF]
        resultDF = pd.concat(frames, axis=1, join='outer')
        return resultDF

    def getExcel_wellsCombinedAnm(self, sWellNames):
        output = io.BytesIO()
        if len(sWellNames)<1:
            return output
        output = io.BytesIO()
        with pd.ExcelWriter(output) as writer:              
            for wellName in sWellNames:
                wellCombinedAnmDF = self.getAnamorphDF(wellName)
                wellCombinedAnmDF.to_excel(writer, sheet_name=wellName, index=False)
        print('ok')
        return output

    def getZip_wellsCombinedAnm(self, wellNames):
        stream = io.BytesIO()
        if len(wellNames)<1:
            return stream
        with ZipFile(stream, 'w') as zf:
            for wellName in wellNames:
                wellCombinedDF = self.getAnamorphDF(wellName)
                csvFile = wellCombinedDF.to_csv(index=False)
                zf.writestr(wellName+'_post_mortem_anamorph_to_{}.csv'.format(self.getPWellName()), csvFile)
        return stream