import re
from Token import *
import os
from urllib.request import  urlopen
import webbrowser as wb



linea = 0
columna = 0
counter = 0
contador = 0 

Errores = []


    
signos = { "SUM":'\+',"RES":'\-', "MULTI":'\*',"DIV":'\/',"PARA":'\(', "PARC":'\)'}

def inic(text):
    global linea, columna, counter, Errores
    linea = 1
    columna = 1
    listaTokens = []
    while counter < len(text):

        if re.search(r"[A-Za-z]", text[counter]): #IDENTIFICADOR
            aux = StateIdentifier(linea, columna, text, text[counter])
            if(aux != None):
                listaTokens.append(aux)

        elif re.search(r"[0-9]", text[counter]): #NUMERO
            aux = StateNumber(linea, columna, text, text[counter])
            if(aux != None):
                listaTokens.append(aux)  

        elif re.search(r"[\n]", text[counter]):#SALTO DE LINEA      
            counter += 1
            linea += 1
            columna = 0 
        elif re.search(r"[ \t]", text[counter]):#ESPACIOS Y TABULACIONES
            counter += 1
            columna += 1 

        else:
            #SIGNOS
            isSign = False
            for clave in signos:
                valor = signos[clave]
                if re.search( r"^" + valor + "$", text[counter]):
                    listaTokens.append(Token(valor.replace("\\",""),'Signo',linea,columna))
                    counter += 1
                    columna += 1
                    isSign = True
                    break
            if not isSign:
                listaTokens.append(Token(text[counter],'texto',linea,columna))
                counter += 1
                columna += 1
    print("terminé")
    return listaTokens

#[linea, columna, tipo, valor]

def StateIdentifier(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[counter]):#IDENTIFICADOR
            return StateIdentifier(line, column, text, word + text[counter])
        else:
            
            Aux = Token(word,'Val',line, column) 
            return Aux 
            #agregar automata de identificador en el arbol, con el valor
    else:
        Aux = Token(word,'Val',line, column)
        return Aux 
     
def StateNumber(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search(r"[0-9]", text[counter]):#ENTERO
            return StateNumber(line, column, text, word + text[counter])
        elif re.search(r"\.", text[counter]):#DECIMAL
            return StateDecimal(line, column, text, word + text[counter])
        else:
            Aux = Token(word,'Val',line, column)
            return Aux 
    else:
        Aux = Token(word,'Val',line, column)
        return Aux

def StateDecimal(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search(r"[0-9]", text[counter]):#DECIMAL
            return StateDecimal(line, column, text, word + text[counter])
        else:
            Aux = Token(word,'Val',line, column) 
            return Aux
            #agregar automata de decimal en el arbol, con el valor
    else:
        Aux = Token(word,'Val',line, column)
        return Aux

def OperacionAUX(Lista):
    conta = 0
    bandera = True
    switch = 0 

    while(bandera == True and conta <len(Lista)):
        print(Lista[conta].get_lexema())
        if re.search(r"[\(]", Lista[conta].get_lexema()):

            if(switch==0):
                switch=2
            else:
                bandera = False
                break

        if switch == 0:
            if Lista[conta].get_tipo() == 'Val':
                switch = 1
            else: 
                bandera = False

        elif switch ==1:
            if Lista[conta].get_tipo() == 'Signo':
                switch = 0
            else: 
                bandera = False

        elif switch ==2:
            bandera = Parentesis(Lista)
            switch=1
        
        conta+=1

    if(bandera==True):
        if switch!=1:
            bandera = False
        
    return bandera

 #END


def Operacion(Lista):
    global contador
    bandera = True
    switch = 0 

    while(bandera == True and contador <len(Lista)):
        print(Lista[contador].get_lexema())
        if re.search(r"[\(]", Lista[contador].get_lexema()):

            if(switch==0):
                switch=2
            else:
                bandera = False
                break

        if switch == 0:
            if Lista[contador].get_tipo() == 'Val':
                switch = 1
            else: 
                bandera = False

        elif switch ==1:
            if Lista[contador].get_tipo() == 'Signo':
                switch = 0
            else: 
                bandera = False

        elif switch ==2:
            bandera = Parentesis(Lista)
            switch=1
        
        contador+=1

    if(bandera==True):
        if switch!=1:
            bandera = False
        
    return bandera

 #END

def Parentesis(Lista):
    global contador
    bandera = True
    Faltantes=[]
    contador+=1
    while(contador<len(Lista)and bandera==True):
        print(Lista[contador].get_lexema())
        if re.search(r"[\)]", Lista[contador].get_lexema()):
            print(len(Faltantes))
            bandera = OperacionAUX(Faltantes)

        elif re.search(r"[\(]", Lista[contador].get_lexema()):
            bandera = Parentesis(Lista)
            Faltantes.append(Token('','ID',0,0))
        else:
            Faltantes.append(Lista[contador])
        
        contador+=1
    return bandera

def GeneradorHTML(TokenList):
    codigo_tabla = ''
    contador=1
    token = TokenList

    text = '<tr><td class="column1">'+str(contador)+ '</td>'+'<td class="column2">'+token.get_lexema()+ '</td>'+'<td class="column3">'+str(token.get_tipo())+ '</td>'+'<td class="column4">'+str(token.get_columna())+ '</td>'+'</tr>'
    contador+=1
    codigo_tabla += text

    
    codigo_pagina ='<!DOCTYPE html> <html lang="en"> <head> 	<title>Sintactico</title> 	<meta charset="UTF-8"> 	<meta name="viewport" content="width=device-width, initial-scale=1"> <!--===============================================================================================-->		<link rel="icon" type="image/png" href="images/icons/favicon.ico"/> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="css/util.css"> 	<link rel="stylesheet" type="text/css" href="css/main.css"> <!--===============================================================================================--> </head> <body> 	 	<div class="limiter"> 		<div class="container-table100"> 			<div class="wrap-table100"> 				<div class="table100"> 					<table> 						<thead> 							<tr class="table100-head"> 								<th class="column1">No.</th> 								<th class="column2">Descripcion</th> 								<th class="column3">Fila</th> 								<th class="column4">Columna</th> <th class=""></th> <th class=""></th>							</tr> 						</thead> 						<tbody>'+ codigo_tabla+'</tbody> 					</table> 				</div> 			</div> 		</div> 	</div>   	  <!--===============================================================================================-->	 	<script src="vendor/jquery/jquery-3.2.1.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/bootstrap/js/popper.js"></script> 	<script src="vendor/bootstrap/js/bootstrap.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/select2/select2.min.js"></script> <!--===============================================================================================--> 	<script src="js/main.js"></script>  </body> </html>'

    html = open('Sintactico.html','w')
    html.write(codigo_pagina)
    html.close()
    wb.open_new('C:\\Users\\Daniel A\\Downloads\\OLC1_2S-master\\OLC1_2S-master\\Ejemplo2\\Sintactico.html')



entrada = open('entrada.rmt')
contenido = entrada.read()

tokens = inic(contenido)

val =Operacion(tokens)
holi = Token(contenido,val,0,0)
GeneradorHTML(holi)
