# Log Data Lookup Utility

## Overview

The objective of this script is to parse network flow logs and assign a tag to each log entry based on the (dstport,protocol) using a hashmap. The output includes a summary list of the counts of each tag and the counts of each port/protocol combination found in the logs.

## Features

- **Load Lookup Table**: Reads a CSV file containing port, protocol, and tag mappings.
- **Parse Flow Logs**: Analyzes flow log data logto categorize entries based on the lookup table.
- **Generate Output**: Produces a txt file with headers and values for tag counts and port/protocol combinations.
- **Handles Case Insensitivity**: Matches are case insensitive.

## Input Requirements

1. **Flow Log File (`flow_log.txt`)**:

   - A text file containing network flow log entries in AWS flow logs format.
   - Each log entry can include fields like version, account-id, interface-id, srcaddr, dstaddr, ports, protocol number, packets, etc..
   - i.e.:
     ```
     2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
     2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK
     ```

2. **Lookup Table File (`lookup.csv`)**:
   - A CSV file with three columns: `dstport`, `protocol`, and `tag`.
   - i.e.:
     ```csv
     dstport,protocol,tag
     25,tcp,sv_P1
     68,udp,sv_P2
     23,tcp,sv_P1
     443,tcp,sv_P2
     22,tcp,sv_P4
     110,tcp,email
     993,tcp,email
     143,tcp,email
     ```

## Expected Output

The script generates an output file (`output.txt`) containing:

1. **Tag Counts**: Number of occurrences for each tag.
2. **Port/Protocol Combination Counts**: Number of occurrences for each port and protocol combination.

### Example Output

```Tag Counts:
Tag,Count
sv_P1,2
sv_P2,1
sv_P4,1
email,3
Untagged,8

Port/Protocol Combination Counts:
Port,Protocol,Count
22,tcp,1
23,tcp,1
25,tcp,1
80,tcp,1
110,tcp,1
143,tcp,1
443,tcp,1
993,tcp,1
1024,tcp,1
1030,tcp,1
49152,tcp,1
49153,tcp,1
49154,tcp,1
49321,tcp,1
56000,tcp,1
```

## Instructions

1. **Prepare Input Files**:

   - **`lookup.csv`**: Create/load a CSV file with the columns `dstport`, `protocol`, and `tag`.
   - **`flow_log.txt`**: Create/load a text file with your network flow log data.

2. **Run the Script**:

   In the directory with `log_data_lookup.py`. Run:

   ```bash
   python log_data_lookup.py
   ```

After running the script, you will get an output.txt file in the same directory.

## Testing

1. **Unit tests are provided as an additional feature**:

   - **`test_log_data_lookup.py`**

2. **Run the Tests**:

```bash
python test_log_data_lookup.py
```

The tests will check if the script is loading the lookup table correctly, parsing the flow logs, and generating the expected output.

### Acknowledgements

Created by Richard Q. Ge (@richardqge). Licensed under the MIT license.
