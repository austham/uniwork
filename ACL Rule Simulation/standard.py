# method to handle output
def packet_handler(packet, out):
    if out == "deny":
        print("Packet from " + packet + " denied.")
    else:
        print("Packet from " + packet + " permitted.")


def main():
    # create array for rules, read in txt files
    acl_rules = []
    f_acls = open("std_acls.txt", "r")
    f_packets = open("std_packets.txt", "r")

    # populate rule array
    for in_acl in f_acls:
        # only need lines before interface statement
        if not in_acl.startswith("interface"):
            # only take in needed information from ACL lines, split for easier manipulation
            # in_acl.split()[2:] = only the permit/deny statement and beyond
            acl_rules.append(in_acl.split()[2:])
            # now, [0] = permit/deny,[1] = dest address, [2] = mask
            acl_rules[-1][1] = acl_rules[-1][1].split(".")
            acl_rules[-1][2] = acl_rules[-1][2].split(".")
            # shorten addresses to only what we need to check based on mask
            while "255" in acl_rules[-1][2]:
                acl_rules[-1][1].pop()
                acl_rules[-1][2].pop()
        else:
            break

    f_acls.close()

    # compare packets to rules
    for in_packet in f_packets:
        in_packet = in_packet.rstrip("\n")
        # flag for if packet matched a rule
        handled = False
        for rule in acl_rules:
            # split packet and shorten to only positions needed to be checked based on len of address in rule
            in_packet_split = in_packet.split(".")
            while len(in_packet_split) != len(rule[1]):
                in_packet_split.pop()
            # if rule matched to packet, handle it
            if in_packet_split == rule[1]:
                packet_handler(in_packet, rule[0])
                handled = True
                break
        # if no rule was matched to packet, deny it by default
        if not handled:
            packet_handler(in_packet, "deny")

    f_packets.close()


# invoke main method
if __name__ == "__main__":
    main()
