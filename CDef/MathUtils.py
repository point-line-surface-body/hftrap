
def CalcDecayFactor (_number_fadeoffs_):
    if _number_fadeoffs_ < 1 : 
        return 1.00
    else:
        return pow(0.5, 1.00/((float)(_number_fadeoffs_)))