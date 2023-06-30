import csv

class GeneralTree:

    """
        Provides attributes and methods for a General Tree search algorithms 
    
    """

    nodes = []
    root = None
    data = []
    def __init__(self,id_position, parent_id_position):

        """
            Parameters
            _ _ _ _ _

            id_position: The position of the id for a given node (e.g. employee) in the csv
            parent_id_position: The position of the parent id for a given node (e.g. manager) in the csv
        
        """

        self.id_column = id_position
        self.parent_column = parent_id_position

    def read_data(self, file:str, encoding:str):
        """

            Read a csv file into the GeneralTree object
        
            Parameters
            ----------
            file: The location of the file to read
            endcoding: Encoding for the file (e.g. utf-8)
        """

        with open(file =file, mode='r', encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            counter = 0
            columns = None
            for row in reader:
                if counter == 0:
                    columns = row
                else:
                    i = 0
                    obj = {}
                    for col in columns:
                        obj[col] = row[i]
                        i += 1
                    self.nodes.append(Node(obj))
                    self.data.append(row)
                    if row[self.parent_column] == '':
                        self.root = Node(obj)
                counter += 1

    def create_map(self,root,queue=[]):

        """
            Recursive function to return traverse
            the hierarchy to update the Node object

            Parameters
            ________

            root: top node in the hierarchy
            queue: list used to store the nodes that need to mapped to the hierarchy default empty list
        
        """
        node = root
        nodes = self.find_child_id(list(node.data.values())[self.id_column])
        queue.extend(nodes)
        node.children = nodes
        self.nodes.append(node)
        self.nodes = self.nodes[1:]
        if len(queue) == 0:
            return
        elif len(nodes) == 0:
            return self.create_map(queue[0], queue[1:])
        for item in queue:
            return self.create_map(item,queue[1:])

    def find_child_id(self,parent_id) -> list:

        """
            Returns a list of child nodes for a given node    
        
            Parameters
            _ _ _ _ _
            parent_id: value that represents the parent node of the current node
        
        """

        items = []
        for node in self.nodes:
            if list(node.data.values())[self.parent_column] == parent_id:
                items.append(node)
        return items


    def to_csv(self, file:str, encoding:str,parent_prefix:str):

        """
        
            Parameters
            _ _ _ _ _
            file: The name of the file of the csv
            parent_suffix: The text concatenated to the front of the parent column
        
        """

        rows = []
        for item in self.nodes:
            row = {}
            parent = self.find_parent_id(list(item.data.values())[self.parent_column])
            parent_node = {}
            if parent != None:
                for key,value in parent.data.items():
                    parent_node[parent_prefix + '_' + key] = value
            else:
                for key, value in item.data.items():
                    parent_node[parent_prefix + '-' + key] = None
            row = {**item.data, **parent_node}
            rows.append(row)
        with open(file,'w', newline='', encoding=encoding) as f:
            write = csv.writer(f)
            write.writerow(rows[0].keys())
            write.writerows([x.values() for x in rows])

    def find_parent_id(self, child_id):

        """
            Returns a the parent node for a given node    
        
            Parameters
            _ _ _ _ _
            child_id: value that represents the child node of the parent node
        
        """

        data = None
        for node in self.nodes:
            if list(node.data.values())[self.id_column] == child_id:
                data = node

                break
        return data


class Node:
    """
       Object to store data for a complex data structure (i.e. graphs, trees, etc.) 
    """
    children = []
    def __init__(self,data:dict):
        self.data = data

        """
        
            Parameters
            _ _ _ _ _

            data: dictionary to hold the attributes for a node
        
        """

if __name__ == '__main__':

    hierarchy = GeneralTree(0,5)
    hierarchy.read_data('Data\employees.csv','utf-8')
    hierarchy.create_map(hierarchy.root)
    hierarchy.to_csv('csv_test.csv', 'utf-8','parent')
 


