import argparse
import mappyfile


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile", type=str, help="the map file to be processed")
    parser.add_argument("outputfile", type=str, help="the file to write output to")

    args = parser.parse_args()

    print("input "+args.inputfile)
    print("output "+args.outputfile)

    ifile = open(args.inputfile, 'r')
    mf = mappyfile.load(ifile, expand_includes=False)

    mappyfile.write(mf, args.outputfile)


if __name__ == "__main__":
    main()
