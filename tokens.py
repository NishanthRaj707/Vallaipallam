
import os
from errors import *
class Token:
    def __init__(self,type,value):
        self.type=type
        self.value=value
    def __repr__(self):
        return str(self.value) 
    def அளவு(self,arguements,line_no):
        try:
            value=arguements[0].value if isinstance(arguements,list) else arguements
            return len(value)
        except:
            Value_Error(line_no,f'{value} alavu ellai')  
    def வெளியிடு(self,arguements):
        for i in arguements:
            print(i,end='  ')
        print()    
    def உள்ளீடு(self,arguements):
        input_value=input(f'{arguements[0].value}')    
        return String(input_value)
    def எண்(self,arguements,line_no):
        try:
           value=arguements[0].value if isinstance(arguements,list) else arguements
           return Number(float(value)) 
        except:
            Value_Error(line_no,f"{arguements[0].value} --> எண் மாற்ற முடியாது")
    def சொல்(self,arguements,line_no):
        try:
           value=arguements[0].value if isinstance(arguements,list) else arguements
           return String(str(value))
        except IndexError:
            return String(str())
        except:
            Value_Error(line_no,f"{arguements[0].value} --> சொல் மாற்ற முடியாது")

    def பட்டியல்(self,arguements,line_no):
        try:
            value=arguements[0].value if isinstance(arguements,list) else arguements
            return List(list(value))
        except IndexError:
            return List(list())
        except:
            Value_Error(line_no,f"{arguements[0].value} --> பட்டியல் மாற்ற முடியாது")
    def வகை(self,arguements):
        value_type=None
        if isinstance(arguements[0],Number):
            value_type='எண்'
        elif isinstance(arguements[0],String):
            value_type='சொல்'
        elif isinstance(arguements[0],List):
            value_type='பட்டியல்'    
        elif isinstance(arguements[0],Function):
            value_type='வேலை'
            
                    
        return value_type
    
    def வரம்பு(self,arguements,line_no):
        number=int(arguements[0]) if type(arguements[0])==int or type(arguements[0])==float else int(arguements[0].value)
        if len(arguements)==1:
            value=list(range(int(number)))
            return List([Number(i) for i in value])
        elif len(arguements)==2:
            number1=arguements[1] if type(arguements[1])==int or type(arguements[1])==float else arguements[1].value
            value=list(range(int(number),int(number1)))
            return List([Number(i) for i in value])
        elif len(arguements):
            number1=arguements[1] if type(arguements[1])==int or type(arguements[1])==float else arguements[1].value
            number2=arguements[2] if type(arguements[2])==int or type(arguements[2])==float else arguements[2].value
            value=list(range(number),int(number1),int(number2))
            return List([Number(i) for i in value])
        else:
            raise Exception('Invalid paramenters')
        
    def திற(self,arguements,line_no):
        file_name=arguements[0].value
        match arguements[1].value:
            case 'ப':
                mode='r'
            case 'எ':
                mode='w'
            case 'சே':
                mode='a' 
            case _:
                ValueError(line_no,f"{arguements[1]} என்ற முறை இல்லை")               
    
        if os.path.isfile(f'{file_name}'):
            return FileObject(open(file_name,mode,encoding='utf-8')) 
        elif mode=='w' or mode=='a':
            return FileObject(open(file_name,mode,encoding='utf-8')) 
        else:
            Name_Error(line_no,f"{file_name} என்ற கோப்பு இல்லை ")
            
class Number(Token):
    def __init__(self,value):
        super().__init__("எண்",value)
class Operator(Token):
    def __init__(self,value):
        super().__init__("கணிதசெயலி",value)
class Declaration(Token):
    def __init__(self, value):
        super().__init__("DEC", value)   
class Variable(Token):
    def __init__(self,value):
        super().__init__("மாறி", value) 

class Logical(Token):
    def __init__(self,value):
        super().__init__("தருக்க",value)
class Comparison(Token):
    def __init__(self,value):
        super().__init__("ஒப்பீடு", value)    
class Boolean(Token):
    def __init__(self,value):
        if value==0.0 or value =='பொய்' :                                            
            value = 'பொய்'
        elif isinstance(value,float) or value=='மெய்':
            value = 'மெய்'    
        super().__init__("மெய்ப்பு",value)                                   
class Null(Token):
    def __init__(self):
        super().__init__("காலி","காலி")
class Condition(Token):
    def __init__(self,value):
        super().__init__("CON",value)
class String(Token):
    def __init__(self,value):
        super().__init__("சொல்",value)
    def பிரி(self,arguements):
        value=arguements[0]
        limit=arguements[1].value if len(arguements)==2 else None
        maxsplit=arguements[2].value if len(arguements)==3 else -1
        if limit:
            return List([String(i) for i in value.split(limit,maxsplit)])
        else:
            return  List([String(i) for i in value.split()])   
class List(Token):
    def __init__(self,value):
        super().__init__("பட்டியல்",value)
    def இணை(self,arguements,line_no):
        value=arguements[0]
        element=arguements[1]
        if type(element)==int or type(element)==float :
            element=self.எண்(element,line_no)
        elif type(element)==str:
            element=self.சொல்(element,line_no)
        elif type(element)==list:
            element=self.பட்டியல்(element,line_no)        
        value.append(element)
        return List(value)    
    def நீக்கு(self,arguements,line_no):
        value=arguements[0]
        element=arguements[1] if isinstance(arguements[1],int) else -1
        value.pop(element)
        return List(value) 
    def செருகு(self,arguements,line_no):
        value=arguements[0]
        index=int(arguements[1].value)
        element=arguements[2]
        if type(element)==int or type(element)==float :
            element=self.எண்(element)
        elif type(element)==str:
            element=self.சொல்(element)
        elif type(element)==list:
            element=self.பட்டியல்(element)              
        value.insert(index,element)
        return List(value)     
class Delimiter(Token):
    def __init__(self,value):
        super().__init__("DELIMIT",value)                                
class Keyword(Token):
    def __init__(self,value):
        super().__init__("KEY",value)      
class Member(Token):
    def __init__(self,value):
        super().__init__("MEM",value)        
class Function(Token):
    def __init__(self,value):
        super().__init__('வேலை',value)
class Built_in_Function(Token):
    def __init__(self,value):
        super().__init__("BIF", value)
        
class FileObject(Token):
    def __init__(self,value):
        self.name=value.name
        self.mode=value.mode
        self.encoding=value.encoding
        super().__init__("FO",value)
    def படி(self,arguements):
        element=arguements[0]
        noofchar=arguements[1] if len(arguements)==2 else -1
        return String(element.value.read(noofchar))
    
    def எழுது(self,arguements,line_no):
        element=arguements[0]
        if type(arguements[1].value)==str:
            return Number(element.value.write(arguements[1].value))
        else:
            Type_Error("","சொல் வகை மட்டும்")
          

    def மூடு(self,arguements):
        element=arguements[0]
        return element.value.close()  
        