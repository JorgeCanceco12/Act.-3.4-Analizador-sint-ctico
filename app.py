from flask import Flask, request, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición de tokens para ply.lex
tokens = (
    'INT',
    'IDENTIFIER',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'READ',
    'PRINT',
    'END',
    'EQUALS',
    'PLUS',
)

# Reglas de tokens
t_INT = r'\bint\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_PLUS = r'\+'
t_READ = r'\bread\b'
t_PRINT = r'\bprintf\b'
t_END = r'\bend\b'
t_IDENTIFIER = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'

# Ignorar espacios y nuevas líneas
t_ignore = ' \t\n'

# Definición del analizador léxico usando ply.lex
lexer = lex.lex()

# Reglas de gramática para el parser
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

# Definir una lista de sentencias
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Definir las diferentes declaraciones permitidas
def p_statement(p):
    '''statement : INT IDENTIFIER SEMICOLON
                 | READ IDENTIFIER SEMICOLON
                 | PRINT LPAREN IDENTIFIER RPAREN SEMICOLON
                 | IDENTIFIER EQUALS IDENTIFIER PLUS IDENTIFIER SEMICOLON
                 | LBRACE statement_list RBRACE
                 | END SEMICOLON'''
    p[0] = ('statement',) + tuple(p[1:])

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at EOF")

# Definición del parser usando ply.yacc
parser = yacc.yacc()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        
        # Análisis léxico
        lexer.input(code)
        tokens_list = []
        for tok in lexer:
            tokens_list.append((tok.type, tok.value))
        
        # Análisis sintáctico (parseo)
        try:
            parse_result = parser.parse(code)
            parse_message = 'Código válido' if parse_result else 'Error de análisis'
        except Exception as e:
            parse_message = f'Error de análisis: {str(e)}'

        return render_template('index.html', tokens=tokens_list, code=code, parse_message=parse_message)

    return render_template('index.html', tokens=[], code='', parse_message='')

if __name__ == '__main__':
    app.run(debug=True)
