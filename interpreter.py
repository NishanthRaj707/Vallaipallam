from tokens import *
from data import Scope,Data
import os
from lexer import Lexer
from parser import Parser
from errors import *
class Interpreter:
    continuing=0 #to know break statement or continue statement is used
    value_to_return=''
    line_no=1
    def __init__(self,tree,root):
        self.tree=tree
        self.data=root
    def read_எண்(self,value,object=None):
        return float(value)
    def read_FO(self,value,object=None):
        return FileObject(value)
    def read_காலி(self,value,object=None):
        return Null()
    def read_KEY(self,value,object=None):
        return value
    def read_சொல்(self,value,object=None):
        return str(value)
    def read_பட்டியல்(self,value,object=None):
        return list(value)
    def read_மாறி(self,id,object=None):
        if not object or id in self.data.variables:
            variable=self.data.get(id)
            variable_type=variable.type
        elif isinstance(object,Scope): 
            variable=object.get(id)
            variable_type=variable.type              
        return getattr(self,f'read_{variable_type}')(variable.value)   

    def read_மெய்ப்பு(self,value):
        return bool(value)
    
    def interpret_if(self,tree,object=None):
        executed=0
        for i in range(len(tree[1][0])):
            #Evaluating the condtition
            
            condition=self.interpret(tree[1][0][i],object)
            actions=[]
            #If true excuting the action
            if condition.value=='மெய்':
                executed+=1
                for j in range(len(tree[1][1][i])):
                    action=self.interpret(tree[1][1][i][j],object)
                    actions.append(action)
                output=condition,actions
                return list(output)
            
        else:
            if executed==0:
                if len(tree[1][0])<len(tree[1][1]):
                    for j in range(len(tree[1][1][-1])):
                        action=self.interpret(tree[1][1][-1][j],object)
                        actions.append(action)
                    output=condition,actions
                    return list(output)
                                    
    #While lopp interpretation   
    def interpret_while(self,tree,object=None):
        executed=0
        condition=self.interpret(tree[1][0]) 
        condition=Boolean(condition)
        actions=[]
            #If true excuting the action
        if condition.value=='மெய்':
            executed+=1
            for i in tree[1][1][0]:
                action=self.interpret(i,object)
                if action=='தொடர்':
                    output=condition,actions
                    return list(output)
                elif action=='ரத்து':
                    actions.append(action)
                    output=condition,actions
                    return list(output)
                if isinstance(action,list) and action[0]=='கொடு':
                    actions.append(action)
                    output=condition,actions
                    return list(output)
                elif isinstance(action,list):
                    if Interpreter.continuing==1:
                        output=condition,actions
                        return list(output)
                    elif Interpreter.continuing==-1:
                        actions.append(action)
                        output=condition,actions,0
                        return list(output)
                actions.append(action)
                output=condition,actions
            return list(output)
            
        else:
            if executed==0:
                if len(tree[1][1])==2:
                    for j in range(len(tree[1][1][-1])):
                        action=self.interpret(tree[1][1][-1][j])
                        actions.append(action)
                    output=condition,actions
                    return list(output)
                  
    #Computation of the function                            
    def compute_function(self,tree):
        actions=[]
        identifier=tree[0]
        values=tree[1]
        f=0

        for i in Scope.details:
            if identifier.value==i[1]:
                identifier=i[0]
                f=1  
        else: 
            if f==0:
                Name_Error("",f"{identifier.value} என்று எதுவும் இல்லை") 
        if len(self.data.get(identifier.value).value[0])==len(values):
            for j in list(zip(identifier.localvariables,['=']*len(values),values)):
                left_node=Variable(j[0])
                right_node=j[2]
                identifier.set(left_node,right_node)    

            if identifier.value in Data.variables:
                action=self.data.get(identifier.value).value[-1]
                for i in action:
                    if i[0].value=='கொடு':
                        return_value=self.interpret(i[1],object=identifier)
                        actions.append(return_value)
                        return return_value
                    
                    returned=self.interpret(i,object=identifier)
                    if Interpreter.continuing==-2:
                        return Interpreter.value_to_return
                    actions.append(returned)
            return None      
        else:
            Type_Error(Interpreter.line_no,"")

    
    def compute_unary(self,operator,operand):
        operand_type= "மாறி" if str(operand.type).startswith("மாறி") else (operand.type)
        left=getattr(self,f"read_{operand_type}")(operand.value)
        if operator.value=='+':
            return +left
        elif operator.value=='-':
            return -left
        elif operator.value=='அல்ல':
            output=1.0 if not operand else 0.0
            return Boolean(output)

        
    def compute_operation(self,left,op,right,object=None):
        output=None
        #Variable assignment
        if  op.value=='=':
            if isinstance(right,float):
                right=Number(right)
            if not object:    
                left.type=f'மாறி({right.type})'
                self.data.set(left,right)
                output=True
            elif isinstance(object,Scope):
                object.set(left,right)
                output=True                  
        
        if not isinstance(left,float):
            left_type="மாறி" if left.type.startswith('மாறி') else left.type
            left=getattr(self,f'read_{left_type}')(left.value,object)
        if not isinstance(right,float):
            right_type="மாறி" if right.type.startswith('மாறி') else right.type
            right=getattr(self,f'read_{right_type}')(right.value,object)
        #Arithematic,Comparison,Logical operations and Membership operators
        if not output:
                if op.value=='+' :
                    output=left+right
                elif op.value=='-' :
                    output=left-right
                elif op.value=='*' :
                    output=left*right
                elif op.value=='/':
                    if right==0:
                        Zero_Division_Error(Interpreter.line_no,"0 வகுக்க கூடாது")
                    output=left/right
                elif op.value=='%':
                    output=left%right    
                elif op.value=='>':
                    output=1.0 if left>right else 0.0
                    return Boolean(output)    
                elif op.value=='<':
                    output=1.0 if left<right else 0.0  
                    return Boolean(output) 
                elif op.value=='>=':
                    output=1.0 if left>=right else 0.0
                    return Boolean(output)   
                elif op.value=='<=':
                    output=1.0 if left<=right else 0.0  
                    return Boolean(output) 
                elif op.value=='==':
                    output=1.0 if left==right else 0.0  
                    return Boolean(output) 
                elif op.value=='!=':
                    output=1.0 if left!=right else 0.0  
                    return Boolean(output) 
                elif op.value=='மற்றும்':
                    output=1.0 if left and right else 0.0   
                    return Boolean(output)
                elif op.value=='அல்லது':
                    output=1.0 if left or right else 0.0   
                    return Boolean(output)
                elif op.value=='உள்ளது':
                    output=1.0 if left in right else 0
                    return Boolean(output)                                                                                                
                
                if type(output)==float:
                    return Number(output)
                elif type(output)==str:
                    return String(output)
        
    def interpret(self,tree=None,object=None):
       if tree is None:
           tree=self.tree
       
       if isinstance(tree,list) and len(tree)==2 and isinstance(tree[0],Operator):
           expression=tree[1]
           if isinstance(expression,list):
               expression=self.interpret(expression)
           return self.compute_unary(tree[0],expression) 

       if isinstance(tree,list) :
            executed=0
            if isinstance(tree[0],Condition) and isinstance(tree,list):
                      
                    if tree[0].value=='இது':
                        return self.interpret_if(tree,object)
                    
                    elif tree[0].value=='அதுவரை':
                        primary_tree=tree
                        output=[]
                        condition='மெய்'
                        while condition=='மெய்':
                            returnedvalue=self.interpret_while(primary_tree)
                            if not returnedvalue:
                                break
                            elif returnedvalue[-1]==0:
                                break
                            output.append(returnedvalue[1])
                            condition=returnedvalue[0].value
                            
                        return output
                    elif tree[0].value=='இதில்':
                        #for loop execution
                        if not isinstance(tree[1][0],list):
                            sequence=self.read_சொல்(tree[1][0].value) if tree[1][0].type.startswith('சொல்') else self.read_பட்டியல்(tree[1][0].value)
                        else:
                            sequence=self.interpret(tree[1][0],object)
                        var=tree[1][1]
                        actions=tree[1][2]
                        output=[]
                        continuing=0
                        for i in sequence if type(sequence)==str else sequence.value:
                            self.data.set(var,String(i) if type(i)==str else i)
                            for j in actions:
                                value=self.interpret(j,object)
                                if Interpreter.continuing==1:
                                    break
                                elif Interpreter.continuing==-1:
                                    break                  
                                output.append(value)
                            if Interpreter.continuing==1:
                                Interpreter.continuing=0
                                continue
                            elif Interpreter.continuing==-1:
                                Interpreter.continuing=0
                                break    
                        return output    
            elif isinstance(tree[0],Function) : 
                #Function implementation and defining the body    
                if tree[0].value=='வேலை':
                    local=tree[1][0]
                    local=Scope(local.value)
                    for i in tree[1][1][0]:
                        if i[1].value=='=':
                            left_node=i[0]
                            right_node=i[2]
                            local.set(left_node,right_node)#asssinging the function body as the value to the function name
                    self.data.set(local,List(tree[1][1]))         
                elif tree[0].value=='கூப்பிடு':
                    return self.compute_function(tree[1])
                elif tree[0].value=='கொடு':
                    Interpreter.continuing=-2
                    return_value=self.interpret(tree[1],object)
                    Interpreter.value_to_return=return_value
                return None
            elif isinstance(tree[0],Built_in_Function):
                values=tree[1]
                arguements=[]
                Hasvariable=False
                #implementation of built in functions
                if len(tree[1])>0:
                    if isinstance(tree[1][0],Variable):
                        variable=tree[1][0]
                        Hasvariable=True
                for i in values:
                    arguement=self.interpret(i,object)
                    arguements.append(arguement)                    
                if tree[0].value=='வெளியிடு':
                    tree[0].வெளியிடு(arguements)
                elif tree[0].value=='அளவு':
                    return tree[0].அளவு(arguements,Interpreter.line_no)    
                elif tree[0].value=='உள்ளீடு':
                    return tree[0].உள்ளீடு(arguements)
                elif tree[0].value=='எண்':
                    return tree[0].எண்(arguements,Interpreter.line_no)  
                elif tree[0].value=='வரம்பு':
                    return tree[0].வரம்பு(arguements,Interpreter.line_no) 
                elif tree[0].value=='சொல்':
                    return tree[0].சொல்(arguements,Interpreter.line_no)
                elif tree[0].value=='பட்டியல்':
                    return tree[0].பட்டியல்(arguements,Interpreter.line_no)
                elif tree[0].value=='வகை':
                    return tree[0].வகை(arguements)
                elif tree[0].value=='பிரி':
                    element=String(arguements[0]) if type(arguements[0])==str else arguements[0]
                    return element.பிரி(arguements)
                elif tree[0].value=='இணை':
                    element=List(arguements[0]) if type(arguements[0])==list else arguements[0]
                    value=element.இணை(arguements,line_no=Interpreter.line_no)  
                    if Hasvariable==True:
                        self.data.set(variable,value)
                elif tree[0].value=='நீக்கு':
                    element=List(arguements[0]) if type(arguements[0])==list else arguements[0]
                    value=element.நீக்கு(arguements,Interpreter.line_no)  
                    if Hasvariable==True:
                        self.data.set(variable,value)                    
                elif tree[0].value=='செருகு':
                    element=List(arguements[0]) if type(arguements[0])==list else arguements[0]
                    value=element.செருகு(arguements,Interpreter.line_no)  
                    if Hasvariable==True:
                        self.data.set(variable,value)                                                             
                elif tree[0].value=='திற':
                    return tree[0].திற(arguements,Interpreter.line_no)
                elif tree[0].value=='படி':
                    element=arguements[0]
                    return element.படி(arguements)
                elif tree[0].value=='எழுது':
                    element=arguements[0]
                    return element.எழுது(arguements,Interpreter.line_no)
                elif tree[0].value=='மூடு':
                    element=arguements[0]
                    return element.மூடு(arguements)
                return None
            
            if not isinstance(tree[0],list) and (tree[0].type=='சொல்' or tree[0].type=='பட்டியல்' or tree[0].value in self.data.variables):
                sliced=None
                if isinstance(tree[1],List):
                    value=tree[0].value if not isinstance(tree[0],Variable) else self.read_மாறி(tree[0].value)
                    if len(tree[1].value)==1:
                       slice_range=tree[1].value
                       sliced=value[int(slice_range[0].value)]
                    elif len(tree[1].value)==3:
                        slice_range=tree[1].value
                        sliced=value[int(slice_range[0].value):int(slice_range[-1].value)]  
                    elif len(tree[1].value)==5:                
                        slice_range=tree[1].value
                        sliced=value[int(slice_range[0].value):int(slice_range[2].value):int(slice_range[-1].value)]     
                    return sliced 
            if not isinstance(tree[0],list) and tree[0].value=='இறக்கு':
                file_name=tree[1]
                if os.path.isfile(f'{file_name}.jnr'):
                    root=Data()

                    f=open(f'{file_name}.jnr','r',encoding='utf-8')
                    b=f.read()

                    if b :
                        tokens=Lexer(b)
                        a=tokens.tokenize()
                        tree=Parser(a,root)
                        trees=tree.parse()
                        output=Interpreter(trees,root)
                else:
                    raise Exception('file not found')
                              
            else:
                #Evaluating of left subtree
                
                left_node=tree[0]
                if isinstance(left_node,list):
                    left_node=self.interpret(left_node,object=object)

                
                #Evaluating of right subtree
                if not len(tree)<=2:     
                    right_node=tree[2]
                    if isinstance(right_node,list):
                        right_node=self.interpret(right_node,object=object)

                root_node=tree[1]    
                return self.compute_operation(left_node,root_node,right_node,object=object)
                       
       if isinstance(tree,Keyword):
           if tree.value=='ரத்து':
               Interpreter.continuing=-1
           elif tree.value=='தொடர்':
               Interpreter.continuing=1    
           return tree.value
       elif isinstance(tree,Boolean):
           return tree
       elif isinstance(tree,Variable):
           return self.read_மாறி(tree.value,object)
       else:
           return tree
       
    def home(self):
        output=[]
        for i in self.tree:
            a=self.interpret(i) 
            Interpreter.line_no+=1
            output.append(a)
        return output
