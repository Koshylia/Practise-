import re
def(NumOftheBand,Textparameter):
    hand = open(r"E:\DZZ\practice\LC81810252016147LGN00\LC81810252016147LGN00_MTL.txt")
    a=hand.read()
    regexp=str(Textparameter)+str(NumOftheBand)+" = ([-+0-9.]+)"
    print regexp
    stuff = re.findall(regexp, a)
    print stuff
    if len(stuff)== 1:
        Parameter = float(stuff[0])
    return Parameter
Parameter("","SUN_ELEVATION")
Parameter("10","K2_CONSTANT_BAND_")
