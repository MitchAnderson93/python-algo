import argparse
from main import calculate_cagr

def print_expected_input():
    print("Expected input format: initial_value final_value years")
    print("Example: 1000 2000 5")

def main():
    parser = argparse.ArgumentParser(description="Calculate CAGR")
    parser.add_argument('--print-expected-input', action='store_true', help="Print the expected input format")
    parser.add_argument('initial_value', type=float, nargs='?', help="The initial value of the investment")
    parser.add_argument('final_value', type=float, nargs='?', help="The final value of the investment")
    parser.add_argument('years', type=float, nargs='?', help="The number of years over which the investment grows")
    args = parser.parse_args()

    if args.print_expected_input:
        print_expected_input()
        return

    try:
        cagr = calculate_cagr(args.initial_value, args.final_value, args.years)
        print(f"CAGR: {cagr * 100:.2f}%")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()