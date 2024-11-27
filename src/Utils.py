def print_nodes_alphabetically(root):
    """
    Affiche les nœuds de l'arbre par ordre alphabétique de leurs noms.
    :param root: Le nœud racine de l'arbre.
    """
    # Collecter tous les nœuds
    nodes = collect_nodes(root)

    # Trier les nœuds par leur valeur (ordre alphabétique)
    sorted_nodes = sorted(nodes, key=lambda node: node.value)

    print("\nNodes sorted alphabetically:")
    for node in sorted_nodes:
        print(f"{node.value}: resolved_value={node.resolved_value}")


def collect_nodes(node, nodes=None):
    """
    Parcourt l'arbre pour collecter tous les nœuds.
    :param node: Le nœud actuel.
    :param nodes: Liste des nœuds collectés.
    :return: Une liste contenant tous les nœuds.
    """
    if nodes is None:
        nodes = []

    if node not in nodes:  # Éviter les doublons
        nodes.append(node)

    # Parcourir les enfants gauche et droit
    if node.left:
        collect_nodes(node.left, nodes)
    if node.right:
        collect_nodes(node.right, nodes)

    # Parcourir les enfants multiples (opérateurs avec plusieurs relations)
    for child in node.children:
        collect_nodes(child, nodes)

    return nodes


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

    # Afficher les enfants multiples
    # (si c'est un opérateur avec plusieurs relations)
    for child in node.children:
        print_tree(child, level + 1)


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


def print_facts_alphabetically(facts):
    """
    Affiche les faits depuis le dictionnaire `facts`
    par ordre alphabétique.
    :param facts: Dictionnaire contenant les faits {nom: valeur}.
    """
    print("\nFacts sorted alphabetically:")
    for fact in sorted(facts.keys()):  # Trier les clés du dictionnaire
        print(f"{fact}: {facts[fact]}")


def print_requested_facts(facts, queries):
    """
    Affiche les faits demandés dans le fichier d'entrée
    (listés dans `queries`), par ordre alphabétique.
    :param facts: Dictionnaire contenant les faits {nom: valeur}.
    :param queries: Ensemble ou liste contenant les faits demandés.
    """
    print("\nRequested Facts (sorted alphabetically):")
    for fact in sorted(queries):  # Trier les faits demandés
        if fact in facts:
            print(f"{fact}: {facts[fact]}")
        else:
            print(f"{fact}: Not found in facts")
