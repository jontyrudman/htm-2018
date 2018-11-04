def generate(filename):
    import markovify

    # Get raw text as string.
    with open(filename) as f:
        text = f.read()

    # Build the model.
    text_model = markovify.NewlineText(text, state_size=3)

    # Print five randomly-generated sentences
    for i in range(5):
        print(text_model.make_sentence())

    # Print three randomly-generated sentences of no more than 140 characters
    for i in range(3):
        print(text_model.make_short_sentence(140))




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='Local Path for text model (.txt)')
    args = parser.parse_args()
    print(generate('{}'.format(args.path)))
