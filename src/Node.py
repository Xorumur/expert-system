from enum import Enum

class connector_type(Enum):
    OR = '|' 
    XOR = '^'
    AND = '&'
    IMPLY = '<='     

class Node:
    def __init__(self, value):
        self.value = value
        self.resolved_value = None  # Stocke la valeur résolue du nœud (True/False)
        self.right = None
        self.left = None
        self.children = []  # Relations sortantes
        self.parents = []   # Relations entrantes
        
    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)
        
    def __repr__(self):
        return f"Node({self.value}, resolved_value={self.resolved_value})"

    def display(self, level=0):
        """
        Affiche l'arbre en utilisant une indentation pour représenter la hiérarchie.
        :param level: Niveau d'indentation (commence à 0 pour la racine).
        """
        result = "  " * level + f"- {self.value} (resolved: {self.resolved_value})\n"
        if self.left:  # Si le nœud a un enfant gauche
            result += self.left.display(level + 1)
        if self.right:  # Si le nœud a un enfant droit
            result += self.right.display(level + 1)
        for child in self.children:  # Si c'est une racine avec plusieurs enfants
            result += child.display(level + 1)
        return result

    
    
class NodeFactory:
    _instances = {}

    @staticmethod
    def get_or_create_node(value):
        """
        Retourne une instance unique pour un nœud donné (Singleton par valeur).
        """
        if value not in NodeFactory._instances:
            NodeFactory._instances[value] = Node(value)
        return NodeFactory._instances[value]
    

# Construire un réseau connecté
def build_logical_network(rpn_rules):
    for rpn in rpn_rules:
        stack = []
        for token in rpn.split():
            if token.isalnum():  # Fait (A, B, ...)
                stack.append(NodeFactory.get_or_create_node(token))
            else:  # Opérateur
                node = NodeFactory.get_or_create_node(token)
                if token != '!':  # Binaire
                    right = stack.pop()
                    left = stack.pop()
                    node.add_child(left)
                    node.add_child(right)
                else:  # Unaise
                    child = stack.pop()
                    node.add_child(child)
                stack.append(node)
        # Relier les conclusions (dernier élément de la pile)
        conclusion = stack.pop()
        NodeFactory.get_or_create_node("ROOT").add_child(conclusion)


def build_global_tree(rpn_rules):
    """
    Construit un arbre global en connectant tous les sous-arbres à une racine "ROOT".
    """
    root = Node("ROOT")
    subtrees = build_trees_from_rpn(rpn_rules)
    root.children = subtrees
    return root

def build_trees_from_rpn(rpn_rules):
    def build_tree_from_single_rule(rpn):
        stack = []
        for token in rpn.split():
            if token.isalnum():  # Fait (A, B, C, ...)
                stack.append(NodeFactory.get_or_create_node(token))  # Toujours partagé
            else:  # Opérateur
                node = Node(token)  # Nouvelle instance pour chaque opérateur
                if token != '!':  # Binaire
                    node.right = stack.pop()
                    node.left = stack.pop()
                else:  # Unaise
                    node.left = stack.pop()
                stack.append(node)
        return stack[0]

    return [build_tree_from_single_rule(rule) for rule in rpn_rules]


def print_tree(node, level=0):
    """
    Affiche l'arbre en commençant par le nœud donné, avec une indentation
    pour représenter les niveaux hiérarchiques.
    :param node: Le nœud actuel à afficher.
    :param level: Le niveau d'indentation actuel.
    """
    if not node:
        return

    # Afficher le nœud actuel avec son niveau d'indentation
    print("  " * level + f"- {node}")

    # Afficher le sous-arbre gauche (si existant)
    if node.left:
        print_tree(node.left, level + 1)

    # Afficher le sous-arbre droit (si existant)
    if node.right:
        print_tree(node.right, level + 1)

    # Afficher les enfants multiples (si c'est un opérateur avec plusieurs relations)
    for child in node.children:
        print_tree(child, level + 1)

def resolve(node, facts):
    """
    Résout l'état logique d'un nœud donné, basé sur les faits connus et les opérateurs.
    Met à jour la valeur résolue dans le nœud (resolved_value).
    """
    # Si la valeur est déjà résolue, la retourner directement
    if node.resolved_value is not None:
        return node.resolved_value

    # Si c'est un fait atomique (A, B, C, ...)
    if node.value.isalnum():
        node.resolved_value = facts.get(node.value, False)  # True si connu, sinon False
        return node.resolved_value

    # Résolution pour l'opérateur UNAIRE '!'
    if node.value == "!":
        node.resolved_value = not resolve(node.left, facts)
        return node.resolved_value

    # Résolution pour les opérateurs BINAIRES
    if node.value in ["+", "|", "^"]:
        left = resolve(node.left, facts)
        right = resolve(node.right, facts)
        if node.value == "+":  # AND
            node.resolved_value = left and right
        elif node.value == "|":  # OR
            node.resolved_value = left or right
        elif node.value == "^":  # XOR
            node.resolved_value = (left or right) and not (left and right)
        return node.resolved_value

    # Résolution pour l'opérateur '=>' (Implication)
    if node.value == "=>":
        left = resolve(node.left, facts)
        right = resolve(node.right, facts)
        if left:  # Si le côté gauche est vrai, le côté droit doit être vrai
            node.resolved_value = right
            # Mettre à jour la valeur du fait impliqué dans le dictionnaire `facts`
            node.right.resolved_value = True
            facts[node.right.value] = True
        else:  # Si le côté gauche est faux, l'implication est toujours vraie
            node.resolved_value = True
        return node.resolved_value

    # Résolution pour l'opérateur '<=>' (Équivalence)
    if node.value == "<=>":
        left = resolve(node.left, facts)
        right = resolve(node.right, facts)
        node.resolved_value = left == right
        return node.resolved_value

    # Par défaut, la valeur reste indéterminée
    node.resolved_value = None
    return None





def get_facts_with_values(node, facts, resolved_facts=None):
    """
    Parcourt l'arbre pour collecter les faits et leurs valeurs.
    :param node: Le nœud actuel à parcourir.
    :param facts: Dictionnaire des faits connus.
    :param resolved_facts: Dictionnaire où les faits résolus seront ajoutés.
    :return: Un dictionnaire {nom_du_fait: valeur}.
    """
    if resolved_facts is None:
        resolved_facts = {}

    # Si c'est une feuille (un fait), récupère sa valeur
    if node.value.isalnum():
        resolved_facts[node.value] = facts.get(node.value, False)

    # Parcourir les enfants gauche, droit ou multiples
    if node.left:
        get_facts_with_values(node.left, facts, resolved_facts)
    if node.right:
        get_facts_with_values(node.right, facts, resolved_facts)
    for child in node.children:
        get_facts_with_values(child, facts, resolved_facts)

    return resolved_facts
