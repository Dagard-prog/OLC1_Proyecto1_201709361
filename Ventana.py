from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from AnalisisCSS import CSS
from AnalisisHTML import HTML
from AnalisisJS import JS
from AnalisisOperaciones import lptm
from Token import *
import os
from urllib.request import  urlopen
import webbrowser as wb


class Ventana:

    def __init__(self, window):
        self.ventana = window
        self.ventana.title("Ejemplo 2")

        frame = LabelFrame(self.ventana, text = '')
        frame.grid(row=0,column=0,columnspan=20,pady=20)

        #############################################_MENU_#############################################
        self.cargar = Button(frame, text ="Cargar", command = self.fileMenu)
        self.cargar.grid(row=0,column=0)

        self.Css = Button(frame, text ="Análisis CSS", command = self.A_CSS)
        self.Css.grid(row=0,column=1)

        self.Js = Button(frame, text ="Análisis JS", command = self.A_JS)
        self.Js.grid(row=0,column=2)

        self.HTML = Button(frame, text ="Análisis HTML", command = self.A_HTML)
        self.HTML.grid(row=0,column=3)

        self.Sintac = Button(frame, text ="Análisis Sintactico", command = self.A_Sintactico)
        self.Sintac.grid(row=0,column=4)

        self.salir = Button(frame, text ="Salir", command = self.terminar)
        self.salir.grid(row=0,column=5)

        ############################################_ENTRADA_############################################
        Label(frame,text='Archivo de Entrada:').grid(row=3,column=5)
        self.entrada = Text(frame, height=30, width=60)
        self.entrada.grid(row=4,column=5)

        Label(frame,text='   =>   ').grid(row=4,column=15)

        Label(frame,text='Resultado:').grid(row=3,column=16)
        self.salida = Text(frame, height=30, width=60)
        self.salida.grid(row=4,column=16)

        Label(frame,text='              ').grid(row=3,column=20)
    #END


    def fileMenu(self):
        filename = askopenfilename()

        archivo = open(filename,"r")
        texto = archivo.read()
        archivo.close()

        self.entrada.insert(INSERT,texto)
        return
    #END

    def A_Sintactico(self):
        texto = self.entrada.get("1.0",END)
        lista = texto.split("\n")
        holi = lptm(lista)

        Ventana.GeneradorHTML(Ventana,holi)

    def A_CSS(self):

        texto = self.entrada.get("1.0",END)

        Lista_Tokens = CSS(texto)
        print(len(Lista_Tokens))
        contador = 0
        listado = ""
        while contador<len(Lista_Tokens):
            listado = listado + Lista_Tokens[contador].get_lexema()+ "    "+ Lista_Tokens[contador].get_tipo()+"\n"
            contador+=1
        self.printSalida(listado)
    #END

    def A_JS(self):

        texto = self.entrada.get("1.0",END)

        Lista_Tokens = JS(texto)
        print(len(Lista_Tokens))
        contador = 0
        listado = ""
        while contador<len(Lista_Tokens):
            listado = listado + Lista_Tokens[contador].get_lexema()+ "    "+ Lista_Tokens[contador].get_tipo()+"\n"
            contador+=1
        self.printSalida(listado)
    #END
    def A_HTML(self):

        texto = self.entrada.get("1.0",END)

        Lista_Tokens = HTML(texto)
        print(len(Lista_Tokens))
        contador = 0
        listado = ""
        while contador<len(Lista_Tokens):
            listado = listado + Lista_Tokens[contador].get_lexema()+ "    "+ Lista_Tokens[contador].get_tipo()+"\n"
            contador+=1
        self.printSalida(listado)
    #END
    

  
    def printSalida(self,texto_a_imprimir):
        self.salida.insert(INSERT,texto_a_imprimir)

        messagebox.showinfo("Holi", "Análisis finalizado:\n")
            
        #END
    def GeneradorHTML(self,TokenList):
        codigo_tabla = ''
        contador=1
        for token in TokenList:

            text = '<tr><td class="column1">'+str(contador)+ '</td>'+'<td class="column2">'+token.get_lexema()+ '</td>'+'<td class="column3">'+str(token.get_tipo())+ '</td>'+'<td class="column4">'+str(token.get_columna())+ '</td>'+'</tr>'
            contador+=1
            codigo_tabla += text

        
        codigo_pagina ='<!DOCTYPE html> <html lang="en"> <head> 	<title>Sintactico</title> 	<meta charset="UTF-8"> 	<meta name="viewport" content="width=device-width, initial-scale=1"> <!--===============================================================================================-->		<link rel="icon" type="image/png" href="images/icons/favicon.ico"/> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css"> <!--===============================================================================================--> 	<link rel="stylesheet" type="text/css" href="css/util.css"> 	<link rel="stylesheet" type="text/css" href="css/main.css"> <!--===============================================================================================--> </head> <body> 	 	<div class="limiter"> 		<div class="container-table100"> 			<div class="wrap-table100"> 				<div class="table100"> 					<table> 						<thead> 							<tr class="table100-head"> 								<th class="column1">No.</th> 								<th class="column2">Descripcion</th> 								<th class="column3">Fila</th> 								<th class="column4">Columna</th> <th class=""></th> <th class=""></th>							</tr> 						</thead> 						<tbody>'+ codigo_tabla+'</tbody> 					</table> 				</div> 			</div> 		</div> 	</div>   	  <!--===============================================================================================-->	 	<script src="vendor/jquery/jquery-3.2.1.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/bootstrap/js/popper.js"></script> 	<script src="vendor/bootstrap/js/bootstrap.min.js"></script> <!--===============================================================================================--> 	<script src="vendor/select2/select2.min.js"></script> <!--===============================================================================================--> 	<script src="js/main.js"></script>  </body> </html>'

        html = open('Sintactico.html','w')
        html.write(codigo_pagina)
        html.close()
        wb.open_new('C:\\Users\\Daniel A\\Downloads\\OLC1_2S-master\\OLC1_2S-master\\Ejemplo2\\Sintactico.html')


    def terminar(self):
        self.ventana.destroy()
        return
        #END

    #END



###################################################################################################

