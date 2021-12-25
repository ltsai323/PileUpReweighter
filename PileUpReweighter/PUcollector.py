#!/usr/bin/env python2
# usage :
#    ./this.py outputname.root

import ROOT
import xPhoton.xPhoton.Managers.LogMgr as LogMgr

mylog=LogMgr.GetLogger(__name__)

def PUValfrom_mix_2016_26ns_Moriond17MC_PoissonOOTPU():
    ''' source file:
    https://github.com/cms-sw/cmssw/blob/master/SimGeneral/MixingModule/python/mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py
    '''
    return (1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,0.00071209 ,0.00130121 ,0.00245255 ,0.00502589 ,0.00919534 ,0.0146697 ,0.0204126 ,0.0267586 ,0.0337697 ,0.0401478 ,0.0450159 ,0.0490577 ,0.0524855 ,0.0548159 ,0.0559937 ,0.0554468 ,0.0537687 ,0.0512055 ,0.0476713 ,0.0435312 ,0.0393107 ,0.0349812 ,0.0307413 ,0.0272425 ,0.0237115 ,0.0208329 ,0.0182459 ,0.0160712 ,0.0142498 ,0.012804 ,0.011571 ,0.010547 ,0.00959489 ,0.00891718 ,0.00829292 ,0.0076195 ,0.0069806 ,0.0062025 ,0.00546581 ,0.00484127 ,0.00407168 ,0.00337681 ,0.00269893 ,0.00212473 ,0.00160208 ,0.00117884 ,0.000859662 ,0.000569085 ,0.000365431 ,0.000243565 ,0.00015688 ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05 ,1.73032e-05 ,1.435e-05 ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05)




def dataPU_2016Legacy():
    f=ROOT.TFile.Open('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/PrelLum15And1613TeV/PileupHistogram-goldenJSON-13tev-2016-69200ub-75bins.root')
    output=f.Get('pileup')
    output.SetDirectory(0)
    return output
    #return f.Get('pileup').Clone()
def datanormalization(datahist):
    return sum( [datahist.GetBinContent(ibin+1) for ibin in range(datahist.GetNbinsX())] )

def checkInputs(hist_data, mc_vallist):
    if len(mc_vallist) <= 0:
        raise IOError('invalid MC values ')
    if not hist_data:
        raise IOError('nothing in data')
    if hist_data.GetNbinsX() <= 0:
        raise IOError('invalid data histogram')
    if len(mc_vallist) > hist_data.GetNbinsX():
        mylog.warning('MC binning is greater than data binning. Please check!')
def RenameOutput(origname):
    import os
    import sys
    outname=origname
    if len(sys.argv) > 1:
        outname=sys.argv[1]
        os.system( 'mv %s %s' % (origname,outname) )
    mylog.info('output file : %s' % outname)
if __name__ == '__main__':
    LogMgr.InitLogger(level='info')
    mylog=LogMgr.GetLogger(__name__)
    mixedPUvals=PUValfrom_mix_2016_26ns_Moriond17MC_PoissonOOTPU()
    hPU_data=dataPU_2016Legacy()
    checkInputs(hPU_data, mixedPUvals)


    tmpoutput='_PUoutput.root'
    fout=ROOT.TFile(tmpoutput,'recreate')
    fout.cd()
    hout=hPU_data.Clone()
    hout.Clear()

    checkdata=0.
    data_normalization=datanormalization(hPU_data)
    for ibin in range(hPU_data.GetNbinsX()):
        iBin=ibin+1
        mcPUval=float(mixedPUvals[ int(hPU_data.GetBinLowEdge(iBin)) ] )
        dataPUval=float(hPU_data.GetBinContent(iBin) ) / data_normalization
        hout.SetBinContent(iBin, dataPUval/mcPUval)
        checkdata+=dataPUval
    hout.SetName('mcwei_run000001')
    hout.Write()
    fout.Close()
    RenameOutput(tmpoutput)

    mylog.info( 'normalizations of data and MC are %.3f and %.3f. Their values must be 1.' % (checkdata,sum( mixedPUvals)) )
