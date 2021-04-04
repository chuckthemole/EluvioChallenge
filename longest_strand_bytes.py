from operator import itemgetter
import os
import numpy as np
import re
from suffix_trees import STree # https://pypi.org/project/suffix-trees/#description

# Completed by Charles Thomas :)
# Takes under 30 seconds to run with current sample files

def main():
    directory = [
        "sample.1", "sample.2", "sample.3", "sample.4", "sample.5",
        "sample.6", "sample.7", "sample.8", "sample.9", "sample.10"
    ]
    files = create_files_array(directory)
    data = find_longest_strand_in_two_or_more_files(files)

    print("The length of the longest strand is " + str(data["length"]))
    for i in range(0, len(data["file names"])):
        print("File with name " + str(directory[data["file names"][i] - 1]) +
            " has an offset at " + str(data["offsets"][i]))

def find_longest_strand_in_two_or_more_files(files):
    sorted_files = sorted(files, key=itemgetter(1), reverse=True) # Largest to smallest file
    files_array = []
    files_byte_array = []
    files_indices = []

    for i in range(0, 10):
        files_array.append(sorted_files[i][3])
        files_byte_array.append(sorted_files[i][2])
        files_indices.append(sorted_files[i][0])

    longest_length = 0
    longest_substr = ""
    files_found = []
    offsets = []

    # print_lengths_of_arrays(files_byte_array)

    broken = False
    for i in range(0, 10):
        for j in range(i + 1, 10):
            if longest_length < len(files_byte_array[i]) and longest_length < len(files_byte_array[j]):
                arry = [files_array[i], files_array[j]]
                suffix_tree = STree.STree(arry)
                lcs = suffix_tree.lcs()

                file_1_index = find_file_index_lcs(files_array[i], files_byte_array[i], lcs)
                file_2_index = find_file_index_lcs(files_array[j], files_byte_array[j], lcs)

                length = -1
                if (file_1_index[1] - file_1_index[0] != file_2_index[1] - file_2_index[0]):
                    print("LCS bytes are not equal!!")
                else:
                    length = file_1_index[1] - file_1_index[0]

                if length > longest_length:
                    longest_length = length
                    longest_substr = lcs
                    files_found = [files_indices[i], files_indices[j]]
                    offsets = [file_1_index[0], file_2_index[0]]
                elif length == longest_length:
                    indices = is_strand_in_all_files(files, lcs)
                    if len(indices) > len(files_found):
                        print("More files with this strand!")
                        longest_substr = lcs
                        files_found = []
                        offsets = []
                        for index in indices:
                            files_found.append(index[0])
                            offsets.append(index[1])
            elif longest_length > len(files_byte_array[i]):
                broken = True
            else:
                break
        if broken:
            break

    indices = is_strand_in_all_files(files, longest_substr)
    files_found = []
    offsets = []
    for index in indices:
        files_found.append(index[0])
        offsets.append(index[1])

    length_filenames_offsets = {
        "length": longest_length,
        "file names": files_found,
        "offsets": offsets
    }
    # print(length_filenames_offsets)
    # check_lcs_of_finds(files, files_found, offsets, longest_length)
    return length_filenames_offsets

def check_lcs_of_finds(files, files_found, offsets, length):
    print("\n\nChecking solutions...")
    j = 0
    for i in files_found:
        print("File " + str(i) + ": ")
        print("  First 5:")
        file = files[i - 1][2]
        offset = offsets[j]
        for byte in range(offset, offset + 5):
            print("   " + str(file[byte]))
        print("  Last 5:")
        for byte in range(offset + length - 5, offset + length):
            print("   " + str(file[byte]))
        j += 1

def print_lengths_of_arrays(arry_of_arrys):
    i = 0
    for arry in arry_of_arrys:
        print("length = " + str(len(arry)))
        i += 1

def find_file_index_lcs(file, byte_array, lcs):
    file_st = STree.STree(file)
    start_of_lcs_in_file = file_st.find(lcs)
    index = 0
    count = 0

    while count < start_of_lcs_in_file:
        substring = re.split("'", str(byte_array[index]))
        byte = substring[1]
        for b in byte:
            count += 1
        index += 1

    start_index = index

    while count < (start_of_lcs_in_file + len(lcs)):
        substring = re.split("'", str(byte_array[index]))
        byte = substring[1]
        for b in byte:
            count += 1
        index += 1

    end_index = index

    indices = [start_index, end_index]

    return indices

def is_strand_in_all_files(files, strand):
    j = 0
    indices = []
    for i in range(0, 10):
        st = STree.STree(files[i][3])
        index = st.find_all(strand)
        if len(index) > 0:
            strand_start_end = find_file_index_lcs(files[i][3], files[i][2], strand)
            element = [i + 1, strand_start_end[0]]
            indices.append(element)
    # print(indices)
    return indices

def create_files_array(array_of_files):
    i = 0
    loop = True
    files = []

    for element in array_of_files:
        string_file = ""
        byte_array = []

        try:
            file_stats = os.stat(element)
            bytes = file_stats.st_size

            f = open(element, "rb")
            byte = f.read(1)
            byte_array.append(byte)
            substring = re.split("'", str(byte))
            string_file += substring[1]
            while byte:
                byte = f.read(1)
                if byte:
                    byte_array.append(str(byte))
                    substring = re.split("'", str(byte))
                    string_file += substring[1]
            f.close()

            file = [i, bytes, byte_array, string_file]
            files.append(file)
        except:
            break
        i += 1

    return files

def print_file_array_element(file):
    print("This is from file smaple." + str(file[0]) + " .")
    print("This file contains " + str(file[1]) + " bytes.")
    print("The array of length " + str(len(file[2])) + " of bytes is below:")
    print(file[2])
    print("The string of bytes is below:")
    print(file[3])

if __name__ == "__main__":
    main()
