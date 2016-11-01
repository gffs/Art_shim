import ROOT as r
import sys

"""
class calo_cluster_iter(object):
    def __init__(self, vecCluster):
        self.vecCluster = vecCluster

    def __iter__(self):
        #return iter(self.vecCluster)
        return (cl for cl in self.vecCluster)

    def next(self):
        for cl in self.vecCluster:
            yield cl
"""

#patched into gm2calo::CrystalHitArtRecord
class crystal_hit_record(object):

    @staticmethod
    def __str__(self):
        return "fill: %d, calo: %d, island: %d, time: %.2f, energy: %.1f" % (self.fillNum, self.caloNum, self.islandNum, self.time, self.energy)

    @property
    def riderChannelHeaderThrough(self):
        key = self.riderChannelHeaderRoot.key_
        tree = r.gDirectory.Get("Events")
        rider_headers = getattr(tree, "gm2calo::RiderChannelHeaders_headerUnpacker_unpacker_slacUnpackerFitter.")
        return rider_headers.obj[key]

    @property
    def amcHeaderThrough(self):
        key = self.amcHeaderRoot.key_
        tree = r.gDirectory.Get("Events")
        amc_headers = getattr(tree, "gm2calo::AMCHeaders_headerUnpacker_unpacker_slacUnpackerFitter.")
        return amc_headers.obj[key]

# patched into gm2calo::ClusterArtRecord
class cluster_record(object):

    @staticmethod
    def __str__(self):
        return "fill: %d, calo: %d, island: %d, time: %.2f, energy: %.1f, x: %.1f, y: %.1f, hits: %d" % (self.fillNum, self.caloNum, self.islandNum, self.time, self.energy, self.x, self.y, self.crystalHits.size())

    @property
    def isSync(self):
        return self.time < 1600 and self.crystalHits.size() > 50

    @property
    def isLaser(self):
        return self.time > 1600 and self.crystalHits.size() > 50

    @property
    def isBeam(self):
        return self.crystalHits.size() < 50


# patched into gm2calo::CaloClusterArtRecord
class calo_cluster_record(object):

    @property
    def numSyncPulses(self):
        return sum([cl.isSync for cl in self.clusters])

    @property
    def numLaserPulses(self):
        return sum([cl.isLaser for cl in self.clusters])

    @property
    def numBeamEvents(self):
        return sum([cl.isBeam for cl in self.clusters])


#patched into CaloIslandArtRecord
class calo_island_record(object):

    @staticmethod
    def __str__(self):
        return "[CaloIslandRecord] for fill %d, calo %d, at tZero %.2f, with %d islands" % (self.fillNum, self.caloNum, self.tZero, self.matrixIslands.size())


class matrix_island_record(object):

    @staticmethod
    def __str__(self):
        res = "[MatrixIslandRecord] for fill %d, calo %d, island number: %d\n" % (self.fillNum, self.caloNum, self.islandNum)
        res += "island first sample number: %d, island length: %d, number of traces: %d" % (self.firstSampleNum, self.length, self.islands.size())
        return res


class island_record(object):

    @staticmethod
    def __str__(self):
        res = "[IslandArtRecord] for fill %d, calo %d, island num %d, xtal num %d\n" % (self.fillNum, self.caloNum, self.islandNum, self.xtalNum)
        res += "first sample num %d, island length %d, trace length %d\n" % (self.firstSampleNum, self.length, self.trace.size())
        res += "first 8 samples: "
        for sample in range(10):
            res += "0x%04x " % self.trace[sample]
        res += "\n"
        return res


class calo(object):
    def __init__(self, tree):
        self.tree = tree

    @property
    def cluster(self):
        #cl = getattr(self.tree, "gm2calo::CaloClusterArtRecords_hitCluster_cluster_reprocessCluster.")
        cl = getattr(self.tree, "gm2calo::CaloClusterArtRecords_hitCluster_cluster_slacUnpackerFitter.")
        return cl.obj[0]

    @property
    def island(self):
        #cl = getattr(self.tree, "dataRecord_moduleName_instanceLabel_processName.")
        branch = getattr(self.tree, "gm2calo::CaloIslandArtRecords_islandUnpacker_unpacker_slacUnpackerFitter.")
        return branch.obj[0]


class art(object):

    @property
    def calo(self):
        return calo(self)

    @staticmethod
    def patchTTree():
        r.TTree.calo = art.calo

        r.gm2calo.CaloClusterArtRecord.numSyncPulses = calo_cluster_record.numSyncPulses
        r.gm2calo.CaloClusterArtRecord.numLaserPulses = calo_cluster_record.numLaserPulses
        r.gm2calo.CaloClusterArtRecord.numBeamEvents = calo_cluster_record.numBeamEvents

        r.gm2calo.ClusterArtRecord.__str__ = cluster_record.__str__
        r.gm2calo.ClusterArtRecord.isSync = cluster_record.isSync
        r.gm2calo.ClusterArtRecord.isLaser = cluster_record.isLaser
        r.gm2calo.ClusterArtRecord.isBeam = cluster_record.isBeam

        r.gm2calo.CaloIslandArtRecord.__str__ = calo_island_record.__str__
        r.gm2calo.MatrixIslandArtRecord.__str__ = matrix_island_record.__str__
        r.gm2calo.IslandArtRecord.__str__ = island_record.__str__

        r.gm2calo.CrystalHitArtRecord.__str__ = crystal_hit_record.__str__
        r.gm2calo.CrystalHitArtRecord.getRiderChannelHeader = crystal_hit_record.getRiderChannelHeader
        r.gm2calo.CrystalHitArtRecord.getAmcHeader = crystal_hit_record.getAmcHeader

        cr_hit = r.gm2calo.CrystalHitArtRecord()
        r.gm2calo.CrystalHitArtRecord.amcHeaderRoot = cr_hit.__class__.__dict__['amcHeader'] #PropertyProxy
        r.gm2calo.CrystalHitArtRecord.amcHeader = crystal_hit_record.amcHeaderThrough
        r.gm2calo.CrystalHitArtRecord.riderChannelHeaderRoot = cr_hit.__class__.__dict__['riderChannelHeader']
        r.gm2calo.CrystalHitArtRecord.riderChannelHeader = crystal_hit_record.riderChannelHeaderThrough

        #r.gm2calo.ClusterArtRecordCollection.__iter__ = calo_cluster_iter()
        #setattr(r.TTree, "caloCluster", art.caloCluster)
