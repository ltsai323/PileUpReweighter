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

def isZero(number):
    if number < 1e-10: return True
    return False

def JsonFile(argv):
    if len(argv)<1+1: raise IOError(PrintHelp())
    return argv[1]

class OutputModule:
    def __init__(self, ofilename):
        self.ofile = ROOT.TFile(ofilename, 'recreate')
        self.hists = {}
    def Write(self):
        self.ofile.cd()
        for key,h in self.hists.iteritems():
            mylog.debug('storing hist ' + key)
            h.Write()
        self.ofile.Close()
    def PUweightCalc(self,pdf_data,pdf_sign):
        hout = ROOT.TH1F('mcwei_run000001','pileup weight', len(pdf_data),1,len(pdf_data))

        for ibin, (p_data,p_MC) in enumerate(zip(pdf_data,pdf_sign)):
            iBin = ibin+1
            if isZero(p_MC):
                hout.SetBinContent(iBin, 0.)
            else:
                mylog.debug('bin %d .....data : %f / mc %f = ratio %f'%(iBin,p_data,p_MC,p_data/p_MC))
                hout.SetBinContent(iBin, p_data/p_MC)
        self.hists['_puweight'] = hout

    def CheckPlot(self,PDF_data,PDF_sign):
        def get_hist(PDF,nametag):
            hist = ROOT.TH1F('pdf_'+nametag,'pileup', 75,0.,75.)
            for ibin, pdf in enumerate(PDF):
                hist.SetBinContent(ibin+1,pdf)
            return hist
        h_data = get_hist(PDF_data,'data')
        h_data.SetMarkerStyle(33)
        self.hists['data'] = h_data

        h_sign = get_hist(PDF_sign,'sign')
        h_sign.SetLineColor(2)
        self.hists['sign'] = h_sign

        self.draw_checkplot(self.ofile.GetName())


    def draw_checkplot(self, ofilename):
        oname = ofilename.replace('.','_') + '.png'

        canv=ROOT.TCanvas('c1','',400,500)
        self.hists['data'].Draw('P')
        self.hists['sign'].Draw("HIST SAME")
        canv.SaveAs(oname)


if __name__ == '__main__':
    LogMgr.InitLogger(level='info')
    mylog=LogMgr.GetLogger(__name__)

    import sys
    mcInfos=InfoLoader( JsonFile(sys.argv) )
    pdf_MC=mcInfos.ExtractProbabilityDesityValues()

    for iFile, oFile in mcInfos.GetIOFiles():
        hPU_data=GetPUHist(iFile)
        pdf_data = [ hPU_data.GetBinContent(ibin+1) / hPU_data.Integral() for ibin in range(hPU_data.GetNbinsX()) ]

        output = OutputModule(oFile)
        output.PUweightCalc(pdf_data,pdf_MC)
        output.CheckPlot(pdf_data,pdf_MC)
        output.Write()
