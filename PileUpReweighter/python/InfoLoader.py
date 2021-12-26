#!/usr/bin/env python2

import json
import os
import PythonToolBox.PythonToolBox.LogMgr as LogMgr
mylog=LogMgr.GetLogger(__name__)


class InfoLoader(object):
    def __init__(self, jsonname):
        #self._dir=jsonname[0: jsonname.rfind('.')] # preserve original path to the output files
        self._dir=jsonname[jsonname.rfind('/')+1: jsonname.rfind('.')] # put outputs to current directory

        with open(jsonname,'r') as fin:
            loadjson=json.load(fin)
            self._gitfile =loadjson['gitsource']
            self._afsfiles=loadjson['dataTarget']
            self._outnames=[ self.outputFilename(fname) for fname in self._afsfiles ]

            InfoLoader.downloadGitFile( self._gitfile )


    def ExtractProbabilityDesityValues(self):
        tmpfile=open('tmpfile.py' ,'r')

        lines=tmpfile.readlines()
        line_binning=[ line for line in lines if 'probFunctionVariable' in line ]
        line_probVal=[ line for line in lines if 'probValue'            in line ]
        if len(line_binning) != 1 or len(line_probVal) != 1:
            raise NameError('''InitLoader::ExtractInfo() : probability cannot be extracted.''')

        return InfoLoader.findNumberSet(line_probVal[0])
    def GetIOFiles(self):
        return  [ (afsfile, outname) for afsfile, outname in zip(self._afsfiles, self._outnames) ]

    @staticmethod
    def findNumberSet(line):
        lBraceIdx=line.find("(")
        rBraceIdx=line.find(")")
        numberStr=line[lBraceIdx:rBraceIdx+1]
        newnumStr=numberStr.replace(' ','')

        return eval(newnumStr)

    def outputFilename(self,origpath):
        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)

        nameidx1=origpath.rfind('/')
        nameidx2=origpath.rfind('.')
        extractedName=origpath[nameidx1+1:nameidx2]
        return '%s/puweights_%s.root' % (self._dir, extractedName)

    @staticmethod
    def downloadGitFile(gitlink):
        mylog.info('downloading from github...')
        os.system( 'curl -o tmpfile.py -O %s' % (gitlink) )
    def __del__(self):
        os.system('touch tmpfile.py && rm tmpfile.py')

if __name__ == '__main__':
    LogMgr.InitLogger(level='info')
    mylog=LogMgr.GetLogger(__name__)
    processor=InfoLoader( 'data/2016ReReco_Moriond17.json' )

    print processor.ExtractProbabilityDesityValues()
    for iFile, oFile in  processor.GetIOFiles():
        print 'GetIOFile() : output file: %s and input file: %s'%(oFile,iFile)
