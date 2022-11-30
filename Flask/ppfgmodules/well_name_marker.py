import oracledb
import pandas as pd
import numpy as np

class WellMarkerDB:
    
    def __init__(self):
        self.db_config = {
            'user': "USER_PPFG",
            'pass': "PPFG1234",
            'dsn': "ORCLPDB"
        }
    
    def getDBMarker(self):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        cur = con.cursor()
        # sql_query = """SELECT SHORT_NAME, MARKER_NAME, X, Y, TVDSS FROM MARKERS"""
        sql_query = """SELECT SHORT_NAME, MARKER_NAME, X, Y, TVDSS FROM gg_marker"""

        markerDF = pd.read_sql(sql_query, con)
        markerDF = markerDF[markerDF['X'].notna()]
        markerDF = markerDF.rename(columns={'TVDSS': 'MARKER_TVDSS_M'})
        self.setMarkerDF(markerDF)
        cur.close()
        con.close()

    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self):
        return self._markerDF

    def getAllMarkerDict(self):
        markersDF = self.getMarkerDF()
        markerNamesList = markersDF['MARKER_NAME'].unique().tolist()
        markerNamesDF = pd.DataFrame({"MARKER_NAME": markerNamesList})
        return markerNamesDF.to_dict(orient='records')
    
    def getWellsXY(self, markerName):
        markersDF = self.getMarkerDF()
        markerDF = markersDF[markersDF['MARKER_NAME']==markerName]
        wellNames = markerDF['SHORT_NAME'].values.tolist()
        wellXs = markerDF['X'].values.tolist()
        wellYs = markerDF['Y'].values.tolist()
        return {
            "SHORT_NAME": wellNames,
            "X": wellXs,
            "Y": wellYs
        }
    
    def getDBFieldName(self):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        # sql_query = """SELECT SHORT_NAME, MARKER_NAME, X, Y, TVDSS FROM MARKERS"""
        sql_query = """SELECT DISTINCT FIELD_NAME FROM gg_marker"""
        fieldNameDF = pd.read_sql(sql_query, con)
        self.setFieldNameDF(fieldNameDF)
        con.close()
    
    def setFieldNameDF(self, fieldNameDF):
        self._fieldName = fieldNameDF
    
    def getFieldNameDF(self):
        return self._fieldName
    
    def getAllFieldNameDict(self):
        fieldNameDF = self.getFieldNameDF()
        return fieldNameDF.to_dict(orient='records')
    
    def getDBFieldMarker(self, fieldName):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        # sql_query = """SELECT SHORT_NAME, MARKER_NAME, X, Y, TVDSS FROM MARKERS"""
        sql_query = """SELECT SHORT_NAME, MARKER_NAME, X, Y, TVDSS FROM gg_marker WHERE FIELD_NAME='{}'""".format(fieldName)

        markerDF = pd.read_sql(sql_query, con)
        markerDF = markerDF[markerDF['X'].notna()]
        markerDF = markerDF.rename(columns={'TVDSS': 'MARKER_TVDSS_M'})
        self.setMarkerDF(markerDF)
        con.close()

class WellGenDB:
    
    def __init__(self):
        self.db_config = {
            'user': "USER_PPFG",
            'pass': "PPFG1234",
            'dsn': "ORCLPDB"
        }
    
    def getDBWellGen(self):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        cur = con.cursor()
        sql_query = """SELECT SHORT_NAME, TVDSS_DRILLER, DRILLER_BOTTOM_X, DRILLER_BOTTOM_Y, SPUD_DATE FROM WELL_INFO"""
        df = pd.read_sql(sql_query, con)
        self.setGenDF(df)
        cur.close()
        con.close()

    def getDBFieldGen(self, fieldName):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        sql_query = """SELECT SHORT_NAME, TVDSS_DRILLER, DRILLER_BOTTOM_X, DRILLER_BOTTOM_Y, to_char(SPUD_DATE,'DD/MM/YYYY') AS SPUD_DATE FROM gg_well_header WHERE FIELD_NAME='{}'""".format(fieldName)
        df = pd.read_sql(sql_query, con)
        self.setGenDF(df)
        con.close()

    def setGenDF(self, genDF):
        self._genDF = genDF
    
    def getGenDF(self):
        return self._genDF
    

class WellNameDB:
    def __init__(self):
        self.db_config = {
            'user': "USER_PPFG",
            'pass': "PPFG1234",
            'dsn': "ORCLPDB"
        }
    
    def getDBFieldGen(self, fieldName):
        oracledb.init_oracle_client()
        con = oracledb.connect(user=self.db_config['user'], password=self.db_config['pass'], dsn=self.db_config['dsn'])
        sql_query = """SELECT SHORT_NAME, TVDSS_DRILLER, DRILLER_BOTTOM_X, DRILLER_BOTTOM_Y, SPUD_DATE FROM gg_well_header WHERE FIELD_NAME='{}'""".format(fieldName)
        df = pd.read_sql(sql_query, con)
        self.setGenDF(df)
        con.close()

    def setGenDF(self, genDF):
        self._genDF = genDF
    
    def getGenDF(self):
        return self._genDF

    def setMarkerDF(self, markerDF):
        self._markerDF = markerDF
    
    def getMarkerDF(self):
        return self._markerDF

    def getAllWellNameDict(self):
        genDF = self.getGenDF()
        markerDF = self.getMarkerDF()
        wellNamesGenList = np.sort(genDF['SHORT_NAME'].tolist())
        wellNamesMarkerList = np.sort(markerDF['SHORT_NAME'].tolist())
        wellNamesList = np.intersect1d(wellNamesGenList, wellNamesMarkerList)
        wellNamesDF = pd.DataFrame({"SHORT_NAME": wellNamesList})
        return wellNamesDF.to_dict(orient='records')