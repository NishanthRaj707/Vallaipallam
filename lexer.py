from tokens import *
from errors import *


class Lexer():
    line_no=1
    letters=u'''அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ,ஔ      
க், ங், ச், ஞ், ட், ண், த், ந், ப், ம், ய், ர், ல், வ், ழ், ள், ற், ன்  
க, கா, கி, கீ, கு, கூ, கெ, கே, கை, கொ, கோ, கௌ
ங, ஙா, ஙி, ஙீ, ஙு, ஙூ, ஙெ, ஙே, ஙை, ஙொ, ஙோ, ஙௌ
ச, சா, சி, சீ, சு, சூ, செ, சே, சை, சொ, சோ, சௌ,ஞ, ஞா, ஞி, ஞீ, ஞு, ஞூ, ஞெ, ஞே, ஞை, ஞொ, ஞோ, ஞௌ
ட, டா, டி, டீ, டு, டூ, டெ, டே, டை, டொ, டோ, டௌ
ண, ணா, ணி, ணீ, ணு, ணூ, ணெ, ணே, ணை, ணொ, ணோ, ணௌ
த, தா, தி, தீ, து, தூ, தெ, தே, தை, தொ, தோ, தௌ
ந, நா, நி, நீ, நு, நூ, நெ, நே, நை, நொ, நோ, நௌ    
ப, பா, பி, பீ, பு, பூ, பெ, பே, பை, பொ, போ, பௌ     
ம, மா, மி, மீ, மு, மூ, மெ, மே, மை, மொ, மோ, மௌ    
ய, யா, யி, யீ, யு, யூ, யெ, யே, யை, யொ, யோ, யௌ    
ர, ரா, ரி, ரீ, ரு, ரூ, ரெ, ரே, ரை, ரொ, ரோ, ரௌ
ல, லா, லி, லீ, லு, லூ, லெ, லே, லை, லொ, லோ, லௌ  
வ, வா, வி, வீ, வு, வூ, வெ, வே, வை, வொ, வோ,வௌ 
ழ, ழா, ழி, ழீ, ழு, ழூ, ழெ, ழே, ழை, ழொ, ழோ, ழௌ      
ள, ளா, ளி, ளீ, ளு, ளூ, ளெ, ளே, ளை, ளொ, ளோ, ளௌ    
ற, றா, றி, றீ, று, றூ, றெ, றே, றை, றொ, றோ, றௌ
ன, னா, னி, னீ, னு, னூ, னெ, னே, னை, னொ, னோ, னௌ'''
    digits="0123456789"
    operators="+-*/=%"    
    stopwords=[' ','\n',',']
    listofkeyword=['தொடர்','ரத்து','இறக்கு']
    keywords=[u'உருவாக்கு']
    members=['உள்ளது']
    function_call='கூப்பிடு'
    function=['வேலை','கொடு']
    built_in_functions=['வெளியிடு','உள்ளீடு','அளவு','எண்','வரம்பு','நீக்கு','பட்டியல்','இணை','சொல்','செருகு','வகை','பிரி','திற','படி','எழுது','மூடு']
    conditions=['என்றால்','இது','இல்லை','இல்லையெனில்','அதுவரை', 'இதில்','இருந்து']
    logical=['மற்றும்','அல்லது','அல்ல']
    comparison=[">","<",">=","<=","!=","=="]
    boolean=['மெய்','பொய்']
    def __init__(self,text):
        self.text=text
        self.idx=0
        self.char=self.text[self.idx]
        self.token=None
        self.tokens=[]
    #A function to tokenise the elements  
    def tokenize(self):
        
        while self.idx<len(self.text):
            #Digit
            if self.char in Lexer.digits:
                self.token=self.extract_number()
            #Spaces and Newlines are handled here
            elif self.char in Lexer.stopwords:
                if self.char=='\n':
                    Lexer.line_no+=1
                self.move()
                continue 
            #String implementation
            elif self.char in '\'\"':
                self.move()
                word=''
                while self.char not in '\'\"' and self.idx<len(self.text):
                    word+=self.char
                    self.move()
                
                self.token=String(word)
                if self.char not in '\'\"':
                    Syntax_Error(Lexer.line_no,f"இங்கு {word} <-- \' அல்லது \" வரவேண்டும்")

                self.move()   
                

            #List
            elif self.char=='[':
                self.token=List(self.extract_list())
        
            elif self.char in '()':
                self.token=Operator(self.char)    
                self.move() 
            #Variable and Keywords
            elif self.char in Lexer.letters:
                word=self.extract_word()
                if  word in Lexer.keywords:
                    self.token=Declaration(word)
                elif word in Lexer.logical:
                    self.token=Logical(word)
                elif word in Lexer.conditions:
                    self.token=Condition(word)    
                elif word in Lexer.boolean:
                    self.token=Boolean(word)    
                elif word in Lexer.listofkeyword:
                    self.token=Keyword(word) 
                elif word in Lexer.members:
                    self.token=Member(word) 
                elif word in Lexer.function:
                    self.token=Function(word)    
                elif word==Lexer.function_call:
                    self.token=Function(word)
                elif word in Lexer.built_in_functions:
                    self.token=Built_in_Function(word)    
                else:
                    self.token=Variable(word)   
            #Operators 
            elif self.char in Lexer.operators and self.text[self.idx+1] not in '=':
                self.token=Operator(self.char)
                self.move()

            elif self.char in Lexer.comparison or (self.char in '!=' and self.text[self.idx+1]=='='):
                operator=''
                while self.char in Lexer.comparison or self.char in '!=':
                    operator +=self.char
                    self.move()
                self.token=Comparison(operator)
            elif self.char == '{' or self.char == '}':
                self.token=Delimiter(self.char)  
                self.move()  
            elif self.char=='.':
                self.token=Delimiter(self.char)
                self.move() 
            elif self.char in '\'\"])}':
                Syntax_Error(Lexer.line_no,f"{self.char} மிகுதியாக உள்ளது")    
            elif self.char.isalpha():
                Syntax_Error(Lexer.line,f"{self.char} ")                     
            self.tokens.append(self.token)
            
        return self.tokens  
    #ASSEMBLING OF A LIST
    def tokenize_sequence(self):
        
            if self.char in Lexer.digits:
                self.token=self.extract_number()
            #Spaces and Newlines are handled here
            elif self.char in Lexer.stopwords:
                self.move()

            elif self.char in ',':
                self.token=None     
            #String implementation
            elif self.char in '\'\"':
                word=''
                self.move()
                while self.char not in '\'\"' and self.idx<len(self.text):
                    word+=self.char
                    self.move()
                self.token=String(word)
                self.move()    
            #List
            elif self.char=='[':
                self.token=self.extract_list()

         
            elif self.char in Lexer.operators and  self.text[self.idx+1] not in '=':
                self.token=Operator(self.char)
                self.move() 
            elif self.char in Lexer.letters:
                word=self.extract_word()
                if  word in Lexer.keywords:
                    self.token=Declaration(word)
                elif word in Lexer.logical:
                    self.token=Logical(word)
                elif word in Lexer.conditions:
                    self.token=Condition(word)    
                elif word in Lexer.boolean:
                    self.token=Boolean(word)    
                        
                else:
                    self.token=Variable(word)   

            elif self.char in Lexer.comparison or (self.char in '!=' and self.text[self.idx+1]=='='):
                operator=''
                while self.char in Lexer.comparison or self.char=='=':
                    operator +=self.char
                    self.move()
                self.token=Comparison(operator)
            elif self.char == '{' or self.char == '}':
                self.token=Delimiter(self.char)  
                self.move()              
            
       
            return self.token
            
       
    
    def extract_word(self):
        word=''
        while self.char in Lexer.letters and self.idx<len(self.text) and not self.char.isspace() and self.char !=',':
            word+=self.char
            self.move()            
        return word          


    
    def extract_number(self):
        number=""
        while (self.char in Lexer.digits or self.char =='.') and self.idx < len(self.text):
            number+=self.char
            self.move()
        if number[0]=='0' and len(number)>1:
            Syntax_Error(Lexer.line_no,"எந்ந எண்ணும் 0 தொடங்காது")    
        return Number(number)    

    def extract_list(self):                                     
        list_extracted=[]
        self.move()
        while self.char != ']' and self.idx<len(self.text):
        
            element=self.tokenize_sequence()
            
            if element :
                list_extracted.append(element) 
            if self.char==':':
                list_extracted.append(Delimiter(':'))     
            if self.char == ']':
                break
            
            self.move()
        if self.char != ']':
            Syntax_Error(Lexer.line_no,f"இங்கு {list_extracted} <-- \' அல்லது \" வரவேண்டும்")    
        self.move()
        
        return list_extracted
    
    def move(self):
        self.idx=self.idx+1
        if self.idx<len(self.text):
            self.char=self.text[self.idx]


