#!/usr/bin/env python3
import sys
import ipaddress
from datetime import datetime

# my_ipaddress = int(input("Please enter the IP Address and Subnet(x.x.x.x/x): "))
#Define variables that would be part of the reverse zone file
host = "sanu.com."
name_server = "ns1.sanu.com."
administrator= "administrator.sanu.com."
zone_serial = datetime.now().strftime("%Y%m%d%H%M%S")
slave_refresh_interval = "1h"
slave_retry_interval = "15m"
slave_expiration_time = "1w"
nxdomain_cache_time = "1h"
record_ttl = "3600s"

#Function to define ipadresses, subnet,wildcard,broadcast
def ip_calc(my_ipaddress):
    try:
        ip = ipaddress.IPv4Network(my_ipaddress, strict=False)
        #get the first octet for example in 172.16.1.0/28.. the first octet will be 172
        my_first_octet = int(str(ip).split('.')[0])
        #define a variable to print the result of each test
        my_class = ""
        if my_first_octet == 0:
            return print("This is probably a source IP, RFC 1122")
        elif my_first_octet >= 1 and my_first_octet <= 126:
            my_class = "CLASS A - ip range 1 - 126"
        elif my_first_octet == 127:
            return print ("This is a loopback IP address")
        elif my_first_octet >= 128 and my_first_octet <= 191:
            my_class = "CLASS B - ip range 128 - 191"
        elif my_first_octet >= 192 and my_first_octet <= 223:
            my_class = "CLASS C - ip range 192 - 223"
        elif my_first_octet >= 224 and my_first_octet <= 239 :
            my_class = "CLASS D - ip range 224 - 239"
        else:
            return print("CLASS E ")
    except ipaddress.AddressValueError:
        return print("Invalid IP Address, please check the IP address part of your entry")
    except ipaddress.NetmaskValueError:
        return print("Invalid Subnet Mask,please check the subnet mask part of youyr entry")

    if ip.is_private:
        print("This is a private IP")
    
    subnet = (ip.with_netmask).split('/')[1]
    wildcard = []
    for x in subnet.split('.'):
        component = 255 - int(x)
        wildcard.append(str(component))
    wildcard = '.'.join(wildcard)

    #Print the result of function 
    print(f'The IP address and the subnet mask is  {ip.with_netmask}')
    print(f'This subnet {subnet} when converted to wildcard is: {wildcard}')
    print(f'The number of host bits is: {ip.num_addresses -2}')
    print(f'The Network address class is {my_class}')
    print(f'The First IP assignable for a host is {ip.network_address +1}and in binary format it is {bin(int(ip.network_address +1))} and in hexadecimal {hex(int(ip.network_address +1))}') 
    print(f'The last IP assignable to a host is {ip.broadcast_address -1} and in binary it is {bin(int(ip.broadcast_address -1))} and in hexadecimal {hex(int(ip.broadcast_address -1))}')
    print(f'The network address is {ip.network_address} and in binary format it is {bin(int(ip.broadcast_address -1))} and in hexadecimal{hex(int(ip.network_address))}')
    print(f'The Broadcast address is {ip.broadcast_address} and in binary format it is {bin(int(ip.broadcast_address))} and in hexadecimal {hex(int(ip.broadcast_address))}') 
    
    
    #Print reverse zone file

    print("; Reverse file built by Sanu Adebo:")
   

    print("$TTL %s	; Default TTL" % record_ttl )

    print("@	IN	SOA	%s	%s (" % (name_server, administrator) )
    print("	%s	; serial" % zone_serial)
    print("	%s	; slave refresh interval" % slave_refresh_interval)
    print("	%s	; slave retry interval" % slave_retry_interval)
    print("	%s	; slave copy expire time" % slave_expiration_time)
    print("	%s	; NXDOMAIN cache time" % nxdomain_cache_time)
    print("	)")
    for i in range(1,ip.num_addresses -1):
        print(f'{i} IN    PTR  host{i}.{host}')
# def wildcard_conversion(subnet):
#     subnet = (ip.with_netmask).split('/')[1]
#     wildcard = []
#     for x in subnet.split('.'):
#         component = 255 - int(x)
#         wildcard.append(str(component))
#     wildcard = '.'.join(wildcard)
#     return wildcard

ip_calc(my_ipaddress = str(input("Please enter the IP Address and Subnet(x.x.x.x/x): ")))

# def main():
#     ip_calc('192.168.1.0/24')


# if __name__ == ('__main__'):
#     main()