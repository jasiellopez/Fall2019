import sys

#This script compares checks if two sequence coordinates have any overlap
#If there is an overlap, the pair is written out to the -out file
#In the output file, file 1 is the first file in the -files argument and 
#file 2 is the second file

def main():
    file1, file2, outFile = ParseArgs(sys.argv)

    file1_dict = {}
    file2_dict = {}
    readInFiles(file1, file1_dict)
    readInFiles(file2, file2_dict)
    file = open(outFile, "w+")
    file.write("chr" + "\t" + "File1" + "\t\t" + "File2" + "\n")
    findOverlap(file1_dict, file2_dict, file)

def findOverlap(file1_dict, file2_dict, file):
    for scaf in file1_dict:
        if scaf in file2_dict:
            for file1Coord in file1_dict[scaf]:
                for file2Coord in file2_dict[scaf]:
                    if ((file1Coord[0] >= file2Coord[0] and file1Coord[0] <= file2Coord[1]) or (file1Coord[1] <= file2Coord[1] and file1Coord[1] >= file2Coord[0]) or (file2Coord[0] >= file1Coord[0] and file2Coord[0] <= file1Coord[1]) or (file2Coord[1] <= file1Coord[1] and file2Coord[1] >= file1Coord[0])):
                        file.write("{}\t{}-{}\t{}-{}\n".format (scaf, file1Coord[0], file1Coord[1], file2Coord[0], file2Coord[1]))

#parses the coordinate file and creates a dict where key is scaffold name and value is a list of pairs
#the pair is the start and end coordinate for the scaffold
def readInFiles(path_to_file, coord_dict):
    file = open(path_to_file, "r")
    seq_coord_as_list = file.readlines()

    for line in range(len(seq_coord_as_list)):
        curr_line = seq_coord_as_list[line].split()
        if curr_line[0] not in coord_dict.keys():
            coord_dict[curr_line[0]] = []
        else:
            coord_dict[curr_line[0]].append((int(curr_line[1]), int(curr_line[2])))


def ParseArgs(inputs):
    i = 1
    file1 = ""
    file2 = ""
    outFile = ""
    path = ""
    if len(inputs) == 1:
        print("Hello, there are 3 required parameters: -files (2 files (seperated by a space) with sequence coordinates to be compared, will be searched for in path directory), -path (path to files) -out (output filename, will be generated in path directory)")
        quit()

    while i < len(inputs) - 1:
        if inputs[i] == "-out":
            outFile = inputs[i + 1]
        elif inputs[i] == "-files":
            file1 = inputs[i + 1]
            file2 = inputs[i + 2]
        elif inputs[i] == "-path":
            path = inputs[i + 1]
        elif inputs[i] == "-help":
            print("Hello, there are 3 required parameters: -files (2 files (seperated by a space) with sequence coordinates to be compared, will be searched for in path directory), -path (path to files) -out (output filename, will be generated in path directory)")
            quit()
        i += 1

    return [path+file1, path+file2, path+outFile]


main()