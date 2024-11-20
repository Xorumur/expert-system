from .Node import *
import re

class Parser:
    def __init__(self):
        self.file_content = []
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
        self.file_content = lines

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
            '(': -1,  # Parenthèses ont la plus basse priorité (pour ne pas être dépilées prématurément)
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
                # Dépiler jusqu'à trouver '(' ou une pile vide
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators:  # Vérifier si '(' est présent
                    operators.pop()  # Retirer '('
                else:
                    raise ValueError(f"Unmatched closing parenthesis in rule: {rule}")
            else:  # Opérateur logique
                # Dépiler les opérateurs avec une priorité >= au token actuel
                while (operators and precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)

        # Dépiler les opérateurs restants
        while operators:
            if operators[-1] == '(':
                raise ValueError(f"Unmatched opening parenthesis in rule: {rule}")
            output.append(operators.pop())

        print(f"RPN for '{rule}': {' '.join(output)}")  # Debugging log
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


    def check_error(self):
        if not self.validate_input(self.file_content):
            raise AssertionError()


    def validate_input(self, lines):
        # Define the regular expressions for each type of line
        # This rule pattern allows operators (+, -, |, ^) to be followed by variables or ! before variables
        rule_pattern = r'^\s*\(?\s*!?[A-Z](?:\s*[\+\|\^]\s*\(?\s*!?[A-Z]\s*\)?)*\s*\)?\s*(?:=>|<=>)\s*\(?\s*!?[A-Z](?:\s*[\+\|\^]\s*\(?\s*!?[A-Z]\s*\)?)*\s*\)?\s*$'
        fact_pattern = r'^=[A-Z]*$'
        query_pattern = r'^\?[A-Z]+$'

        # Track parentheses balance
        def check_parentheses(line):
            count = 0
            for char in line:
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
                    if count < 0:
                        return False
            return count == 0

        # Split the file content into lines and process
        rules = []
        facts = []
        queries = []

        for line_number, line in enumerate(lines, start=1):
            # Skip empty lines or comments
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Check if the line matches a rule, fact, or query
            if re.match(rule_pattern, line):
                if facts or queries:
                    print(f"Invalid format: rules must appear before facts and queries. Error on line {line_number}: {line}")
                    return False
                rules.append(line)
            elif re.match(fact_pattern, line):
                if queries or facts:
                    print(f"Invalid format: only one facts line is allowed. Error on line {line_number}: {line}")
                    return False
                facts.append(line)
            elif re.match(query_pattern, line):
                if len(facts) != 1:
                    print(f"Invalid format: a single facts line must precede the query. Error on line {line_number}: {line}")
                    return False
                queries.append(line)
            else:
                print(f"Invalid syntax on line {line_number}: {line}")
                return False

            # Check parentheses balance
            if not check_parentheses(line):
                print(f"Unmatched parentheses on line {line_number}: {line}")
                return False

        # Validate the structure of the file
        if not rules:
            print("Invalid format: at least one rule is required.")
            return False
        if len(facts) != 1:
            print("Invalid format: exactly one facts line is required.")
            return False
        if len(queries) != 1:
            print("Invalid format: exactly one query line is required.")
            return False

        return True
