
import sys
import pygeoip
import dpkt
import socket
import time
import webbrowser

# These dictionaries are used for key-value pairs. Keys are IP addresses, and values are lat-long positions
source_ips = {}
destination_ips = {}

blacklisted_ips = ['217.168.1.2', '192.37.115.0', '212.242.33.35', '147.137.21.94']

# This dictionary is used for keeping the record of authorized users.
auth_users = {"root": "root", "soumil": "soumil"}

def geoip_city(ip_address):
    if ip_address in blacklisted_ips:
        path = '/home/soumil/build/geoip/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(path)
        try:
            record = gic.record_by_addr(ip_address)
            print("\n[*] Target: {} Geo Located.".format(ip_address))
            print("\n[+] City: {}, Region: {}, Country: {}".format(record['city'], record['region_code'], record['country_name']))
            print("\n[+] Latitude: {}, Longitude: {}".format(record['latitude'], record['longitude']))
        except Exception as e:
            print("\n********** IP Unregistered **********")
    else:
        pass

def kml_geoip_city(ip_address):
    if ip_address in blacklisted_ips:
        path = '/home/soumil/build/geoip/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(path)
        try:
            record = gic.record_by_addr(ip_address)
            source_ips[ip_address] = "{},{}".format(record['latitude'], record['longitude'])
        except Exception as e:
            pass
    else:
        pass

def kml_dest_geoip_city(ip_address):
    if ip_address in blacklisted_ips:
        path = '/home/soumil/build/geoip/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(path)
        try:
            record = gic.record_by_addr(ip_address)
            destination_ips[ip_address] = "{},{}".format(record['latitude'], record['longitude'])
        except Exception as e:
            pass
    else:
        pass

def printpcap(pcap):
    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            if src in blacklisted_ips:
                print("-------------------------------------------------------------------------------------------------")
                print('[+] Source IP: {} ------>  Destination IP: {}'.format(src, dst))
                print("Source IP Information:")
                geoip_city(src)
            elif dst in blacklisted_ips:
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-")
                print("Destination IP Information:")
                geoip_city(dst)
                print("--------------------------------------------------------------------------------------------------")
            else:
                pass
        except Exception as e:
            pass

def view_google(pcap):
    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            kml_geoip_city(src)
            kml_dest_geoip_city(dst)
        except Exception as e:
            pass

def print_placemarks_in_kml(ip_dict, address_type):
    for ip, coordinates in ip_dict.items():
        print("""
    <Placemark>
        <name> {} IP Address: {}</name>
        <styleUrl>#exampleStyleDocument</styleUrl>
        <Point>
            <coordinates>{}</coordinates>
        </Point>
    </Placemark>
    """.format(address_type, ip, coordinates))

def main():
    if len(sys.argv) < 4:
        print("\n -------------------- Please enter the required arguments------------------------- ")
        print("\n Correct syntax is : <FileName>.py username password cli/kml\n")
        print("\ncli- stands for Command Line Output")
        print("\nkml- stands for a KML output which is required for visualization using a Google Map")
    else:
        try:
            username = sys.argv[1]
            if username in auth_users:
                try:
                    password = sys.argv[2]
                    if password == auth_users[username]:
                        try:
                            output_type = sys.argv[3]
                            if output_type == "cli" or output_type == "kml":
                                if output_type == "cli":
                                    with open('/home/soumil/Downloads/fuzz-2006-06-26-2594.pcap') as f:
                                        pcap = dpkt.pcap.Reader(f)
                                        printpcap(pcap)
                                elif output_type == "kml":
                                    print("""
                                <?xml version="1.0" encoding="UTF-8"?>
                                <kml xmlns="http://www.opengis.net/kml/2.2">
                                <Document>
                                    <name>sourceip.kml</name>
                                    <open>1</open>
                                    <Style id="exampleStyleDocument">
                                        <LabelStyle>
                                            <color>ff0000cc</color>
                                        </LabelStyle>
                                    </Style>\n""")
                                    with open('/home/soumil/Downloads/fuzz-2006-06-26-2594.pcap') as f:
                                        pcap = dpkt.pcap.Reader(f)
                                        view_google(pcap)
                                    print_dest_placemarks_in_kml(destination_ips)
                                    print_placemarks_in_kml(source_ips, "SOURCE")
                                    print("""\n
                                </Document>
                                </kml>
                                """)
                                    new = 1
                                    url = "https://www.google.com/maps/d/splash?app=mp"
                                    webbrowser.open(url, new=new)
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        except ValueError:
                            print("\nYou Entered a wrong option. Or maybe your Syntax is wrong")
                            print("\n Correct syntax is : <FileName>.py username password cli/kml\n")
                            print("\ncli- stands for Command Line Output")
                            print("\nkml- stands for a KML output which is required for visualization using a Google Map")
                    else:
                        raise ValueError
                except ValueError:
                    print("\nThe PASSWORD you entered is NOT CORRECT !!!!!! ")
                    print("\n Correct syntax is : <FileName>.py username password cli/kml\n")
                    print("\ncli- stands for Command Line Output")
                    print("\nkml- stands for a KML output which is required for visualization using a Google Map")
            else:
                raise ValueError
        except ValueError:
            print("\nSorry %s. You are NOT AUTHORIZED to use this tool!!!!!!!!!!!" % username)
            print("\nCorrect syntax is : <FileName>.py username password cli/kml\n")
            print("\ncli- stands for Command Line Output")
            print("\nkml- stands for a KML output which is required for visualization using a Google Map")

if __name__ == "__main__":
    main()
