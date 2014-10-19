import time

def CalcDecayFactor (_number_fadeoffs_):
    if _number_fadeoffs_ < 1 : 
        return 1.00
    else:
        return pow(0.5, 1.00/((float)(_number_fadeoffs_)))

# It takes the utc_time in 4 digit, and convert into total seconds from midnight    
def GetMSecsFromUTC(utc_time):
    hr = (int)(utc_time/100)
    mins = (int)(utc_time%100)
    secs = hr * 60 * 60 + mins *60
    return secs*1000

#return milli seconds from midnight
def GetMsecsFromEpoch(_tv_sec_, _tv_usec_):
    epoch_time = _tv_sec_ + float(_tv_usec_) / 1000000
    msecs = int(1000*(epoch_time - (int)(epoch_time)))
    t = time.gmtime(epoch_time)
    hr = t.tm_hour
    mins = t.tm_min
    secs = t.tm_sec
    total_secs = hr*60*60 + mins *60 + secs
    total_msecs = total_secs * 1000 + msecs
    return total_msecs