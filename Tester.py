import subprocess


def run_test(script_path, input_file, expected_output):
    """
    Exécute un script Python avec un fichier d'entrée et compare son output
    avec le résultat attendu.
    """
    try:
        # Commande pour exécuter le script avec l'argument
        result = subprocess.run(
            ["python3", script_path, input_file],
            text=True,
            capture_output=True  # Capture stdout et stderr
        )

        # Afficher l'output réel
        print(f"Output for {input_file}:")
        print(result.stdout)

        # Comparer avec le résultat attendu
        print("\nExpected Output:")
        print(expected_output)

        green = "\033[92m"
        red = "\033[91m"
        reset = "\033[0m"

        print("\nTest Result:",
              f"{green}PASS{reset}" if result.stdout.strip() ==\
                expected_output.strip() else f"{red}FAIL{reset}")
        print("=" * 50)
    except Exception as e:
        print(f"Error while testing {input_file}: {e}")


if __name__ == "__main__":
    try:
        # Liste des tests
        tests = [
            {
                "input_file": "./input/good_input/classique.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nB: True"""
            },
            {
                "input_file": "./input/good_input/simple_test.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nG: True\nV: False\nX: False"""
            },
            {
                "input_file": "./input/good_input/test.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nD: True\nG: False\nH: False\nX: True\n"""
            },
            {
                "input_file": "./input/good_input/very_simple.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nB: True\nD: True\nE: False\n"""
            },
            {
                "input_file": "./input/good_input/profound_tree.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nD: True"""
            },
            {
                "input_file": "./input/good_input/equivalence.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nB: True"""
            },
            {
                "input_file": "./input/bad_input/bad_close_paranthese.txt",
                "expected_output": """error: Unmatched closing parenthesis in rule: A + B) <=> !C"""
            },
            {
                "input_file": "./input/bad_input/bad_open_paranthese.txt",
                "expected_output": """error: Unmatched opening parenthesis in rule: (A + B => Y + Z"""
            },
            {
                "input_file": "./input/bad_input/operators.txt",
                "expected_output": """Invalid syntax on line 9: A ++ B <=> C\nerror:"""
            },
            {
                "input_file": "./input/bad_input/invalid_parameters.txt",
                "expected_output": """Invalid syntax on line 11: =7\nerror:"""
            },
            {
                "input_file": "./input/bad_input/invalid_parameters_2.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nP: Not found in facts\n"""
            },
            {
                "input_file": "./input/bad_input/bad_input.txt",
                "expected_output": """Invalid syntax on line 1: tdsa\nerror:"""
            },
            {
                "input_file": "./input/good_input/reverse_profound_tree.txt",
                "expected_output": """Requested Facts (sorted alphabetically):\nD: True"""
            },
        ]

        # Chemin vers votre script principal
        main_script_path = "./main.py"

        # Exécuter chaque test
        for test in tests:
            run_test(main_script_path, test["input_file"], test["expected_output"])
    except Exception as e:
        print(f"error : {e}")
