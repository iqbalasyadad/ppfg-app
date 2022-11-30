import io
import os
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory

from ppfgmodules.well_name_marker import WellMarkerDB, WellGenDB, WellNameDB

from ppfgmodules.summ_well import SummWellRecord

from ppfgmodules.well_trajectory import WellTrajectory
from ppfgmodules.well_post_mortem import PostMortemProfile

from ppfgmodules.post_mortem_anamorph import PostMortemProfileCombineAnamorph

from ppfgmodules.well_get_event import WellEvent
from ppfgmodules.download_well_ppp_post import PPPDownloadFile

from ppfgmodules.download_post_mortem_combined_common import DownloadPostMortemCombinedCommon
from ppfgmodules.download_post_mortem_combined_anamorph import DownloadPostMortemCombinedAnamorph

from ppfgmodules.well_get_data_list import DataFileList
from ppfgmodules.download_data_files import DownloadFiles

from flask_cors import CORS
from waitress import serve


# folder path goes here
deviationSurveyFile = "C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/deviation_survey.csv"
logFolder = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/log'
markerFile = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/well_marker.csv'
wellAddInfoFile = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/well_add_info.csv'
wellRootFolder = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/well_files'
wpFile = "C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/well_parameter.csv"
eventFile = "C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/well_event.csv"
tempFolder = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/get_database/temp_folder'
postMortemFolderName = 'post_mortem_profile'
postMortemAsciiFolder = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/post_mortem_ascii'
postMortemFolderOri = 'C:/Users/asyad/Documents/Magang/phm/testing/DATA_MANAGEMENT/Database/SISI/POST_MORTEM'
# end folder path

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

@app.route('/')
def hello():
    return 'main page'


@app.route('/getfieldname', methods = ['POST'])
def getFieldName():
    wm = WellMarkerDB()
    wm.getDBFieldName()
    fieldNameRecords = wm.getAllFieldNameDict()
    return jsonify(fieldNameRecords)

@app.route('/gettrajectory', methods = ['POST'])
def getTrajectory():
    inputJson = request.json
    fieldName = inputJson['map_field']

    wTrace = WellTrajectory()
    wTrace.getDBFieldDeviation(fieldName)
    wTrajectoryRecords = wTrace.getAllWellTrajectoryRecords()
    return jsonify(wTrajectoryRecords)

@app.route('/getfieldmarkername', methods = ['POST'])
def getFieldMarkerName():
    inputJson = request.json
    fieldName = inputJson['map_field']
    wm = WellMarkerDB()
    wm.getDBFieldMarker(fieldName)
    wellMarkerDic = wm.getAllMarkerDict()
    return jsonify(wellMarkerDic)

@app.route('/getfieldwellname', methods = ['POST'])
def getallwellname():
    inputJson = request.json
    fieldName = inputJson['map_field']

    wm = WellMarkerDB()
    wm.getDBFieldMarker(fieldName)
    markerDF = wm.getMarkerDF()

    wn = WellNameDB()
    wn.setMarkerDF(markerDF)
    wn.getDBFieldGen(fieldName)
    wellNameDic = wn.getAllWellNameDict()
    return jsonify(wellNameDic)

@app.route('/getwellmarkerpos', methods = ['POST'])
def getwellmarkerpos():
    inputJson = request.json
    fieldName = inputJson['map_field']
    mapMarker = inputJson['map_marker']
    print(fieldName, mapMarker)
    wm = WellMarkerDB()
    wm.getDBFieldMarker(fieldName)
    wellMarkerPosDic = wm.getWellsXY(mapMarker)
    return jsonify(wellMarkerPosDic)


@app.route('/getwellsumm', methods = ['POST'])
def getsumm():
    inputJson = request.json
    fieldName = inputJson["fieldName"]
    mapMarker = inputJson["mapMarker"]
    mode  = inputJson["mode"]
    sRadius = int(inputJson["sRadius"])

    wm = WellMarkerDB()
    wm.getDBFieldMarker(fieldName)
    markerDF = wm.getMarkerDF()

    wgen = WellGenDB()
    wgen.getDBFieldGen(fieldName)
    genDF = wgen.getGenDF()
    
    print(genDF)


    summWell = SummWellRecord()
    summWell.readWellAddInfo(wellAddInfoFile)
    # summWell.readMarkerFile(markerFile)
    summWell.setMarkerDF(markerDF)
    summWell.setGenDF(genDF)
    # summWell.readGenFile(genFile)
    summWell.readEventFile(eventFile)
    summWell.setPostMortemAsciiFolder(postMortemAsciiFolder)
    summWell.setLogFolder(logFolder)
    summWell.setMapMarker(mapMarker)
    # summWell.setWellRootFolder(wellRootFolder)
    # summWell.setPPFGFolder(postMortemFolderName)

    if mode=="well":
        pWell = inputJson["pWell"]
        pTDX, pTDY, pTDZ = summWell.getTDXYZ(pWell)
        pMarkerName, pMarkerDepth, pMarkerPlus = summWell.getDepthMarker(pWell, pTDZ)
        propWell = {
            "well_name": pWell,
            "TD": {
                "x": pTDX,
                "y": pTDY,
                "z": pTDZ,
                "marker_name": pMarkerName,
                "marker_depth": pMarkerDepth,
                "marker_plus": pMarkerPlus
            }
        }
        summWell.setPropWell(propWell)

    elif mode=="point":
        pTDX = inputJson["pTDX"]
        pTDY = inputJson["pTDY"]
        propWell = {}
    
    summWell.calcSurrWellPos(pTDX, pTDY, sRadius)
    surrWellNames = summWell.getSurrWellNames()
    if len(surrWellNames)>0:
        summWellRecords = summWell.getSummWellsRecords(mode=mode, wellNames=surrWellNames)
    else:
        summWellRecords = []
    summWell = {
        "surrSettings": {
            "pTDX": pTDX,
            "pTDY": pTDY,
            "sRadius": sRadius
        }, 
        "surrWellNames": surrWellNames,
        "summWellRecords": summWellRecords,
        "propWell": propWell
    }
    return jsonify(summWell)

@app.route('/getwellppp', methods = ['POST'])
def getwellppp():
    # inputJson = request.json
    # wellNames = inputJson['wellNames']
    # ppp = PPPPost()
    # ppp.setWellRootFolder(wellRootFolder)
    # ppp.setLogFolder(logFolder)
    # ppp.setPPPFolderName(postMortemFolderName)
    # ppp.readMarkerFile(markerFile)
    # ppp.readEventFile(eventFile)
    # wellsPPP_Dic = ppp.getDic_wellsPPP(wellNames)
    # return jsonify(wellsPPP_Dic)
    
    inputJson = request.json
    wellNames = inputJson['wellNames']

    wm = WellMarkerDB()
    wm.getDBMarker()
    markerDF = wm.getMarkerDF()

    postMortemPP = PostMortemProfile()
    postMortemPP.setLogFolder(logFolder)
    # postMortemPP.readMarkerFile(markerFile)
    postMortemPP.setMarkerDF(markerDF)

    postMortemPP.readEventFile(eventFile)
    postMortemPP.setPostMortemAsciiFolder(postMortemAsciiFolder)
    postMortemPropsDic = postMortemPP.getWellsPostMortemProfileDic(wellNames)
    return jsonify(postMortemPropsDic)

@app.route('/getwellcombinedanamorph', methods = ['POST'])
def getwellppanamorph():
    inputJson = request.json
    sWellNames = inputJson['wellNames']
    pWellName = inputJson['pWellName']

    # ppAnm = CombineAnamorphPP()
    # ppAnm.setWellRootFolder(wellRootFolder)
    # ppAnm.setPPPFolderName(postMortemFolderName)
    # ppAnm.readMarkerFile(markerFile)
    # ppAnm.readEventFile(eventFile)
    # ppAnm.setPWellName(pWellName)
    # wellsPPAnamorph_Dic = ppAnm.getDic_wellsPPP(sWellNames)

    wm = WellMarkerDB()
    wm.getDBMarker()
    markerDF = wm.getMarkerDF()

    postMortemCombineAnm = PostMortemProfileCombineAnamorph()
    postMortemCombineAnm.setPWellName(pWellName)
    # postMortemCombineAnm.readMarkerFile(markerFile)
    postMortemCombineAnm.setMarkerDF(markerDF)
    postMortemCombineAnm.readEventFile(eventFile)
    postMortemCombineAnm.setPostMortemAsciiFolder(postMortemAsciiFolder)
    wellsPPAnamorph_Dic = postMortemCombineAnm.getWellsAnamorphDic(sWellNames)

    return jsonify(wellsPPAnamorph_Dic)


@app.route('/geteventsum', methods = ['POST'])
def geteventsum():
    inputJson = request.json
    wellNames = inputJson['wellNames']
    wevent = WellEvent()
    wevent.readEventFile(eventFile)
    eventRecords = wevent.getWellsEventRecords(wellNames)
    return jsonify(eventRecords)

@app.route('/downloadppppost', methods = ['POST'])
def downloadppppost():
    inputJson = request.json
    wellName = inputJson['wellName']
    
    pppFile = PPPDownloadFile()
    pppFile.setWellRootFolder(wellRootFolder)
    pppFile.setPPPFolderName(postMortemFolderName)
    pppFile.readMarkerFile(markerFile)
    pppFile.setOutputFolder(tempFolder)

    ppppostDF = pppFile.getDF_PPPPost(wellName)

    response = make_response(ppppostDF.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename={}_post_mortem_data.csv".format(wellName)
    response.headers["Content-Type"] = "text/csv"
    response.headers["x-filename"] = "{}_post_mortem_data.csv".format(wellName)
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/downloadpppcombinedcommonexcel', methods = ['POST'])
def downloadpppcombinedcommon():
    inputJson = request.json
    sWellNames = inputJson['wellNames']

    # dCombinedPP = DownloadCombinedPP()
    # dCombinedPP.setWellRootFolder(wellRootFolder)
    # dCombinedPP.setPPPFolderName(postMortemFolderName)
    # dCombinedPP.readMarkerFile(markerFile)

    downloadCombinedPMAscii = DownloadPostMortemCombinedCommon()
    downloadCombinedPMAscii.setLogFolder(logFolder)
    downloadCombinedPMAscii.readMarkerFile(markerFile)
    downloadCombinedPMAscii.readEventFile(eventFile)
    downloadCombinedPMAscii.setPostMortemAsciiFolder(postMortemAsciiFolder)

    byteOutput = downloadCombinedPMAscii.getExcel_wellsCombinedCommon(sWellNames)
    byteOutput.seek(0)
    
    response = send_file(byteOutput, download_name="combined.xlsx", as_attachment=True)
    response.headers["x-filename"] = 'combined'
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/downloadpppcombinedcommonzip', methods = ['POST'])
def downloadpppcombinedcommonzip():
    inputJson = request.json
    wellNames = inputJson['wellNames']

    # dCombinedPP = DownloadCombinedPP()
    # dCombinedPP.setWellRootFolder(wellRootFolder)
    # dCombinedPP.setPPPFolderName(postMortemFolderName)
    # dCombinedPP.readMarkerFile(markerFile)

    # byteOutput = dCombinedPP.getZip_wellsCombinedCommon(wellNames)
    downloadCombinedPMAscii = DownloadPostMortemCombinedCommon()
    downloadCombinedPMAscii.setLogFolder(logFolder)
    downloadCombinedPMAscii.readMarkerFile(markerFile)
    downloadCombinedPMAscii.readEventFile(eventFile)
    downloadCombinedPMAscii.setPostMortemAsciiFolder(postMortemAsciiFolder)

    byteOutput = downloadCombinedPMAscii.getZip_wellsCombinedCommon(wellNames)

    byteOutput.seek(0)
    
    response = send_file(byteOutput, download_name="combined.zip", as_attachment=True)
    response.headers["x-filename"] = 'combined'
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/downloadpppcombinedanmexcel', methods = ['POST'])
def downloadpppcombinedanm():
    inputJson = request.json
    sWellNames = inputJson['wellNames']
    pWellName = inputJson['pWellName']

    # dCombineAnamorphPP = DownloadCombineAnamorphPP()
    # dCombineAnamorphPP.setWellRootFolder(wellRootFolder)
    # dCombineAnamorphPP.setPPPFolderName(postMortemFolderName)
    # dCombineAnamorphPP.readMarkerFile(markerFile)
    # dCombineAnamorphPP.readEventFile(eventFile)
    # dCombineAnamorphPP.setPWellName(pWellName)

    # byteOutput = dCombineAnamorphPP.getExcel_wellsCombinedAnm(sWellNames)

    downloadCombinedAnm = DownloadPostMortemCombinedAnamorph()
    downloadCombinedAnm.setPWellName(pWellName)
    downloadCombinedAnm.setLogFolder(logFolder)
    downloadCombinedAnm.readMarkerFile(markerFile)
    downloadCombinedAnm.readEventFile(eventFile)
    downloadCombinedAnm.setPostMortemAsciiFolder(postMortemAsciiFolder)
    byteOutput = downloadCombinedAnm.getExcel_wellsCombinedAnm(sWellNames)
    byteOutput.seek(0)
    response = send_file (
        byteOutput, 
        download_name="combined_anamorph_to_{}.xlsx".format(downloadCombinedAnm.getPWellName()), 
        as_attachment=True )
    response.headers["x-filename"] = "combined_anamorph_to_{}".format(downloadCombinedAnm.getPWellName())
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/downloadpppcombinedanmzip', methods = ['POST'])
def downloadpppcombinedanmzip():
    inputJson = request.json
    sWellNames = inputJson['wellNames']
    pWellName = inputJson['pWellName']

    # dCombineAnamorphPP = DownloadCombineAnamorphPP()
    # dCombineAnamorphPP.setWellRootFolder(wellRootFolder)
    # dCombineAnamorphPP.setPPPFolderName(postMortemFolderName)
    # dCombineAnamorphPP.readMarkerFile(markerFile)
    # dCombineAnamorphPP.readEventFile(eventFile)
    # dCombineAnamorphPP.setPWellName(pWellName)
    # byteOutput = dCombineAnamorphPP.getZip_wellsCombinedAnm(sWellNames)

    downloadCombinedAnm = DownloadPostMortemCombinedAnamorph()
    downloadCombinedAnm.setPWellName(pWellName)
    downloadCombinedAnm.setLogFolder(logFolder)
    downloadCombinedAnm.readMarkerFile(markerFile)
    downloadCombinedAnm.readEventFile(eventFile)
    downloadCombinedAnm.setPostMortemAsciiFolder(postMortemAsciiFolder)
    byteOutput = downloadCombinedAnm.getZip_wellsCombinedAnm(sWellNames)

    byteOutput.seek(0)
    response = send_file(
        byteOutput, 
        download_name="combined.zip", 
        as_attachment=True)
    response.headers["x-filename"] = 'combined_anamorph_to_{}'.format(downloadCombinedAnm.getPWellName())
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/getdatalist', methods = ['POST'])
def getdatalist():
    inputJson = request.json
    wellNames = inputJson['wellNames']
    dataTypes = inputJson['dataTypes']

    filelist = DataFileList()
    filelist.setPostMortemAsciiFolder(postMortemAsciiFolder)
    filelist.setWellParentFolder(wellRootFolder)
    filelist.setLogFolder(logFolder)
    filelist.setPostMortemFolder(postMortemFolderOri)
    dataDF = filelist.getDataDF(wellNames, dataTypes)
    dataRecords = dataDF.to_dict(orient='records')
    return jsonify(dataRecords)

@app.route('/downloadindatatab', methods = ['POST'])
def downloadindatatab():
    inputJson = request.json
    selectedDatas = inputJson["selectedDatas"]

    if len(selectedDatas)==1:
        fName = selectedDatas[0]["FILE_NAME"]
        fFolder = selectedDatas[0]["FOLDER_PATH"]

        response = send_from_directory(
            directory=fFolder,
            path=fName,
            download_name=fName,
            as_attachment=True,
        )
        response.headers["x-filename"] = fName
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'

        return response
    else:
        filePaths = []
        for dic in selectedDatas:
            filePath = os.path.join(dic["FOLDER_PATH"], dic["FILE_NAME"])
            filePaths.append(filePath)

        downloadfiles = DownloadFiles()
        stream = downloadfiles.getDownlodStream(filePaths)
        stream.seek(0)

        response = send_file(
            stream,
            as_attachment=True,
            download_name='download.zip',
            mimetype='application/x-zip-compressed'
        )
        response.headers["x-filename"] = 'download'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'

        return response

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)

# if __name__ == "__main__":
#     serve(app, host="0.0.0.0", port=8080)