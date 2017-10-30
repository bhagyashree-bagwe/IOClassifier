import sys
import clang.cindex
import json
import cPickle 
from collections import OrderedDict
import pprint

arguments={}
parents=[]
def find_typerefs(node,filename):
	#global i
	#arguments={}
	#i=i+1
	print("%s %s"%(node.displayname,node.semantic_parent.displayname if node.semantic_parent else "null"))
	
	#if node.displayname==filename or (node.semantic_parent and node.semantic_parent.displayname and node.semantic_parent.displayname in parents):
		#parents.append(node.displayname)	
	for c in node.get_children():
		parents.append(c.displayname)
		if c.kind==clang.cindex.CursorKind.VAR_DECL or  c.kind==clang.cindex.CursorKind.PARM_DECL:
			variables={}
			scope=c.lexical_parent.displayname if c.lexical_parent and c.lexical_parent.displayname and not c.lexical_parent.displayname==filename else "Global"
			if scope in arguments:
				variables=arguments[scope]
			val=""
			if c.get_children():
				for ci in c.get_children():
					if ci.kind==clang.cindex.CursorKind.INTEGER_LITERAL:
						present=False
						for token in ci.get_tokens():
							present=True
						if present:
							val=ci.get_tokens().next().spelling
						#variables[c.displayname]=ci.get_tokens().next().spelling
			variables[c.displayname]=val
			arguments[scope]=variables
		#arugments.append(c.lexical_parent.dispalyname if c.lexical_parent else "Global" : {)
		#arguments['Scope' : c.lexical_parent.displayname if c.lexical_parent else "global"] = 'variablenmae': c.dissplaynam
		else:
			find_typerefs(c,filename)
		#print arguments




index = clang.cindex.Index.create()
tu = index.parse(sys.argv[1])
#print(vars(tu.cursor))
parents.append(sys.argv[1])
find_typerefs(tu.cursor,sys.argv[1])
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(arguments)
#pprint arguments
