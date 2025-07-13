from tokens import Null,Operator
from errors import *
class Parser:
    line_no=1
    def __init__(self,token,root):
        self.tokens=token
        self.idx=0
        self.token=self.tokens[self.idx]
        self.root=root
    
    def factor(self):
        if self.token.type == 'எண்':
            return self.token
        elif self.token.type=='சொல்':
            return self.token
        elif self.token.type=='மாறி':
            return self.token
        elif self.token.type=='மெய்ப்பு':
            return self.token
        elif self.token.type=='பட்டியல்':
            return self.token
        elif self.token.value=='கொடு':
            return self.token
        elif self.token.type=='KEY':
            return self.token  
        elif self.token.value=='கூப்பிடு':
            return self.token
        elif self.token.type=='BIF':
            return self.token
        elif self.token.value=='(':
            self.move()
            expression=self.expression()
            return expression
        elif self.token.value==')':
            return self.token
        elif self.token.value=='+' or self.token.value=='-':
            operator=self.token
            self.move()
            operand=self.factor()
            return [operator,operand]
        
        elif self.token.type.startswith('மாறி'):
            return self.token
        elif self.token.value=='அல்ல':
            operator = self.token
            self.move()
            operand=self.comparison_expression()
            return [operator,operand]
        elif self.token.type =='மெய்ப்பு':
            return self.token
        

    def if_statement(self):
        keyword=self.token.value
        self.move()
        action_list=[]
        condition=self.logical_expression()
         
        if self.token.value=='என்றால்':
            self.move()
            if self.token.value=='{':
                self.move()
                while self.token.value!='}' and self.idx<len(self.tokens): 
                    action=self.statement()
                    action_list.append(action)
                else:
                    if self.token.value != '}':
                        Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")      
                return condition,action_list   
            else:
                Syntax_Error(Parser.line_no," <-- { வரவேண்டும்")
        else:
            Syntax_Error(Parser.line_no," <-- என்றால் வரவேண்டும்")  

        if keyword=='இல்லையெனில்':
            if self.token.value=='{':
                self.move()
                while self.token.value!='}':
                    action=self.statement()
                    action_list.append(action)
                return condition,action_list 

                   
    
    #IF STATEMENTS
    def if_statements(self):
        
        else_executed=0
        conditions=[]
        actions=[]

        if_=self.if_statement()
        conditions.append(if_[0])
        actions.append(if_[1])
        
        
        self.move()

        while self.token.value == 'இல்லையெனில்':
            if_=self.if_statement()
            conditions.append(if_[0])
            actions.append(if_[1])
            self.move()
          
        
        
        
        if self.token.value == 'இல்லை':
            self.move()
            
            if self.token.value=='{':
                action_list=[]
                self.move()
                while self.token.value !='}' and self.idx < len(self.tokens):
                    action=self.statement()
                    action_list.append(action)
                else:
                    if self.token.value!='}':
                        Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")    

            else:
                Syntax_Error(Parser.line_no,"<-- { வரவேண்டும்")  
            actions.append(action_list)        
            self.move()
        
        output=conditions,actions
        return list(output)
    
    def while_statement(self):
        self.move()
        condition=self.statement()
        action_list=[]
        if self.token.value=='{':
            actions=[]
            self.move()
            while self.token.value !='}' and self.idx < len(self.tokens):
               action=self.statement()
               actions.append(action)
            else:
                if self.token.value != '}':
                    Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")    
            action_list.append(actions)
        else:
            Syntax_Error(Parser.line_no," <-- { வரவேண்டும்")   

        self.move()  

        if self.token.value=='இல்லை':
            self.move()
            actions=[]
            if self.token.value=='{':
                self.move()
                while self.token.value !='}' and self.idx < len(self.tokens):
                    action=self.statement()
                    actions.append(action)
                else:
                    if self.token.value !='}':
                       Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")
            else:
                Syntax_Error(Parser.line_no,"<-- { வரவேண்டும்")        
            action_list.append(actions)    
                   
            self.move()            
        output=[condition,action_list]
        return output 
      
    def for_statement(self):
        actions=[]
        self.move()
        sequence=self.statement()
        if self.token.value=='இருந்து':
            self.move()
            var=self.token if self.token.type.startswith('மாறி') else Type_Error(Parser.line_no,f"{self.token} தொடர் வகை அல்ல")
            self.move()
            if self.token.value=='{':
                self.move()
                while self.token.value!='}' and self.idx < len(self.tokens):
                    action=self.statement()
                    actions.append(action)
                else:
                    if self.token.value!='}':
                        Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")     
                self.move()
                output=[sequence,var,actions]
            else:
                Syntax_Error(Parser.line_no,"<-- { வரவேண்டும்")     
        else:
            Syntax_Error(Parser.line_no,"<-- இருந்து வரவேண்டும்") 

        return output        
    def function_block(self):
        parameters=[]
        actions=[]
        self.move()
        identifier=self.token
        self.move()
        if self.token.value=='(':
            self.move()
            while self.token.value !=')' and self.idx < len(self.tokens):
                var=self.statement()
                parameters.append(var)
            else:
                if self.token.value != ')':
                    Syntax_Error(Parser.line_no,"<-- ) வரவேண்டும்")

            self.move()    
        else:
            Syntax_Error(Parser.line_no,"<-- ( வரவேண்டும்")         
        
        if self.token.value=='{':
            self.move()
            while self.token.value !='}':
                action=self.statement()
                actions.append(action)
            else:
                if self.token.value !='}':
                    Syntax_Error(Parser.line_no,"<-- } வரவேண்டும்")    
            self.move() 
        else:
            Syntax_Error(Parser.line_no,"<-- { வரவேண்டும்")    
        output=[identifier,[parameters,actions]]       
        return output
    
    def function_call(self):
        values=[]
        self.move()
        identifier=self.token
        self.move()
        if self.token.value=='(':
            self.move()
            while self.token.value !=')' and len(self.tokens):
                value=self.statement()
                values.append(value)
                if self.token.value==',':
                    self.move()
            else:
                if self.token.value != ')':
                    Syntax_Error(Parser.line_no,"<-- ) வரவேண்டும்")        
            self.move()
        else:
            Syntax_Error(Parser.line_no,"<-- ( வரவேண்டும்")    
        output=[identifier,values]
        return output          
      
    def builtin_function(self,var=None):
        arguements=[]
        self.move()
        if self.token.value=='(':
            self.move()
            while self.token.value !=')':
                arguement=self.statement()
                arguements.append(arguement)
                if self.token.value==',':
                    self.move()
            else:
                if self.token.value != ')':
                    Syntax_Error(Parser.line_no,"<-- ) வரவேண்டும்") 

            self.move() 
        else:
            Syntax_Error(Parser.line_no,"<-- ( வரவேண்டும்")    
        if var:
            arguements.insert(0,var)    


        return arguements            

        
    def variable(self):
        if self.token.type.startswith('மாறி'):
            return self.token
        elif self.token.value in ['வெளியிடு','உள்ளிடு','எண்','வரம்பு','பட்டியல்','சொல்','வகை','பிரி','திற','படி','எழுது','மூடு','என்றால்','இது','இல்லை','இல்லையெனில்','அதுவரை', 'இதில்','இருந்து','மற்றும்','அல்லது','அல்ல','மெய்','பொய்','தொடர்','ரத்து','கொடு','இறக்கு','உருவாக்கு','உள்ளது','கூப்பிடு''வேலை'] :
            Syntax_Error(Parser.line_no,f"{self.token} மாறியாக பயன்படுத்தக்கூடாது")
        else:
            Syntax_Error(Parser.line_no,f"மாறி பயன்படுத்த ")    
            
  
    def term(self):
        left_node=self.factor()
        if not isinstance(left_node,list):
            if left_node.value=='கூப்பிடு':
                left_node=[left_node,self.function_call()]
                op=self.token.value

            elif left_node.type=='சொல்' or left_node.type=='பட்டியல்' or left_node.type=='மாறி':
                self.move()
                if self.token.type=='பட்டியல்' and len(self.token.value)<=5 and self.idx<len(self.tokens):
                    left_node=[left_node,self.token]

                    self.move()   
                    
            else:    
                self.move()  
              

            if self.token.value=='.':
                self.move()
                if self.token.type=='BIF':
                    return [self.token,self.builtin_function(left_node)]
        else:
            self.move()

        while self.token.value == '*' or self.token.value=='/' or self.token.value=='%':
            operation=self.token
            self.move()
            right_node=self.factor()
            self.move()
            left_node=[left_node,operation,right_node]
        return left_node
    
    def comparison_expression(self):
        left_node=self.expression()
        while self.token.value in [">","<",">=","<=","!=","=="]:
            operation=self.token
            self.move()
            right_node=self.expression()
            left_node=[left_node,operation,right_node]
           
        return left_node 
    
    def logical_expression(self):
        left_node=self.comparison_expression()
        while self.token.value in ['மற்றும்','அல்லது','அல்ல']:
            operation=self.token
            self.move()
            right_node=self.comparison_expression()
            left_node=[left_node,operation,right_node]
        if self.token.value=='உள்ளது':
            operation=self.token
            self.move()
            right_node=self.comparison_expression()
            left_node=[left_node,operation,right_node]    
        return left_node        
    
    def expression(self):
        left_node=self.term()
        while self.token.value=='+' or self.token.value=='-':
            operation=self.token
            self.move()
            right_node=self.term()
            left_node=[left_node,operation,right_node]
        return left_node
    def statement(self):
       #Assignment 

        if self.token.type.startswith('DEC') :
            self.move()
            left_node=self.variable()
            self.move()
            if self.token.value=='=':
                operation=self.token
                self.move()
                right_node=self.statement()
                return [left_node,operation,right_node]
            else:
                operation=Operator('=')
                right_node=Null()
                return [left_node,operation,right_node]
        elif self.token.value =='கொடு':
            token=self.token
            self.move()
            return [token,self.statement()]   
        
        elif self.token.value=='கூப்பிடு':
            return [self.token,self.function_call()]        
        
        elif self.token.value=='இறக்கு':
            token=self.token
            self.move()
            file_name=self.token
            self.move()
            return [token,file_name]
                 
        #Arithematic operation
        elif self.token.type in ['எண்',"கணிதசெயலி" ,'பட்டியல்',"மாறி",'சொல்','KEY','மெய்ப்பு','MEM'] or self.token.value ==['கூப்பிடு','(',')']:
            return self.logical_expression()
        
        elif self.token.value =='இது':
            return [self.token,self.if_statements()]
        elif self.token.value =='அதுவரை':
            return [self.token,self.while_statement()]
        elif self.token.value=='இதில்':
            return [self.token,self.for_statement()]
        
        elif self.token.value =='வேலை':
            return [self.token,self.function_block()]
        elif self.token.type =='BIF':
            return [self.token,self.builtin_function()]
        else:
            Name_Error(Parser.line_no,f"{self.token} என்று எதுவும் இல்லை")


        
    def parse(self):
        
        output=[]

        while self.idx<len(self.tokens):
            a=self.statement()
            output.append(a)
            Parser.line_no+=1
           
        return output    
    
    
    
    def move(self):
        self.idx+=1
        if self.idx<len(self.tokens):
            self.token=self.tokens[self.idx]
    
      

        