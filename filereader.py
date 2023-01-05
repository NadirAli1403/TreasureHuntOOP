from csv import reader

def import_csv_layout(path):
    terrain_map=[]
    with open(path) as map:
        layout = reader(map,delimiter=',') #this is the reader, it converts our csv file into something that can be read in python, the first argument represents the filename and the second argument is the delimeter(what the data is spaced out by)
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


