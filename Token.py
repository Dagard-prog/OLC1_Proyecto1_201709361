class Token:

    fila = 0
    columna = 0
    lexema = ""
    tipo_lexema = ""

    def __init__(self,lexema,tipo_lexema,fila,columna):
        self.fila = fila
        self.columna = columna
        self.lexema = lexema
        self.tipo_lexema = tipo_lexema

    #END
#SETS------------------------------------------------------------------
    def set_fila(self,fila):
        self.fila = fila

    #END

    def set_columna(self,columna):
        self.columna = columna

    #END


    def set_lexema(self,lexema):
        self.lexema = lexema
    
    #END

    def set_tipo(self,tipo):
        self.tipo_lexema = tipo

    #END

#GETS--------------------------------------------------------------------
    def get_fila(self):
        return self.fila

    #END

    def get_columna(self):
        return self.columna 

    #END


    def get_lexema(self):
        return self.lexema
    
    #END

    def get_tipo(self):
        return self.tipo_lexema 

    #END


#END