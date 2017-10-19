#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex

def find_typerefs(node):
    """ Find all references to the type named 'typename'
    """
    print 'TYPE:%s#NAME:%s#LINE:%s#START:%s#END:%s#PARENT:%s' % (node.kind,node.displayname, node.location.line, node.extent.start.line,node.extent.end.line,node.lexical_parent.displayname if node.lexical_parent else "null")
    for c in node.get_children():
	find_typerefs(c)

index = clang.cindex.Index.create()
tu = index.parse(sys.argv[1])
print 'Translation unit:', tu.spelling
find_typerefs(tu.cursor)
