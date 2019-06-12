import os
port=os.environ["PORT"]
import requests
import urllib.parse

from flask import Flask, render_template, request, abort
app = Flask(__name__)	

def eleging():
    import requests
    URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
    parametros={'i':'list'}
    cont=0
    lista_ingredientes=requests.get(URL_BASE+"list.php",params=parametros)
    if lista_ingredientes.status_code==200:
        listaing=[]
        listap=[]
        doc=lista_ingredientes.json()
        ingredientes=doc["drinks"]
        for ingrediente in ingredientes:
            cont=cont+1
            listap.append(ingrediente["strIngredient1"])
            if cont%6==0:
                listaing.append(listap)
                listap=[]
    return listaing

def cocfiltrado(ing):
    URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
    parametros={ 'i' : ing } 
    lista_ingrediente=requests.get(URL_BASE+"filter.php",params=parametros)
    if lista_ingrediente.status_code==200:
        listacoc=[]
        doc=lista_ingrediente.json()
        cocteles=doc["drinks"]
        for coc in cocteles:
            listacoc.append(coc)
    return listacoc

def cocteles():
    URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
    parametros={ 'c' : 'list' } 
    lista_ingrediente=requests.get(URL_BASE+"list.php",params=parametros)
    if lista_ingrediente.status_code==200:
        listacoc=[]
        doc=lista_ingrediente.json()
        cocteles=doc["drinks"]
        for coc in cocteles:
            listacoc.append(coc)
    return listacoc

def aleatorio():
    listarandom=[]
    for i in range(4):
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        lista_ingrediente=requests.get(URL_BASE+"random.php")
        if lista_ingrediente.status_code==200:
            doc=lista_ingrediente.json()
            cocteles=doc["drinks"]
            listarandom.append(cocteles)
    return listarandom

def infococ(id):
        listainfo=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={ 'i' : id } 
        lista_ingrediente=requests.get(URL_BASE+"lookup.php",params=parametros)
        if lista_ingrediente.status_code==200:
            doc=lista_ingrediente.json()
            coctel=doc["drinks"]
            for coc in coctel:
                listainfo.append(coc)
        return listainfo

def ingcoc(listacoc):
        listaing=[]
        listap=[]
        
        for i in range(1,16):
                if listacoc[0]['strIngredient'+str(i)]!='' and listacoc[0]['strIngredient'+str(i)]!=None:
                        listap.append(listacoc[0]['strIngredient'+str(i)])
                        listap.append(listacoc[0]['strMeasure'+str(i)])
                        listaing.append(listap)
                        listap=[]
        
        print(listaing)
        return listaing

def recomendado(ingrediente, coctel):
        listarecomendado=[]
        listacocteles=cocfiltrado(ingrediente)
        if len(listacocteles)<4:
                for i in listacocteles:
                        listarecomendado.append(i)
        else:
                for i in range(4):
                        listarecomendado.append(listacocteles[i])
        return listarecomendado

def resuling(ingint, listaing):
        listaresultados=[]
        for i in listaing:
                for x in i:
                        if ingint.lower() in x.lower():
                                listaresultados.append(x)
        return listaresultados

def bebidasalcoholicas():
        listaalcoholicas=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={'a':'Alcoholic'}
        lista_alcoholicas=requests.get(URL_BASE+"filter.php",params=parametros)
        if lista_alcoholicas.status_code==200:
                doc=lista_alcoholicas.json()
                coctel=doc["drinks"]
                for coc in coctel:
                        listaalcoholicas.append(coc)
        return listaalcoholicas

def bebidasnoalcoholicas():
        listanoalcoholicas=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={'a':'Non_Alcoholic'}
        lista_noalcoholicas=requests.get(URL_BASE+"filter.php",params=parametros)
        if lista_noalcoholicas.status_code==200:
                doc=lista_noalcoholicas.json()
                coctel=doc["drinks"]
                for coc in coctel:
                        listanoalcoholicas.append(coc)
        return listanoalcoholicas

def ordinary():
        listaordinary=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={'c':'Ordinary_Drink'}
        lista=requests.get(URL_BASE+"filter.php",params=parametros)
        if lista.status_code==200:
                doc=lista.json()
                coctel=doc["drinks"]
                for coc in coctel:
                        listaordinary.append(coc)
        return listaordinary

def tipococtel():
        listacoctel=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={'c':'Cocktail'}
        lista=requests.get(URL_BASE+"filter.php",params=parametros)
        if lista.status_code==200:
                doc=lista.json()
                coctel=doc["drinks"]
                for coc in coctel:
                        listacoctel.append(coc)
        return listacoctel

def listacerveza():
        listacerveza=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        parametros={'c':'beer'}
        lista=requests.get(URL_BASE+"filter.php",params=parametros)
        if lista.status_code==200:
                doc=lista.json()
                cervezas=doc["drinks"]
                for i in cervezas:
                        listacerveza.append(i)
        return listacerveza

def filtrarcerveza(palabra):
        listacyt=[]
        lista=listacerveza()
        for i in lista:
                if palabra.lower() in i['strDrink'].lower():
                        listacyt.append(i)
        return lista

def crearlistacoc():
        listacoc=[]
        listaordinary=ordinary()
        listacoctel=tipococtel()
        listasinalcohol=bebidasnoalcoholicas()
        listacer=listacerveza()
        for i in listaordinary:
                listacoc.append(i)
        for i in listacoctel:
                listacoc.append(i)
        for i in listasinalcohol:
                listacoc.append(i)
        for i in listacer:
                listacoc.append(i)
        return listacoc

def filtrarcoctel(palabra):
        listacoc=crearlistacoc()
        listafiltrado=[]
        for i in listacoc:
                if palabra.lower() in i['strDrink'].lower():
                        listafiltrado.append(i)
        return listafiltrado

def cafeyte():
        listacafeyte=[]
        URL_BASE="https://www.thecocktaildb.com/api/json/v1/1/"
        lista=requests.get(URL_BASE+"filter.php?c=Coffee / Tea")
        if lista.status_code==200:
                doc=lista.json()
                coctel=doc["drinks"]
                for coc in coctel:
                        listacafeyte.append(coc)
        return listacafeyte

def filtrartyc(palabra):
        listacyt=[]
        lista=cafeyte()
        for i in lista:
                if palabra.lower() in i['strDrink'].lower():
                        listacyt.append(i)
        return lista




@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/ingredientes' ,methods=["GET", "POST"])
def ingredientes():
        if request.method=="GET":
                listaing=eleging()
                listarandom=aleatorio()
                return render_template("ingredientes.html", listaing=listaing, listarandom=listarandom)
        else:
                ingint=request.form.get("ingrediente")
                listaing=eleging()
                resultados=resuling(ingint, listaing)
                return render_template("ingredientesb.html", resultados=resultados, listaing=listaing)
    
@app.route('/ingredientes/<string:nombre>')
def ingrediente(nombre):
        listaing=cocfiltrado(nombre)
        return render_template("filtroing.html", nombre=nombre, listaing=listaing)


@app.route('/cocteles' ,methods=["GET","POST"])
def coctelel():
        if request.method == 'GET':
                coc=cocteles()
                cocrandom=aleatorio()
                listacafeyte=cafeyte()
                listasinalcohol=bebidasnoalcoholicas()
                return render_template("cocteles.html", coc=coc, cocrandom=cocrandom, listacafeyte=listacafeyte, listasinalcohol=listasinalcohol)




@app.route('/coctel/<id>')
def coctel(id):
        listacoc=infococ(id)
        listaing=ingcoc(listacoc)
        listacocing=recomendado(listacoc[0]['strIngredient1'], listacoc[0]['strDrink'])
        return render_template("coctel.html", listacoc=listacoc, listaing=listaing, listacocing=listacocing)

@app.route('/busqueda', methods=["POST"])
def coctelresultado():
        palabra=request.form.get("coctel")
        listabusqueda=filtrarcoctel(palabra)
        return render_template("coctelresultado.html", palabra=palabra, listabusqueda=listabusqueda)

@app.route('/sin_alcohol', methods=["GET", "POST"])
def sin_alcohol():
        if request.method=="GET":
                listabusqueda=bebidasnoalcoholicas()
                return render_template("sin_alcohol.html", listabusqueda=listabusqueda)
        else:
                palabra=request.form.get("nombre")
                resultadossina=filtrarcoctel(palabra)
                return render_template("sin_alcoholb.html", resultadossina=resultadossina) 

@app.route('/cafe_te', methods=["GET", "POST"])
def cafe_te():
        if request.method=="GET":
                listabusqueda=cafeyte()
                return render_template("cafe_te.html", listabusqueda=listabusqueda)
        else:
                palabra=request.form.get("nombre")
                resultadoscyt=filtrartyc(palabra)
                return render_template("cafe_teb.html", resultadoscyt=resultadoscyt) 

@app.route('/cerveza', methods=["GET", "POST"])
def cerveza():
        if request.method=="GET":
                listabusqueda=listacerveza()
                return render_template("cervezas.html", listabusqueda=listabusqueda)
        else:
                palabra=request.form.get("nombre")
                resultadoscyt=filtrarcerveza(palabra)
                return render_template("cervezasb.html", resultadoscyt=resultadoscyt) 

@app.route('/contacto')
def contacto():
    return render_template("contact.html")

app.run('0.0.0.0', int(port),debug=True)