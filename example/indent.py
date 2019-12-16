#!/usr/bin/env python3.6

from indenter import ZeekIndenter
from indenter.utils import Utils

def getExportedOptionIDs(root):
    # the second argument list is the list of nodes as defined in the Zeek grammar
    nodes = Utils.queryParseTree([root], ["export_decl", "option_decl", "id"])
    lst = []
    for n in nodes:
        token = "".join([x for x in n.children])
        lst.append(token)
    return lst

def main():
    parser = Utils.parseArgs()
    args = parser.parse_args()

    DEBUG_FLAG = True if args.verbose else False
    TIMEOUT = args.timeout
    EARLEY = True if args.earley else False
    ZEEK_PARSER = Utils.zeek_parser(EARLEY)

    indent = ZeekIndenter(TIMEOUT, DEBUG_FLAG, ZEEK_PARSER)

    if args.file:
        if args.parse:
            tree = indent.parse_file(args.file, True)
            # do something with the parse tree
            # traverse the tree
            print (Utils.traverseParseTree(tree))
            # filter the nodes to print IDs
            print (getExportedOptionIDs(tree))
        else:
            indent.indent_file(args.file, 1, args.outdir, True)
    
    if args.dir:
        if args.parse:
            parser.error("-d/--dir does not currently support -p/--parse.")
        else:
            indent.indent_directory(args.dir, args.outdir)

if __name__ == '__main__':
	main()