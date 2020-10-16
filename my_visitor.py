import sys
from pycparser import c_ast


class MyVisitor(c_ast.NodeVisitor):

    def __init__(self, dest=sys.stdout):
        self.dest = dest

    def visit_ArrayDecl(self, node):
        s = self.visit(node.type)
        a = "[" + self.visit(node.dim) + "]"
        return s, a

    def visit_ArrayRef(self, node):
        ref = self.visit(node.name)
        index = self.visit(node.subscript)
        return ref + "[" + index + "]"

    def visit_Assignment(self, node):
        rvalue = self.visit(node.rvalue)
        lvalue = self.visit(node.lvalue)
        return "{} {} {}".format(lvalue, node.op, rvalue)

    def visit_BinaryOp(self, node):
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return "({} {} {})".format(lhs, node.op, rhs)

    def visit_Break(self, node):
        print("unsupported:", node)

    def visit_Case(self, node):
        print("unsupported:", node)

    def visit_Cast(self, node):
        to_type = self.visit(node.to_type)
        expr = self.visit(node.expr)
        return "(({})({}))".format(to_type, expr)

    def visit_Compound(self, node):
        lst = []
        for block in node.block_items:
            lst.append(self.visit(block) + ";")
        return "{\n" + "\n".join(lst) + "\n}"

    def visit_CompoundLiteral(self, node):
        print("unsupported:", node)

    def visit_Constant(self, node):
        return node.value

    def visit_Continue(self, node):
        print("unsupported:", node)

    def visit_Decl(self, node):
        s = ""
        if isinstance(node.type, c_ast.FuncDecl):
            t, a = self.visit(node.type)
            s += t + " " + node.name + a
        elif isinstance(node.type, c_ast.ArrayDecl):
            t, a = self.visit(node.type)
            s += t + " " + node.name + a
        else:
            t = self.visit(node.type)
            s += t + " " + node.name

        if node.init is not None:
            init = self.visit(node.init)
            s += " = " + init
        return s

    def visit_DeclList(self, node):
        lst = [self.visit(e) for e in node.decls]
        return ", ".join(lst)

    def visit_Default(self, node):
        print("unsupported:", node)

    def visit_DoWhile(self, node):
        print("unsupported:", node)

    def visit_EllipsisParam(self, node):
        print("unsupported:", node)

    def visit_EmptyStatement(self, node):
        print("unsupported:", node)

    def visit_Enum(self, node):
        print("unsupported:", node)

    def visit_Enumerator(self, node):
        print("unsupported:", node)

    def visit_EnumeratorList(self, node):
        print("unsupported:", node)

    def visit_ExprList(self, node):
        lst = [self.visit(e) for e in node.exprs]
        return ", ".join(lst)

    def visit_FileAST(self, node):
        for ext in node.ext:
            self.visit(ext)

    def visit_For(self, node):
        init_expr = self.visit(node.init)
        cond_expr = self.visit(node.cond)
        next_expr = self.visit(node.next)
        stmt = self.visit(node.stmt)
        s = ""
        s += "for({}; {}; {})\n".format(init_expr, cond_expr, next_expr)
        s += stmt
        return s

    def visit_FuncCall(self, node):
        funcname = self.visit(node.name)
        args = self.visit(node.args)
        return "{}({})".format(funcname, args)

    def visit_FuncDecl(self, node):
        s = self.visit(node.type)
        a = "()"
        if node.args is not None:
            a = "({})".format(self.visit(node.args))
        return s, a

    def visit_FuncDef(self, node):
        s = self.visit(node.decl)
        s += "\n" + self.visit(node.body) + "\n"
        self.dest.write(s)
        return s

    def visit_Goto(self, node):
        print("unsupported:", node)

    def visit_ID(self, node):
        return node.name

    def visit_IdentifierType(self, node):
        return " ".join(node.names)

    def visit_If(self, node):
        cond_expr = self.visit(node.cond)
        s = "if({})\n".format(cond_expr)
        iftrue = self.visit(node.iftrue)
        s += iftrue
        if node.iffalse is not None:
            iffalse = self.visit(node.iffalse)
            s += "\n"
            s += "else\n"
            s += iffalse
        return s

    def visit_InitList(self, node):
        lst = []
        for init in node.exprs:
            lst.append(self.visit(init))
        return "{" + ", ".join(lst) + "}"

    def visit_Label(self, node):
        print("unsupported:", node)

    def visit_NamedInitializer(self, node):
        print("unsupported:", node)

    def visit_ParamList(self, node):
        lst = [self.visit(e) for e in node.params]
        return ", ".join(lst)

    def visit_PtrDecl(self, node):
        t = self.visit(node.type)
        return t + "*"

    def visit_Return(self, node):
        expr = self.visit(node.expr)
        return "return " + expr

    def visit_Struct(self, node):
        print("unsupported:", node)

    def visit_StructRef(self, node):
        print("unsupported:", node)

    def visit_Switch(self, node):
        print("unsupported:", node)

    def visit_TernaryOp(self, node):
        cond_expr = self.visit(node.cond)
        iftrue = self.visit(node.iftrue)
        iffalse = self.visit(node.iffalse)
        return "{} ? {} : {}".format(cond_expr, iftrue, iffalse)

    def visit_TypeDecl(self, node):
        s = self.visit(node.type)
        return s

    def visit_Typedef(self, node):
        s = self.visit(node.type)
        return s

    def visit_Typename(self, node):
        return self.visit(node.type)

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        if node.op[0] == 'p':
            return node.op[1:] + expr
        else:
            return expr + node.op

    def visit_Union(self, node):
        print("unsupported:", node)

    def visit_While(self, node):
        print("unsupported:", node)

    def visit_Pragma(self, node):
        print("unsupported:", node)
