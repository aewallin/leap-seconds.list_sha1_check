
# utility for creating a leap-seconds.list file
# Anders Wallin (anders.e.e.wallin "at" gmail.com) 2017-12-20

import datetime as dt
import pytz
import sha

def ntp_timestamp(date):
    #t = datetime.datetime(date.year,date.month,date.day,
    #                    date.hour,date.minute,date.second,tzinfo=pytz.utc)
    #NTP leap-seconds.list wants seconds since 1900
    epoch_start = dt.datetime(1900,1,1,0,0,0,tzinfo=pytz.utc)
    delta = date-epoch_start
    delta_s = delta.total_seconds()
    return int(delta_s)

# when was the file updated?
update = dt.datetime(2016,7,8,tzinfo=pytz.utc)
# the leap-seconds
leap_seconds = [ (dt.datetime(1972,1,1, tzinfo=pytz.utc), 10),
                (dt.datetime(1972,7,1, tzinfo=pytz.utc), 11),
                (dt.datetime(1973,1,1, tzinfo=pytz.utc), 12),
                (dt.datetime(1974,1,1, tzinfo=pytz.utc), 13),
                (dt.datetime(1975,1,1, tzinfo=pytz.utc), 14),
                (dt.datetime(1976,1,1, tzinfo=pytz.utc), 15),
                (dt.datetime(1977,1,1, tzinfo=pytz.utc), 16),
                (dt.datetime(1978,1,1, tzinfo=pytz.utc), 17),
                (dt.datetime(1979,1,1, tzinfo=pytz.utc), 18),
                (dt.datetime(1980,1,1, tzinfo=pytz.utc), 19),
                (dt.datetime(1981,7,1, tzinfo=pytz.utc), 20),
                (dt.datetime(1982,7,1, tzinfo=pytz.utc), 21),
                (dt.datetime(1983,7,1, tzinfo=pytz.utc), 22),
                (dt.datetime(1985,7,1, tzinfo=pytz.utc), 23),
                (dt.datetime(1988,1,1, tzinfo=pytz.utc), 24),
                (dt.datetime(1990,1,1, tzinfo=pytz.utc), 25),
                (dt.datetime(1991,1,1, tzinfo=pytz.utc), 26),
                (dt.datetime(1992,7,1, tzinfo=pytz.utc), 27),
                (dt.datetime(1993,7,1, tzinfo=pytz.utc), 28),
                (dt.datetime(1994,7,1, tzinfo=pytz.utc), 29),
                (dt.datetime(1996,1,1, tzinfo=pytz.utc), 30),
                (dt.datetime(1997,7,1, tzinfo=pytz.utc), 31),
                 (dt.datetime(1999,1,1, tzinfo=pytz.utc), 32),
                 (dt.datetime(2006,1,1, tzinfo=pytz.utc), 33),
                 (dt.datetime(2009,1,1, tzinfo=pytz.utc), 34), 
                 (dt.datetime(2012,7,1, tzinfo=pytz.utc), 35),
                 (dt.datetime(2015,7,1, tzinfo=pytz.utc), 36),
                 (dt.datetime(2017,1,1, tzinfo=pytz.utc), 37),
                  ]
                  
# This program:
# #h	5101445a 69948b51 09153e2b 2086e3d8 d54561a3
# IETF file: (missing "0")
# #h	5101445a 69948b51  9153e2b 2086e3d8 d54561a3

# when does the file expire?
expires = dt.datetime(2018,06,28,tzinfo=pytz.utc)


if __name__ == "__main__":
    fname = "my_leap-seconds.list"
    s=sha.new()
    with open("my_leap-seconds.list","w") as f:
        f.write("# generated on %s\n" % dt.datetime.now())
        f.write("# this program/generator available from:\n")
        f.write("# https://github.com/aewallin/leap-seconds.list_sha1_check\n")
        f.write("# \n")
        f.write("# updated %s\n" % update)
        f.write("#$\t%d\n" % ntp_timestamp(update))
        f.write("# \n")
        f.write("# expires %s\n"%expires)
        f.write("#@\t%d\n" % ntp_timestamp(expires))
        f.write("# \n")
        s.update(str(ntp_timestamp(update)))
        s.update(str(ntp_timestamp(expires)))
        f.write("# Leap seconds\n")
        for l in leap_seconds:
            f.write( "%d\t%d\t# %04d-%02d-%02d\n"%( ntp_timestamp( l[0] ), l[1], l[0].year, l[0].month, l[0].day ) )
            s.update(str(ntp_timestamp( l[0] )))
            s.update(str(l[1]))
        sha1 = s.hexdigest()
        f.write("# \n")
        f.write("# SHA1 hash for this file: \n")
        f.write("#h\t"+sha1[0:8]+" "+
                      sha1[8:16]+" "+
                      sha1[16:24]+" "+
                      sha1[24:32]+" "+
                      sha1[32:40]+"\n"  )
        f.write("# end of file.\n")

# test that this generates OK values.
# from existing leap-seconds.list
# 2918937600    27    # 1 Jul 1992
# 2950473600    28    # 1 Jul 1993
# 2982009600    29    # 1 Jul 1994
# 3029443200    30    # 1 Jan 1996
# 3076704000    31    # 1 Jul 1997
# 3124137600    32    # 1 Jan 1999
# 3345062400    33    # 1 Jan 2006
# 3439756800    34    # 1 Jan 2009
