import unittest
from log_data_lookup import load_lookup_table, parse_flow_log, write_output
from collections import defaultdict
import os


class TestLogDataLookup(unittest.TestCase):

    def setUp(self):
        # Set up paths for test files
        self.lookup_file = 'test_lookup.csv'
        self.flow_log_file = 'test_flow_log.txt'
        self.output_file = 'test_output.txt'

        # Create lookup table sample data
        with open(self.lookup_file, 'w') as f:
            f.write("dstport,protocol,tag\n")
            f.write("25,tcp,sv_P1\n")
            f.write("68,udp,sv_P2\n")
            f.write("23,tcp,sv_P1\n")
            f.write("443,tcp,sv_P2\n")
            f.write("22,tcp,sv_P4\n")
            f.write("110,tcp,email\n")
            f.write("993,tcp,email\n")

        # Create flow log sample data
        with open(self.flow_log_file, 'w') as f:
            f.write(
                "2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
            f.write(
                "2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK\n")
            f.write(
                "2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK\n")
            f.write(
                "2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK\n")
            f.write(
                "2 123456789012 eni-7i8j9k0l 172.16.0.101 192.0.2.203 993 49157 6 8 5000 1620140761 1620140821 ACCEPT OK\n")

    def test_load_lookup_table(self):
        # Load lookup table and verify it matches expected dictionary
        lookup_dict = load_lookup_table(self.lookup_file)
        expected_dict = {
            ('25', 'tcp'): 'sv_P1',
            # Edge case: this won't match in logs, used to verify handling case
            ('68', 'udp'): 'sv_P2',
            ('23', 'tcp'): 'sv_P1',
            ('443', 'tcp'): 'sv_P2',
            ('22', 'tcp'): 'sv_P4',
            ('110', 'tcp'): 'email',
            ('993', 'tcp'): 'email'
        }
        self.assertEqual(lookup_dict, expected_dict)

    def test_parse_flow_log(self):
        # Parse flow logs and verify counts
        lookup_dict = load_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_log(
            self.flow_log_file, lookup_dict)

        # Verify: tag counts
        expected_tag_counts = {
            'sv_P2': 1,
            'sv_P1': 2,
            'email': 2,
            'Untagged': 0
        }

        # Verify: port/protocol combination counts
        expected_port_protocol_counts = {
            ('443', 'tcp'): 1,
            ('23', 'tcp'): 1,
            ('25', 'tcp'): 1,
            ('110', 'tcp'): 1,
            ('993', 'tcp'): 1
        }

        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)

    def test_write_output(self):
        # Generate output and compare it to the expected content
        lookup_dict = load_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_log(
            self.flow_log_file, lookup_dict)
        write_output(tag_counts, port_protocol_counts, self.output_file)

        # Read generated output and verify correct
        with open(self.output_file, 'r') as f:
            output_content = f.read()

        # Expect output sorted correctly (caveat: with email before Untagged at end of list)
        expected_output = """Tag Counts:
Tag,Count
sv_P1,2
sv_P2,1
email,2
Untagged,0

Port/Protocol Combination Counts:
Port,Protocol,Count
23,tcp,1
25,tcp,1
110,tcp,1
443,tcp,1
993,tcp,1
"""

        # Validate output matches expected output
        self.assertEqual(output_content, expected_output)

    def tearDown(self):
        # Clean up
        os.remove(self.lookup_file)
        os.remove(self.flow_log_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)


if __name__ == '__main__':
    unittest.main()
