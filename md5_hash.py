import sys
import hashlib
#save as md5_study.py
 
def md5(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print ("Reading file has problem:", fileName)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest().upper()
 
if __name__ == "__main__":
    for eachFile in sys.argv[1:]:
        print ("%s %s" % (md5(eachFile), eachFile))