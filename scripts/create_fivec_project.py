#!/usr/bin/env python

import sys
import optparse

import hifive


def main():
    usage = "usage: %prog [options] <data_file> <out_file>\n\nArguments:"
    usage += "\n<data_file>  HiFive 5C data file"
    usage += "\n<out_file>   destination for 5C project file"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--min-interactions", dest="minint", default=20, metavar="MININT", type="int",
                      help="minimum number of interactions needed for valid fragment [default: %default]",
                      action="store")
    parser.add_option("-m", "--min-distance", dest="mindist", default=0, metavar="MINDIST", type="int",
                      help="minimum interaction distance to include in learning [default: %default]",
                      action="store")
    parser.add_option("-x", "--max-distance", dest="maxdist", default=0, metavar="MAXDIST", type="int",
                      help="maximum interaction distance to include in learning [default: %default]",
                      action="store")
    parser.add_option("-q", "--quiet", dest="silent", action="store_true", default=False,
                      help="silence output messages [default: %default]")
    options, args = parser.parse_args()
    if len(args) < 2:
        parser.error('incorrect number of arguments')
    fivec = hifive.FiveC(args[1], 'w', silent=options.silent)
    fivec.load_data(args[0])
    fivec.filter_fragments(mininteractions=options.minint, mindistance=options.mindist, maxdistance=options.maxdist)
    fivec.find_distance_parameters()
    fivec.save()


if __name__ == "__main__":
    main()