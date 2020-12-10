# This are the various packages that are used throughout the program
import ipaddress
import sys
# Function to check if the address provided is a valid ip address
def validIPAddress(IP):
    def isIPv4(s):
        try:
            return str(int(s)) == s and 0 <= int(s) <= 255
        except:
            return False

    def isIPv6(s):
        if len(s) > 4:
            return False
        try:
            return int(s, 16) >= 0 and s[0] != '-'
        except:
            return False

    if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
        return "IPv4"
    elif IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
        return "IPv6"
    else:
        return False


# Function to split the string values of ip and mask by '.'

def split_ip_mask(ip, mask):
    return ip.split('.'), mask.split('.')

# Function to convert value of ip address to binary

def convert_ip_to_binary(ip):
    ip = [int(bin(int(octet)), 2) for octet in ip]
    return ip

# Function to convert value of mask address to binary

def convert_mask_to_binary(mask):
    return [int(bin(int(octet)), 2) for octet in mask]

# Function to calculate the subnet value of ip and mask value that you input

def calculate_subnet(ip, mask):
    return [str(int(bin(ioctet & moctet), 2)) for ioctet, moctet in zip(ip, mask)]

# Function to calculate the host value from ip and mask value

def calculate_host(ip, mask):
    return [str(int(bin(ioctet & ~moctet), 2)) for ioctet, moctet in zip(ip, mask)]

# Function to calculate the broadcast value from ip value and msk


def calculate_broadcast(ip, mask):
    net=ipaddress.IPv4Network(ip+'/'+mask,False)
    return net.broadcast_address

# The main function that call all the other functions
def get_ID(ip, mask):
    ip, mask = split_ip_mask(ip, mask)

    ip = convert_ip_to_binary(ip)

    mask = convert_mask_to_binary(mask)
    subnet = calculate_subnet(ip, mask)
    host = calculate_host(ip, mask)
    broadcast = calculate_broadcast(ip, mask)
    print('Subnet: {0}'.format('.'.join(subnet)))
    print('Host: {0}'.format('.'.join(host)))
    print('Broadcast address: {0}'.format('.'.join(broadcast)))

# Getting the user input from the console
try:
    ip = sys.argv[1]
    mask = sys.argv[2]
    hex=sys.argv[-1]
    if hex=='hex':
        hex=True


    if validIPAddress(ip) == False:
        print('The ip address you passed is not a valid ip address')
    else:
        get_ID(ip, mask)
except Exception:
    print('You did not provide the required arguments')





