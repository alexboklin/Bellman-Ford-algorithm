import time
import argparse
import sys

def main(infinity = 9999999):

    start = time.process_time()

    parser = argparse.ArgumentParser(description="Solves the 0/1 knapsack problem for a given set of items.")
    parser.add_argument("-d", help="distances", action="store_true")
    parser.add_argument("-p", help="paths from the source vertex", action="store_true")
    parser.add_argument("-i", help="default number sifnifying infinity", action="store_true")
    parser.add_argument("-t", help="execution time", action="store_true")
    parser.add_argument("filename", help=".txt file to parse")
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as file:
            raw = [ list(map(int, i.split())) for i in file.readlines() ]
    except IOError:
        print("No such file.")
        sys.exit()
   
    while True:
        source = int(input("Source node: ")) # Number of vertex - 1 (source = 0 if vertex #1)
        if source not in range(1, raw[0][0] + 1):
            source = int(input("Source node: ")) 
            continue
        else:
            source -= 1
            break

    if args.i:
        no_path = int(input("Number for infinity: "))

    data = [ (i[0], i[1], i[2]) for i in raw[1:] ]
    tempDistances = [ infinity if i != source else  0 for i in range(raw[0][0])]
    paths = [ [source + 1] for i in range(raw[0][0]) ]
    negativeCycle = False

    # Calculate paths and distances
    for i in range(len(tempDistances)):
        for edge in [ (i[0], i[1]) for i in data ]:
            weight = [ j[2] for j in data if set([edge[0], edge[1]]) == set([j[0], j[1]]) ][0]

            if not (weight < 0 and tempDistances[edge[0]-1] == infinity):
                if tempDistances[edge[0]-1] + weight < tempDistances[edge[1]-1] :
                    tempDistances[edge[1]-1] = tempDistances[edge[0]-1] + weight
                    paths[edge[1]-1].extend(paths[edge[0]-1])      
                    paths[edge[1]-1].append(edge[1])
                
    # Report if there is a negative weight cycle in graph
    for edge in [ (i[0], i[1]) for i in data ]:
        weight = [ j[2] for j in data if set([edge[0], edge[1]]) == set([j[0], j[1]]) ][0]
        if not (weight < 0 and tempDistances[edge[0]-1] == infinity):
            if tempDistances[edge[1]-1] > tempDistances[edge[0]-1] + weight:
                negativeCycle = True
                print("The graph contains negative weight cycle")
                break    

    if not negativeCycle:    
        tempPaths = [ paths[i][ len(paths[i]) - paths[i][::-1].index(source+1) - 1 : ]  for i in range(len(paths)) ]
        finalPaths = [ tuple(tempPaths[i]) if tempDistances[i] != infinity else 'infinity' for i in range(len(tempDistances)) ]
        finalDistances = [ tempDistances[i] if tempDistances[i] != infinity else 'infinity' for i in range(len(tempDistances)) ]

        if args.d:
            print("Distances from the source edge: {}".format(finalDistances))
    
        if args.p:
            print("Paths to each vertex from the source: {}".format(finalPaths))
        
    if args.t:
        print("--- {} seconds ---".format(time.process_time() - start))

if __name__ == "__main__":
    main()         
