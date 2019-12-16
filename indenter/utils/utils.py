import subprocess, os, sys, argparse, time, re

from lark import Lark
import logging

from .indent.visit import *

class Utils(object):
    @staticmethod
    def parseArgs():
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-f', '--file', metavar = '\b', help = "File to parse and indent.")
        group.add_argument('-d', '--dir', metavar = '\b', help = "Directory to parse and indent.")
        parser.add_argument('-p', '--parse', action = "store_true", help = "File to parse only.")
        parser.add_argument('-o', '--outdir', metavar = '\b', required=True, help = "Output directory.")
        parser.add_argument('-v', '--verbose', action = "store_true", help = "Print debug messages to stdout.")
        parser.add_argument('-t', '--timeout', metavar = '\b', type=int, default=10, help="Set the execution timeout.")
        parser.add_argument('-e', '--earley', action = "store_true", help = "Use Earley parser. Default is LALR.")
        return parser

    @staticmethod
    def zeek_parser(isEarley):
        kwargs = dict(propagate_positions=True, rel_to=__file__, start='zeek')
        if isEarley:
            return Lark.open('zeek-earley.lark', parser='earley', **kwargs)
        else:
            logging.basicConfig(level=logging.DEBUG)
            return Lark.open('zeek-lalr.lark', parser='lalr', **kwargs, debug=False)

    @staticmethod 
    def zeek_can_parse(f):
        Utils.runCmd(['zeek', '-a', f], "Zeek script parsing failed.", False)

    @staticmethod 
    def runCmd(cmd, err, flag):
        try:
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
            try:
                outs, errs = proc.communicate()
                if proc.returncode != 0:
                    if flag:
                        print('\nProcess returned an error.' + 
                            '\nstderr: {}\nstdout: {}'.format(errs.decode(
                            'utf-8'), outs.decode('utf-8')))
                    raise Exception("ZeekParseError")
                return outs
            except subprocess.SubprocessError:
                proc.kill()
                if flag:
                    print ("Subprocess returned an error.")
                raise Exception("ZeekParseError")
        except Exception as exc:
            if flag:
                print (exc)
            raise Exception("ZeekParseError")

    @staticmethod
    def parse(zeek_parser, fp, debug_flag):
        # adapted from https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
        def remove_comments(string):
            # check if '#' is not part of a quoted string or a regular expression
            pattern = r"(\".*?\"|\'.*?\'|/.*/)|(#[^\r\n]*$)"
            regex = re.compile(pattern)
            def _replacer(match):
                if match.group(2) is not None:
                    if string.lstrip() == match.group(2):
                        return string
                    return ""
                else:
                    return match.group(1)
            return regex.sub(_replacer, string)

        def read(fn):
            with open(fn) as f:
                lines = f.readlines()
            content = [remove_comments(re.sub('[ \t]+', ' ', x.strip())) for x in lines]
            return "\n".join(content)

        try:
            content = read(os.path.join(fp))
            return zeek_parser.parse(content)
        except Exception as exc:
            if debug_flag:
                print (exc)
            if str(exc) == "TimeoutError":
                raise Exception("TimeoutError")
            raise Exception("LarkParseError")       

    @staticmethod
    def indent_file(parser, fp, idx, ofile, summary_flag, debug_flag):
        start = time.time()
        tree = Utils.parse(parser, fp, debug_flag)
        mid = time.time()
        try:
            node = transform(indent=0, node=tree, outfile=ofile, debug=debug_flag)
            node.pretty()
        except Exception as exc:
            if debug_flag:
                print (exc)
            if str(exc) == "TimeoutError":
                raise Exception("TimeoutError")
            raise Exception("TransformError")
        end = time.time()
        if summary_flag:
            print("\nAnalyzed 1 Zeek file.\nParse time:\t%s secs.\nTransform time:\t%s secs.\n" % (mid - start, end - mid))
        Utils.zeek_can_parse(ofile)

    @staticmethod
    def printProgress(iteration, total, prefix='', suffix='', file='', decimals=1, bar_length=100):
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\033[FAnalyzing %s\033[K\n' % (file)),
        sys.stdout.write('%s |%s| %s%s (%s/%s) %s\r\033[A' % (prefix, bar, percents, '%', iteration, total, suffix)),
        
        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    @staticmethod
    def traverseParseTree(node):
        def _traverse(node, level, indent_str):
            if len(node.children) == 1 and not isinstance(node.children[0], Tree):
                return [ indent_str*level, node.data, ' ', '%s' % (node.children[0],), '\n']

            l = [ indent_str*level, node.data, '\n' ]
            for n in node.children:
                if isinstance(n, Tree):
                    l += _traverse(n, level+1, indent_str)
                else:
                    l += [ indent_str*(level+1), '%s' % (n,), '\n' ]

            return l

        return ''.join(_traverse(node, 0, ' '))

    @staticmethod
    def queryParseTree(nodes, queryNodeNames):
        """
        * nodes is a list of root nodes in the parse tree.
        * queryNodeNames is a list of node names that must occur in sequence for 
        the function to return the terminal identifier for that path from the root.
        * The function returns a list of satisfying terminal identifiers.
        """
        def _queryParseTree(node, queryNodeName):
        
            def _isInstance(node):
                if not isinstance(node, Tree):
                    return False
                return True

            def _traverse(node):
                nodes = []
                if node.data == queryNodeName:
                    nodes += [node]
                for n in node.children:
                    if _isInstance(n):
                        nodes += _traverse(n)

                return nodes

            return _traverse(node)

        tmp = []
        for i in range(len(queryNodeNames)):
            name = queryNodeNames[i]
            for node in nodes:
                tmp += _queryParseTree(node, name)
            nodes = tmp
            tmp = []
        return nodes