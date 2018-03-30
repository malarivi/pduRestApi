
import argparse
import pprint

def get_args():
    parser = argparse.ArgumentParser(description='Personal Data')
    parser.add_argument('-n', '--name', nargs='*', default='n/a')
    parser.add_argument('-a', '--age', default=0, type=int)
    parser.add_argument('-m', '--is-male', action='store_true')

    return parser.parse_args()

args = get_args()
print(args)

pprint.pprint(vars(args)), width=1, indent=2
