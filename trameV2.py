#-*-coding:utf-8-*-

class Trame:

    def __init__(self,packet,identifiant):
        self.poids=0
        self.id=identifiant
        print("Creating frame {}...".format(self.id))
        self.layers=packet.layers()
        self.protocol="Ethernet"
        print(self.layers)
        for i,layer in enumerate(self.layers):
            current_layer=layer.__name__

            #---------------------------- Verification functions / Upgrade functions ----------------------- 
            
            if(current_layer!="Ether" and i==0):
                print("First layer of frame {} is not ethernet -> need to be checked".format(identifiant))
            if(current_layer!="IP" and current_layer!="ARP" and i==1):
                print("Second layer of frame {} is not IP or ARP -> need an upgrade".format(self.id))
            
            # -----------------------------------------------------------------------------------------------
            
            functions_layer={
                "Ether" : self.setEthernetAttributs,
                "ARP" : self.setArpAttributs,
                "IP" : self.setIpAttributs,
                "UDP" : self.setUdpAttributs,
                "TCP" : self.setTcpAttributs,
                "Raw" : self.setRawAttributs,
                "Padding" : self.setPaddingAttributs,
                "DNS" : self.setDnsAttributs,
                "ICMP" : self.setIcmpAttributs,
                "BOOTP" : self.setDhcpAttributs,
                "DHCP" : self.doNothing,
            }

            functions_layer[current_layer](packet)
    def setEthernetAttributs(self,packet):
        self.mac_src=packet["Ethernet"].src
        self.mac_dst=packet["Ethernet"].dst
        self.type=packet["Ethernet"].type
    def setRawAttributs(self,packet):
        print("TO FINISH RAW")
        self.data=packet["Raw"].load
        if(self.data[1:3]==b'\x03\x03' or self.data[1:3]==b'\x03\x01'):
            self.setTlsAttributs(packet)
        elif(self.port_src==80 or self.port_dst==80):
            self.setHttpAttributs(packet)
        elif(self.port_src==23 or self.port_dst==23):
            self.setTelnetAttributs(packet)
        elif(self.port_src==22 or self.port_dst==22):
            self.setSshAttributs(packet)
        elif(self.port_src==443 or self.port_dst==443):
            self.setHttpsAttributs(packet)
        elif(self.port_src==21 or self.port_dst==21):
            self.setFtpAttributs(packet)
    def setDnsAttributs(self,packet):
        print("TODO DNS")
    def setFtpAttributs(self,packet):
        print("TODO FTP")
    def setFtpDataAttributs(self,packet):
        print("TODO FTP-Data")
    def setSshAttributs(self,packet):
        self.protocol="SSH"
    def setTelnetAttributs(self,packet):
        self.protocol="TELNET"
    def setPaddingAttributs(self,packet):
        print("TODO PADDING")
    def setDhcpAttributs(self,packet):
        self.protocol="DHCP"
        dhcp_options={
            1 : "Discover",
            2 : "Offer",
            3 : "Request",
            5 : "Ack",
        }
        try:
            self.option=dhcp_options[packet["DHCP options"].options[0][1]]
        except Exception as e:
            print("Frame {}".format(self.id))
            print("Error : {} | Value {} incorrect -> fill dict dhcp_options".format(e,packet["DHCP options"].options[0][1]))
    def setArpAttributs(self,packet):
        self.protocol="ARP"
        self.ip_src=packet[self.protocol].psrc
        self.ip_dst=packet[self.protocol].pdst
        arp_op={
                1 : "request",
                2 : "answer",
        }
        try:
            self.op=arp_op[packet[self.protocol].op]
        except Exception as e:
            print("Frame {}".format(self.id))
            print("Error : {} | Value {} incorrect -> fill dict arp_op".format(e,packet[self.protocol].op))

    def setIpAttributs(self,packet):
        self.protocol="IP"
        self.ip_src=packet["IP"].src
        self.ip_dst=packet["IP"].dst
        self.ip_len=packet["IP"].len


    def setUdpAttributs(self,packet):
        self.protocol="UDP"
        self.port_src=packet["UDP"].sport
        self.port_dst=packet["UDP"].dport
        self.udp_len=packet["UDP"].len

    def setTcpAttributs(self,packet):
        flags= {
            'F': 'FIN',
            'S': 'SYN',
            'R': 'RST',
            'P': 'PSH',
            'A': 'ACK',
            'U': 'URG',
            'E': 'ECE',
            'C': 'CWR',
        }
        self.protocol="TCP"
        self.port_src=packet["TCP"].sport
        self.port_dst=packet["TCP"].dport
        self.flags=[flags[x] for x in str(packet["TCP"].flags)]

    def setIcmpAttributs(self,packet):
        self.protocol="ICMP"
        icmp_types= {
            0 : "Reply",
            8: "Request",
        }
        try:
            self.icmp_type=icmp_types[packet["ICMP"].type]
        except Exception as e:
            print("Frame {}".format(self.id))
            print("Error : {} | Value {} incorrect -> fill dict icmp_types".format(e,packet["ICMP"].type))

    def setHttpAttributs(self,packet):
        self.protocol="HTTP"
        self.data=packet["Raw"].load
    def doNothing(self,packet):
        pass
