class RoutingTableEntry:
    # class for routing table entires
    def __init__(self, destination, next_hop, interface) -> None:
        self.destination = destination
        self.next_hop = next_hop
        self.interface = interface
        if self.next_hop == '-':
            self.out = (" will be forwarded on the directly connected network interface "
                        + interface + ".\n")
        else:
            self.out = (" will be forwarded to " + next_hop + " on interface "
                        + interface + ".\n")


# populate routing table by reading in RoutingTable.txt
with open("RoutingTable.txt") as f_routing:
    lines = [line.rstrip('\n') for line in f_routing]
f_routing.close()

i = 0
routing_table = []
while i < len(lines):
    table_entry = RoutingTableEntry(
        # split destination entries and convert to int for easier comaparison
        [int(x) for x in lines[i].split('/')[0].split('.')], lines[i+1], lines[i+2])
    # bring host-specific entires to top of routing table to compare first
    if table_entry.destination[3] != 0:
        routing_table.insert(0, table_entry)
    else:
        routing_table.append(table_entry)
    i += 3

# read in RandomPackets.txt
packets = []
with open('RandomPackets.txt') as f_packets:
    packets = [packet.rstrip('\n') for packet in f_packets]
f_packets.close()

with open("RoutingOutput.txt", 'w') as f_output:
    for packet in packets:
        # split packets and cast to int for easier comaparisons
        packet_split = [int(x) for x in packet.split('.')]
        # handle loopback and malformed packets
        if packet_split[0] == 127:
            f_output.write(packet + " is loopback; discarded.\n")
            continue
        elif packet_split[0] > 223:
            f_output.write(packet + " is malformed; discarded.\n")
            continue
        # compare packets with each entry in the routing table
        for entry in routing_table:
            # host-specific forwarding
            if packet_split == entry.destination:
                f_output.write(packet + entry.out)
                break
            # network forwarding
            if packet_split[0] == entry.destination[0] and packet_split[1] == entry.destination[1] and packet_split[2] == entry.destination[2]:
                f_output.write(packet + entry.out)
                break
            # default forwarding
            elif entry.destination[0] == 0:
                f_output.write(packet + entry.out)
                break

f_output.close()
