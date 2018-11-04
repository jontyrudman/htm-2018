import markovify
from util import *

def generate(filename):

    # Get raw text as string.
    with open(filename) as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text, state_size=2)

    # Print five randomly-generated sentences
    for i in range(5):
        print(text_model.make_sentence())

def create_model(file):
    text = read_file(file)
    output = open(file+'.json', 'w')
    output.write(markovify.Text(text, state_size=2))
    output.close()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='Local Path for text model (.txt)')
    args = parser.parse_args()
    print(generate('{}'.format(args.path)))
