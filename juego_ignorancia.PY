import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion import *
from ed_categoria import *

pantalla = Tk()
pantalla.resizable(1,1)
pantalla.geometry("1200x1000")
pantalla.config(background="orange")
pantalla.title("proyecto juego ignorancia")

# 1. Creamos un Canvas que ocupe TODA la pantalla (1200x1000)
canvas_pista = Canvas(pantalla, width=1500, height=1300, highlightthickness=0)
canvas_pista.place(x=0, y=0)

# 2. Dibujamos la imagen de fondo general en la coordenada (0,0)
fondo_img = PhotoImage(file=r"./fotos_proyecto/fondodeprueba.png")
canvas_pista.create_image(0, 0, anchor=NW, image=fondo_img)

# 3. Dibujamos tu tabla_juego.png transparente encima, en su posición original (x=7, y=160)
fon_img = PhotoImage(file=r"./fotos_proyecto/tablajuego.png")
canvas_pista.create_image(16, 160, anchor=NW, image=fon_img)



seleccion=()

str_preg = StringVar()
str_res1 = StringVar()
str_res2 = StringVar()
str_res3 = StringVar()
str_res4 = StringVar()

str_sig = StringVar()
str_sig.set("Pregunta")

correcto = 0

x1 = 70
x2 = 70
x3 = 70
x4 = 70

turno = 1

puntos1 = 0
puntos2 = 0
puntos3 = 0

str_puntos1 = StringVar()
str_puntos2 = StringVar()
str_puntos3 = StringVar()

str_puntos1.set("Jugador 1: 0 puntos")
str_puntos2.set("Jugador 2: 0 puntos")
str_puntos3.set("Jugador 3: 0 puntos")

meta = 1240

finturno1 = False
finturno2 = False
finturno3 = False
fin_ign = False



juego_terminado = False
ventana_win = None
img_ganador = None
lbl_ganador = None
gif_frames = []
gif_actual = 0
orden_llegada = []
categoria_seleccionada = False

def marcar_llegada(j):
    if j not in orden_llegada:
        orden_llegada.append(j)

ventana_ign = None

def penalizar_jugador():
    global turno, puntos1, puntos2, puntos3

    if turno == 1:
        puntos1 = max(0, puntos1 - 2)

    elif turno == 2:
        puntos2 = max(0, puntos2 - 2)

    elif turno == 3:
        puntos3 = max(0, puntos3 - 2)

    actualizar_puntos()

def actualizar_puntos():

    str_puntos1.set(
        "Jugador 1: " + str(puntos1) + " puntos"
    )

    str_puntos2.set(
        "Jugador 2: " + str(puntos2) + " puntos"
    )

    str_puntos3.set(
        "Jugador 3: " + str(puntos3) + " puntos"
    )

def ventana_ignorancia_sola():

    global ventana_ign
    global gif_frames
    global gif_actual
    global lbl_ganador

    ventana_ign = Toplevel()
    ventana_ign.geometry("700x500")
    ventana_ign.config(bg="orange")
    ventana_ign.title("LA IGNORANCIA GANÓ")

    # 🔒 BLOQUEO DE VENTANA
    def bloquear_cierre():
        pass  # no deja cerrar con X

    ventana_ign.protocol("WM_DELETE_WINDOW", bloquear_cierre)
    ventana_ign.resizable(False, False)
    ventana_ign.grab_set()
    ventana_ign.focus_force()

    # TEXTO
    Label(
        ventana_ign,
        text="LA IGNORANCIA LLEGÓ A LA META\nNINGÚN JUGADOR LLEGÓ",
        font=("Helvetica", 20, "bold"),
        bg="orange",
        fg="blue"
    ).pack(pady=20)

    # LIMPIAR GIF
    gif_frames.clear()

    # CARGAR GIF
    i = 0
    while True:
        try:
            gif_frames.append(
                PhotoImage(
                    file=r"./fotos_proyecto/ignoranciawinpoint.gif",
                    format="gif -index " + str(i)
                )
            )
            i += 1
        except:
            break

    gif_actual = 0

    # LABEL DEL GIF
    lbl_ganador = Label(
        ventana_ign,
        image=gif_frames[0],
        bg="orange"
    )
    lbl_ganador.pack()

    # ANIMACIÓN
    animar_gif()

    # BOTÓN REINICIAR
    Button(
        ventana_ign,
        text="REINICIAR PARTIDA",
        font=("Helvetica", 16, "bold"),
        bg="blue",
        fg="white",
        command=reiniciar_partida
    ).pack(pady=20)
         
def ganador_ignorancia():

    global ventana_ign
    global puntos1, puntos2, puntos3
    global gif_frames
    global gif_actual
    global lbl_ganador

    if not finturno1:
        puntos1 = max(0, puntos1 - 10)

    if not finturno2:
        puntos2 = max(0, puntos2 - 10)

    if not finturno3:
        puntos3 = max(0, puntos3 - 10)

    actualizar_puntos()

    ventana_ign = Toplevel()
    ventana_ign.geometry("700x500")
    ventana_ign.config(bg="orange")
    ventana_ign.title("LA IGNORANCIA cruzo la meta")
    def bloquear_cierre():
     pass
    ventana_ign.protocol("WM_DELETE_WINDOW", bloquear_cierre)
    ventana_ign.resizable(False, False)

    texto = Label(
        ventana_ign,
        text="la ignorancia llego a la meta - 10 puntos",
        font=("Helvetica", 18, "bold"),
        bg="blue",
        fg="white"
    )

    texto.pack(pady=20)

    gif_frames.clear()

    i = 0
    while True:
        try:
            gif_frames.append(
                PhotoImage(
                    file=r"./fotos_proyecto/ignoraciagokuwinposicion.gif",
                    format="gif -index " + str(i)
                )
            )
            i += 1
        except:
            break

    gif_actual = 0

    lbl_gif = Label(
        ventana_ign,
        image=gif_frames[0],
        bg="blue"
    )

    lbl_gif.pack()

    lbl_ganador = lbl_gif

    animar_gif()
    

    btn = Button(
        ventana_ign,
        text="Continuar juego",
        font=("Helvetica", 16, "bold"),
        bg="blue",
        fg="white",
        command=reiniciar_partida
    )

    ventana_ign.transient(pantalla)
    ventana_ign.grab_set()

    btn.pack(pady=20)



def reiniciar_partida():

    global juego_terminado
    global x1, x2, x3, x4
    global puntos1, puntos2, puntos3
    global turno
    global finturno1, finturno2, finturno3, fin_ign
    global ventana_win, ventana_ign
    global categoria_seleccionada
    

    juego_terminado = False

    if ventana_win is not None:
        try:
            ventana_win.grab_release()
        except:
            pass
        ventana_win.destroy()
        ventana_win = None

    if ventana_ign is not None:
        try:
            ventana_ign.grab_release()
        except:
            pass
        ventana_ign.destroy()
        ventana_ign = None

    x1 = 45
    x2 = 45
    x3 = 45
    x4 = 45

    puntos1 = 0
    puntos2 = 0
    puntos3 = 0


    finturno1 = False
    finturno2 = False
    finturno3 = False
    fin_ign = False

    turno = 1


    actualizar_puntos()
    str_sig.set("jugador " + str(turno))

    # REPOSICIONAR PIEZAS
    canvas_pista.coords(j1, x1, 190)
    canvas_pista.coords(j2, x2, 325)
    canvas_pista.coords(j3, x3, 470)
    canvas_pista.coords(ign, x4, 600)
    categoria_seleccionada = False
    categorias.config(state="readonly")
    categorias.set("")

def continuar_juego():

    global ventana_ign
    global x1, x2, x3, x4
    global finturno1, finturno2, finturno3
    global fin_ign

    if ventana_ign is not None:
        ventana_ign.destroy()
        ventana_ign = None

    x1 = 45
    x2 = 45
    x3 = 45
    x4 = 45

    # REINICIAR METAS
    finturno1 = False
    finturno2 = False
    finturno3 = False
    fin_ign = False

    # MOVER PERSONAJES
    canvas_pista.coords(j1, x1, 190)
    canvas_pista.coords(j2, x2, 325)
    canvas_pista.coords(j3, x3, 470)
    canvas_pista.coords(ign, x4, 600)

def animar_gif():
    global gif_actual
    global gif_frames
    global lbl_ganador
    global ventana_win
    global ventana_ign

    if len(gif_frames) == 0:
        return

    # Cambiar frame
    lbl_ganador.config(image=gif_frames[gif_actual])

    gif_actual = (gif_actual + 1) % len(gif_frames)

    # Repetir animación dependiendo de la ventana activa
    if ventana_win is not None:
        ventana_win.after(100, animar_gif)

    elif ventana_ign is not None:
        ventana_ign.after(80, animar_gif)

def revisar_ganador():

    global juego_terminado
    global ventana_win
    global gif_frames
    global gif_actual
    global lbl_ganador

    if juego_terminado:
        return

    ganador = ""

    if puntos1 >= 50:
        ganador = "Jugador 1"

    elif puntos2 >= 50:
        ganador = "Jugador 2"

    elif puntos3 >= 50:
        ganador = "Jugador 3"

    if ganador == "":
        return

    juego_terminado = True

    ventana_win = Toplevel()
    ventana_win.geometry("600x450")
    ventana_win.config(bg="gold")
    ventana_win.title("GANADOR")

    def bloquear_cierre():
        pass

    ventana_win.protocol(
        "WM_DELETE_WINDOW",
        bloquear_cierre
    )

    ventana_win.grab_set()

    Label(
        ventana_win,
        text=f"{ganador} ganó",
        font=("Helvetica",18,"bold"),
        bg="gold"
    ).pack(pady=15)

    if ganador == "Jugador 1":

        img = PhotoImage(
            file=r"./fotos_proyecto/chayannewinpoint.png"
        )

        lbl_ganador = Label(
            ventana_win,
            image=img,
            bg="gold"
        )

        lbl_ganador.image = img
        lbl_ganador.pack()

    elif ganador == "Jugador 2":

        gif_frames.clear()

        i = 0

        while True:
            try:
                gif_frames.append(
                    PhotoImage(
                        file=r"./fotos_proyecto/vegetto1j1winposicion-ezgif.com-repair.gif",
                        format="gif -index " + str(i)
                    )
                )
                i += 1
            except:
                break

        gif_actual = 0

        lbl_ganador = Label(
            ventana_win,
            image=gif_frames[0],
            bg="gold"
        )

        lbl_ganador.pack()

        animar_gif()

    elif ganador == "Jugador 3":

        gif_frames.clear()

        i = 0

        while True:
            try:
                gif_frames.append(
                    PhotoImage(
                        file=r"./fotos_proyecto/fromtogepiwinpoint.gif",
                        format="gif -index " + str(i)
                    )
                )
                i += 1
            except:
                break

        gif_actual = 0

        lbl_ganador = Label(
            ventana_win,
            image=gif_frames[0],
            bg="gold"
        )

        lbl_ganador.pack()

        animar_gif()

    Button(
        ventana_win,
        text="Reiniciar partida",
        font=("Helvetica",16,"bold"),
        bg="green",
        fg="white",
        command=reiniciar_partida
    ).pack(pady=20)

def revisar_meta_completa():

    global puntos1
    global puntos2
    global puntos3
    global orden_llegada
    global x1, x2, x3, x4
    global finturno1, finturno2, finturno3
    global fin_ign

    if not (finturno1 and finturno2 and finturno3):
        return

    ventana_meta = Toplevel()
    ventana_meta.geometry("700x500")
    ventana_meta.config(bg="orange")
    ventana_meta.title("TODOS LLEGARON")

    def bloquear_cierre():
        pass

    ventana_meta.protocol("WM_DELETE_WINDOW", bloquear_cierre)
    ventana_meta.grab_set()

    Label(
        ventana_meta,
        text="LOS 3 JUGADORES\nLLEGARON A LA META",
        font=("Helvetica", 22, "bold"),
        bg="orange",
        fg="white"
    ).pack(pady=10)

    img_ganador_meta = PhotoImage(file=r"./fotos_proyecto/victoryplayers.png")

    lbl_img_meta = Label(
        ventana_meta,
        image=img_ganador_meta,
        bg="orange"
    )
    lbl_img_meta.pack()

    lbl_img_meta.image = img_ganador_meta

   
    def continuar_partida():

        global x1, x2, x3, x4
        global finturno1, finturno2, finturno3
        global fin_ign
        global puntos1, puntos2, puntos3

        puntos1 += 8
        puntos2 += 5
        puntos3 += 2

        actualizar_puntos()

        ventana_meta.destroy()

        x1 = 45
        x2 = 45
        x3 = 45
        x4 = 45

        finturno1 = False
        finturno2 = False
        finturno3 = False
        fin_ign = False

        canvas_pista.coords(j1, x1, 174)
        canvas_pista.coords(j2, x2, 315)
        canvas_pista.coords(j3, x3, 470)
        canvas_pista.coords(ign, x4, 600)

    Button(
        ventana_meta,
        text="CONTINUAR PARTIDA",
        command=continuar_partida,
        font=("Helvetica", 16, "bold"),
        bg="yellow"
    ).pack(pady=20)
    
def avanza_jug():

    global x1, x2, x3, juego_terminado
    global finturno1, finturno2, finturno3
    if turno == 1:

        if not finturno1:

            x1 += 130

            if x1 >= meta:
                x1 = meta
                finturno1 = True
                messagebox.showinfo("META", "Jugador 1 llegó a la meta")
            revisar_meta_completa()
            canvas_pista.coords(j1, x1, 173)

    elif turno == 2:

        if not finturno2:

            x2 += 130

            if x2 >= meta:
                x2 = meta
                finturno2 = True
                messagebox.showinfo("META", "Jugador 2 llegó a la meta")
                revisar_meta_completa()
            canvas_pista.coords(j2, x2, 316)
    elif turno == 3:

        if not finturno3:

            x3 += 130

            if x3 >= meta:
                x3 = meta
                finturno3 = True
                messagebox.showinfo("META", "Jugador 3 llegó a la meta")
                revisar_meta_completa()

            canvas_pista.coords(j3, x3, 470)

def siguiente_turno():
    global turno

    turno += 1
    if turno > 3:
        turno = 1
    if finturno1 and finturno2 and finturno3:
     return
    while (
        (turno == 1 and finturno1) or
        (turno == 2 and finturno2) or
        (turno == 3 and finturno3)
    ):
        turno += 1
        if turno > 3:
            turno = 1

    str_sig.set("jugador " + str(turno))

def opc1():

    global turno, x4
    global puntos1, puntos2, puntos3
    global fin_ign, juego_terminado

    if juego_terminado:
        return

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

    if correcto == 1:

        avanza_jug()

        if turno == 1 and not finturno1:
            puntos1 += 4

        elif turno == 2 and not finturno2:
            puntos2 += 4

        elif turno == 3 and not finturno3:
            puntos3 += 4

        actualizar_puntos()
        revisar_ganador()

    else:

        penalizar_jugador()

        if not fin_ign:

            x4 += 130

            if x4 >= meta:
                x4 = meta

            canvas_pista.coords(ign, x4, 600)
            pantalla.update()

            if x4 >= meta:

                fin_ign = True
                juego_terminado = True

                messagebox.showinfo(
                    "IGNORANCIA",
                    "La ignorancia llegó a la meta"
                )

                if not finturno1 and not finturno2 and not finturno3:
                    ventana_ignorancia_sola()
                else:
                    ganador_ignorancia()

    if not juego_terminado:
        siguiente_turno()

def opc2():


    global turno, x4
    global puntos1, puntos2, puntos3
    global fin_ign, juego_terminado

    if juego_terminado:
        return

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

    if correcto == 2:

        avanza_jug()

        if turno == 1 and not finturno1:
            puntos1 += 4

        elif turno == 2 and not finturno2:
            puntos2 += 4

        elif turno == 3 and not finturno3:
            puntos3 += 4

        actualizar_puntos()
        revisar_ganador()

    else:

        penalizar_jugador()

        if not fin_ign:

            x4 += 130

            if x4 >= meta:
                x4 = meta

            canvas_pista.coords(ign, x4, 600)
            pantalla.update()

            if x4 >= meta:

                fin_ign = True
                juego_terminado = True

                messagebox.showinfo(
                    "IGNORANCIA",
                    "La ignorancia llegó a la meta"
                )

                if not finturno1 and not finturno2 and not finturno3:
                    ventana_ignorancia_sola()
                else:
                    ganador_ignorancia()

    if not juego_terminado:
        siguiente_turno()

def opc3():

    global turno, x4
    global puntos1, puntos2, puntos3
    global fin_ign, juego_terminado

    if juego_terminado:
        return

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

    if correcto == 3:

        avanza_jug()

        if turno == 1 and not finturno1:
            puntos1 += 4

        elif turno == 2 and not finturno2:
            puntos2 += 4

        elif turno == 3 and not finturno3:
            puntos3 += 4

        actualizar_puntos()
        revisar_ganador()

    else:

        penalizar_jugador()

        if not fin_ign:

            x4 += 130

            if x4 >= meta:
                x4 = meta

            canvas_pista.coords(ign, x4, 600)
            pantalla.update()

            if x4 >= meta:

                fin_ign = True
                juego_terminado = True

                messagebox.showinfo(
                    "IGNORANCIA",
                    "La ignorancia llegó a la meta"
                )

                if not finturno1 and not finturno2 and not finturno3:
                    ventana_ignorancia_sola()
                else:
                    ganador_ignorancia()

    if not juego_terminado:
        siguiente_turno()
 
def opc4():

    global turno, x4
    global puntos1, puntos2, puntos3
    global fin_ign, juego_terminado

    if juego_terminado:
        return

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

    if correcto == 4:

        avanza_jug()

        if turno == 1 and not finturno1:
            puntos1 += 4

        elif turno == 2 and not finturno2:
            puntos2 += 4

        elif turno == 3 and not finturno3:
            puntos3 += 4

        actualizar_puntos()
        revisar_ganador()

    else:

        penalizar_jugador()

        if not fin_ign:

            x4 += 130

            if x4 >= meta:
                x4 = meta

            canvas_pista.coords(ign, x4, 600)
            pantalla.update()

            if x4 >= meta:

                fin_ign = True
                juego_terminado = True

                messagebox.showinfo(
                    "IGNORANCIA",
                    "La ignorancia llegó a la meta"
                )

                if not finturno1 and not finturno2 and not finturno3:
                    ventana_ignorancia_sola()
                else:
                    ganador_ignorancia()

    if not juego_terminado:
        siguiente_turno()

def preguntas(event):

    global seleccion
    global categoria_seleccionada

    if categoria_seleccionada:
        return

    categorias.config(state="disabled")

    cat = event.widget.get()
    cat = str(cat).replace("_", " ")

    seleccion = recupera_preguntas(cat)

    categoria_seleccionada = True 

    sel_preg()
def sel_preg():

    global str_preg
    global correcto

    tam = len(seleccion)

    if tam != 0:

        n = random.randint(0, tam - 1)

        str_preg.set(seleccion[n][1])
        str_res1.set(seleccion[n][2])
        str_res2.set(seleccion[n][3])
        str_res3.set(seleccion[n][4])
        str_res4.set(seleccion[n][5])

        correcto = seleccion[n][6]

        print(correcto)

        r1.config(state=NORMAL)
        r2.config(state=NORMAL)
        r3.config(state=NORMAL)
        r4.config(state=NORMAL)

    else:

        str_preg.set("categoria sin preguntas")

        str_res1.set("")
        str_res2.set("")
        str_res3.set("")
        str_res4.set("")

        r1.config(state=DISABLED)
        r2.config(state=DISABLED)
        r3.config(state=DISABLED)
        r4.config(state=DISABLED)

def pregunta_sig():

    global seleccion
    global categoria_seleccionada

    cat = categorias.get()
    cat = str(cat).replace("_", " ")

    seleccion = recupera_preguntas(cat)

    categoria_seleccionada = True 

    sel_preg()

def edita_categorias():
    manipula_categorias()
l_cats=recupera_categoria()
cats=[]
for cat in l_cats:
    cat2 = str(cat[1]).replace(" ", "_")
    cats.append(cat2)

eti = Label(pantalla,bg="blue",text="categorias", font='Helvetica 18 bold',fg="white")
eti.place(x=10, y=10)
categorias=ttk.Combobox(pantalla,font='Helvetica 18 bold')
categorias['values']=cats
categorias.config(state="readonly")
categorias.place(x=150, y=10)
categorias.bind("<<ComboboxSelected>>", preguntas)

sig = Button(pantalla, text="siguiente", command=pregunta_sig, font='helvetica 14 bold',bg="#0055A5",fg="white")
sig.place(x=670, y=10)


eti = Label(pantalla, bg="orange", textvariable=str_sig, font='helvetica 18 bold',fg="white")
eti.place(x=10, y=60)

#linea preguntas
str_preg.set("")
pre = Entry(pantalla, textvariable=str_preg, font='Helvetica 14 bold ',bg="lavender",width=100,state=DISABLED)
pre.place(x=150, y=60)


str_res1.set("")
r1 = Button(pantalla, textvariable=str_res1, command=opc1, font='Helvetica 12 bold ',bg="blue", fg="white", width=27)
r1.place(x=20, y=110)# 100 y 110

str_res2.set("")
r2 = Button(pantalla, textvariable=str_res2,command=opc2, font='helvetica 12 bold ',bg="blue",fg="white", width=27)
r2.place(x=340, y=110)

str_res3.set("")
r3 = Button(pantalla, textvariable=str_res3,command=opc3, font='helvetica 12 bold ',bg="blue",fg="white", width=27)
r3.place(x=660, y=110)

str_res4.set("")
r4 = Button(pantalla, textvariable=str_res4,command=opc4, font='helvetica 12 bold ',bg="blue",fg="white", width=27)
r4.place(x=980, y=110)

ju1 = PhotoImage(file=r"./fotos_proyecto/chayannej1.png")
j1 = canvas_pista.create_image(
    45,
    174,
    image=ju1,
    anchor=NW
)

ju2 = PhotoImage(file=r"./fotos_proyecto/vegettoj2.png")
j2 = canvas_pista.create_image(
    37,
    315,
    image=ju2,
    anchor=NW
)

ju3 = PhotoImage(file=r"./fotos_proyecto/togepi_j3_resized.png")
j3 = canvas_pista.create_image(
    45,
    470,
    image=ju3,
    anchor=NW
)

img_ign = PhotoImage(file=r"./fotos_proyecto/gokuignorancia.png")
ign = canvas_pista.create_image(
    30,
    600,
    image=img_ign,
    anchor=NW
)

str_ver_puntos = StringVar()
str_ver_puntos.set("Puntos")

def ver_puntaje(event):

    jugador = combo_puntos.get()

    if jugador == "Jugador_1":
        str_ver_puntos.set("Jugador 1: "+str(puntos1)+" puntos")

    elif jugador == "Jugador_2":
        str_ver_puntos.set("Jugador 2: "+str(puntos2)+" puntos")

    elif jugador == "Jugador_3":
        str_ver_puntos.set("Jugador 3: "+str(puntos3)+" puntos")


combo_puntos = ttk.Combobox(
    pantalla,
    font='Helvetica 13 bold',
    state="readonly",
    width=15
)

combo_puntos['values'] = (
    "Jugador_1",
    "Jugador_2",
    "Jugador_3"
)

combo_puntos.place(x=1000,y=10)

combo_puntos.bind("<<ComboboxSelected>>", ver_puntaje)


lbl_ver_puntos = Label(
    pantalla,
    textvariable=str_ver_puntos,
    font='Helvetica 13 bold',
    bg="white",
    width=17,
    anchor="w"
)

lbl_ver_puntos.place(x=800,y=10)

pantalla.mainloop()