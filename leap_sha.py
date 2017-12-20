# leap-seconds.list SHA-1 checksum calculator
# Anders Wallin (anders.e.e.wallin "at" gmail.com) , 2017-12-20

import sha
# https://docs.python.org/2.3/lib/module-sha.html
import urllib2



url_list = [ "https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list",
             "ftp://tycho.usno.navy.mil/pub/ntp/leap-seconds.list",
            "https://www.ietf.org/timezones/data/leap-seconds.list",
             ]
#leap = 'leap-seconds_ietf.list'

def sha1_calc(leapsecfile):
    # given a leap-seconds.list file, parse it
    # and return both the old and a newly calculated SHA1
    s = sha.new()
    nlines=0
    for line in leapsecfile:
        nlines+=1
        if line.startswith('#$'): # last update time-stamp
            line = line.replace('\n','')
            line = line.replace('\t',' ')
            line = line.split() # separate #$ and number
            #print line
            #print "update: ",line[1]
            s.update(line[1])
        elif line.startswith('#@'): # expiration time-stamp
            line = line.replace('\n','')
            line=line.replace('\t',' ')
            line = line.split() # separate #$ and number
            #print "expire: ",line[1]
            s.update(line[1])
        elif line.startswith('#h'): # the SHA-1
            line=line.replace('\n','')
            line=line.replace('\t',' ')
            line=line.split(' ')
            line.pop(0) # remove the "#h"
            old_hash = "".join(line)
            #print "Old hash: ", old_hash
        elif line.startswith('#'): #comment
            pass
        else: # actual data
            line=line.split()
            s.update(line[0])
            s.update(line[1])
            #print line
    print "read ",nlines," lines"
    return (old_hash, s.hexdigest() )

def sha1_check(url):
    f = urllib2.urlopen(url)
    (old_hash, new_hash) = sha1_calc(f)

    print "New: ", new_hash
    print "Old: ", old_hash
    success = old_hash==new_hash
    print "Identical ? ", success
    print ""
    return success

for u in url_list:
    print u
    sha1_check(u)
