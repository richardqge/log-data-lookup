import csv
from collections import defaultdict


def load_lookup_table(lookup_file):
    # Load the lookup table from a CSV file into a dictionary
    lookup_dict = {}
    with open(lookup_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            dstport, protocol, tag = row[0].strip(
            ), row[1].strip().lower(), row[2].strip()
            # map tuple to tag
            lookup_dict[(dstport, protocol)] = tag
    return lookup_dict


def parse_flow_log(flow_log_file, lookup_dict):
    # Parse flow log and generate counts
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    tag_counts['Untagged'] = 0  # Init 'Untagged' count

    # set up Protocol mapping for 'tcp', 'udp', 'icmp'
    protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}

    with open(flow_log_file, 'r') as file:
        for line in file:
            parts = line.split()

            # Edge case: skip lines that don't have enogh parts to avoid breaking the code
            if len(parts) < 8:
                continue

            dstport = parts[5].strip()
            protocol_num = parts[7].strip()
            protocol = protocol_map.get(protocol_num, 'unknown')

            # Edge case: add a warning if unknown protocol
            if protocol == 'unknown':
                print(
                    f"Warning: Unknown protocol number '{protocol_num}' in line: {line.strip()}")

            # Get the tag or default to 'Untagged'
            tag = lookup_dict.get((dstport, protocol), 'Untagged')

            # Update counts
            tag_counts[tag] += 1
            port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts


def write_output(tag_counts, port_protocol_counts, output_file):
    # Write the tag and port/protocol counts to a file
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\nTag,Count\n")

        # Sort tags: all others alphabetically, then 'email', then 'Untagged'
        sorted_tags = sorted(tag_counts.keys(), key=lambda x: (
            x == 'Untagged', x == 'email', x))

        for tag in sorted_tags:
            file.write(f"{tag},{tag_counts[tag]}\n")

        # Write sorted port/protocol counts
        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")

        # Sort by port (numeric sort) and then by protocol
        sorted_port_protocol = sorted(
            port_protocol_counts.items(), key=lambda x: (int(x[0][0]), x[0][1]))

        for (port, protocol), count in sorted_port_protocol:
            file.write(f"{port},{protocol},{count}\n")


def main():
    lookup_file = 'lookup.csv'
    flow_log_file = 'flow_log.txt'
    output_file = 'output.txt'

    # Load lookup table
    lookup_dict = load_lookup_table(lookup_file)

    # Parse logs
    tag_counts, port_protocol_counts = parse_flow_log(
        flow_log_file, lookup_dict)

    # Write results
    write_output(tag_counts, port_protocol_counts,
                 output_file)


if __name__ == "__main__":
    main()
