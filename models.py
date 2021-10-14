import db


#Clase para manejar los usuarios
class usuario():
    id=0
    nombre=''
    identificacion= ''
    usuario=''
    password=''
    tipo=''

    def __init__(self, pid, pusuario, ppassword): 
        self.id = pid
        self.usuario = pusuario
        self.password = ppassword
    
    #Metodo para verificar el usuario contra la base de datos
    def autenticar(self):
        sql = "SELECT * FROM usuarios WHERE usuario = ? AND password = ?;"
        obj = db.ejecutar_select(sql, [self.usuario, self.password])
        if obj:
            if len(obj) >0:
                return True
        return False
