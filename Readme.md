# Flow Log Parser with Tag Lookup

## Overview

This program parses AWS flow logs and assigns tags to each log entry based on a lookup table (`lookup.csv`). The tags are applied based on the destination port (`dstport`) and protocol (`tcp`, `udp`, `icmp`, `igmp`) combination, as defined in the CSV lookup table. The program also generates counts for each tag and the combinations of port/protocol seen in the flow logs.

## Assumptions

- **Flow Log Version**: The program only supports **Version 2** of the flow log format.

- **Log Format**: The program supports default AWS flow logs. Custom log formats are not supported.

- **Log Fields**: This program expects a flow log entry to have the following structure:

**Syntax**:
  ```plaintext
  version account-id eni srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status 
  ```
   
Sample: 
```
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
```

- **Supported Protocols**: The program supports the following protocols:
  
  - `tcp` for protocol number `6`
  - `udp` for protocol number `17`
  - `icmp` for protocol number `1`
  - `igmp` for protocol number `2`

- **Tagging Logic**: **Tags are applied based on the destination port and protocol combination only.** Source ports are counted in combination with protocols but do not affect the tagging.

- **Case Insensitivity**: The lookup of tags is case insensitive.

- **Default Tag**: If no matching port/protocol combination is found in the lookup table, the entry is tagged as **"Untagged"**.

## Input Files

- **Flow Log File (`flowlogs.txt`)**: Contains the flow logs in the default format, with Version 2 as the log version. For manual verification, I took 30 records for analysis purposes. The design can be scaled to handle larger datasets by optimizing memory usage, but the current program is sufficient for the scope outlined (default flow logs).

- **Lookup Table (`lookup.csv`)**: Contains the mapping of destination port and protocol combinations to corresponding tags. I have used up to 40 records for `dstport` mappings, and these ports have also been considered for `srcport` when counting port/protocol combinations.

- **Code File (`illumio.py`)**: This Python script contains the logic to parse the flow logs, apply tags based on the lookup table, and generate the output file. Ensure that `illumio.py` is placed in the same directory as `flowlogs.txt` and `lookup.csv` to execute the program.

## Output

The program generates an `output.txt` file containing two sections:

1. **Tag Counts**: This lists the number of occurrences for each tag based on the destination port/protocol combinations.
   ```
    Tag,Count
    Untagged,20
    web,1
    sv_P2,1
    sv_P1,3
    email,3
    ftp,1
    snmp,1
    ```

2. **Port/Protocol Combination Counts**: This lists the number of occurrences of each port/protocol combination from both the source and destination ports.
    ```
    Port,Protocol,Count
    49153,tcp,4
    443,tcp,3
    49154,tcp,5
    23,tcp,4
    49155,tcp,2
    25,tcp,3
    49156,tcp,2
    110,tcp,3
    49157,tcp,2
    993,tcp,3
    49158,tcp,1
    143,tcp,3
    80,tcp,4
    1024,tcp,4
    1030,tcp,1
    56000,tcp,1
    49321,tcp,1
    49152,tcp,1
    49154,udp,1
    53,udp,2
    21,tcp,1
    3389,tcp,1
    12345,udp,2
    67,udp,1
    445,tcp,1
    123,igmp,2
    161,igmp,2
    ```

## Instructions to Run the Program

1. **Clone the repository**: In your terminal clone my repository:
```
git clone https://github.com/Nikhil010301/illumioassessment.git
```

2. **Place your input files**: Ensure that `flowlogs.txt` (flow log file), `lookup.csv` (lookup table), and `Illumio.py` (Python script) are present in the same directory. When you give your own csv and txt files, make sure you change the name of the files to `flowlogs.txt` and `lookup.csv`.

3. **Run the Python script**: Run the program in terminal:
```
python illumio.py
```
4. **Output**: The program will generate an `output.txt` file in the same directory, containing the tag counts and port/protocol combination counts.


## Tests

### Test 1: Basic Functionality
Tested with a standard `flowlogs.txt` log file containing a variety of port/protocol combinations that are mapped to the tags in the `lookup.csv` file.  
**Expected Output**: Verified that the tag counts and port/protocol counts match the expected values based on the lookup table.

### Test 2: Untagged Entries
Tested with entries in the `flowlogs.txt` file that contain ports and protocols not found in the `lookup.csv`.  
**Expected Output**: These entries are tagged as **"Untagged"**.

### Test 3: Mixed Protocols
Tested with TCP, UDP, ICMP, and IGMP protocols in the log file.  
**Expected Output**: Tags are correctly applied based on the respective protocol and port combinations from the `lookup.csv` table.
