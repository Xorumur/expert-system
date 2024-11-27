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


# import re
# import sys
# from src.Parser import *
# from src.Utils import *

# if __name__ == "__main__":
#     try:
#         if len(sys.argv) < 2:
#             file_path = "./input/very_simple.txt"
#             print(f"Without filepath using the default path = {file_path}")
#             print("Usage: python script.py <file_path>")
#         # else:
#         if len(sys.argv) == 2:
#             file_path = sys.argv[1]
#         parser = Parser()
#         parser.parse_file(file_path)
#         # print(parser)

#         parser.check_error()

#         # Construire l'arbre global
#         global_tree = build_global_tree(parser.rules_rpn)


#         # Résolution des règles
#         # facts = {fact: (fact in parser.facts) for fact, node in NodeFactory._instances.items() if fact.isalnum()}
#         facts = {fact: True if fact in parser.facts else None for fact, node in NodeFactory._instances.items() if fact.isalnum()}
#         # print_facts_alphabetically(facts)
#         for subtree in global_tree.children:
#             resolve(subtree, facts)

#         # Afficher les nœuds par ordre alphabétique
#         # print_facts_alphabetically(facts)
#         for node in NodeFactory._instances.values():
#             if node.resolved_value is None:
#                 node.resolved_value = False
        
        
#         # Mettre à jour facts avec les nouvelles valeurs des Nodes
#         facts = {node.value: node.resolved_value for node in NodeFactory._instances.values() if node.value.isalnum()}
        
#         print_requested_facts(facts, parser.queries)
#     except Exception as e:
#         print(f"error: {e}")
import re
import sys
from src.Parser import *
from src.Utils import *

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            file_path = "./input/good_input/reverse_profound_tree.txt"
            print(f"Without filepath using the default path = {file_path}")
            print("Usage: python script.py <file_path>")
        # else:
        if len(sys.argv) == 2:
            file_path = sys.argv[1]
        parser = Parser()
        parser.parse_file(file_path)
        parser.check_error()

        # Construire l'arbre global
        global_tree = build_global_tree(parser.rules_rpn)

        # Initialiser les facts
        facts = {fact: True if fact in parser.facts else None for fact, node in NodeFactory._instances.items() if fact.isalnum()}

        # Fonction pour vérifier si des nœuds ont changé
        def nodes_have_changed():
            for node in NodeFactory._instances.values():
                if node.resolved_value is None:
                    return True
            return False

        # Fonction de comparaison pour détecter les changements dans les facts
        def facts_have_changed(old_facts, new_facts):
            return old_facts != new_facts

        # Boucle de résolution
        max_iterations = 3  # Limite de sécurité pour éviter les boucles infinies
        iteration = 0
        while True:
            iteration += 1
            # print(f"\nIteration: {iteration}")

            # Sauvegarder l'état des facts avant résolution
            previous_facts = facts.copy()

            # Résolution des règles
            for subtree in global_tree.children:
                resolve(subtree, facts)

            # print_tree(global_tree)

            # Mettre à jour facts avec les nouvelles valeurs des Nodes
            facts = {node.value: node.resolved_value for node in NodeFactory._instances.values() if node.value.isalnum()}

            # Vérification des changements dans les facts et les nœuds
            if not facts_have_changed(previous_facts, facts) and not nodes_have_changed():
                # print("\nNo changes in facts or nodes, stopping resolution.")
                break

            # Arrêt si on atteint le maximum d'itérations
            if iteration >= max_iterations:
                # print("\nMaximum iterations reached, stopping resolution.")
                break

        # Affecter les valeurs False aux nœuds non résolus
        for node in NodeFactory._instances.values():
            if node.resolved_value is None:
                node.resolved_value = False

        # Mise à jour finale des facts
        facts = {node.value: node.resolved_value for node in NodeFactory._instances.values() if node.value.isalnum()}

        # Affichage des résultats
        print_requested_facts(facts, parser.queries)
    except Exception as e:
        print(f"error: {e}")
