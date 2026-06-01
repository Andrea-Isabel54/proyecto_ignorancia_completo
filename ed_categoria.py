from tkinter import *
from tkinter import ttk
from conexion import *
from ed_pregunta import *

def manipula_categorias():
    pantalla_cat=Toplevel()
    pantalla_cat.resizable(1,1)
    pantalla_cat.geometry("750x350")
    pantalla_cat.config(background="Light Sky Blue")
    pantalla_cat.title("catalogo de categorias")
    str_cat=StringVar()
    datos=()

    marco_per=Frame(pantalla_cat)
    marco_per.pack()
    marco_per.place(x=20, y=100)
    ver_sb=ttk.Scrollbar(marco_per,orient="vertical")
    ver_sb.pack(side=RIGHT, fill=Y)
    
    tabl_cat = ttk.Treeview(marco_per, columns=("col1"), yscrollcommand=ver_sb.set)
    tabl_cat.column("#0",width=155)
    tabl_cat.column("col1",width=500)
    tabl_cat.heading("#0",text="id_categoria")
    tabl_cat.heading("col1",text="Descripcion")
    tabl_cat.pack()
    
    ver_sb.config(command=tabl_cat.yview)

    def recupera_db():
        for record in tabl_cat.get_children():
            tabl_cat.delete(record)
        categs = tabla_categorias()
        for categ in categs:
            #tabl_cat.insert(parents="",index="end", iid=categ[0], text=str[0]), values=(str(categ[1]).replace(' ','_')) # la original
            tabl_cat.insert(parents="", index="end", iid=categ[0], text=str(categ[0]), values=(str(categ[1]).replace(' ','_')))
    def agrega_cat():
      inserta_categoria(str_cat.get())
      recupera_db()

    def borra_catsel():
      ab=tabl_cat.selection()[0]
      borra_categoria(ab)
      recupera_db()

    def selec_cat():
        global datos
        ab=tabl_cat.selection()[0]
        datos=selec_categoria(ab)
        print(datos)
        str_cat.set(datos[1])

    def modif_catsel():
       ab=tabl_cat.selection()[0]
       modif_categoria(ab,str_cat.get())
       recupera_db()

    recupera_db()
    et=Label(pantalla_cat,text="categoria",bg="Light Sky Blue", font='Helvetica 14 bold ')
    et.place(x=20, y=20)

    def edita_preguntas():
       global datos
       print(datos)
       manipula_preguntas(datos)

    str_cat.set("")
    pre = Entry(pantalla_cat, textvariable=str_cat, font='heelvetica 14 bold ',bg="Lavender", width=50)
    pre.place(x=120, y=20)
    b_pregunta = Button(pantalla_cat, text="pregunta",command=edita_preguntas,fg="white",bg="red4", font='Arial 12').place(x=570, y=20)
    b_per = Button(pantalla_cat, text="agregar categorias",command=agrega_cat,fg="white",bg="red4", font='Arial 12').place(x=10, y=60)
    b_modif_cat=Button(pantalla_cat,text="Modifica categoria",command=modif_catsel,fg="White",bg="red4", font='Arial 12',width=20).place(x=180,y=60)
    b_borra_cat=Button(pantalla_cat,text="Borrar categorias",command=borra_catsel,fg="White",bg="red4",font="Arial 12",width=20).place(x=400,y=60)
    b_selec_cat=Button(pantalla_cat,text="Selecciona categoria",command=selec_cat,fg="white",bg="red4",font="Arial 12",width=20).place(x=570,y=60)
    pantalla_cat.mainloop()
