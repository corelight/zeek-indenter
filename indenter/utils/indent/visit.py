from lark.tree import Tree
from .format import *

import sys, textwrap, re

# this limit is too high, but needed when using python3.6 for one particular
# test case where the number of entries in the expression lists is huge.
# note, that the same test case passes with a lower limit (5000) with pypy3.
sys.setrecursionlimit(10000)

fmt = None
DEBUG = False

def transform(indent, node, outfile=None, debug=False):
    global fmt, DEBUG

    def isinstance_(node, name):
        if not isinstance(node, Tree):
            return True
        return node.data == name

    if outfile:
        fmt = FormatCode(outfile)
        DEBUG = debug

    meta = dict({"lineno": "-", "column": "-", "symbol": "-"})
    if hasattr(node, "meta"):
    	if hasattr(node.meta, "line"):
    		meta["lineno"] = node.meta.line
    		meta["column"] = node.meta.column
    meta["symbol"] = node if isinstance_(node, "token") else "-"

    if isinstance_(node, "token"):
        evalStr = "Node_Token(meta, indent, node)"
    else:
        evalStr = "Node_" + node.data.title() + "(meta, indent, node.children)"

    return eval(evalStr)

class Node(Tree):
    tag = 'Node'
    
    def __init__(self, meta, indent):
        self.indent = indent
        if DEBUG:
        	sys.stderr.write('%s - %s [%s] @ %s, %s\n' % ('\t'*indent, self.tag, meta["symbol"], meta["lineno"], meta["column"]))
        return

    def line_init(self):
        fmt.line_init(self.indent)
        return self

    def line_more(self, chunk=Constants.NULL, can_break_after=False,):
        fmt.line_more(chunk, can_break_after,)
        return self

    def line_term(self):
        fmt.line_term()
        return self

    def pretty(self):
        for node in self.nodes:
            node.pretty()
        return self

    def addNewline(self):
        self.line_init()
        self.line_term()

    def addComment(self, comment):
    	comment = ' '.join(re.sub(' +', ' ', comment.strip()).split())
    	# Compensate '3' characters for the '## '
    	comments = textwrap.wrap(comment, Constants.COL_LIMIT-self.indent-3)
    	for i in range(len(comments)):
    		self.line_init()
    		self.line_more("## " + comments[i])
    		self.line_term()
    	return self

    def wrap(self):
    	comment = ""
    	for node in self.nodes:
    		text = re.sub('[# \t\r\n]+', ' ', node.to_str()).strip()
    		if len(text):
    			comment += text + " "
    	self.addComment(comment)
    	return self

class Node_Token(Node):
	tag = "token"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.token = "".join([x for x in nodes])
		return

	def pretty(self):
		self.line_more(self.token)
		return self

	def to_str(self):
		return self.token

class Node_Stmt_If_Else_Comments(Node):
	tag = "stmt_if_else_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Expr_Last_Comment(Node):
	tag = "expr_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_term()
		self.wrap()
		self.line_init()
		return self

class Node_Expr_Comment(Node):
	tag = "expr_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Case_With_Comments(Node):
	tag = "case_with_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_Last_Comment(Node):
	tag = "stmt_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Type_Decl_With_Comments(Node):
	tag = "type_decl_with_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		l = len(self.nodes)
		if l > 1:
			self.line_term()
			self.nodes[0].pretty()
			self.line_init()
		self.nodes[-1].pretty()
		return self

class Node_Enum_Body_Elem_With_Comments(Node):
	tag = "enum_body_elem_with_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		l = len(self.nodes)
		if l > 1:
			self.line_term()
			self.nodes[0].pretty()
			self.line_init()
		self.nodes[-1].pretty()
		return self	

class Node_Decl_With_Comments(Node):
	tag = "decl_with_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_With_Comments(Node):
	tag = "stmt_with_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Enum_Body_Last_Comment(Node):
	tag = "enum_body_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_term()
		self.wrap()
		self.line_init()
		return self

class Node_Enum_Body_Elem_Comments(Node):
	tag = "enum_body_elem_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Case_Comments(Node):
	tag = "case_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Case_Last_Comment(Node):
	tag = "case_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Type_Decl_Last_Comment(Node):
	tag = "type_decl_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_term()
		self.wrap()
		self.line_init()
		return self

class Node_Type_Decl_Comments(Node):
	tag = "type_decl_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Zeek_Comments(Node):
	tag = "zeek_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Decl_Comments(Node):
	tag = "decl_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Decl_Last_Comment(Node):
	tag = "decl_last_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Stmt_Comments(Node):
	tag = "stmt_comments"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.wrap()
		return self

class Node_Zeek(Node):
	tag = "zeek"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in self.nodes:
			node.pretty()
		fmt.close()
		return self

class Node_Decl_List(Node):
	tag = "decl_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:-1]:
			node.pretty()
			self.addNewline()
		if len(self.nodes) > 0:
			self.nodes[-1].pretty()
		return self

class Node_Opt_Expr(Node):
	tag = "opt_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_1(Node):
	tag = "expr_1"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_2(Node):
	tag = "expr_2"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_(Node):
	tag = "expr_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more("", can_break_after=True)
		self.nodes[1].pretty()
		self.nodes[2].pretty()		
		return self

class Node_Expr_Copy(Node):
	tag = "expr_copy"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_more(" " + self.nodes[0].to_str() + " ", can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Atom(Node):
	tag = "expr_atom"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Incr(Node):
	tag = "expr_incr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_more(" " + self.nodes[0].to_str(), can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Decr(Node):
	tag = "expr_decr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_more(" " + self.nodes[0].to_str(), can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Not(Node):
	tag = "expr_not"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		return self

class Node_Expr_Tilde(Node):
	tag = "expr_tilde"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		return self

class Node_Expr_Minus(Node):
	tag = "expr_minus"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		return self

class Node_Expr_Plus(Node):
	tag = "expr_plus"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		return self

class Node_Expr_Add(Node):
	tag = "expr_add"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Add_To(Node):
	tag = "expr_add_to"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Sub(Node):
	tag = "expr_sub"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Remove_From(Node):
	tag = "expr_remove_from"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Multiply(Node):
	tag = "expr_multiply"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Divide(Node):
	tag = "expr_divide"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Modulo(Node):
	tag = "expr_modulo"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_And(Node):
	tag = "expr_and"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Or(Node):
	tag = "expr_or"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Caret(Node):
	tag = "expr_caret"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_And_And(Node):
	tag = "expr_and_and"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Or_Or(Node):
	tag = "expr_or_or"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Eq(Node):
	tag = "expr_eq"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Ne(Node):
	tag = "expr_ne"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Lt(Node):
	tag = "expr_lt"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Le(Node):
	tag = "expr_le"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Gt(Node):
	tag = "expr_gt"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Ge(Node):
	tag = "expr_ge"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Ternary(Node):
	tag = "expr_ternary"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		self.line_more(" " + self.nodes[3].to_str() + " ", can_break_after=True)
		self.nodes[4].pretty()
		return self

class Node_Expr_Equals(Node):
	tag = "expr_equals"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Local_Assign(Node):
	tag = "expr_local_assign"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_more(" " + self.nodes[2].to_str() + " ", can_break_after=True)
		self.nodes[3].pretty()
		return self

class Node_Expr_Expr_List(Node):
	tag = "expr_expr_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Dollar(Node):
	tag = "expr_dollar"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		return self

class Node_Expr_Dollar_Id(Node):
	tag = "expr_dollar_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" " + self.nodes[2].to_str() + " ", can_break_after=True)
		self.nodes[3].pretty()
		return self

class Node_Expr_Dollar_Func(Node):
	tag = "expr_dollar_func"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent, nodes[2]), transform(indent, nodes[3]),
						transform(indent+1, nodes[4])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_more(self.nodes[3].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[4].pretty()
		self.line_init()
		return self

class Node_Expr_In(Node):
	tag = "expr_in"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" in ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Not_In(Node):
	tag = "expr_not_in"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" !in ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Expr_List_(Node):
	tag = "expr_expr_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Empty(Node):
	tag = "expr_empty"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		return self

class Node_Expr_Record(Node):
	tag = "expr_record"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[3].pretty()
		return self

class Node_Expr_Opt_List_(Node):
	tag = "expr_opt_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more("", can_break_after=True)
		for node in (self.nodes)[1:-1]:
			node.pretty()
		self.line_more("", can_break_after=True)
		self.nodes[-1].pretty()
		return self

class Node_Expr_Opt_List_Opt_Attr(Node):
	tag = "expr_opt_list_opt_attr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Table(Node):
	tag = "expr_table"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more("", can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Set(Node):
	tag = "expr_set"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Vector(Node):
	tag = "expr_vector"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Opt_List(Node):
	tag = "expr_opt_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Hook(Node):
	tag = "expr_hook"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		return self

class Node_Expr_Has_Field(Node):
	tag = "expr_has_field"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Schedule(Node):
	tag = "expr_schedule"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent+1, nodes[2]), transform(indent+1, nodes[3]),
						transform(indent+1, nodes[4])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_more(" " + self.nodes[2].to_str() + " ", can_break_after=True)
		self.nodes[3].pretty()
		self.line_more(" ")
		self.nodes[4].pretty()
		return self

class Node_Expr_Regex(Node):
	tag = "expr_regex"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Size(Node):
	tag = "expr_size"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_As(Node):
	tag = "expr_as"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Is(Node):
	tag = "expr_is"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_Without_Comment(Node):
	tag = "expr_without_comment"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr(Node):
	tag = "expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	# def pretty(self):
	# 	if len(self.nodes) == 2:
	# 		self.line_term()
	# 		self.nodes[0].pretty()
	# 		self.line_init()
	# 		self.nodes[1].pretty()
	# 	else:
	# 		self.nodes[0].pretty()
	# 	return self

class Node_Expr_List_1(Node):
	tag = "expr_list_1"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Expr_List_2(Node):
	tag = "expr_list_2"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		l = len(self.nodes)
		if l == 1:
			self.nodes[0].pretty()
		else:
			self.line_term()
			self.nodes[0].pretty()
			self.line_init()
			self.nodes[1].pretty()
		return self

class Node_Expr_List(Node):
	tag = "expr_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Expr_List(Node):
	tag = "opt_expr_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Enum_Body(Node):
	tag = "enum_body"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		for node in (self.nodes)[1:]:
			node.pretty()
		self.line_term()
		return self

class Node_Enum_Body_List_(Node):
	tag = "enum_body_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str())
		self.line_term()
		self.line_init()
		self.nodes[2].pretty()
		return self

class Node_Enum_Body_List(Node):
	tag = "enum_body_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Enum_Body_Elem_Id_1(Node):
	tag = "enum_body_elem_id_1"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:1]:
			node.pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ")
			node.pretty()
		return self

class Node_Enum_Body_Elem_Id_2(Node):
	tag = "enum_body_elem_id_2"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:1]:
			node.pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ")
			node.pretty()
		return self

class Node_Enum_Body_Elem_Id_3(Node):
	tag = "enum_body_elem_id_3"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:1]:
			node.pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ")
			node.pretty()
		return self

class Node_Enum_Body_Elem(Node):
	tag = "enum_body_elem"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Int(Node):
	tag = "type_simple_int"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Interval(Node):
	tag = "type_simple_interval"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Count(Node):
	tag = "type_simple_count"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Counter(Node):
	tag = "type_simple_counter"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Opaque(Node):
	tag = "type_simple_opaque"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Type_Simple_Time(Node):
	tag = "type_simple_time"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple_Timer(Node):
	tag = "type_simple_timer"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Simple(Node):
	tag = "type_simple"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Set(Node):
	tag = "type_set"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent+1, nodes[2]), transform(indent, nodes[3])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		return self

class Node_Type_Table(Node):
	tag = "type_table"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent+1, nodes[2]), transform(indent, nodes[3]),
						transform(indent, nodes[4]), transform(indent, nodes[5])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		self.line_more(" ")
		self.nodes[4].pretty()
		self.line_more(" ")
		self.nodes[5].pretty()
		return self

class Node_Type_Record(Node):
	tag = "type_record"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent+1, nodes[2]), transform(indent, nodes[3])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		return self

class Node_Type_Union(Node):
	tag = "type_union"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		return self

class Node_Type_Enum(Node):
	tag = "type_enum"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent+1, nodes[2]), transform(indent, nodes[3])
					 ]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		return self

class Node_Type_List_Type(Node):
	tag = "type_list_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ")
		self.nodes[2].pretty()
		return self

class Node_Type_Vector(Node):
	tag = "type_vector"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ")
		self.nodes[2].pretty()
		return self

class Node_Type_Func(Node):
	tag = "type_func"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes):
			node.pretty()
		return self

class Node_Type_Event(Node):
	tag = "type_event"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		for node in (self.nodes)[2:-1]:
			node.pretty()
		self.nodes[-1].pretty()
		return self

class Node_Type_Hook(Node):
	tag = "type_hook"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		for node in (self.nodes)[2:-1]:
			node.pretty()
		self.nodes[-1].pretty()
		return self

class Node_Type_File(Node):
	tag = "type_file"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[1].pretty()
		self.line_more(" ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Type_Id(Node):
	tag = "type_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_Complex(Node):
	tag = "type_complex"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in self.nodes:
			node.pretty()
		return self		

class Node_Type(Node):
	tag = "type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Type_List(Node):
	tag = "type_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		num = len(self.nodes)
		for n in range(0, num-1, 2):
			self.line_init()
			self.nodes[n].pretty()
			self.nodes[n+1].pretty()
			self.line_term()
		self.line_init()
		self.nodes[num-1].pretty()
		self.line_term()
		return self

class Node_Type_Decl_List(Node):
	tag = "type_decl_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		for node in (self.nodes)[:-1]:
			node.pretty()
			# self.line_more(" ", can_break_after=True)
			self.line_term()
			self.line_init()
		if len(self.nodes) > 0:
			self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Type_Decl(Node):
	tag = "type_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ")
		self.nodes[2].pretty()
		for node in (self.nodes)[3:-1]:
			self.line_more(" ")
			node.pretty()
		self.nodes[-1].pretty()
		return self

class Node_Formal_Args(Node):
	tag = "formal_args"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Formal_Args_Decl_List_Semicolon(Node):
	tag = "formal_args_decl_list_semicolon"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		num = len(self.nodes)
		for n in range(0, num-1, 2):
			self.nodes[n].pretty()
			self.line_more(self.nodes[n+1].to_str(), can_break_after=True)
			self.line_more(" ")
		self.nodes[num-1].pretty()
		return self

class Node_Formal_Args_Decl_List_Comma(Node):
	tag = "formal_args_decl_list_comma"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		num = len(self.nodes)
		for n in range(0, num-1, 2):
			self.nodes[n].pretty()
			self.line_more(self.nodes[n+1].to_str(), can_break_after=True)
			self.line_more(" ")
		self.nodes[num-1].pretty()
		return self

class Node_Formal_Args_Decl_List(Node):
	tag = "formal_args_decl_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Formal_Args_Decl(Node):
	tag = "formal_args_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str() + " ", can_break_after=True)
		for node in (self.nodes)[2:-1]:
			node.pretty()
			self.line_more(" ")
		self.nodes[-1].pretty()
		return self

class Node_Module_Decl(Node):
	tag = "module_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_term()
		return self

class Node_Export_Decl(Node):
	tag = "export_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]),
						transform(indent, nodes[1]), 
						transform(indent + 1, nodes[2]), 
						transform(indent, nodes[3])
					 ]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		self.nodes[3].pretty()
		self.line_term()
		return self

class Node_Global_Decl(Node):
	tag = "global_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		for node in (self.nodes)[2:-1]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
		self.nodes[-1].pretty()
		self.line_term()
		return self		

class Node_Option_Decl(Node):
	tag = "option_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		for node in (self.nodes)[2:-1]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
		self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Const_Decl(Node):
	tag = "const_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		for node in (self.nodes)[2:-1]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
		self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Global_Type_Decl(Node):
	tag = "global_type_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_more(" ")
		self.nodes[3].pretty()
		for node in (self.nodes)[4:-1]:
			self.line_more(" ")
			node.pretty()
		self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Redef_Global_Decl(Node):
	tag = "redef_global_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		for node in (self.nodes)[:2]:
			node.pretty()
			self.line_more(" ")
		for node in (self.nodes)[2:-1]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
		self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Redef_Enum_Decl(Node):
	tag = "redef_enum_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), 
						transform(indent, nodes[2]), transform(indent, nodes[3]), 
						transform(indent, nodes[4]), transform(indent+1, nodes[5]),
						transform(indent, nodes[6]), transform(indent, nodes[7])
					 ]
		return

	def pretty(self):
		self.line_init()
		for node in (self.nodes)[:5]:
			node.pretty()
			self.line_more(" ")
		self.line_term()
		self.nodes[5].pretty()
		self.line_init()
		for node in (self.nodes)[6:]:
			node.pretty()
		self.line_term()
		return self

class Node_Redef_Record_Decl(Node):
	tag = "redef_record_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), 
						transform(indent, nodes[2]), transform(indent, nodes[3]), 
						transform(indent, nodes[4]), transform(indent+1, nodes[5]),
					 ] + [transform(indent, node) for node in (nodes)[6:]]
		return

	def pretty(self):
		self.line_init()
		for node in (self.nodes)[:5]:
			node.pretty()
			self.line_more(" ")
		self.line_term()
		self.nodes[5].pretty()
		self.line_init()
		for node in (self.nodes)[6:]:
			node.pretty()
		self.line_term()
		return self	

class Node_Redef_Decl(Node):
	tag = "redef_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Func_Decl(Node):
	tag = "func_decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.function_hdr = [transform(indent, x) for x in nodes[:-1]]
		self.function_body = transform(indent+1, nodes[-1])
		return

	def pretty(self):
		for node in self.function_hdr:
			node.pretty()
		self.function_body.pretty()
		return self

class Node_Decl(Node):
	tag = "decl"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in self.nodes:
		 	node.pretty()
		return self

class Node_Directives(Node):
	tag = "directives"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		for node in (self.nodes)[:1]:
			node.pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Conditional_List(Node):
	tag = "conditional_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Conditional(Node):
	tag = "conditional"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		for node in (self.nodes)[1:]:
			node.pretty()
		self.line_term()
		return self

class Node_Func_Hdr_Global(Node):
	tag = "func_hdr_global"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		for node in (self.nodes)[3:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Func_Hdr_Event(Node):
	tag = "func_hdr_event"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		for node in (self.nodes)[3:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Func_Hdr_Hook(Node):
	tag = "func_hdr_hook"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		for node in (self.nodes)[3:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Func_Hdr_Redef(Node):
	tag = "func_hdr_redef"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_more(" ")
		self.nodes[2].pretty()
		self.nodes[3].pretty()
		for node in (self.nodes)[4:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Func_Hdr(Node):
	tag = "func_hdr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Func_Body(Node):
	tag = "func_body"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_term()
		self.nodes[1].pretty()
		self.line_init()
		self.nodes[2].pretty()
		self.line_term()
		return self

class Node_Anonymous_Function(Node):
	tag = "anonymous_function"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		self.line_init()
		return self

class Node_Begin_Func(Node):
	tag = "begin_func"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Func_Params_Without_Type(Node):
	tag = "func_params_without_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_more(self.nodes[0].to_str(), can_break_after=True)
		for node in (self.nodes)[1:-1]:
			node.pretty()
		self.line_more(self.nodes[-1].to_str(), can_break_after=True)
		return self

class Node_Func_Params_With_Type(Node):
	tag = "func_params_with_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_more(self.nodes[0].to_str(), can_break_after=True)
		for node in (self.nodes)[1:-3]:
			node.pretty()
		self.line_more(self.nodes[-3].to_str(), can_break_after=True)
		self.line_more(self.nodes[-2].to_str(), can_break_after=True)
		self.line_more(" ")
		self.nodes[-1].pretty()
		return self

class Node_Func_Params(Node):
	tag = "func_params"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Type(Node):
	tag = "opt_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		return self

class Node_Init_Class(Node):
	tag = "init_class"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Init(Node):
	tag = "opt_init"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

# class Node_Init_Opt_List_(Node):
# 	tag = "init_opt_list_"

# 	def __init__(self, meta, indent, nodes):
# 		super().__init__(meta, indent)
# 		self.nodes = [transform(indent, node) for node in nodes]
# 		return

# 	def pretty(self):
# 		self.line_init()
# 		for node in self.nodes:
# 			node.pretty()
# 		self.line_term()
# 		return self

class Node_Init_Opt_List(Node):
	tag = "init_opt_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0])] + [transform(indent+1, node) for node in nodes[1:-1]] + [transform(indent, nodes[-1])]
		return

	# def pretty(self):
	# 	self.nodes[0].pretty()
	# 	# self.line_term()
	# 	for node in (self.nodes)[1:-1]:
	# 		node.pretty()
	# 	# self.line_init()
	# 	self.nodes[-1].pretty()
	# 	return self

class Node_Init_Expr_List_(Node):
	tag = "init_expr_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		if len(self.nodes) > 2:
			self.nodes[2].pretty()
		return self

class Node_Init_Expr_List(Node):
	tag = "init_expr_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent+1, nodes[1]), transform(indent, nodes[2])]
		return

class Node_Init_Expr(Node):
	tag = "init_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Init(Node):
	tag = "init"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Index_Slice(Node):
	tag = "index_slice"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Attr(Node):
	tag = "opt_attr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ", can_break_after=True)
			node.pretty()
		return self

# class Node_Attr_List(Node):
# 	tag = "attr_list"

# 	def __init__(self, meta, indent, nodes):
# 		super().__init__(meta, indent)
# 		self.nodes = [transform(indent, node) for node in nodes]
# 		return

# 	def pretty(self):
# 		self.nodes[0].pretty()
# 		for node in (self.nodes)[1:]:
# 			self.line_more(" ", can_break_after=True)
# 			node.pretty()
# 		return self

	# def pretty(self):
	# 	self.nodes[0].pretty()
	# 	if len(self.nodes) > 1:
	# 		self.line_term()
	# 		for node in (self.nodes)[1:-1]:
	# 			self.line_init()
	# 			node.pretty()
	# 			self.line_term()
	# 		self.line_init()
	# 		self.nodes[-1].pretty()
	# 	return self

class Node_Attr_Expr(Node):
	tag = "attr_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return		

class Node_Attr(Node):
	tag = "attr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		if len(self.nodes) > 1:
			self.line_more(self.nodes[1].to_str(), can_break_after=True)
			self.nodes[2].pretty()
		return self

class Node_Stmt_Stmt_List(Node):
	tag = "stmt_stmt_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		for node in (self.nodes)[1:-2]:
			node.pretty()
		self.line_term()
		self.nodes[-2].pretty()
		self.line_init()
		self.nodes[-1].pretty()
		self.line_term()
		return self

class Node_Stmt_Print(Node):
	tag = "stmt_print"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		for node in (self.nodes)[4:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Event(Node):
	tag = "stmt_event"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		for node in (self.nodes)[4:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_If_No_Else(Node):
	tag = "stmt_if_no_else"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		if len(nodes) == 3:
			self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		else:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
							transform(indent+1, nodes[2]), transform(indent+1, nodes[3])
						 ]
		return

	def pretty(self):
		if len(self.nodes) == 3:
			self.line_init()
			self.nodes[0].pretty()
			self.line_more(" ", can_break_after=True)
			self.nodes[1].pretty()
			self.line_term()
			self.nodes[2].pretty()
		else:
			self.line_init()
			self.nodes[0].pretty()
			self.line_more(" ", can_break_after=True)
			self.nodes[1].pretty()
			self.line_term()
			self.nodes[2].pretty()
			self.nodes[3].pretty()
		return self

# class Node_Stmt_Else_No_Brace(Node):
# 	tag = "stmt_else_no_brace"

# 	def __init__(self, meta, indent, nodes):
# 		super().__init__(meta, indent)
# 		self.nodes = [transform(indent, node) for node in nodes]

# 	def pretty(self):
# 		for node in (self.nodes)[1:]:
# 			node.pretty()
# 		# self.nodes[1].pretty()
# 		return self


# class Node_Stmt_Else_Brace(Node):
# 	tag = "stmt_else_brace"

# 	def __init__(self, meta, indent, nodes):
# 		super().__init__(meta, indent)
# 		self.nodes = [transform(indent, node) for node in nodes]

class Node_Stmt_Else(Node):
	tag = "stmt_else"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		if len(nodes) == 2:
			self.nodes = [transform(indent, nodes[0]), transform(indent+1, nodes[1])]
		else:
			self.nodes = [transform(indent, nodes[0]), transform(indent+1, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		if len(self.nodes) == 2:
			self.line_init()
			self.nodes[0].pretty()
			self.line_term()
			self.nodes[1].pretty()
		else:
			self.line_init()
			self.nodes[0].pretty()
			self.line_term()
			self.nodes[1].pretty()
			self.nodes[2].pretty()
		return self

class Node_Stmt_Else_If(Node):
	tag = "stmt_else_if"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		if len(nodes) == 3:
			self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		else:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
							transform(indent+1, nodes[2]), transform(indent+1, nodes[3])
						 ]
		return

	def pretty(self):
		if len(self.nodes) == 3:
			self.line_init()
			self.nodes[0].pretty()
			self.line_more(" ", can_break_after=True)
			self.nodes[1].pretty()
			self.line_term()
			self.nodes[2].pretty()
		else:
			self.line_init()
			self.nodes[0].pretty()
			self.line_more(" ", can_break_after=True)
			self.nodes[1].pretty()
			self.line_term()
			self.nodes[2].pretty()
			self.nodes[3].pretty()
		return self

class Node_Stmt_If(Node):
	tag = "stmt_if"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_Case(Node):
	tag = "stmt_case"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent, nodes[2])]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_term()
		self.nodes[1].pretty()
		self.line_init()
		self.nodes[2].pretty()
		self.line_term()
		return self

class Node_Stmt_Switch(Node):
	tag = "stmt_switch"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		return self

class Node_Stmt_While(Node):
	tag = "stmt_while"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		return self

class Node_Stmt_Next(Node):
	tag = "stmt_next"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ")
		for node in (self.nodes)[2:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Break(Node):
	tag = "stmt_break"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ")
		for node in (self.nodes)[2:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Fallthrough(Node):
	tag = "stmt_fallthrough"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ")
		for node in (self.nodes)[2:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Return_No_Expr(Node):
	tag = "stmt_return_no_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		self.line_more(" ")
		for node in (self.nodes)[2:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Return_With_Expr(Node):
	tag = "stmt_return_with_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_more(" ")
		for node in (self.nodes)[3:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Return(Node):
	tag = "stmt_return"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_Add(Node):
	tag = "stmt_add"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_more(" ")
		for node in (self.nodes)[3:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Delete(Node):
	tag = "stmt_delete"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_more(" ")
		for node in (self.nodes)[3:]:
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Local(Node):
	tag = "stmt_local"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		for node in (self.nodes)[2:]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "token":
				node.pretty()
			elif node.tag == "opt_no_test":
				self.line_more(" ")
				node.pretty()
		self.line_term()
		return self

class Node_Stmt_Const(Node):
	tag = "stmt_const"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		for node in (self.nodes)[2:]:
			if node.tag == "opt_type":
				node.pretty()
			elif node.tag == "init_class":
				self.line_more(" ", can_break_after=True)
				node.pretty()
			elif node.tag == "opt_init":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "opt_attr":
				self.line_more(" ")
				node.pretty()
			elif node.tag == "token":
				node.pretty()
			elif node.tag == "opt_no_test":
				self.line_more(" ")
				node.pretty()
		self.line_term()
		return self

class Node_Stmt_When_No_Expr(Node):
	tag = "stmt_when_no_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		return self

class Node_Stmt_When_Expr(Node):
	tag = "stmt_when_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		if len(nodes) == 4:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
							transform(indent, nodes[2]), transform(indent+1, nodes[3])
						 ]
		else:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent, nodes[2]),
							transform(indent, nodes[3]), transform(indent+1, nodes[4])
						 ]
		return

	def pretty(self):
		if len(self.nodes) == 4:
			self.nodes[0].pretty()
			self.line_init()
			self.nodes[1].pretty()
			self.line_more(" ")
			self.nodes[2].pretty()
			self.line_term()
			self.nodes[3].pretty()
		else:
			self.nodes[0].pretty()
			self.nodes[1].pretty()
			self.line_init()
			self.nodes[2].pretty()
			self.line_more(" ")
			self.nodes[3].pretty()
			self.line_term()
			self.nodes[4].pretty()
		return self

class Node_Stmt_When(Node):
	tag = "stmt_when"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_Return_When_Expr(Node):
	tag = "stmt_return_when_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
						transform(indent, nodes[2]), transform(indent+1, nodes[3])
					 ]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_more(" ")
		self.nodes[2].pretty()
		self.line_term()
		self.nodes[3].pretty()
		return self

class Node_Stmt_Return_When_Stmt(Node):
	tag = "stmt_return_when_stmt"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		if len(nodes) == 4:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]),
							transform(indent, nodes[2]), transform(indent+1, nodes[3])
						 ]
		else:
			self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent, nodes[2]),
							transform(indent, nodes[3]), transform(indent+1, nodes[4])
						 ]
		return

	def pretty(self):
		if len(self.nodes) == 4:
			self.nodes[0].pretty()
			self.line_init()
			self.nodes[1].pretty()
			self.line_more(" ")
			self.nodes[2].pretty()
			self.line_term()
			self.nodes[3].pretty()
		else:
			self.nodes[0].pretty()
			self.nodes[1].pretty()
			self.line_init()
			self.nodes[2].pretty()
			self.line_more(" ")
			self.nodes[3].pretty()
			self.line_term()
			self.nodes[4].pretty()
		return self

class Node_Stmt_Return_When(Node):
	tag = "stmt_return_when"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_Slice(Node):
	tag = "stmt_slice"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		self.nodes[3].pretty()
		for node in (self.nodes)[4:]:
			self.line_more(" ")
			node.pretty()
		self.line_term()
		return self

class Node_Stmt_Expr(Node):
	tag = "stmt_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.nodes[1].pretty()
		if len(self.nodes) > 2:
			self.line_more(" ")
			for node in (self.nodes)[2:]:
				node.pretty()
		self.line_term()
		return self

class Node_Stmt(Node):
	tag = "stmt"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_List(Node):
	tag = "stmt_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:-1]:
			node.pretty()
			self.addNewline()
		if len(self.nodes) > 0:
			self.nodes[-1].pretty()
		return self

class Node_Event(Node):
	tag = "event"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Case_List(Node):
	tag = "case_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		for node in (self.nodes)[:-1]:
			node.pretty()
			self.addNewline()
		if len(self.nodes) > 0:
			self.nodes[-1].pretty()
		return self

class Node_Case_List_Expr(Node):
	tag = "case_list_expr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), 
						transform(indent, nodes[2]), transform(indent+1, nodes[3])
					 ]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_term()
		self.nodes[3].pretty()
		return self

class Node_Case_List_Type(Node):
	tag = "case_list_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [	transform(indent, nodes[0]), transform(indent, nodes[1]), 
						transform(indent, nodes[2]), transform(indent+1, nodes[3])
					 ]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.nodes[2].pretty()
		self.line_term()
		self.nodes[3].pretty()
		return self

class Node_Case_Default(Node):
	tag = "case_default"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent, nodes[1]), transform(indent+1, nodes[2])]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		self.line_term()
		self.nodes[2].pretty()
		return self

class Node_Case(Node):
	tag = "case"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Case_Type_List_(Node):
	tag = "case_type_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str() + " ", can_break_after=True)		
		self.nodes[2].pretty()
		return self

class Node_Case_Type_List(Node):
	tag = "case_type_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Case_Type_(Node):
	tag = "case_type_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(" ")
		self.nodes[1].pretty()
		return self

class Node_Case_Type_Id(Node):
	tag = "case_type_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		for node in (self.nodes)[1:]:
			self.line_more(" ")
			node.pretty()
		return self

class Node_Case_Type(Node):
	tag = "case_type"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_For_Head_Id(Node):
	tag = "for_head_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str(), can_break_after=True)
		self.nodes[2].pretty()
		self.line_more(" ")
		self.nodes[3].pretty()
		self.line_more(" ")
		self.nodes[4].pretty()
		self.nodes[5].pretty()
		self.line_term()
		return self

class Node_For_Head_List(Node):
	tag = "for_head_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str(), can_break_after=True)
		self.nodes[2].pretty()
		self.nodes[3].pretty()
		self.nodes[4].pretty()
		self.line_more(" ")
		self.nodes[5].pretty()
		self.line_more(" ")
		self.nodes[6].pretty()
		self.nodes[7].pretty()
		self.line_term()
		return self

class Node_For_Head_In(Node):
	tag = "for_head_in"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str(), can_break_after=True)
		self.nodes[2].pretty()
		self.nodes[3].pretty()
		self.line_more(" ")
		self.nodes[4].pretty()
		self.line_more(" ")
		self.nodes[5].pretty()
		self.line_more(" ")
		self.nodes[6].pretty()
		self.nodes[7].pretty()
		self.line_term()
		return self

class Node_For_Head_List_(Node):
	tag = "for_head_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.line_init()
		self.nodes[0].pretty()
		self.line_more(" " + self.nodes[1].to_str(), can_break_after=True)
		self.nodes[2].pretty()
		self.nodes[3].pretty()
		self.nodes[4].pretty()
		self.nodes[5].pretty()
		self.line_more(" ")
		self.nodes[6].pretty()
		self.line_more(" ")
		self.nodes[7].pretty()
		self.line_more(" ")
		self.nodes[8].pretty()
		self.nodes[9].pretty()
		self.line_term()
		return self

class Node_For_Head(Node):
	tag = "for_head"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Stmt_For(Node):
	tag = "stmt_for"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, nodes[0]), transform(indent+1, nodes[1])]
		return


class Node_Local_Id_List_(Node):
	tag = "local_id_list_"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str() + " ", can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Local_Id_List(Node):
	tag = "local_id_list"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Local_Id(Node):
	tag = "local_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Global_Id(Node):
	tag = "global_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Def_Global_Id(Node):
	tag = "def_global_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Event_Id(Node):
	tag = "event_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Global_Or_Event_Id(Node):
	tag = "global_or_event_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Resolve_Id(Node):
	tag = "resolve_id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_No_Test(Node):
	tag = "opt_no_test"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_No_Test_Block(Node):
	tag = "opt_no_test_block"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Deprecated_1(Node):
	tag = "opt_deprecated_1"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Opt_Deprecated_2(Node):
	tag = "opt_deprecated_2"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

	def pretty(self):
		self.nodes[0].pretty()
		self.line_more(self.nodes[1].to_str(), can_break_after=True)
		self.nodes[2].pretty()
		return self

class Node_Opt_Deprecated(Node):
	tag = "opt_deprecated"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Id_Cname(Node):
	tag = "id_cname"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Id_Namespace(Node):
	tag = "id_namespace"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Id(Node):
	tag = "id"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Signed_Number(Node):
	tag = "signed_number"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Hexnumber(Node):
	tag = "hexnumber"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Escaped_Strings(Node):
	tag = "escaped_strings"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Mime(Node):
	tag = "mime"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Ipaddr(Node):
	tag = "ipaddr"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Atdir(Node):
	tag = "atdir"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Atfilename(Node):
	tag = "atfilename"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_True(Node):
	tag = "true"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_False(Node):
	tag = "false"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Hostname(Node):
	tag = "hostname"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Atom_Simple(Node):
	tag = "atom_simple"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Interval(Node):
	tag = "interval"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Port(Node):
	tag = "port"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Subnet(Node):
	tag = "subnet"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Atom_Complex(Node):
	tag = "atom_complex"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Atom(Node):
	tag = "atom"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return

class Node_Expr_Unary(Node):
	tag = "expr_unary"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return	

class Node_Expr_Binary(Node):
	tag = "expr_binary"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return	

class Node_Expr_Misc(Node):
	tag = "expr_misc"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return	

class Node_Unary_Op(Node):
	tag = "unary_op"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return	

class Node_Binary_Op(Node):
	tag = "binary_op"

	def __init__(self, meta, indent, nodes):
		super().__init__(meta, indent)
		self.nodes = [transform(indent, node) for node in nodes]
		return	