import ROOT as r
from .art import art


#r.gInterpreter.GenerateDictionary("art::Hash<2>","include/art_shim.h")
r.gSystem.Load("lib/libArtShim")
r.gInterpreter.ProcessLine("#include \"include/art_shim.h\"")


art.patchTTree()

print("[art_shim]: ducktyped gm2calo into ROOT::TTree.")

#modb = r.TClass.GetClass("gm2midastoart::MidasODBArtRecord") #generate dictionary
#r.TClass.GetClass("gm2midastoart::MidasODBArtRecord").GetTypeInfo() #0x0 we don't have one
#modbi = r.TStreamerInfo(modb);
#modbd = r.TDictionary.GetDictionary("gm2midastoart::MidasODBArtRecord")
