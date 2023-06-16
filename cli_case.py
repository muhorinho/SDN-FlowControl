from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.util import pmonitor

def add_flow_rule(switch, priority, match, actions):
    """
    Adding an OpenFlow flow rule to a specific switch
    """
    switch.dpctl(f"add-flow priority={priority},dl_dst={match},actions={actions}")

def main():
    # Creating of mininet and switches
    net = Mininet(controller=Controller, switch=OVSSwitch)
    c0 = net.addController("c0")
    s1 = net.addSwitch("s1")

    # Creating hosts
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")

    # Creating links
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    # Initializing Mininet
    net.start()

    # Adding OpenFlow rules to switches
    add_flow_rule(s1, 1, "00:00:00:00:00:01", "output:1")
    add_flow_rule(s1, 1, "00:00:00:00:00:02", "output:2")

    # CLI Case: Traffic generation and disconnection
    # Pinging from h1 to h2 to generate traffic
    h1.cmd("ping -c 5 10.0.0.2")

    # To disconnect, we set the connection on the s1 switch to the down state
    s1.cmd("ifconfig s1-eth1 down")

    # CLI Case: Analyzing the behavior of controls
    # Wireshark ile OpenFlow mesajlarını izleme
    p = pmonitor(s1)
    for host, line in p:
        if "OFPT_PACKET_IN" in line:
            print(f"OFPT_PACKET_IN: {line}")

    # Initializing Mininet CLI
    CLI(net)

    # Mininet termination
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    main()
