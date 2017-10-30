#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex
import json
import cPickle
from collections import OrderedDict
functionMap=[]
main_variables={}
line_map={}
function_decl={}
i=0;
import pprint
call_stack=[]
def find_typerefs(node,parent):
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
        elif c.kind==clang.cindex.CursorKind.VAR_DECL or  c.kind==clang.cindex.CursorKind.PARM_DECL:
		variables={}
                scope=c.lexical_parent.displayname if c.lexical_parent else (c.location.file.name if c.location.file else "null3")
                if scope in main_variables:
                	variables=main_variables[scope]
                val=""
                val_t=None
		if c.get_children():
                	for ci in c.get_children():
                        	if ci.kind==clang.cindex.CursorKind.INTEGER_LITERAL:
                                	present=False
                                        for token in ci.get_tokens():
                                        	present=True
                                        if present:
                                        	val=ci.get_tokens().next().spelling
						val_t=ci.type.kind
                                                #variables[c.displayname]=ci.get_tokens().next().spelling
		if val_t == clang.cindex.TypeKind.INT:
			variables[c.displayname]=int(val)
		else:
			variables[c.displayname]=val
                main_variables[scope]=variables
		find_typerefs(c,node.displayname)
	else:
            find_typerefs(c,node.displayname)
    lines={}
    if  node.location.line in line_map:
        lines=line_map[node.location.line]
    lines[node.spelling]={'node':node,'arguments':arguments}
    line_map[node.location.line]=lines
    dast_string=""
    parent_file= node.location.file.name if node.location.file else  (node.lexical_parent.displayname if node.lexical_parent else "null2")
    parent_node= node.lexical_parent.displayname if node.lexical_parent else (node.location.file.name if node.location.file else "null3")
    for j in range(0,i):
    	dast_string+="-"
    if node.kind is clang.cindex.CursorKind.FUNCTION_DECL:
        arg_string=""
        for argument in arguments:
            arg_string+=argument["attr"]+":"+argument["type"]+";"

        arg_string = arg_string[:-1]
	if node.displayname in function_decl:
		if function_decl[node.displayname]['end'] - function_decl[node.displayname]['start'] == 0 and  function_decl[node.displayname]['line'] !=node.location.line:
			function_decl[node.displayname]={'line':node.location.line,'start': node.extent.start.line,'end':node.extent.end.line,'parent': parent_node,'node':node,'arguments':arguments}
	else:
		function_decl[node.displayname]={'line':node.location.line,'start': node.extent.start.line,'end':node.extent.end.line,'parent': parent_node,'node':node,'arguments':arguments}
        print '%s#%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, parent_node,arg_string)
    elif node.kind is clang.cindex.CursorKind.CALL_EXPR:
        arg_string=""
        if len(arguments) !=0:
            for argument in arguments:
                arg_string+=argument["attr"]+":"+argument["type"]+":"+argument["value"]+";"

        arg_string = arg_string[:-1]
        print '%s#%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, parent_node,arg_string)

    else:
        print '%s#%s#%s#%s#%s#%s#%s' % (
            dast_string,node.kind, node.displayname if node.displayname else "null1", node.location.line, node.extent.start.line,
            node.extent.end.line, parent_node)
    i=i-1

def get_variable(variable_name):
	global call_stack
	#print(variable_name)
	for current_scope in reversed(call_stack):
		#current_scope=call_stack[i]
		#print(current_scope)
		if current_scope in main_variables and variable_name in main_variables[current_scope]:
			return variable_name,current_scope
	#print(variable_name)
	return None,None 
def is_number(string):
	try:
   		val = int(string)
		return True
	except ValueError:
		return False

def str_eval(tokens):
	tokens=tokens[:-1]
	value=0
	current_scope=None
	print(tokens)
	for token in tokens:
		if token not in ["==",">=","<=","<",">",")","(","=","+=","-=","*=","/=","++","--","+","-","/","*",";"] and not is_number(token):
			variable,current_scope = get_variable(token)
			#print("exec %s,%s"%( variable,current_scope))
			if not(current_scope and variable and current_scope in main_variables and variable in  main_variables[current_scope]):
				return None
			if main_variables[current_scope][variable]:
				exec(variable + "=" + str(main_variables[current_scope][variable]))
	for token in tokens:
		if token in ["=","+=","-=","*=","/="]:
			lhs=tokens[0]
			rhs=tokens[2:]
			#print(''.join(rhs))
			value=eval(''.join(rhs))
			#print(eval(lhs))
			variable,current_scope = get_variable(lhs)
			#print("eval %s,%s,%s,%s"%( variable,current_scope,lhs,rhs))
			if token == "+=":
				main_variables[current_scope][variable]+=value
			elif token == "/=":
                                main_variables[current_scope][variable]/=value
			elif token == "-=":
                                main_variables[current_scope][variable]-=value
			elif token == "*=":
                                main_variables[current_scope][variable]*=value
			elif token == "=":
                                main_variables[current_scope][variable]=value
			print( main_variables[current_scope][variable])
			break;
		elif token in ["==",">=","<=","<",">"]:
			#print("condition %s"%(''.join(tokens)))
			return eval(''.join(tokens))
                        
 	if current_scope and variable and current_scope in main_variables and variable in  main_variables[current_scope]:		
		return main_variables[current_scope][variable]
	return None
def calc(node):
	#print(node.displayname,node.type.kind)
	if node.kind in [clang.cindex.CursorKind.VAR_DECL,clang.cindex.CursorKind.BINARY_OPERATOR,clang.cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR]:
		
		token_str=[]
                for token in node.get_tokens():
                	token_str.append(token.spelling)
                if node.kind==clang.cindex.CursorKind.VAR_DECL:
			token_str=token_str[1:]
		val=str_eval(token_str)
		#print("token %s value %s"%(token_str,val))
	else:
		for c in node.get_children():
			calc(c)
		
def traverse_build(function_name,node_type=clang.cindex.CursorKind.CALL_EXPR):
	global call_stack
	print("call function %s %s start"%(function_name,node_type))
    	if node_type==clang.cindex.CursorKind.CALL_EXPR:
		call_stack.append(function_name)
	start=-1
	end=-1
	if function_name in function_decl:
		start=function_decl[function_name]['start']
                end=function_decl[function_name]['end']
    	#print("start %s, end %s"%(start,end))
    	if not (start==-1 or end==-1):
        	while start<=end and start in line_map:
            		nodes=line_map[start]
            		for key, value in nodes.iteritems():
				if value['node'].kind==clang.cindex.CursorKind.CALL_EXPR:
					node_name=value['node'].displayname+"("
					for argument in value['arguments'][1:]:
						node_name+=argument['type']+", "
					if len( value['arguments'][1:])>0:
						node_name=node_name[:-2]
					node_name+=")"
					traverse_build(node_name); 
				else:
					calc(value['node'])
            		start+=1
	call_stack=call_stack[:-1]
	print("call function %s end"%(function_name))
index = clang.cindex.Index.create()
tu = index.parse(sys.argv[1])
#print 'Translation unit:', tu.spelling
print(vars(tu.cursor))
pp = pprint.PrettyPrinter(indent=4)
find_typerefs(tu.cursor,sys.argv[1])
pp.pprint(main_variables)
#pp.pprint(function_decl["foo(int, int)"])
#pp.pprint(line_map)
traverse_build("main(int, char **)")
pp.pprint(main_variables)
