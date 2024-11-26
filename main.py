# import re
# from src.Parser import *

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 2:
#         print("Usage: python script.py <file_path>")
#     else:
#         file_path = sys.argv[1]
#         parser = Parser()
#         parser.parse_file(file_path)
        
#         print(parser)
        
#         # Construire l'arbre global
#         global_tree = build_global_tree(parser.rules_rpn)

#         print_tree(global_tree)

#         # Initialiser facts depuis NodeFactory
#         facts = {fact: (fact in parser.facts) for fact, node in NodeFactory._instances.items() if fact.isalnum()}

#         print("\nInitial Facts (from NodeFactory):")
#         print(facts)

#         # print(global_tree.children)
        
#         # Résolution de chaque règle
#         print("\nResolutions:")
#         for i, subtree in enumerate(global_tree.children):
#             resolve(subtree, facts)

#         # Résultats pour les queries spécifiées
#         print("\nQuery Results:")
#         for query in parser.queries:
#             value = facts.get(query, None)
#             print(f"{query}: {value}")

#         # Afficher tous les faits avec leur état final
#         print("\nAll Facts (Final States from NodeFactory):")
#         for fact, node in NodeFactory._instances.items():
#             if fact.isalnum():  # S'assurer qu'on imprime uniquement les faits
#                 value = facts.get(fact, None)
#                 print(f"{fact}: {value}")
                
#         print_tree(global_tree)


import re
import sys
from src.Parser import *
from src.Utils import *

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            file_path = "./input/very_simple.txt"
            print(f"Without filepath using the default path = {file_path}")
            print("Usage: python script.py <file_path>")
        # else:
        if len(sys.argv) == 2:
            file_path = sys.argv[1]
        parser = Parser()
        parser.parse_file(file_path)
        # print(parser)

        parser.check_error()

        # Construire l'arbre global
        global_tree = build_global_tree(parser.rules_rpn)


        # Résolution des règles
        # facts = {fact: (fact in parser.facts) for fact, node in NodeFactory._instances.items() if fact.isalnum()}
        facts = {fact: True if fact in parser.facts else None for fact, node in NodeFactory._instances.items() if fact.isalnum()}
        # print_facts_alphabetically(facts)
        for subtree in global_tree.children:
            resolve(subtree, facts)

        # Afficher les nœuds par ordre alphabétique
        # print_facts_alphabetically(facts)
        for node in NodeFactory._instances.values():
            if node.resolved_value is None:
                node.resolved_value = False
        
        
        # Mettre à jour facts avec les nouvelles valeurs des Nodes
        facts = {node.value: node.resolved_value for node in NodeFactory._instances.values() if node.value.isalnum()}
        
        print_requested_facts(facts, parser.queries)
    except Exception as e:
        print(f"error: {e}")
