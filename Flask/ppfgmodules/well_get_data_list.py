import os
import re
import glob
import pandas as pd

class DataFileList:
    
    def __init__(self):
        self._pmPPFGFolder = 'PPFG'
        # self._deviationFileFmt = '_deviation.csv'

    def setWellParentFolder(self, wellParentFolder):
        self._wellParentFolder = wellParentFolder
    
    def getWellParentFolder(self):
        return self._wellParentFolder
    
    def setLogFolder(self, logFolder):
        self._logFolder = logFolder
    
    def getLogFolder(self):
        return self._logFolder
    
    # def setDeviationSurveyFile(self, deviationSurveyFile):
    #     self._devSurFile = deviationSurveyFile
    
    # def getDeviationSurveyFile(self):
    #     return self._devSurDF

    # def setDeviationSurveyDF(self, deviationSurveyDF):
    #     self._devSurDF = deviationSurveyDF
    
    # def getDeviationSurveyDF(self):
    #     return self._devSurDF

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

    def setPostMortemFolder(self, postMortemFolder):
        self._postMortemFolder = postMortemFolder
        pmWellFolders = [f for f in os.listdir(postMortemFolder) if os.path.isdir(os.path.join(postMortemFolder, f))]
        self.setPostMortemWellFolders(pmWellFolders)

    def getPostMortemFolder(self):
        return self._postMortemFolder

    def setPostMortemWellFolders(self, wellFolders):
        self._postMortemWellFolders = wellFolders
    
    def getPostMortemWellFolders(self):
        return self._postMortemWellFolders
    
    def getPostMortemWellFolderName(self, wellName):
        postMortemFolder = self.getPostMortemFolder()
        postMortemWellFolders = self.getPostMortemWellFolders()
        wellNameLower = wellName.lower()
        postMortemSelectedWellFolders = []
        for postMortemWellFolder in postMortemWellFolders:
            postMortemWellFolderSplitted = re.split('\s|_', postMortemWellFolder.lower())
            for el in postMortemWellFolderSplitted:
                if el == wellNameLower:
                    postMortemSelectedWellFolders.append(postMortemWellFolder)
        return postMortemSelectedWellFolders
    
    def getPostMortemWellPPFG(self, wellName):
        pmPPFGFiles = []
        pmPPFGFoldersPath = []
        pmFolder = self.getPostMortemFolder()
        pmWellFolderNames = self.getPostMortemWellFolderName(wellName)
        if len(pmWellFolderNames)>0:
            for pmWellFolderName in pmWellFolderNames:
                pmWellFolderPPFGPath = os.path.join(*[pmFolder, pmWellFolderName, self._pmPPFGFolder])
                if os.path.exists(pmWellFolderPPFGPath):
                    childFiles = os.listdir(pmWellFolderPPFGPath)
                    for childFile in childFiles:
                        pmPPFGFiles.append(childFile)
                        pmPPFGFoldersPath.append(os.path.abspath(pmWellFolderPPFGPath))
        else:
            pass
        return pmPPFGFiles, pmPPFGFoldersPath

    def getPostMortemWellsPPFGFile(self, wellNames):
        pmPPFGFiles = []
        pmPPFGFoldersPath = []
        pmFolder = self.getPostMortemFolder()
        if len(wellNames)>0:
            for wellName in wellNames:
                pmPPFGFilesTemp, pmPPFGFilesPathTemp = self.getPostMortemWellPPFG(wellName)
                pmPPFGFiles.extend(pmPPFGFilesTemp)
                pmPPFGFoldersPath.extend(pmPPFGFilesPathTemp)
        else:
            pass
        return pmPPFGFiles, pmPPFGFoldersPath
    
    # def getWellPreFile(self, wellName, fileNameFmt):
    #     wellParentFolder = self.getWellParentFolder()
    #     wellFolder = os.path.join(wellParentFolder, wellName)
    #     preFileName =  wellName + fileNameFmt
    #     preFilePath = os.path.join(*[wellParentFolder, wellName, preFileName])
    #     preFilesName = []
    #     preFoldersPath = []
    #     if os.path.exists(preFilePath):
    #         preFilesName.append(preFileName)
    #         preFoldersPath.append(os.path.abspath(wellFolder))
    #     return preFilesName, preFoldersPath
    
    # def getWellsPreFile(self, wellNames, fileNameFmt):
    #     preFilesName = []
    #     preFoldersPath = []
    #     if len(wellNames)>0:
    #         for wellName in wellNames:
    #             preFilesNameTemp, preFilesPathTemp = self.getWellPreFile(wellName, fileNameFmt)
    #             preFilesName.extend(preFilesNameTemp)
    #             preFoldersPath.extend(preFilesPathTemp)
    #     else:
    #         pass
    #     return preFilesName, preFoldersPath
    
    def getWellLog(self, wellName):
        logFolder = self.getLogFolder()
        logFileName = wellName + '.csv'
        logFilePath = os.path.join(logFolder, logFileName)
        logFilesName = []
        logFoldersPath = []
        if os.path.exists(logFilePath):
            logFilesName.append(logFileName)
            logFoldersPath.append(os.path.abspath(logFolder))
        return logFilesName, logFoldersPath

    def getWellsLog(self, wellNames):
        logFileNames = []
        logFolderPaths = []
        if len(wellNames)>0:
            for wellName in wellNames:
                logFilesNameTemp, logFoldersPathTemp = self.getWellLog(wellName)
                logFileNames.extend(logFilesNameTemp)
                logFolderPaths.extend(logFoldersPathTemp)
        else:
            pass
        return logFileNames, logFolderPaths
    
    def getPostMortemAsciiWellFile(self, wellName):
        pmAsciiFilesName = []
        pmAsciiFoldersPath = []
        pmAsciiFolder = self.getPostMortemAsciiFolder()
        pmAsciiWellFileNames = self.getPostMortemAsciiWellFileNames()
        wellNameLower = wellName.lower()
        for pmAsciiWellFileName in pmAsciiWellFileNames:
            pmAsciiWellFileNameSplitted = re.split('\s|_', pmAsciiWellFileName.lower())
            if wellNameLower in pmAsciiWellFileNameSplitted:
                pmAsciiFilesName.append(pmAsciiWellFileName+'.csv')
                pmAsciiFoldersPath.append(os.path.abspath(pmAsciiFolder))

        return pmAsciiFilesName, pmAsciiFoldersPath

    def getPostMortemAsciiWellsFile(self, wellNames):
        pmAsciiFilesName = []
        pmAsciiFoldersPath = []
        if len(wellNames)>0:
            for wellName in wellNames:
                pmAsciiFilesNameTemp, pmAsciiFoldersPathTemp = self.getPostMortemAsciiWellFile(wellName)
                pmAsciiFilesName.extend(pmAsciiFilesNameTemp)
                pmAsciiFoldersPath.extend(pmAsciiFoldersPathTemp)
        else:
            pass
        return pmAsciiFilesName, pmAsciiFoldersPath
    
    def getDataDF(self, wellNames, dataTypes):
        fileNames = []
        fileTypes = []
        folderPaths = []
        for dataType in dataTypes:
            if dataType == 'post_mortem_profile_original':
                pmFileNames, pmFolderPaths = self.getPostMortemWellsPPFGFile(wellNames)
                fTypes = ['post mortem' for _ in pmFileNames]
                fileNames.extend(pmFileNames)
                fileTypes.extend(fTypes)
                folderPaths.extend(pmFolderPaths)
            
            elif dataType == 'post_mortem_profile_ascii':
                pmFileNames, pmFolderPaths = self.getPostMortemAsciiWellsFile(wellNames)
                fTypes = ['post mortem (ASCII)' for _ in pmFileNames]
                fileNames.extend(pmFileNames)
                fileTypes.extend(fTypes)
                folderPaths.extend(pmFolderPaths)

            elif dataType == 'log':
                logFileNames, logFolderPaths = self.getWellsLog(wellNames)
                fTypes = ['log' for _ in logFileNames]
                fileNames.extend(logFileNames)
                fileTypes.extend(fTypes)
                folderPaths.extend(logFolderPaths)

            # elif dataType == 'deviation':
            #     deviationSurveyFile = self.getDeviationSurveyFile()
            #     if os.path.exists(deviationSurveyFile):
            #         deviationSurveyDF = pd.read_csv(deviationSurveyFile)
            #         self.setDeviationSurveyDF(deviationSurveyDF)
            #     devFileNames, devFolderPaths = self.getWellsPreFile(wellNames, self._deviationFileFmt)
            #     fTypes = ['deviation' for _ in devFileNames]
            #     fileNames.extend(devFileNames)
            #     fileTypes.extend(fTypes)
            #     folderPaths.extend(devFolderPaths)
        
        dataFileDF = pd.DataFrame({
            'FILE_NAME': fileNames,
            'FILE_TYPE': fileTypes,
            'FOLDER_PATH': folderPaths
        })
        return dataFileDF