# method to handle output
def packet_handler(packet_split, out):
    if out == "deny":
        print("Packet from " + packet_split[0] + " to " +
              packet_split[1] + " on port " + packet_split[2] + " denied.")
    else:
        print("Packet from " + packet_split[0] + " to " +
              packet_split[1] + " on port " + packet_split[2] + " permitted.")


def main():

    acl_rules = []
    f_acls = open("ext_acls.txt", "r")
    f_packets = open("ext_packets.txt", "r")

    # populate rule array
    for in_acl in f_acls:
        # only need lines before interface statement
        if not in_acl.startswith("interface"):
            # only take in needed information from ACL lines, split for easier manipulation
            # in_acl.split()[2:] = only the permit/deny statement and beyond
            acl_rules.append(in_acl.split()[2:])
            # now, [0] = permit/deny,[1] = dest address, [2] = desk mask, [3] = src address, [4] = src mask,
            # [5] = "range" (if present) followed by port range in [6] OR [5] = "eq" followed by specific port in [6]
            for i in range(2, 6):
                acl_rules[-1][i] = acl_rules[-1][i].split(".")
            if "range" in acl_rules[-1]:
                acl_rules[-1][-1] = acl_rules[-1][-1].split("-")
            # shorten addresses to only what we need to check
            while "255" in acl_rules[-1][3]:
                acl_rules[-1][2].pop()
                acl_rules[-1][3].pop()
            while "255" in acl_rules[-1][5]:
                acl_rules[-1][4].pop()
                acl_rules[-1][5].pop()
        else:
            break

    f_acls.close()

    # compare packets and destinations to rules
    for in_packet in f_packets:
        in_packet = in_packet.rstrip("\n")
        # flag for if packet matched a rule
        handled = False
        for rule in acl_rules:
            # split packet and destination, shorten them only positions needed to be checked
            in_packet_split = in_packet.split(" ")
            in_packet_split[0] = in_packet_split[0].split(".")
            in_packet_split[1] = in_packet_split[1].split(".")
            while len(in_packet_split[0]) != len(rule[2]):
                in_packet_split[0].pop()
            while len(in_packet_split[1]) != len(rule[4]):
                in_packet_split[1].pop()
            # if rule matched to packet and destination, handle it
            if in_packet_split[0] == rule[2] and in_packet_split[1] == rule[4]:
                # check for lone port
                if "eq" in rule:
                    if int(in_packet_split[2]) == int(rule[-1]):
                        packet_handler(in_packet.split(), rule[0])
                        handled = True
                        break
                    else:
                        continue
                # check for port range
                if "range" in rule:
                    if int(in_packet_split[2]) in range(int(rule[-1][0]), int(rule[-1][1]) + 1):
                        packet_handler(in_packet.split(), rule[0])
                        handled = True
                        break
                    else:
                        continue
                # handle for no ports matched
                packet_handler(in_packet.split(), rule[0])
                handled = True
                break
        # if no rule was matched to packet and destination, deny it by default
        if not handled:
            packet_handler(in_packet.split(), "deny")

    f_packets.close()


# invoke main method
if __name__ == "__main__":
    main()
