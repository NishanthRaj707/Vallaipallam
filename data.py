from errors import *
class Data:
    variables={}
    def __init__(self):
        self.variables={}
        Data.variables.update(self.variables) 
    def get(self,id):
        try:    
           return Data.variables[id]
        except KeyError:
             Name_Error("",f"{id} என்று எதுவும் இல்லை")
    def get_all(self):
        return self.variables
    def set(self,variable,expression):
        variable_name=variable.value
        self.variables[variable_name]=expression 
        Data.variables.update(self.variables)

class Scope(Data):
    details=[]
    def __init__(self,name):
          self.localvariables={}
          self.value=name
          Scope.details.append([self,name])
    def get(self,id):
        try:    
            if id in self.variables:
                 return self.variables[id]
            else: 
                return self.localvariables[id]
        except KeyError:
            Name_Error("",f"{id} என்று எதுவும் இல்லை")
                
    def get_all(self):
        return self.localvariables
    
    def set(self,variable,expression):
        variable_name=variable.value
        self.localvariables[variable_name]=expression                     

        