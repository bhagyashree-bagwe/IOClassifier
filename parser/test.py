#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex
import json
import cPickle
from collections import OrderedDict
functionMap=[]
i=0;
def find_typerefs(node,filename):
    global i
    """ Find all references to the type named 'typename'
    """
    #if not node.displayname=="" and filename in str(node.location) and node and ((node.kind in [clang.cindex.CursorKind.FUNCTION_DECL,clang.cindex.CursorKind.CXX_METHOD,clang.cindex.CursorKind.VAR_DECL,clang.cindex.CursorKind.CLASS_DECL] and node.lexical_parent and node.lexical_parent.displayname) or node.kind==clang.cindex.CursorKind.CALL_EXPR):
    arguments = []
    i=i+1
    for c in node.get_children():
        if c.kind==clang.cindex.CursorKind.PARM_DECL:
            arguments.append({'attr':c.displayname,'type':c.type.spelling})
            functionMap.append({node.displayname: arguments});
        elif c.kind==clang.cindex.CursorKind.UNEXPOSED_EXPR:
            arguments.append({'attr':c.displayname,'type':c.type.spelling,'value':str(c.data)})
        else:
            find_typerefs(c,filename)
    dast_string=""
    for j in range(0,i):
        dast_string+="-";
    if node.kind is clang.cindex.CursorKind.FUNCTION_DECL:
        arg_string=""
        for argument in arguments:
            arg_string+=argument["attr"]+":"+argument["type"]+";"

        arg_string = arg_string[:-1]
        print '%s#%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, node.lexical_parent.displayname if node.lexical_parent else "null2",arg_string)
    elif node.kind is clang.cindex.CursorKind.CALL_EXPR:
        arg_string=""
        if len(arguments) !=0:
            for argument in arguments:
                arg_string+=argument["attr"]+":"+argument["type"]+":"+argument["value"]+";"

        arg_string = arg_string[:-1]
        print '%s#%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, node.lexical_parent.displayname if node.lexical_parent else "null2",arg_string)

    else:
        print '%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, node.lexical_parent.displayname if node.lexical_parent else "null2")
    i=i-1

index = clang.cindex.Index.create()
tu = index.parse(sys.argv[1])
#print 'Translation unit:', tu.spelling
print(vars(tu.cursor))
find_typerefs(tu.cursor,sys.argv[1])
