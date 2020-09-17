import re
from Token import *
import os
from urllib.request import  urlopen
import webbrowser as wb



linea = 0
columna = 0
counter = 0

Errores = []


reservadas = ['html','head','tittle','body','h1','h2','h3','h4','h5','h6','p','br','img','a','ol',
              'ul','li','style','src','href','table','th','tr','td','caption','colgroup','col','thead',
              'tbody','tfoot']

signos = { "IGUAL":'=',"MAYOR":'>', "MENOR":'<',"DIV":'\/'}

def HTML(text):
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
        elif re.search(r"[\"]", text[counter]): #STRING
            aux = StateString(linea, columna, text, text[counter])
            if(aux != None):
                listaTokens.append(aux)
       
        elif re.search(r"[\']", text[counter]): #STRING
            aux = StateChar(linea, columna, text, text[counter])
            if(aux != None):
                listaTokens.append(aux)
              

        elif re.search(r"[\n]", text[counter]):#SALTO DE LINEA      
            counter += 1
            linea += 1
            columna = 0 
        elif re.search(r"[ \t]", text[counter]):#ESPACIOS Y TABULACIONES
            Aux = Token(' ','ESPACIO',linea,columna)
            listaTokens.append(Aux)
            counter += 1
            columna += 1 

        else:
            #SIGNOS
            isSign = False
            for clave in signos:
                valor = signos[clave]
                if re.search( r"^" + valor + "$", text[counter]):
                    listaTokens.append(Token(valor.replace("\\",""),clave,linea,columna))
                    counter += 1
                    columna += 1
                    isSign = True
                    break
            if not isSign:
                listaTokens.append(Token(text[counter],'texto',linea,columna))
                counter += 1
                columna += 1
    print(len(listaTokens))
    Reserved(listaTokens)
    GeneradorHTML(Errores)
    return listaTokens

#[linea, columna, tipo, valor]

def LPTM(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search( r"[\*]", text[counter]):#IDENTIFICADOR
            return StateMultiComment(line, column, text, word + text[counter])
        else:
            Aux = Token(word,'DIV',line, column)
            return Aux 
            #agregar automata de identificador en el arbol, con el valor
    else:
        Aux = Token(word,'DIV',line, column)
        return Aux 

def StateString(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if  re.search(r"[\"]",text[counter]):#IDENTIFICADOR
            Aux = Token(word+text[counter],'String',line, column)
            counter+=1
            columna+=1 
            return Aux 

        else:
            return StateString(line, column, text, word + text[counter])
            #agregar automata de identificador en el arbol, con el valor
    else:
        Errores.append(Token(word,'Error',linea,columna))
        counter += 1
        columna += 1
def StateChar(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if  re.search(r"[\']",text[counter]):#IDENTIFICADOR
            Aux = Token(word+text[counter],'String',line, column)
            counter+=1
            columna+=1 
            return Aux 

        else:
            return StateString(line, column, text, word + text[counter])
            #agregar automata de identificador en el arbol, con el valor
    else:
        Errores.append(word,'Error',linea,columna)
        counter += 1
        columna += 1


def StateMultiComment(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if (counter+1< len(text)):
        if (re.search(r"[\*]", text[counter]) and re.search(r"[\/]", text[counter+1])):#IDENTIFICADOR     
             Aux = Token(word+text[counter]+text[counter+1],'Comentario Multiilinea',line, column)
             counter+=2
             columna+=2
             return Aux
        else: 
            return StateMultiComment(line, column, text, word + text[counter])

            #agregar automata de identificador en el arbol, con el valor
    else:
        
        Errores.append(Token(word,'Error',linea,columna))
        counter += 1
        columna += 1

def StateIdentifier(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search(r"[a-zA-Z0-9\-]", text[counter]):#IDENTIFICADOR
            return StateIdentifier(line, column, text, word + text[counter])
        else:
            
            Aux = Token(word,'texto',line, column) 
            return Aux 
            #agregar automata de identificador en el arbol, con el valor
    else:
        Aux = Token(word,'texto',line, column)
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
            Aux = Token(word,'Integer',line, column)
            return Aux 
    else:
        Aux = Token(word,'Integer',line, column)
        return Aux

def StateDecimal(line, column, text, word):
    global counter, columna
    counter += 1
    columna += 1
    if counter < len(text):
        if re.search(r"[0-9]", text[counter]):#DECIMAL
            return StateDecimal(line, column, text, word + text[counter])
        else:
            Aux = Token(word,'Decimal',line, column) 
            return Aux
            #agregar automata de decimal en el arbol, con el valor
    else:
        Aux = Token(word,'Decimal',line, column)
        return Aux

def Reserved(TokenList):
    for token in TokenList:
        aux = token
        
        if (aux.get_tipo() == 'texto'):
            for reservada in reservadas:
                palabra = r"^" + reservada + "$"
                if re.match(palabra, aux.get_lexema(), re.IGNORECASE):
                    aux.set_tipo('reservada') 
                    break


def GeneradorHTML(TokenList):
    codigo_tabla = ''
    contador=1
    for token in TokenList:

        text = '<tr><td class="column1">'+str(contador)+ '</td>'+'<td class="column2">'+'El lexema  "'+token.get_lexema()+'"  no pertenece al abecedario'+ '</td>'+'<td class="column3">'+str(token.get_fila())+ '</td>'+'<td class="column4">'+str(token.get_columna())+ '</td>'+'</tr>'
        contador+=1
        codigo_tabla += text

    
    codigo_pagina ='<!DOCTYPE html> <html lang="en"> <head> 	<title>Errores HTML</title> 	<meta charset="UTF-8"> 	<meta name="viewport" content="width=device-width, initial-scale=1"> <!--===============================================================================================-->		<link rel="icon" type="image/png" href="images/icons/favicon.ico"/> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="css/util.css"> 	<link rel="stylesheet" type="text/css" href="css/main.css"> <!--===============================================================================================--> </head> <body> 	 	<div class="limiter"> 		<div class="container-table100"> 			<div class="wrap-table100"> 				<div class="table100"> 					<table> 						<thead> 							<tr class="table100-head"> 								<th class="column1">No.</th> 								<th class="column2">Descripcion</th> 								<th class="column3">Fila</th> 								<th class="column4">Columna</th> <th class=""></th> <th class=""></th>							</tr> 						</thead> 						<tbody>'+ codigo_tabla+'</tbody> 					</table> 				</div> 			</div> 		</div> 	</div>   	  <!--===============================================================================================-->	 	<script src="vendor/jquery/jquery-3.2.1.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/bootstrap/js/popper.js"></script> 	<script src="vendor/bootstrap/js/bootstrap.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/select2/select2.min.js"></script> <!--===============================================================================================--> 	<script src="js/main.js"></script>  </body> </html>'

    html = open('ErroresHTML.html','w')
    html.write(codigo_pagina)
    html.close()
    wb.open_new('C:\\Users\\Daniel A\\Downloads\\OLC1_2S-master\\OLC1_2S-master\\Ejemplo2\\ErroresHTML.html')


