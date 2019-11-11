import sys

def main():
    outFile, srcFile = ParseArgs(sys.argv)
    outFile += ".fasta"
    file = open(outFile, "w+") #merged_hits_from_robu_run
    file = open(srcFile, "r")# merged_hits_robu_run_coordinates
    seq_coord_as_list = file.readlines()
    hit_dict = {}
    path_to_scaf_files = "/home/davidsonlab/Desktop/Genomes/Robusta/"

    parse_hits(seq_coord_as_list, hit_dict)
    scaf_dict = {}
    
    for scaf in hit_dict:
        scaf_dict[scaf] = parse_scaffolds(scaf, path_to_scaf_files)
        write_hits(scaf_dict[scaf], hit_dict[scaf], scaf)    

#writes out the files in fasta format
def write_hits(scaf_sequence, hits_as_list, scaf_name):
    curr_hit = ""
    file = open("/home/davidsonlab/Desktop/hits_from_xmlparser.fasta", "a") #merged_hits_from_robu_run.fasta
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
    i = 0
    
    while i < len(inputs):

        if inputs[i] == "-out":
            onOut = True
            onSrc = False
            i += 1
        elif inputs[i] == "-src":
            onOut = False
            onSrc = True
            i += 1

        elif inputs[i] == "-help":
            print("Hello, there are 2 required parameters: -src (file with 3 columns: scaffold, begin, and end seperated by whitespace, please provide full path), -out (prefix for fasta file))

        elif onSrc == True:
            srcFile = input[i]
        elif onOut == True:
            outFile = input[i]

        i += 1
    return [srcFile, outFile]


main()
