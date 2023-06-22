import os
import argparse
import tokenizer
import parser


def main() -> None:
    """Main entry point."""
    argparser = argparse.ArgumentParser(
            prog = "corvus",
            )
    # non-positional
    argparser.add_argument("-V", "--version", action = "version", version = "%(prog)s 0.1")

    # required
    argparser.add_argument("<FILE>", help = "input file")

    # optional
    argparser.add_argument("-l", "--lang", action = "store", choices = ["python"], default = "python", help = "output language")
    argparser.add_argument("-o", "--output", action = "store", dest = "<OUT>", help = "output file")

    args = vars(argparser.parse_args())

    if not os.path.isfile(args["<FILE>"]):
        print(f"Error: file \"{args['<FILE>']}\" does not exist")
        return

    print("Tokenizing...")
    tokens = tokenizer.tokenize(args["<FILE>"])
    print(tokens)

    print("Parsing...")
    parsed = parser.parse(tokens)
    print(parsed)


if __name__ == "__main__":
    main()

