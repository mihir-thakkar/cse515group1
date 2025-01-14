import numpy as np
import time
import networkx as nx
import operator
import utils

# graph file
global INPUT_FILE, INPUT_PATH
INPUT_PATH = "../Input/"
INPUT_FILE = "in_file.gspc"

global excluded_nodes_set

global first_intput_video, first_intput_frame, \
    second_intput_video, second_intput_frame, \
    third_intput_video, third_intput_frame

def creatGraph(m):
    #creat a new graph
    G = nx.DiGraph()
    #get the database size
    (row, column) = database.shape

    personalize = {}
    for r in range(row):
        #add edge weight(similarity) btw query node and object nodes
        for c in range(column):
            if (c % 5) == 4:
                q_video_number = database[r, c - 4]
                q_frame_number = database[r, c - 3]
                o_video_number = database[r, c - 2]
                o_frame_number = database[r, c - 1]
                weight = database[r, c]
                # add nodes
                #G.add_node((int(q_video_number), int(q_frame_number)))
                # add edge weight
                G.add_edge((int(q_video_number),int(q_frame_number)), (int(o_video_number),int(o_frame_number)), weight=weight)

                if int(q_video_number) == first_intput_video and int(q_frame_number) == first_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                elif int(q_video_number) == second_intput_video and int(q_frame_number) == second_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                elif int(q_video_number) == third_intput_video and int(q_frame_number) == third_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                else:
                    personalize[(int(q_video_number),int(q_frame_number))] = 0



    pr = nx.pagerank(G, alpha=0.9, personalization=personalize)
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    printInfo(sorted_pr, m)
    #print G.out_degree((1,1),weight='weight')
    utils.visualizeTopRankFrames(sorted_pr, m, excluded_nodes_set)

def printInfo(page_rank, m):
    printerFile = open("../Output/" + "output_t4_" + str(m) + ".pgr", "ab")

    M = 0
    count = 0
    while (count != m):
        node, sim = page_rank[M]
        if node != (first_intput_video, first_intput_frame) and \
                        node != (second_intput_video, second_intput_frame) and \
                        node != (third_intput_video, third_intput_frame):
            print node
            printerFile.write(str(page_rank[M]))
            printerFile.write("\n")
            count += 1;
        M += 1

    printerFile.close()

def calculate_k():
    column1 = ''
    column2 = ''
    count = 0;
    with open(INPUT_FILE) as f:
        for line in f:
            a = line.split(',');
            if column1 == '' and column2 == '':
                column1 = a[0]
                column2 = a[1]
            elif column1 != a[0] or column2 != a[1]:
                break
            count += 1
    return count;

def preProcessing(m):

    # Clear the file
    transfile = open("../Input/" + "trans_output_t2.gspc", "wb")
    printerFile = open("../Output/" + "output_t4_" + str(m) + ".pgr", "wb")
    printerFile.close()
    # Load the database
    print 'Loading database......'

    k = calculate_k()

    count = 0
    with open(INPUT_FILE) as f:
        for line in f:
            line = line.strip('\n')
            transfile.write(line)
            count += 1
            if count == k:
                transfile.write("\n")
                count = 0
            else:
                transfile.write(",")

    transfile.write("\n")
    transfile.close()

    global database
    database = np.loadtxt("../Input/" + "trans_output_t2.gspc", delimiter=",")
    print 'Database loaded......'

# Function : Main
# Description: Run the main program
if __name__ == '__main__':
    try:
        input_file = raw_input("Enter file name (default: in_file.gspc), the path is 'Input/', don't contain path:")
    except SyntaxError:
        input_file = None
    if input_file is not None:
        INPUT_FILE = input_file;
    INPUT_FILE = INPUT_PATH + INPUT_FILE

    # Take k as an input
    m = int(input("Enter m, for the m most significant frames (relative to the input frames):"))
    first_intput_video, first_intput_frame = input("Enter first input frame:")
    second_intput_video, second_intput_frame = input("Enter second input frame:")
    third_intput_video, third_intput_frame = input("Enter third input frame:")
    start_time = time.time();
    # visulization
    utils.clearOutputFramesDirectory()
    utils.output_a_frame(first_intput_video, first_intput_frame, "Input");
    utils.output_a_frame(second_intput_video, second_intput_frame, "Input");
    utils.output_a_frame(third_intput_video, third_intput_frame, "Input");
    excluded_nodes_set = {(first_intput_video, first_intput_frame),(second_intput_video, second_intput_frame),(third_intput_video, third_intput_frame)}

    preProcessing(m)
    creatGraph(m)

    end_time = time.time();
    utils.printTime(end_time - start_time)
