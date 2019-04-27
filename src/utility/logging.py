import datetime
import math

TIME_START = datetime.datetime.now()
TIME_SOFAR = datetime.datetime.now()

def getTime():
    global TIME_START
    return (datetime.datetime.now()-TIME_START)

def processing(name):
    global TIME_SOFAR
    TIME_SOFAR = datetime.datetime.now()
    print("%s\t%s..." % (getTime(),name))

def starting():
    print("%s\tProgram Starting" % (getTime()))

def ending():
    print("%s\tProgram Exiting" % (getTime()))

def sofar(name,count,total,numberOfMessages):
    mod = math.ceil(total/numberOfMessages)
    if (mod != 0 and count % mod == mod-1) or (count+1 == total):
        global TIME_SOFAR
        countReal = count
        amt2go = total-countReal
        ttp = datetime.datetime.now()-TIME_SOFAR
        eta = datetime.timedelta(0,ttp.total_seconds()*(amt2go/mod))
        fin = datetime.datetime.now()+eta
        perc = (float(countReal)+1)/float(total)*100
        print("%s\t\t%s...\t%2d/%2d %3.2f%%\tETA %s @ %s" % (getTime(),name,countReal,total,perc,eta,fin))
        TIME_SOFAR = datetime.datetime.now()

def info(s):
    print("%s\t%s" % (getTime(),s))