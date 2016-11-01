#ifdef __CLING__
    #pragma link C++ nestedclasses;
    #pragma link C++ nestedtypedefs;

    #pragma link C++ class std::set<art::Hash<2>>+;
    #pragma link C++ class std::set<art::Hash<2>>::*+;
    #pragma link C++ operators std::set<art::Hash<2>>::iterator;
    #pragma link C++ operators std::set<art::Hash<2>>::const_iterator;
    #pragma link C++ operators std::set<art::Hash<2>>::reverse_iterator;

//    #pragma link C++ class gm2midastoart::MidasODBArtRecord+;
//    #pragma link C++ class gm2midastoart::MidasODBArtRecord::*+;
#endif
