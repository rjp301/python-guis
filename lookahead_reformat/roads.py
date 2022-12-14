import pandas as pd

def gen_roads():
  data = [
    {"id": "KO", "chainage": 987100},
    {"id": "1", "chainage": 994316},
    {"id": "1A", "chainage": 994325},
    {"id": "2", "chainage": 997575},
    {"id": "3", "chainage": 998060},
    {"id": "4A", "chainage": 999000},
    {"id": "4", "chainage": 999907},
    {"id": "5", "chainage": 1003439},
    {"id": "6", "chainage": 1005866},
    {"id": "7", "chainage": 1006760},
    {"id": "8", "chainage": 1007498},
    {"id": "9", "chainage": 1007791},
    {"id": "10", "chainage": 1009755},
    {"id": "11", "chainage": 1012147},
    {"id": "12", "chainage": 1013588},
    {"id": "14", "chainage": 1015397},
    {"id": "15", "chainage": 1015482},
    {"id": "16", "chainage": 1015745},
    {"id": "17", "chainage": 1017603},
    {"id": "18", "chainage": 1019024},
    {"id": "18A", "chainage": 1019624},
    {"id": "19", "chainage": 1020076},
    {"id": "19A", "chainage": 1019835},
    {"id": "20", "chainage": 1021052},
    {"id": "21", "chainage": 1021420},
    {"id": "22", "chainage": 1022877},
    {"id": "23", "chainage": 1023795},
    {"id": "24", "chainage": 1024138},
    {"id": "25", "chainage": 1024985},
    {"id": "26", "chainage": 1025837},
    {"id": "26A", "chainage": 1025246},
    {"id": "27", "chainage": 1030162},
    {"id": "27A", "chainage": 1030440},
    {"id": "28", "chainage": 1032206},
    {"id": "29", "chainage": 1032678},
    {"id": "30", "chainage": 1033479},
    {"id": "31", "chainage": 1034574},
    {"id": "32", "chainage": 1034780},
    {"id": "33", "chainage": 1035834},
    {"id": "34", "chainage": 1036482},
    {"id": "35", "chainage": 1036525},
    {"id": "36", "chainage": 1036657},
    {"id": "37", "chainage": 1037703},
    {"id": "38", "chainage": 1037876},
    {"id": "39", "chainage": 1038571},
    {"id": "39A", "chainage": 1038579},
    {"id": "40", "chainage": 1039368},
    {"id": "41", "chainage": 1039812},
    {"id": "42", "chainage": 1039906},
    {"id": "43", "chainage": 1040206},
    {"id": "44", "chainage": 1040344},
    {"id": "44A", "chainage": 1040469},
    {"id": "45", "chainage": 1040860},
    {"id": "46", "chainage": 1041115},
    {"id": "47A", "chainage": 1041500},
    {"id": "47", "chainage": 1041935},
    {"id": "48", "chainage": 1042496},
    {"id": "49", "chainage": 1042590},
    {"id": "50", "chainage": 1042864},
    {"id": "51", "chainage": 1043376},
    {"id": "52", "chainage": 1044015},
    {"id": "53", "chainage": 1044096},
    {"id": "54", "chainage": 1044460},
    {"id": "55", "chainage": 1045023},
    {"id": "56", "chainage": 1045350},
    {"id": "57", "chainage": 1045675},
    {"id": "58", "chainage": 1045838},
    {"id": "59", "chainage": 1046038},
    {"id": "60", "chainage": 1046089},
    {"id": "61", "chainage": 1046531},
    {"id": "62", "chainage": 1046863},
    {"id": "63", "chainage": 1046880},
    {"id": "64", "chainage": 1048056},
    {"id": "64A", "chainage": 1048063},
    {"id": "65", "chainage": 1048472},
    {"id": "66", "chainage": 1048778},
    {"id": "67", "chainage": 1048885},
    {"id": "68", "chainage": 1050310},
    {"id": "69", "chainage": 1051046},
    {"id": "70", "chainage": 1052007},
    {"id": "71", "chainage": 1052508},
    {"id": "72", "chainage": 1053120},
    {"id": "73", "chainage": 1054227},
    {"id": "74", "chainage": 1054728},
    {"id": "75", "chainage": 1054939},
    {"id": "76", "chainage": 1055073},
    {"id": "77", "chainage": 1057053},
    {"id": "78", "chainage": 1057294},
    {"id": "79", "chainage": 1057456},
    {"id": "80", "chainage": 1057918},
    {"id": "81", "chainage": 1058338},
    {"id": "82", "chainage": 1058789},
    {"id": "83", "chainage": 1059354},
    {"id": "84", "chainage": 1060013},
    {"id": "85", "chainage": 1062024},
    {"id": "85A", "chainage": 1062597},
    {"id": "86", "chainage": 1063992},
    {"id": "87", "chainage": 1064753},
    {"id": "88", "chainage": 1067147},
    {"id": "89", "chainage": 1067521},
    {"id": "90", "chainage": 1069020},
    {"id": "91", "chainage": 1069330},
    {"id": "92", "chainage": 1070218},
    {"id": "93", "chainage": 1070617},
    {"id": "93A", "chainage": 1070699},
    {"id": "94", "chainage": 1071517},
    {"id": "95", "chainage": 1072362},
    {"id": "96", "chainage": 1073611},
    {"id": "97", "chainage": 1075027},
    {"id": "98", "chainage": 1075407},
    {"id": "99", "chainage": 1075687},
    {"id": "100", "chainage": 1075858},
    {"id": "Hope", "chainage": 1042100},
    {"id": "Herrling", "chainage": 1068280},
    {"id": "Popkum", "chainage": 1075600},
  ]
  return pd.DataFrame(data)

if __name__ == "__main__":
  print(gen_roads())