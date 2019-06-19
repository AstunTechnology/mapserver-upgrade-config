import argparse
import mappyfile
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile", type=str, help="the map file to be processed")
    parser.add_argument("outputfile", type=str, help="the file to write output to")
    parser.add_argument("--layers", type=str, help="comma separated list of layers to remove.")

    args = parser.parse_args()
    layers=[]
    for l in args.layers.split(','):
        layers.append(l);
    remove(args.inputfile, args.outputfile, layers)


def remove(infile, outfile, layers):
    ifile = open(infile,'r')
    mf = mappyfile.load(ifile, expand_includes=False)
    for l in layers:
        ml=mappyfile.find(mf["layers"],"name",l)
        mf["layers"].remove(ml)
    mappyfile.save(mf, outfile)


if __name__ == "__main__":
    main()
                      
