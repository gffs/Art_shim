import math
import ROOT as r
import art_shim as art
import glob, sys
import ctypes

class SlacRun:
    def __init__(
            self,
            fname,
            eng = 3.0,
        ):
        self.eng = eng
        self.fl_list = glob.glob('/Users/jarek/work/slac_data/gm2slac_run*' + str(fname) + '.art')
        # print self.fl_list

if __name__ == '__main__':
    run = SlacRun(3051)
    t = r.TFile(run.fl_list[0])
    e = t.Get("Events")
    #rt = t.Get("Runs")
    #srt = t.Get("SubRuns")

    e.SetBranchStatus('*', 0)
    e.SetBranchStatus('gm2calo::CaloClusterArtRecords_hitCluster_cluster_slacUnpackerFitter*', 1)
    # e.SetBranchStatus('gm2calo::CaloClusterArtRecords_hitCluster_cluster_reprocessCluster*', 1)
    e.SetBranchStatus('gm2calo::RiderChannelHeaders_headerUnpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('gm2calo::AMCHeaders_headerUnpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('gm2calo::CDFHeaders_headerUnpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('art::TriggerResults_TriggerResults__slacUnpackerFitter*', 1)
    #e.SetBranchStatus('art::TriggerResults_TriggerResults__reprocessCluster*', 1)
    e.SetBranchStatus('gm2calo::IslandArtRecords_laserUnpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('gm2calo::FC7Headers_fc7Unpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('gm2calo::CaloIslandArtRecords_islandUnpacker_unpacker_slacUnpackerFitter*', 1)
    e.SetBranchStatus('gm2calo::CaloFitResultArtRecords_islandFitter_fitter_slacUnpackerFitter*', 1)


    #scl = r.art.Wrapper("gm2calo::CaloClusterArtRecordCollection")()

    #scl = r.std.vector("gm2calo::CaloClusterArtRecord")(54)
    #e.SetBranchAddress("gm2calo::CaloClusterArtRecords_hitCluster_cluster_reprocessCluster.", r.AddressOf(scl))


    e_hist = r.TH2F("cl_eng", "eng vs time;time [nsec];eng [MeV]", 100, 0, 10000, 100, 0, 60000)
    i_h = r.TH2F("cl_time", "island sort vs time; time [nsec]; island num", 100, 0, 100000, 20, 0, 20)
    numBeam_h = r.TH1I("numBeam", "number of beam events per fill; number of events;", 5, 0, 5)

    entry_num = 0

    for fill in e:
        entry_num += 1
        #fill.Show()
        #cl = getattr(fill, "gm2calo::CaloClusterArtRecords_hitCluster_cluster_reprocessCluster.")
        acl = fill.calo.cluster
        print(acl)
        # numBeam_h.Fill(acl.numBeamEvents)
        # print "fill:", entry_num, "numSyncPulses:", acl.numSyncPulses

        #print cl.obj[0].clusters[10].crystalHits[24].time
        #print

        for cl in acl.clusters:
        # for isl in acl.matrixIslands:
            print(cl)
            # e_hist.Fill(cl.time, cl.energy)
            # i_h.Fill(entry_num, cl.islandNum)

            # trc = isl.islands[13]
            # print(trc)

            cr_hit = cl.crystalHits[13]
            print(cr_hit)

            amc = cr_hit.amcHeader
            # amc = cr_hit.getAmcHeader()
            print(amc)
            # print(amc.key_)
            # print(amc.amcNum, amc.triggerNum, amc.clockCounter)

            #amc = cl.crystalHits[22].amcHeader


            #print(amc.__dict__)
            #print("key: ", amc.key_)
            #ra = r.AddressOf(amc)
            #ra0 = ra[0]
            #print("ra at: 0x%016x" % ra0)
            #print(r.AddressOf(amc))
            #print(ctypes.string_at(ra0, 128))

            break

        if (entry_num > 2):
            break



    c = r.TCanvas()
    numBeam_h.Draw('l')
    # e_hist.Draw("box")
    # i_h.Draw("box")
    c.SaveAs("cluster_eng.pdf")
