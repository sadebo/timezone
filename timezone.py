#!/usr/bin/env python3
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import datetime
import pytz
from pytz import timezone
from dateutil import parser
 
def getNTPTime(host = "pool.ntp.org"):
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'
 
        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800L # 1970-01-01 00:00:00
 
        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg, address)
        msg, address = client.recvfrom( buf )
 
        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970
        now = time.asctime(time.gmtime(t))
        #datetime_obj = datetime.datetime.strptime(now, "%a %b %d %H:%M:%S %Y")
        #return datetime_obj
       # return now
        return t
#        return time.ctime(t).replace("  "," ")
 
if __name__ == "__main__":
        final_time =  getNTPTime()
        utc_time = datetime.datetime.fromtimestamp(final_time, pytz.utc)
        utc_time_zone = utc_time.astimezone(timezone('US/Eastern'))
        # utc_time_zone1 = utc_time_zone.strftime("%B")
        # utc_time_zone = time.ctime(utc_time.astimezone(timezone('US/Eastern')))
        fmt = '%Y-%m-%d %H:%M:%S%z'
        datetime_obj = datetime.datetime.strptime('utc_time_zone',fmt)
        #parsed_date = parser.parse(utc_time_zone)
        print parsed_date
