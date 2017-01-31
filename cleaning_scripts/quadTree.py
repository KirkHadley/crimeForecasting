class Node(object):
    def __init__(self, attribute, bounds):
        '''
        attribute: val associated w this square
        bounds: 4 points, organized in a list as in:
            [xmin, ymin, xmax, ymax]
        '''
        self.attribute = attribute
        self.bounds = bounds


class QuadTree(object):
    def __init__(self, bounds=None,x=None, y=None, height=None, width=None,  max_items=10, max_depth=20, _depth=0):
        self.max_depth = max_depth
        self.max_items = max_items
        self.children = []
        self.nodes = []
        self._depth = _depth
        if bounds:
            x_1, y_1, x_2, y_2 = bounds
            self.width = abs(x_2 - x_1)
            self.height = abs(y_2 - y_1)
            x_mid = x_1+self.width/2.0
            y_mid = y_1+self.height/2.0
            self.center = (x_mid, y_mid)
        elif x is not None and y is not None:
            self.center = (x,y)
            self.width = width
            self.height = height
        else:
            raise Exception("require box or coords w width and height to begin")


    def insert(self, attribute, bounds):
        if len(self.children) == 0:
            node = Node(attribute, bounds)
            self.nodes.append(node)
            if len(self.nodes) > self.max_items and self._depth < self.max_depth:
                self.split()
        else:
            self.insert_into_children(attribute, bounds)


    def intersect(self, box, matches=None):
        if matches is None:
            matches = set()
        if self.children:
            if box[0] <= self.center[0]:
                if box[1] <= self.center[1]:
                    self.children[0].intersect(box, matches)
                if box[3] >= self.center[1]:
                    self.children[1].intersect(box, matches)
            if box[2] >= self.center[0]:
                if box[1] <= self.center[1]:
                    self.children[2].intersect(box, matches)
                if box[3] >= self.center[1]:
                    self.children[3].intersect(box, matches)
        for node in self.nodes:
            if(node.bounds[2] >= box[0] and 
                    node.bounds[0] <= box[2] and
                    node.bounds[3] >= box[1] and 
                    node.bounds[1] <= box[3]):
                matches.add(node.attribute)
        return matches

    def insert_into_children(self, attribute, bounds):
        if(bounds[0] <= self.center[0] and 
                bounds[2] >= self.center[0] and 
                bounds[1] <= self.center[1] and 
                bounds[3] >= self.center[1]):
            node = Node(attribute, bounds)
            self.nodes.append(node)
        else:
            if bounds[0] <= self.center[0]:
                if bounds[1] <= self.center[1]:
                    self.children[0].insert(attribute, bounds)
                if bounds[3] >= self.center[1]:
                    self.children[1].insert(attribute, bounds)
            if bounds[2] > self.center[0]:
                if bounds[1] <= self.center[1]:
                    self.children[2].insert(attribute, bounds)
                if bounds[3] >= self.center[1]:
                    self.children[3].insert(attribute, bounds)
    
    def split(self):
        q_width = self.width / 4.0
        q_height = self.height / 4.0
        med_width = self.width / 2.0
        med_height = self.height / 2.0
        x1 = self.center[0] - q_width
        x2 = self.center[0] + q_width
        y1 = self.center[1] - q_width
        y2 = self.center[1] + q_width
        next_depth = self._depth + 1
        self.children = [QuadTree(x=x1, y=y1, width=med_width, 
            height=med_height,max_items=self.max_items,
            max_depth=self.max_depth, _depth=next_depth),
            QuadTree(x=x1, y=y2, width=med_width, 
                height=med_height,max_items=self.max_items,
                max_depth=self.max_depth, _depth=next_depth),
            QuadTree(x=x2, y=y1, width=med_width, 
                height=med_height,max_items=self.max_items,
                max_depth=self.max_depth, _depth=next_depth),
            QuadTree(x=x2, y=y2, width=med_width, 
                height=med_height,max_items=self.max_items,
                max_depth=self.max_depth, _depth=next_depth)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self.insert_into_children(node.attribute, node.bounds)

    def __len__(self):
        """
        Returns:
        
        - A count of the total number of members/items/nodes inserted
        into this quadtree and all of its child trees.
        """
        size = 0
        for child in self.children:
            size += len(child)
        size += len(self.nodes)
        return size


if __name__ == '__main__':
    import random
    import time
    class Item:
        def __init__(self, x, y):
            left = x-1
            right = x+1
            top = y-1
            bottom = y+1
            self.bbox = [left,top,right,bottom]
    #items = [Item(random.randrange(5,95),random.randrange(5,95)) for _ in range(10000)]
    spindex = QuadTree(bounds=[-11,-33,100,100])
    for i in range(1000):
        spindex.insert('a', [random.randrange(0,100), random.randrange(0,100),
            random.randrange(0,100),random.randrange(0,100)])
    print("{0} members in this index.".format(len(spindex)))
    print("testing hit")
    testitem = (51,51,86,86)
    t = time.time()
    matches = spindex.intersect(testitem)
    print("{0} seconds".format(time.time()-t))
