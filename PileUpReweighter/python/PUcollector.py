#!/usr/bin/env python2
# usage :
#    ./this.py outputname.root

import ROOT
from PileUpReweighter.PileUpReweighter.InfoLoader import InfoLoader
import PythonToolBox.PythonToolBox.LogMgr as LogMgr
mylog=LogMgr.GetLogger(__name__)

def PrintHelp():
    mylog.error(
            '''This file needs to input a json file.
            arg1: path to json file. (Both absolute and relative paths are available.
            The output file is at current directory
            '''
            )



def GetPUHist(ifile):
    mylog.debug('loading input file : ' + ifile)
    f=ROOT.TFile.Open(ifile)
    output=f.Get('pileup')
    output.SetDirectory(0)
    return output

def datanormalization(datahist):
    return sum( [datahist.GetBinContent(ibin+1) for ibin in range(datahist.GetNbinsX())] )

def JsonFile(argv):
    if len(argv)<1+1: raise IOError(PrintHelp())
    return argv[1]

if __name__ == '__main__':
    LogMgr.InitLogger(level='info')
    mylog=LogMgr.GetLogger(__name__)

    import sys
    mcInfos=InfoLoader( JsonFile(sys.argv) )
    mixedPUvals=mcInfos.ExtractProbabilityDesityValues()

    for iFile, oFile in mcInfos.GetIOFiles():
        hPU_data=GetPUHist(iFile)

        fout=ROOT.TFile(oFile,'recreate')
        fout.cd()
        hout=hPU_data.Clone('mcwei_run000001')

        checkdata=0.
        data_normalization=datanormalization(hPU_data)
        for ibin in range(hPU_data.GetNbinsX()):
            iBin=ibin+1
            mixedPUidx=int(hPU_data.GetBinLowEdge(iBin))
            dataPUval=float(hPU_data.GetBinContent(iBin) ) / data_normalization

            # only set a warning when data contains value but no MC recorded at large bin.
            if mixedPUidx < len(mixedPUvals):
                mcPUval=float( mixedPUvals[mixedPUidx] )
                hout.SetBinContent(iBin, dataPUval/mcPUval)
                checkdata+=dataPUval
            else:
                if dataPUval < 1e-6: hout.SetBinContent(iBin, 0.)
                else: mylog.warning('filling reweight hist -- no PU mixed in MC but some record at data at bin %d' % iBin)
        hout.Write()
        fout.Close()

        mylog.info( 'normalizations of data and MC are %.3f and %.3f. Their values must be 1.' % (checkdata,sum( mixedPUvals)) )
