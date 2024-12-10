import csv
import argparse


class NTM:
    def __init__(self, file_name):
        """Initialize the NTM by loading transitions from the given file."""
        self.name = ""
        self.states = []
        self.sigma = []
        self.gamma = []
        self.start_state = ""
        self.accept_state = ""
        self.reject_state = ""
        self.transitions = {}
        self.load_ntm(file_name)
    
    def load_ntm(self, file_name):
        """Parse the .csv file and load NTM configuration."""
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            self.name = next(reader)[0]
            self.states = next(reader)
            self.sigma = next(reader)
            self.gamma = next(reader)
            self.start_state = next(reader)[0]
            self.accept_state = next(reader)[0]
            self.reject_state = next(reader)[0]
            for row in reader:
                state, char, next_state, write, move = row
                self.transitions.setdefault((state, char), []).append((next_state, write, move))
        
    def trace(self, input_string, max_depth=50):
        """Trace all possible paths of the NTM."""
        tree = [[["", self.start_state, input_string]]]  # Root of the configuration tree
        configs_explored = 0  # Total configurations explored
        non_leaves = 0  # Non-leaf configurations (nodes with children)
        
        # Debug: Verify initial configuration
        print(f"Initial configuration: [left='', state='{self.start_state}', right='{input_string}']")

        for depth in range(max_depth):
            level = tree[-1]
            next_level = []
            for left, state, right in level:
                configs_explored += 1
                # Stop if an accept state is reached
                if state == self.accept_state:
                    self.print_accept_path(tree, [left, state, right], depth)
                    return "Accepted", configs_explored, depth, configs_explored / max(non_leaves, 1)
                # Skip if a reject state is reached
                if state == self.reject_state:
                    continue
                    
                # Read the current character on the tape
                char = right[0] if right else "_"
                
                # Check all possible transitions for this state and character
                for next_state, write, move in self.transitions.get((state, char), []):
                    non_leaves += 1
                    # Update the tape and head position
                    if move == "L":
                        if left:
                            new_right = left[-1] + char + right
                            new_left = left[:-1]
                        else:
                            new_left = ""
                            new_right = "_" + char + right
                    elif move == "R":
                        new_left = left + char
                        new_right = right[1:] if len(right) > 1 else "_"

                    next_level.append([new_left, next_state, new_right])
                    
            # If no further configurations, reject
            if not next_level:
                print(f"Rejected at depth {depth}")
                return "Rejected", configs_explored, depth, configs_explored / max(non_leaves, 1)
                
            # Add the next level to the tree
            tree.append(next_level)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        # Max depth reached without decision                    
        print(f"Execution stopped after reaching max depth: {max_depth}")
        return "Undecided", configs_explored, max_depth, configs_explored / max(non_leaves, 1)

    def print_accept_path(self, tree, config, depth): 
        """Print the path to the accepting configuration."""
        print(f"String accepted at depth {depth}.")
        print("Path to acceptance:")
        for d, level in enumerate(tree):
            for c in level:
                if c == config:
                    print(f"Depth {d}: {c}")
    
    def print_tree_summary(self, result, configs, depth, avg_nd):
        """Print the summary of the simulation."""
        print(f"\n--- Simulation Summary ---")
        print(f"Result: {result}")
        print(f"Configurations explored: {configs}")
        print(f"Depth of configuration tree: {depth}")
        print(f"Average nondeterminism: {avg_nd:.2f}")
        print("--------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NTM Simulator")
    parser.add_argument("file", help="Path to the NTM definition file (.csv)")
    parser.add_argument("input", help="Input string to test")
    parser.add_argument("--max_depth", type=int, default=50, help="Maximum depth of exploration")
    args = parser.parse_args()
    
    # Load NTM and simulate
    ntm = NTM(args.file)
    print(f"Simulating NTM: {ntm.name}")
    print(f"Input string: {args.input}\n")
    
    result, configs, depth, avg_nd = ntm.trace(args.input, max_depth=args.max_depth)
    
    # Print final results
    ntm.print_tree_summary(result, configs, depth, avg_nd)
