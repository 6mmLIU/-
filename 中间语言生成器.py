import tkinter as tk
from tkinter import messagebox


# 定义树节点类
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# 词法分析部分
program = []


def output(str, a, b, type):
    global program
    program.append([type, str[a:b + 1]])


def iskeywords(str, a, b):
    keywords = {"if", "int", "for", "while", "do", "return", "break", "continue", 'then'}
    s = str[a:b + 1]
    return 1 if s in keywords else 2


def belong_to(char, type):
    if type == 4:
        library = "+-*/=><!"
    else:
        library = ",;{}()"
    if char in library:
        return 2 if type == 4 and library.index(char) >= 4 else 1
    return 0


def scan(str, n):
    i = n
    type = 0
    while i < len(str):
        if type == 0:
            if str[i] == ' ':
                n += 1
                i += 1
                continue
            elif str[i] in ['\0', '\n']:
                return
            elif 'a' <= str[i] <= 'z' or 'A' <= str[i] <= 'Z':
                type = 1
            elif str[i] == '0':
                type = 6
            elif '1' <= str[i] <= '9':
                type = 3
            else:
                type = belong_to(str[i], 4)
                if type > 0:
                    if type == 2 and i + 1 < len(str) and str[i + 1] == '=':
                        i += 1
                    output(str, n, i, 4)
                    scan(str, i + 1)
                    return
                elif belong_to(str[i], 5):
                    output(str, n, i, 5)
                    scan(str, i + 1)
                    return
                else:
                    print("词法分析失败:", str[i])
                    return
        elif type == 1:
            if not ('a' <= str[i] <= 'z' or 'A' <= str[i] <= 'Z'):
                if '0' <= str[i] <= '9':
                    type = 2
                else:
                    type = iskeywords(str, n, i - 1)
                    output(str, n, i - 1, type)
                    scan(str, i)
                    return
        elif type == 2:
            if not ('a' <= str[i] <= 'z' or 'A' <= str[i] <= 'Z' or '0' <= str[i] <= '9'):
                output(str, n, i - 1, type)
                scan(str, i)
                return
        elif type == 3:
            if not ('0' <= str[i] <= '9'):
                output(str, n, i - 1, type)
                scan(str, i)
                return
        elif type == 6:
            if str[i] == 'x':
                type = 7
            elif str[i] == 'o':
                type = 8
            elif str[i] == ' ':
                output(str, n, i - 1, 3)
                scan(str, i)
                return
            else:
                print("16/8进制分析失败")
                return
        elif type == 7:
            if not ('0' <= str[i] <= '9' or 'a' <= str[i] <= 'f'):
                output(str, n, i - 1, 3)
                scan(str, i)
                return
        elif type == 8:
            if not ('0' <= str[i] <= '7'):
                output(str, n, i - 1, 3)
                scan(str, i)
                return
        else:
            print("未知类型失败")
            return
        i += 1


# 递归下降语法分析程序
def Parse():
    def ParseS():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[0] == 2:
            MatchToken(2)
            MatchToken('=')
            ParseE()
        elif lookahead[1] == 'if':
            MatchToken('if')
            ParseC()
            MatchToken('then')
            ParseS()
        elif lookahead[1] == 'while':
            MatchToken('while')
            ParseC()
            MatchToken('do')
            ParseS()
        elif lookahead[1] == 'return':
            MatchToken('return')
            MatchToken(2)
            MatchToken(';')
        elif lookahead[1] == 'int':
            MatchToken('int')
            MatchToken(2)
            MatchToken('=')
            ParseE()
            MatchToken(';')
        else:
            print("S 解析错误")
            parseerror = 1

    def ParseC():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '(' or lookahead[0] in [2, 3]:
            ParseE()
            ParseC1()
        else:
            print("C 解析错误")
            parseerror = 2

    def ParseE():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '(' or lookahead[0] in [2, 3]:
            ParseT()
            ParseE1()
        else:
            print("E 解析错误")
            parseerror = 3

    def ParseT():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '(' or lookahead[0] in [2, 3]:
            ParseF()
            ParseT1()
        else:
            print("T 解析错误")
            parseerror = 4

    def ParseF():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '(':
            MatchToken('(')
            ParseE()
            MatchToken(')')
        elif lookahead[0] == 2:
            MatchToken(2)
        elif lookahead[0] == 3:
            MatchToken(3)
        else:
            print("F 解析错误")
            parseerror = 5

    def ParseE1():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '+':
            MatchToken('+')
            ParseT()
            ParseE1()
        elif lookahead[1] == '-':
            MatchToken('-')
            ParseT()
            ParseE1()
        elif lookahead[1] in [')', ';', '>', '=', '<', 'then', 'do']:
            pass
        else:
            print("E1 解析错误")
            parseerror = 5

    def ParseT1():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '*':
            MatchToken('*')
            ParseF()
            ParseT1()
        elif lookahead[1] == '/':
            MatchToken('/')
            ParseF()
            ParseT1()
        elif lookahead[1] in ['+', '-', ')', ';', '>', '=', '<', 'then', 'do']:
            pass
        else:
            print("T1 解析错误")
            parseerror = 5

    def ParseC1():
        global lookahead, parseerror
        if parseerror:
            return
        if lookahead[1] == '>':
            MatchToken('>')
            ParseE()
        elif lookahead[1] == '=':
            MatchToken('=')
            ParseE()
        elif lookahead[1] == '<':
            MatchToken('<')
            ParseE()
        else:
            print("C1 解析错误")
            parseerror = 5

    def MatchToken(need_type):
        global lookahead, parseerror
        mate = 0
        if parseerror:
            return
        if isinstance(need_type, int):
            if lookahead[0] == need_type:
                mate = 1
        elif lookahead[1] == need_type:
            mate = 1
        if mate:
            lookahead = GetToken()
        else:
            print("需要", need_type, "实际", lookahead, "匹配错误")
            parseerror = 6

    def GetToken():
        global program
        return program.pop(0) if program else (None, None)

    global program, lookahead, parseerror
    parseerror = 0
    lookahead = GetToken()
    ParseS()
    if parseerror == 0:
        print("语法正确")


# 逆波兰表示转换
def to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []

    for char in expression:
        if char.isalnum():  # 如果是操作数
            output.append(char)
        elif char in precedence:  # 如果是运算符
            while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return ''.join(output)


# 创建抽象语法树
def build_ast(expression):
    stack = []
    for char in to_postfix(expression):
        node = TreeNode(char)
        if char.isalnum():
            stack.append(node)
        else:
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack[-1]  # 返回根节点


# 中间代码生成
def generate_three_address_code(expression):
    temp_counter = 1
    stack = []
    three_address_code = []

    def get_temp():
        nonlocal temp_counter
        temp = f't{temp_counter}'
        temp_counter += 1
        return temp

    postfix_expr = to_postfix(expression)
    for char in postfix_expr:
        if char.isalnum():
            stack.append(char)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = get_temp()
            three_address_code.append((char, operand1, operand2, result))
            stack.append(result)

    # 最后添加赋值操作
    target_var = expression.split('=')[0].strip()
    three_address_code.append(('=', stack.pop(), None, target_var))

    return three_address_code


def generate_four_address_code(expression):
    three_address_code = generate_three_address_code(expression)
    return [(op, op1, op2, res) for op, op1, op2, res in three_address_code]


# GUI部分
def on_submit():
    expression = entry.get()
    if not expression:
        messagebox.showwarning("输入错误", "请输入赋值表达式")
        return

    try:
        postfix_expr = to_postfix(expression)
        ast_root = build_ast(expression)
        three_address_code = generate_three_address_code(expression)
        four_address_code = generate_four_address_code(expression)

        postfix_label.config(text=f"逆波兰表示: {postfix_expr}")
        tac_label.config(text=f"三元式: {three_address_code}")
        fac_label.config(text=f"四元式: {four_address_code}")

        # 显示抽象语法树
        ast_text = f"抽象语法树:\n{display_ast(ast_root)}"
        ast_label.config(text=ast_text, justify="left")

    except Exception as e:
        messagebox.showerror("错误", f"解析表达式时出错: {e}")


def display_ast(node, depth=0, is_right=False, indent=""):
    if node is None:
        return ""

    node_repr = f"{node.value}"
    left_indent = indent + ("    " if is_right else "|   ")
    right_indent = indent + ("    " if not is_right else "|   ")

    left = display_ast(node.left, depth + 1, False, left_indent)
    right = display_ast(node.right, depth + 1, True, right_indent)

    if left or right:
        return f"{node_repr}\n{left}{right}"
    else:
        return f"{node_repr}"


app = tk.Tk()
app.title("中间语言生成器")

frame = tk.Frame(app)
frame.pack(pady=10)

tk.Label(frame, text="请输入赋值表达式:").grid(row=0, column=0)
entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1)

submit_btn = tk.Button(frame, text="转换", command=on_submit)
submit_btn.grid(row=0, column=2, padx=10)

postfix_label = tk.Label(app, text="逆波兰表示: ")
postfix_label.pack(pady=5)

tac_label = tk.Label(app, text="三元式: ")
tac_label.pack(pady=5)

fac_label = tk.Label(app, text="四元式: ")
fac_label.pack(pady=5)

ast_label = tk.Label(app, text="抽象语法树: ")
ast_label.pack(pady=5)

app.mainloop()
