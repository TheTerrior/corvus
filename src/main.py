import os
import argparse
import tokenizer
import ambester.parser


def main() -> None:
    """Main entry point."""
    argparser = argparse.ArgumentParser(
        prog = "corvus",
    )

    # non-positional arguments
    argparser.add_argument("-V", "--version", action = "version", version = "%(prog)s 0.1")

    # required arguments
    argparser.add_argument("<FILE>", help = "input file")

    # optional arguments
    argparser.add_argument("-l", "--lang", action = "store", choices = ["python"], default = "python", help = "output language")
    argparser.add_argument("-o", "--output", action = "store", dest = "<OUT>", help = "output file")

    args = vars(argparser.parse_args())

    file: str = args["<FILE>"]
    if not os.path.isfile(file):
        print(f"Error: file \"{file}\" does not exist")
        return

    extension = file[file.rfind('.')+1:]
    match extension:
        case "ambester":

            print("Tokenizing...")
            tokens = tokenizer.tokenize(args["<FILE>"]).unwrap() #throws any errors that exist

            print(tokens)

            #print("Parsing...")
            #ast = ambester.parser.parse(tokens)

            #if isinstance(ast[1], str):
            #    print(ast[1])
            #    return

            #print(ast[1])
            #parser.verify_ast(ast[1])

        case "nm":
            print("error: language not yet implemented")
            pass
        case "laev":
            print("error: language not yet implemented")
            pass
        case _:
            print("error: filetype not supported")


if __name__ == "__main__":
    main()

