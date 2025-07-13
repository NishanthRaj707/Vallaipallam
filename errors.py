import sys
class Error:
    color='\033[91m'
    default='\033[0m'
    def __init__(self,error,line,value):
        self.error=error
        self.line=line
        self.value=value
        print(f"{Error.color}வரிசை:{self.line}\nபிழை:{self.error}\n{self.value}{Error.default}",file=sys.stderr) 
        sys.exit(1)
        
class Syntax_Error(Error):
    def __init__(self,line,value):
        self.value=str(value)
        super().__init__("தொடரியல்பிழை",line,self.value)

class Name_Error(Error):
    def __init__(self,line,value):
        self.value=str(value)+" "
        super().__init__("பெயர்பிழை",line,self.value)

class Value_Error(Error):
    def __init__(self,line,value):
        self.value=str(value)+" "
        super().__init__("மதிப்புபிழை",line,self.value)

class Type_Error(Error):
    def __init__(self,line,value):
        self.value=str(value)+" "
        super().__init__("வகைபிழை",line,self.value)   

class Zero_Division_Error(Error):
    def __init__(self, line, value):
        super().__init__("0பிழை", line, value)       

class Index_Error(Error):
    def __init__(self, line, value):
        super().__init__("கரிசொல்பிழை", line, value)    

