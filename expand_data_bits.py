import re
import argparse
import os

def expand_data_bits(input_file):
    # Pattern to match the data lines with array [63:0]
    data_pattern = re.compile(r'\.data\[63:0\]')

    # Get the output file path based on the input file
    output_file = os.path.join(os.path.dirname(input_file), "expanded_bits_output.txt")

    # Open the input file and the output file
    with open(input_file, 'r') as file, open(output_file, 'w') as output:
        for line in file:
            # Check if the line contains .data[63:0]
            if data_pattern.search(line):
                # Extract the base name of the signal without the array specifier
                base_name = line.strip().replace(".data[63:0]", "")
                
                # Expand to bit-by-bit notation
                expanded_bits = [f"{base_name}[{i}]" for i in range(63, -1, -1)]
                
                # Join with commas & write to the output file
                expanded_line = ', '.join(expanded_bits)
                output.write(expanded_line + '\n')
    
    print(f"Expanded data bits saved to {output_file}")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Expand array signals to bit-by-bit representation.")
    parser.add_argument('-input', type=str, required=True, help="Path to the input file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with provided input file path
    expand_data_bits(args.input)
