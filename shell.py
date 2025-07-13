from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from data import Data
from errors import Syntax_Error
root=Data()

def main(file_name):
    if len(file_name)<4:
        return Syntax_Error(0,'inappropriate file name.')
    elif not file_name.endswith('.jnr'):
        return Syntax_Error(0,'not a vallaipallam file.')
    else:
        f=open(f'{file_name}','r',encoding='utf-8')
        b=f.read()

        if b :
            tokens=Lexer(b)
            a=tokens.tokenize()
            tree=Parser(a,root)
            trees=tree.parse()
            output=Interpreter(trees,root)
            output1=output.home()
        
