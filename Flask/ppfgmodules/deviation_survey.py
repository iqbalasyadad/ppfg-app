import oracledb
import pandas as pd

class DeviationSurvey:

    def __init__(self):
        self.db_config = {
            'user': "USER_PPFG",
            'pass': "PPFG1234",
            'dsn': "ORCLPDB"
        }
    
    # def getDBDeviation(self):
    #     oracledb.init_oracle_client()
    #     con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
    #     sql_query = """SELECT SHORT_NAME, X, Y, TVDSS FROM GG_DEVIATION_SURVEY WHERE FIELD_NAME='SISI-NUBI'"""
    #     df = pd.read_sql(sql_query, con)
    #     con.close()
    #     self.setDeviationSurveyDF(df)

    def getDBFieldDeviation(self, fieldName):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        sql_query = """SELECT SHORT_NAME, X, Y, TVDSS FROM GG_DEVIATION_SURVEY WHERE FIELD_NAME='{}'""".format(fieldName)
        df = pd.read_sql(sql_query, con)
        con.close()
        self.setDeviationSurveyDF(df)

    def setDeviationSurveyDF(self, devSurDF):
        self._devSurDF = devSurDF
    
    def getDeviationSurveyDF(self):
        return self._devSurDF

    def getAllWellNames(self):
        devSurDF = self.getDeviationSurveyDF()
        wellNames = devSurDF['SHORT_NAME'].unique()
        return wellNames

    def getWellDeviationSurveyDF(self, wellName):
        devSurDF = self.getDeviationSurveyDF()
        wellDevSurDF = devSurDF[devSurDF['SHORT_NAME']==wellName]
        wellDevSurDF = wellDevSurDF.sort_values(by="TVDSS")
        return wellDevSurDF