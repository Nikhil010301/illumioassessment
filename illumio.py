# storing lookup table
lookup = {}
# storing counts for tags and port/protocol combinations
count_tag = {}
count_combination = {}

# Reading the lookup table from CSV
with open('lookup.csv', 'r') as file:
    data = file.readlines()

# Parsing the lookup CSV and store the mapping
for line in data[1:]:
    row = line.strip().split(',')
    port_protocol = f"{row[0]}{row[1].lower()}"  # dstport and protocol combination
    lookup[port_protocol] = row[2]

# Function to get the protocol from a number
def get_protocol(num):
    if num == "6":
        return "tcp"
    elif num == "17":
        return "udp"
    elif num == "1":
        return "icmp"
    elif num == "2":
        return "igmp"
    else:
        return "untagged"

# Reading the flow log file
with open('flowlogs.txt', 'r') as file:
    data = file.readlines()

# Parsing each flow log entry
for line in data:
    row = line.strip().split()
    src_port = row[5]
    dst_port = row[6]
    protocol = get_protocol(row[7])
    
    # Checking if destination port/protocol exists in the lookup (for tagging)
    dst_comb = f"{dst_port}{protocol}"
    
    # Assigning tag based on destination port only
    if dst_comb in lookup:
        tag = lookup[dst_comb]
    else:
        tag = "Untagged"
    
    # Counting tags for destination port/protocol
    if tag in count_tag:
        count_tag[tag] += 1
    else:
        count_tag[tag] = 1
    
    # Counting destination port/protocol combination
    dst_tuple = (dst_port, protocol)
    if dst_tuple in count_combination:
        count_combination[dst_tuple] += 1
    else:
        count_combination[dst_tuple] = 1

    # Counting source port/protocol combination (without tagging)
    src_tuple = (src_port, protocol)
    if src_tuple in count_combination:
        count_combination[src_tuple] += 1
    else:
        count_combination[src_tuple] = 1

# Writing the outputs to a file
with open('output.txt', 'w') as output_file:
    # Writing tag counts
    output_file.write("Tag Counts:\n")
    output_file.write("Tag,Count\n")
    for tag, count in count_tag.items():
        output_file.write(f"{tag},{count}\n")
    
    output_file.write("\nPort/Protocol Combination Counts:\n")
    output_file.write("Port,Protocol,Count\n")
    for (port, protocol), count in count_combination.items():
        output_file.write(f"{port},{protocol},{count}\n")

# Printing for testing purposes
print("Tag Counts:", count_tag)
print("Port/Protocol Combination Counts:", count_combination)















# lookup={}
# count_tag={}
# count_combination={}
# with open('lookup.csv', 'r') as file:
#     data = file.readlines()


# for line in data[1:]:
#     row = line.strip().split(',')
#     lookup[row[0]+row[1]]=row[2]


# with open('sample.txt', 'r') as file:
#     data = file.readlines()

# for line in data:
#     row = line.strip().split(' ')
#     src_port = row[5]
#     dst_port = row[6]
#     if str(row[7])=="6":
#         protocol="tcp"
#     elif str(row[7])=="17":
#         protocol="udp"
#     elif str(row[7])=="1":
#         protocol="icmp"
#     elif str(row[7])=="2":
#         protocol="igmp"
#     else:
#         protocol="untagged"
        
        
#     if dst_port+protocol in lookup.keys():
#         tag=lookup[dst_port+protocol]
#     else:
#         tag="Untagged"
        
#     if tag in count_tag.keys():
#         count_tag[tag]+=1
#     else:
#         count_tag[tag]=1

#     comb=(src_port,protocol)
#     if comb in count_combination.keys():
#         count_combination[comb]+=1
#     else:
#         count_combination[comb]=1
    

#     if src_port+protocol in lookup.keys():
#         tag=lookup[src_port+protocol]
#     else:
#         tag="Untagged"
#     if tag in count_tag.keys():
#         count_tag[tag]+=1
#     else:
#         count_tag[tag]=1
        
#     comb=(src_port,protocol)
#     if comb in count_combination.keys():
#         count_combination[comb]+=1
#     else:
#         count_combination[comb]=1
    
    
# print(count_tag)
# print(count_combination)
