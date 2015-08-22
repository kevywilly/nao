__author__ = 'kevywilly'

#import sqlite3
#import string

#class CustomData:
#    db_name = "NaoCustomData"
#    db = None

#    def __init__(self):
#        result = self.db = sqlite3.connect(self.db_name + ".sqlite")
#        print(result)
#        print "Opened database successfully"


from py2neo import Graph, Node, Relationship


class GraphDB:

    class SimpleNode:
        def __init__(self, node):
            self.name = node['name'].encode('utf-8')
            labels = map(lambda l: l.encode('utf-8'), node.labels)
            self.label = filter(lambda l: l != 'Concept', labels)[0]

    db_path = "http://neo4j:nao@127.0.0.1:7474/db/data/"

    graph = None

    interactions = ["Request", "Engagement", "Exploration", "Judgement", "Share", "Disengagment", "Unknown"]
    sentiments = ["Positive", "Neutral", "Negative", "Unknown"]

    def __init__(self):
        self.graph = Graph(self.db_path)

    def add_constraints(self):
        self.add_constraint("Thing", "name")
        self.add_constraint("Trait", "name")
        self.add_constraint("Sense", "name")
        self.add_constraint("Action", "name")

    def add_index(self, label, property):
        self.__add_index(label, property)

    def __add_index(self, label, property):
        try:
            self.graph.cypher.execute(("CREATE INDEX ON :%s(%s)") % (label,property))
            print("%s:%s index created" % (label,property))
        except:
            print("%s:%s constraint already exists" % (label,property))

    def add_constraint(self, label, property):
        self.__add_constraint(label,property)

    def __add_constraint(self, label,property):
        try:
            self.graph.schema.create_uniqueness_constraint(label, property)
            print("%s:%s constraint created" % (label,property))
        except:
            print("%s:%s constraint already exists" % (label,property))

    def add_unique_constraint(self, name, attr):
        self.graph.schema.create_uniqueness_constraint(name, attr)

    # --------------------------- Add / Remove Nodes and Relationships ------------------- #

    # -- Assign a thing to a parent thing (or remove)
    def assign_parent(self, label, name, parent, remove=False):
        if remove is True:
            return self.remove_relationship(label, name, 'IS_A', label, parent)
        else:
            return self.add_relationship(label, name, 'IS_A', label, parent)

    # -- Assign similarity between two things (or remove)
    def assign_similar(self, label, name, similar, remove=False):
        if remove is True:
            return self.remove_relationship(label, name, 'SIMILAR_TO', label, similar)
        else:
            return self.add_relationship(label, name, 'SIMILAR_TO', label, similar)

    # -- Assign an ability (action) to a thing (or remove)
    def assign_ability(self, name, a_name, remove=False):
        if remove is True:
            return self.remove_relationship("Concept", name, 'CAN', "Action", a_name)
        else:
            return self.add_relationship("Thing", name, 'CAN', "Action", a_name)

    # -- Add a node (or remove)
    def add_node(self, label, name, remove=False):
        if remove is True:
            return self.delete(Node(label, "name", name))
        else:
            return self.graph.cypher.execute_one("Merge(n:Concept:%s {name: '%s'}) return n" % (label, name))

    # -- Assign a trait to a thing (or remove)
    def assign_trait(self, thing, trait, remove=False):
        if remove is True:
            return self.remove_relationship("Trait", trait, "DESCRIBES", "Thing", thing)
        else:
            return self.add_relationship("Trait", trait, "DESCRIBES", "Thing", thing)

    # -- Assign a sense to a thing
    def assign_sense(self, thing, sense, remove=False):
        if remove is True:
            return self.remove_relationship("Thing", thing, "HAS", "Sense", sense)
        else:
            return self.add_relationship("Thing", thing, "HAS", "Sense", sense)

    # -- Add a relationship to two nodes
    def add_relationship(self, label, name, rel, r_label, r_name):
        """
        Add a relationship
        :param a_label:
        :param a_name:
        :param rel:
        :param b_label:
        :param b_name:
        :return:
        """
        n = self.graph.cypher.execute_one("Merge(n:Concept:%s {name: '%s'}) return n" % (label, name))
        r = self.graph.cypher.execute_one("Merge(n:Concept:%s {name: '%s'}) return n" % (r_label, r_name))

        return self.graph.create_unique(Relationship(n, rel, r))

    # -- remove a relationship from two nodes
    def remove_relationship(self, label, name, rel, r_label, r_name):
        r = Relationship(Node(label, "name", name), rel, Node(r_label, "name", r_name))
        self.graph.delete(r)

    # ----------------------------------------------------------------------------
    # Query nodes for relationships and abilities
    # ----------------------------------------------------------------------------

    # -- get definition of a thing by finding its parents
    def definition_of(self, name, neighbors=3):
        stmt = "MATCH (n:Concept { name: '%s' })-[:IS_A*1..%s]->(neighbors) RETURN neighbors.name as name" % (name, neighbors)
        return map(lambda x: x.name.encode('utf-8'), self.graph.cypher.execute(stmt))

    # -- ask whether a thing is another thing by inheritance
    def is_it_a(self, name, parent):
        statement = "match p=shortestPath((a:Thing {name:'%s'})-[:IS_A*1..2]->(b:Thing {name:'%s'})) return p" % (name, parent)
        return self.graph.cypher.execute_one(statement) is not None
        #return self.definition_of(name).count(parent) > 0

    # -- show examples of a thing through its children
    def examples_of(self, name):
        stmt = "MATCH (n:Concept { name: '%s' })<-[:IS_A*1..2]-(neighbors) RETURN neighbors.name as name" % name
        return map(lambda x: x.name.encode('utf-8'), self.graph.cypher.execute(stmt))

    # -- what can a thing do?
    def what_can_it_do(self, name):
        """
        What is a thing
        :param name:
        :param neighbors:
        :return: [SimpleNode(label,name)]
        """
        stmt = "MATCH (n:Concept { name: '%s' })-[:CAN]->(neighbors) RETURN neighbors" % name
        results = self.graph.cypher.execute(stmt)
        return map(lambda result: GraphDB.SimpleNode(result.neighbors), results)

    # -- can a thing perform an action (through direct knowledge) or through deduction
    def can_it(self, thing, action):
        """
        Can a thing do an action
        :param thing:
        :param action:
        :return: Tuple(Bool, NameOfMatchingParent)
        """
        statement = "match p=shortestPath((a:Thing {name:'%s'})-[:CAN*1..3]->(b:Action {name:'%s'})) return p" % (thing, action)
        if self.graph.cypher.execute_one(statement) is not None:
            return True, None

        statement2 = "MATCH (n:Concept { name: '%s' })-[:IS_A*1..3]->(neighbors)-[:CAN]-(b:Action {name: '%s'}) RETURN neighbors.name" % (thing, action)
        result = self.graph.cypher.execute_one(statement2)
        if result is not None:
            return True, result.encode('utf-8')
        else:
            return False, None












