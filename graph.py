__author__ = 'kevywilly'


from py2neo import Graph, Node, Relationship
from naomodule import NaoModule

class GraphModule(NaoModule):

    # db path TODO make this a parameter
    db_path = "http://neo4j:nao@127.0.0.1:7474/db/data/"
    db = None
    valid_relations = ["is", "can", "similar", "describes", "likes", "dislikes"]

    def __init__(self, name):
        NaoModule.__init__(self, name)
        self.graph = Graph(self.db_path)

    def exit(self):
        NaoModule.exit(self)

    def add_constraints(self):
        self.add_constraint("Concept", "name")
        self.add_constraint("Trait", "name")
        self.add_constraint("Action", "name")

    def add_constraint(self, label, property):
        self.__add_constraint(label, property)

    def __add_constraint(self, label,property):
        try:
            self.graph.schema.create_uniqueness_constraint(label, property)
            print("%s:%s constraint created" % (label,property))
        except:
            print("%s:%s constraint already exists" % (label,property))

    # --------------------------- Add / Remove Nodes and Relationships ------------------- #

    # -- Assign a thing to a parent thing (or remove)

    def try_parse_relationship(self, text):
        params = map(lambda p: p.trim()), text.lower().split("--")

        if len(params) < 3:
            print("invalid relation use the form 'rel -- concept -- concept'")
            return None

        if self.valid_relations.count(params[0]) == 0:
            print("invalid relationship should be one of " + ', '.join(self.valid_relations))
            return None

        return params

    def relate_concepts(self, concept1, concept2, rel, label="Concept"):

        if self.valid_relations.count(rel) == 0:
            print("invalid relationship should be one of " + ', '.join(self.valid_relations))
            self.add_relationship(label, concept1, rel, label, concept2)

    def unrelate_concepts(self, text, label="Concept"):
        params = self.try_parse_relationship(text)

        if params is not None:
            rel, concept1, concept2 = params
            self.remove_relationship(label, concept1, rel, label, concept2)

    # -- Add a node (or remove)
    def add_concept(self, name, label="Concept"):
        return self.graph.cypher.execute_one("Merge(n:%s {name: '%s'}) return n" % (label, name))

    # -- Add a relationship to two nodes
    def add_relationship(self, label1, name1, rel, label2, name2):
        """ add a relationship"""
        if rel == "can":
            label2 = label2 + ":" + "Action"
        elif rel == "describes":
            label1 = label1 + ":" + "Trait"

        n = self.graph.cypher.execute_one("Merge(n:%s {name: '%s'}) return n" % (label1, name1))
        r = self.graph.cypher.execute_one("Merge(n:%s {name: '%s'}) return n" % (label2, name2))

        return self.graph.create_unique(Relationship(n, rel, r))

    # -- remove a relationship from two nodes
    def remove_relationship(self, label1, name1, rel, label2, name2):
        r = Relationship(Node(label1, "name", name1), rel, Node(label2, "name", name2))
        self.graph.delete(r)

    # ----------------------------------------------------------------------------
    # Query nodes for relationships and abilities
    # ----------------------------------------------------------------------------

    # -- get definition of a thing by finding its parents
    def what_is(self, name, neighbors=3):
        stmt = "MATCH (n:Concept { name: '%s' })-[:is*1..%s]->(neighbors) RETURN neighbors.name as name" % (name, neighbors)
        return map(lambda x: x.name.encode('utf-8'), self.graph.cypher.execute(stmt))

    # -- ask whether a thing is another thing by inheritance
    def is_it(self, name, parent):
        statement = "match p=shortestPath((a:Concept {name:'%s'})-[:IS_A*1..2]->(b:Concept {name:'%s'})) return p" % (name, parent)
        return self.graph.cypher.execute_one(statement) is not None

    # -- show examples of a thing through its children
    def instances_of(self, name):
        """ Get instances of (children of) a concept """
        stmt = "MATCH (n:Concept { name: '%s' })<-[:is*1..2]-(neighbors) RETURN neighbors.name as name" % name
        return map(lambda x: x.name.encode('utf-8'), self.graph.cypher.execute(stmt))

    # -- what can a thing do?
    def what_can_it_do(self, name):
        """ what can a concept do """
        stmt = "MATCH (n:Concept { name: '%s' })-[:can]->(neighbors) RETURN neighbors.name as name" % name
        return map(lambda result: result.name.encode('utf-8'), self.graph.cypher.execute(stmt))

    # -- can a thing perform an action (through direct knowledge) or through deduction
    def can_it(self, thing, action):
        """ can concept do concept """
        stmt1 = "match p=shortestPath((a:Concept {name:'%s'})-[:can*1..3]->(b:Concept {name:'%s'})) return p" % (thing, action)
        if self.graph.cypher.execute_one(stmt1) is not None:
            return True, None

        stmt2 = "MATCH (n:Concept { name: '%s' })-[:IS_A*1..3]->(neighbors)-[:CAN]-(b:Concept {name: '%s'}) RETURN neighbors.name" % (thing, action)
        result = self.graph.cypher.execute_one(stmt2)
        if result is not None:
            return True, result.encode('utf-8')
        else:
            return False, None












