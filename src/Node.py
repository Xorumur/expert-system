class Node:
    def __init__(self, value):
        self.value = value
        # Stocke la valeur résolue du noeud (True/False)
        self.resolved_value = None
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
        Affiche l'arbre en utilisant une indentation
        pour représenter la hiérarchie.
        :param level: Niveau d'indentation (commence à 0 pour la racine).
        """
        result = "  " * level +\
            f"- {self.value} (resolved: {self.resolved_value})\n"
        if self.left:  # Si le nœud a un enfant gauche
            result += self.left.display(level + 1)
        if self.right:  # Si le nœud a un enfant droit
            result += self.right.display(level + 1)
        # Si c'est une racine avec plusieurs enfants
        for child in self.children:
            result += child.display(level + 1)
        return result


class NodeFactory:
    _instances = {}

    @staticmethod
    def get_or_create_node(value):
        """
        Retourne une instance unique pour
        un noeud donné (Singleton par valeur).
        """
        if value not in NodeFactory._instances:
            NodeFactory._instances[value] = Node(value)
        return NodeFactory._instances[value]


def build_global_tree(rpn_rules):
    """
    Construit un arbre global en connectant
    tous les sous-arbres à une racine "ROOT".
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
                # Toujours partagé
                stack.append(NodeFactory.get_or_create_node(token))
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


def resolve(node, facts):
    """
    Résout l'état logique d'un nœud donné,
    basé sur les faits connus et les opérateurs.
    Met à jour la valeur résolue dans le nœud (resolved_value).
    """
    # Si la valeur est déjà résolue, la retourner directement
    if node.resolved_value is not None:
        return node.resolved_value

    # Si c'est un fait atomique (A, B, C, ...)
    if node.value.isalnum():
        # False si non trouvé
        node.resolved_value = facts.get(node.value, False)
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
            node.resolved_value = True
            # Mettre à jour la valeur de la droite
            node.right.resolved_value = True
            facts[node.right.value] = True  # Mettre à jour les faits
        # Si la régle n'est pas encore résolvable
        elif left is None and right is None:
            return node.resolved_value
        else:  # Si le côté gauche est faux, l'implication est toujours vraie
            node.resolved_value = True
        return node.resolved_value

    # Résolution pour l'opérateur '<=>' (Équivalence)
    if node.value == "<=>":
        left = resolve(node.left, facts)
        right = resolve(node.right, facts)

        # Si un côté est indéterminé,
        # propager la valeur de l'autre côté s'il est connu
        if left is True and right is None:
            node.right.resolved_value = True
            facts[node.right.value] = True
        elif left is False and right is None:
            node.right.resolved_value = False
            facts[node.right.value] = False
        elif right is True and left is None:
            node.left.resolved_value = True
            facts[node.left.value] = True
        elif right is False and left is None:
            node.left.resolved_value = False
            facts[node.left.value] = False
        elif right is None and left is None:
            node.resolved_value = None
            return None
        # Calculer l'équivalence logique
        node.resolved_value = left == right
        return node.resolved_value

    # Par défaut, la valeur reste indéterminée
    node.resolved_value = None
    return None
