#Andrea Isabel Acevez Alvarez
import pymysql

def recupera_categoria():
    conn = pymysql.connect(host='localhost', user='root', password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('SELECT ID_CATEGORIA, CATEGORIA from categoria')
    categorias = cursor.fetchall()
    conn.close()
    return categorias

def recupera_preguntas(cat):
    conn = pymysql.connect(host='localhost', user='root', password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    consulta='select b.ID_PREGUNTA,b.PREGUNTA,b.OPCION_1,b.OPCION_2,b.OPCION_3,b.OPCION_4,b.CORRECTO,b.ID_CATEGORIA'
    consulta=consulta+' from categoria a, PREGUNTA b '
    consulta=consulta+' where CATEGORIA ="'+cat+'" and b.ID_CATEGORIA = a.ID_CATEGORIA '
    cursor.execute(consulta)
    preguntas = cursor.fetchall()
    conn.close()
    return preguntas

def tabla_categorias():
    conn = pymysql.connect(host='localhost', user='root', password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('select ID_CATEGORIA ,CATEGORIA from categoria')
    cats= cursor.fetchall()
    conn.close()
    return cats

def inserta_categoria(descrip):
    conn = pymysql.connect(host='localhost', user='root',password='',database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('insert into categoria (CATEGORIA) values(%s)', (descrip))
    conn.commit()
    conn.close()

def tabla_preguntas(id):
    conn = pymysql.connect(host='localhost', user='root',password='',database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('select id_pregunta,pregunta,opcion_1,opcion_2,opcion_3,opcion_4,correcto,id_categoria from pregunta where id_categoria=%s',(id,))
    preguntas = cursor.fetchall()
    conn.close()
    return preguntas
    

def selec_pregunta(ab):
    conn = pymysql.connect(host='localhost', user='root',password='',database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('update pregunta set pregunta=%s,opcion_1=%s,opcion_2=%s,opcion_3=%s,opcion_4=%s,correcto=%s where id_pregunta')
    dato=cursor.fetchone()
    return dato

def borra_categoria(ab):
    conn = pymysql.connect(host='localhost', user='root',password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('delete from categoria where id_categoria=%s', (ab))
    conn.commit()
    conn.close()

def selec_categoria(ab):
    conn = pymysql.connect(host='localhost', user='root',password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('select ID_CATEGORIA,CATEGORIA from categoria where ID_CATEGORIA=%s', (ab))
    dato=cursor.fetchone()
    return dato

def modif_categoria(ab,descripcion):
    conn = pymysql.connect(host='localhost', user='root',password='',database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('update categoria set CATEGORIA=%s where id_categoria=%s', (descripcion,ab))
    conn.commit()
    conn.close()

def selec_preguntas(ab):
    conn = pymysql.connect(host='localhost',user='root',password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('select id_pregunta,pregunta,opcion_1,opcion_2,opcion_3,opcion_4,correcto,id_categoria from pregunta where id_pregunta=%s',(ab,))
    dato=cursor.fetchone()
    conn.close()
    return dato

def modif_pregunta(ab,datos):
    conn = pymysql.connect(host='localhost', user='root',password='', database='proyecto_juego_ignorancia')
    cursor = conn.cursor()
    cursor.execute('update pregunta set pregunta=%s,opcion_1=%s,opcion_2=%s,opcion_3=%s,opcion_4=%s,correcto=%s where id_pregunta=%s',
    (datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],ab))
    conn.commit()
    conn.close()

def borra_pregunta(ab):
        conn = pymysql.connect(host='localhost', user='root',password='', database='proyecto_juego_ignorancia')
        cursor = conn.cursor()
        cursor.execute('delete from pregunta where id_pregunta=%s', (ab))
        conn.commit()
        conn.close()

def inserta_pregunta(datos,id):
        conn = pymysql.connect(host='localhost',user='root',password='', database='proyecto_juego_ignorancia')
        cursor = conn.cursor()
        cursor.execute('insert into pregunta (pregunta,opcion_1,opcion_2,opcion_3,opcion_4,correcto,id_categoria) values(%s,%s,%s,%s,%s,%s,%s)',(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],id))
        conn.commit()
        conn.close()

