import sys

#This script reads in a 3-column file containing a scaffold name, beginning coordinate, 
#and end coordinate. The columns should be seperated by whitespace. Each of the 
#scaffolds should have a separate file named exactly how its named in the 3-column file.
#The script will read in the sequences and write them into the file from the -out parameter.
#The files should all be in the same directory which should be included in the -path parameter

def main():
    outFile, srcFile, path_to_files = ParseArgs(sys.argv)
    outFile = path_to_files + outFile + ".fasta"
    file = open(outFile, "w+")
    file = open(path_to_files+srcFile, "r")
    seq_coord_as_list = file.readlines()
    hit_dict = {}

    parse_hits(seq_coord_as_list, hit_dict)
    scaf_dict = {}
    
    for scaf in hit_dict:
        scaf_dict[scaf] = parse_scaffolds(scaf, path_to_files)
        write_hits(scaf_dict[scaf], hit_dict[scaf], scaf, outFile)    

#writes out the files in fasta format
def write_hits(scaf_sequence, hits_as_list, scaf_name, output_file):
    curr_hit = ""
    file = open(output_file, "a")
    for hit in hits_as_list:
        curr_hit = scaf_sequence[int(hit[0]) - 1:int(hit[1])]
        seq_name_coord = ">{} {}-{}\n"
        hitBeg = str(hit[0])
        hitEnd = str(hit[1])
        file.write(seq_name_coord.format(scaf_name, hitBeg, hitEnd))
        file.write(curr_hit + "\n")

#collects sequences from scaffolds files
def parse_scaffolds(scaf, path_to_scaf_files):
    curr_file = path_to_scaf_files + scaf
    file = open(curr_file, "r")
    fasta_sequence = file.readlines()
    curr_sequences = ""

    for i in fasta_sequence: 
        if i[0] != ">":
            curr_sequences += i.strip("\n")

    return curr_sequences

#parses the coordinate file and creates a dict where key is scaffold name and value is a pair
#the pair is the start and end coordinate for the scaffold
def parse_hits(seq_coord_as_list, hit_dict):
    for line in range(1, len(seq_coord_as_list) - 1):
        curr_line = seq_coord_as_list[line].split()
        if curr_line[0] not in hit_dict.keys():
            hit_dict[curr_line[0]] = []
        else:
            hit_dict[curr_line[0]].append((curr_line[1], curr_line[2]))

def ParseArgs(inputs):
    i = 1
    outFile = ""
    srcFile = ""
    path = ""
    if len(inputs) == 0:
        print("Hello, there are 3 required parameters: -src (file with 3 columns: scaffold, begin, and end seperated by whitespace, please provide full path), -path (path to src and scaffold files) -out (prefix for fasta file, will be generated in path directory)")
        quit()

    while i < len(inputs) - 1:
        if inputs[i] == "-out":
            outFile = inputs[i + 1]
        elif inputs[i] == "-src":
            srcFile = inputs[i + 1]
        elif inputs[i] == "-path":
            path = inputs[i + 1]
        elif inputs[i] == "-help":
            print("Hello, there are 3 required parameters: -src (file with 3 columns: scaffold, begin, and end seperated by whitespace, please provide full path), -path (path to src and scaffold files) -out (prefix for fasta file, will be generated in path directory)")
            quit()
        i += 1

    return [outFile, srcFile, path]


main()
