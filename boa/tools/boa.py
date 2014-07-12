from argparse import ArgumentParser

parser = ArgumentParser(
    prog='boa',
    description='Compile some python files and '
                'bundle them into a browser-ready JS file.'
)

parser.add_argument(
    'dirs',
    nargs='+',
    help='a list of directories to recursively scan for files'
)

parser.add_argument(
    '--main', '-m',
    metavar='main',
    help='specify a main file to be run when the whole file is executed'
)

parser.add_argument(
    '--out', '-o',
    metavar='output',
    help='specify an output file for the bundle'
)

parser.add_argument(
    '--print', '-p',
    action='store_true',
    help='print the output to standard out'
)

args = parser.parse_args()
print args