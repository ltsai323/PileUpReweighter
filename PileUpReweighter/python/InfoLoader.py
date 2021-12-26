#!/usr/bin/env python2

import json
import os


class InfoLoader(object):
    def __init__(self, jsonname):
        self._dir=jsonname[0: jsonname.rfind('.')]

        with open(jsonname,'r') as fin:
            loadjson=json.load(fin)
            self._gitfile =loadjson['gitsource']
            self._afsfiles=loadjson['dataTarget']
            self._outnames=[ self.outputFilename(fname) for fname in self._afsfiles ]
            # for a in self._outnames: print a

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
        return  [ {'iFile': afsfile, 'oFile': outname} for afsfile, outname in zip(self._afsfiles, self._outnames) ]

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
        #print extractedName
        return '%s/puweights_%s.root' % (self._dir, extractedName)

    @staticmethod
    def downloadGitFile(gitlink):
        print 'downloading from github...'
        os.system( 'curl -o tmpfile.py -O %s' % (gitlink) )
    def __del__(self):
        os.system('touch tmpfile.py && rm tmpfile.py')

if __name__ == '__main__':
    processor=InfoLoader( 'data/2016ReReco_Moriond17.json' )

    print processor.ExtractProbabilityDesityValues()
    for IOFile in  processor.GetIOFiles():
        print '  --  '.join( ( IOFile['iFile'], IOFile['oFile'] ) )
