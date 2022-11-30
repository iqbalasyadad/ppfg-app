from ppfgmodules.deviation_survey import DeviationSurvey

class WellTrajectory(DeviationSurvey):

    def getAllWellTrajectoryRecords(self):
        wellNames = self.getAllWellNames()
        wellsTrajectoryDic = []
        for wellName in wellNames:
            wellDeviationSurveyDF = self.getWellDeviationSurveyDF(wellName)
            wellTrajectoryDF = wellDeviationSurveyDF[['X', 'Y']].dropna()
            wellTrajectoryDic = {
                'SHORT_NAME': wellName,
                'X': wellTrajectoryDF['X'].values.tolist(),
                'Y': wellTrajectoryDF['Y'].values.tolist()
            }
            wellsTrajectoryDic.append(wellTrajectoryDic)
        
        return wellsTrajectoryDic