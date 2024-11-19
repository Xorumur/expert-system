from .Node import *

class Parser:
    def __init__(self):
        self.rules = []         # Règles au format original
        self.rules_rpn = []     # Règles converties en RPN
        self.facts = set()      # Faits initiaux
        self.queries = set()    # Requêtes

    def parse_file(self, file_path):
        """
        Parse le fichier pour extraire les règles, les faits et les requêtes.
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Ignorer les lignes vides ou les commentaires
            
            if "=>" in line or "<=>" in line:
                self.rules.append(line)
                self.rules_rpn.append(self.to_rpn(line))
            elif line.startswith("="):
                self.facts.update(line[1:])
                for fact in line[1:]:
                    node = NodeFactory.get_or_create_node(fact)
                    node.resolved_value = True  # Définit les faits initiaux à True
            elif line.startswith("?"):
                self.queries.update(line[1:])

    def to_rpn(self, rule):
        """
        Convertit une règle en notation polonaise inversée (RPN).
        """
        precedence = {
            '!': 5,   # Non logique
            '+': 4,   # ET logique
            '|': 3,   # OU logique
            '^': 2,   # XOR logique
            '=>': 1,  # Implication
            '<=>': 0, # Biconditionnelle
            '(': 0,   # Parenthèses ont la plus basse priorité
        }
        output = []
        operators = []

        # Séparer la règle en tokens (opérateurs, variables, etc.)
        tokens = self.tokenize_rule(rule)

        for token in tokens:
            if token.isalnum():  # Variable ou symbole logique (A, B, etc.)
                output.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Retirer '('
            else:  # Opérateur logique
                while (operators and precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        return ' '.join(output)

    def tokenize_rule(self, rule):
        """
        Tokenize une règle pour extraire les opérateurs, parenthèses et variables.
        """
        tokens = []
        buffer = ''
        i = 0
        while i < len(rule):
            char = rule[i]
            if char in "()+|^!":  # Opérateurs et parenthèses simples
                if buffer:
                    tokens.append(buffer)
                    buffer = ''
                tokens.append(char)
            elif char == '=' and i + 1 < len(rule) and rule[i + 1] == '>':
                if buffer:
                    tokens.append(buffer)
                    buffer = ''
                tokens.append('=>')
                i += 1
            elif char == '<' and i + 2 < len(rule) and rule[i + 1:i + 3] == '=>':
                if buffer:
                    tokens.append(buffer)
                    buffer = ''
                tokens.append('<=>')
                i += 2
            elif char.strip():  # Ignorer les espaces
                buffer += char
            i += 1

        if buffer:
            tokens.append(buffer)

        return tokens

    def __repr__(self):
        return (f"Rules: {self.rules}\n"
                f"Rules in RPN: {self.rules_rpn}\n"
                f"Facts: {sorted(self.facts)}\n"
                f"Queries: {sorted(self.queries)}\n")
