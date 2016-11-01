#pragma once

#include "boost/array.hpp"
#include <set>
#include <string>

namespace cet {

class sha1 {
public:
    static  std::size_t const             digest_sz  = 20;
    typedef  unsigned char                uchar;
    typedef  boost::array<uchar,digest_sz>  digest_t;
};

} //namespace cet


namespace fhicl {

struct ParameterSetID {
    bool                 valid_;
    cet::sha1::digest_t  id_;
};

} //namespace fhicl


namespace art {

struct ProductID {
    unsigned short processIndex_;
    unsigned short productIndex_;
};

struct EDProductGetter { };

struct RefCore {
    ProductID id_;
    struct RefCoreTransients {} transients_;
};

template <typename T>
class Ptr {
public:
    RefCore core_;
    std::size_t key_;
};

template <typename T>
class Wrapper {
  public:
    bool present;
    T obj;

  public:
    Wrapper(): present(0), obj() {}
};

struct Timestamp {
    unsigned int timeLow_;
    unsigned int timeHigh_;
};

struct RunID {
    unsigned int run_;
};

struct SubRunID {
    RunID run_;
    unsigned int subRun_;
};

enum HashedTypes {
    ParameterSetType = 1,
    ProcessHistoryType,
    ProcessConfigurationType,
    ParentageType = 5
};

template<int I>
class Hash {
  public:
    bool operator< (Hash<I> const& other) const {
        return hash_ < other.hash_;
    }
  public:
    std::string hash_;
};

using ProcessHistoryID = Hash<ProcessHistoryType>;
using SetProcessHistoryID = std::set<ProcessHistoryID>;

struct RunAuxiliary {
    ProcessHistoryID processHistoryID_;
    SetProcessHistoryID allEventsProcessHistories_;
    RunID id_;
    Timestamp beginTime_;
    Timestamp endTime_;
  public:
    RunAuxiliary() {}
};

struct SubRunAuxiliary {
    ProcessHistoryID processHistoryID_;
    unsigned int rangeSetID_;
    SubRunID id_;
    Timestamp beginTime_;
    Timestamp endTime_;
public:
    SubRunAuxiliary() {}
};

struct HLTPathStatus {
    unsigned short status_;
};

struct HLTGlobalStatus {
    std::vector<HLTPathStatus> paths_;
};

struct DoNotRecordParents { };

class TriggerResults: public HLTGlobalStatus, public DoNotRecordParents {
public:
    fhicl::ParameterSetID psetid_;
};

} //namespace art

namespace gm2midastoart {

struct MidasODBArtRecord {
    unsigned int runNum;
    std::string odb_string;
};

} //gm2midastoart


namespace gm2calo {

struct CDFHeader {
    unsigned int crateNum;
    unsigned int FOV;
    unsigned int sourceID;
    unsigned int lv1ID;
    unsigned int eventType;
    unsigned long clockCounter;
    unsigned int nAMC;
};

using CDFHeaderCollection = std::vector<CDFHeader>;

struct AMCHeader {
	unsigned int amcNum;
	unsigned int triggerNum;
	unsigned long clockCounter;
	unsigned int fillType;
	unsigned int boardType;
	unsigned int boardID;
};

using AMCHeaderCollection = std::vector<AMCHeader>;

struct RiderChannelHeader {
	unsigned int waveformCount;
	unsigned int waveformGap;
	unsigned int channelTag;
	unsigned int triggerNum;
	unsigned int fillType;
	unsigned int waveformLength;
};

using RiderChannelHeaderCollection = std::vector<RiderChannelHeader>;

struct FC7Header {
    unsigned int amcNum;
    unsigned int triggerNum;
    unsigned long clockCounter;
    unsigned int fillType;
    unsigned int boardType;
    unsigned int boardID;
};

using FC7HeaderCollection = std::vector<FC7Header>;

struct CrystalHitArtRecord {
	art::Ptr<AMCHeader> amcHeader;
	art::Ptr<RiderChannelHeader> riderChannelHeader;

	int fillNum;
	int caloNum;
	int islandNum;
	int xtalNum;
	double time;
	double energy;
};

using CrystalHitArtRecordCollection = std::vector<CrystalHitArtRecord>;

struct ClusterArtRecord {
	int fillNum;
	int caloNum;
	int islandNum;
	double time;
	double energy;
	double x, y;
	CrystalHitArtRecordCollection crystalHits;

  public:
	ClusterArtRecord() {}; //to silence TClass::New()
};

using ClusterArtRecordCollection = std::vector<ClusterArtRecord>;

struct CaloClusterArtRecord {
	int fillNum;
	int caloNum;
	ClusterArtRecordCollection clusters;

  public:
	CaloClusterArtRecord() {};
};

using CaloClusterArtRecordCollection = std::vector<CaloClusterArtRecord>;

struct IslandArtRecord {
    art::Ptr<AMCHeader> amcHeader;
    art::Ptr<RiderChannelHeader> riderChannelHeader;
    int fillNum;
    int caloNum;
    int islandNum;
    int xtalNum;
    int firstSampleNum;
    int length;
    std::vector<short> trace;

public:
    IslandArtRecord() {}
};

using IslandArtRecordCollection = std::vector<IslandArtRecord>;

struct MatrixIslandArtRecord {
    int fillNum;
    int caloNum;
    int islandNum;
    int firstSampleNum;
    int length;
    IslandArtRecordCollection islands;

public:
    MatrixIslandArtRecord() {}
};

using MatrixIslandArtRecordCollection = std::vector<MatrixIslandArtRecord>;

struct CaloIslandArtRecord {
    int fillNum;
    int caloNum;
    double tZero;
    MatrixIslandArtRecordCollection matrixIslands;

public:
    CaloIslandArtRecord() {}
};

using CaloIslandArtRecordCollection = std::vector<CaloIslandArtRecord>;

struct FitResultArtRecord {
    art::Ptr<AMCHeader> amcHeader;
    art::Ptr<RiderChannelHeader> riderChannelHeader;
    int fillNum;
    int caloNum;
    int islandNum;
    int xtalNum;
    double time;
    double energy;
    double pedestal;
    double pulsewidth;
    double chi2;

public:
    FitResultArtRecord() {}
};

using FitResultArtRecordCollection = std::vector<FitResultArtRecord>;

struct MatrixFitResultArtRecord {
    int fillNum;
    int caloNum;
    int islandNum;
    FitResultArtRecordCollection fitResults;

public:
    MatrixFitResultArtRecord() {}
};

using MatrixFitResultArtRecordCollection = std::vector<MatrixFitResultArtRecord>;

struct CaloFitResultArtRecord {
    int fillNum;
    int caloNum;
    double tZero;
    MatrixFitResultArtRecordCollection matrixFitResults;

public:
    CaloFitResultArtRecord() {}
};

using CaloFitResultArtRecordCollection = std::vector<CaloFitResultArtRecord>;



} //namespace gm2calo
