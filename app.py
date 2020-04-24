from flask import Flask ,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from flask_wtf import Form
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps


app=Flask(__name__)

##configmysql

app.config['MYSQL_HOST']="dbprecios.csi2qxwigzjl.us-east-1.rds.amazonaws.com"
app.config['MYSQL_USER']="admin"
app.config['MYSQL_PASSWORD']="32dexter"
app.config['MYSQL_DB']="precios"
app.config['MYSQL_CURSORCLASS']='DictCursor'


mysql=MySQL(app)



class LoginForm(Form):
    username=StringField("email",[validators.length(min=6,max=50)],description="Correo@dominio.com")    
    password=PasswordField("password",[validators.DataRequired()],description="Password")

##verifico si esta logueado el usuario
def logueado(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('home'))
    return wrap

@app.route('/',methods=["GET","POST"])
@app.route('/home',methods=["GET","POST"])
def home():
    if request.method=="POST":
        username=request.form['MERGE1']
        password_candidate=request.form['MERGE0']
        ####cursor
        cur=mysql.connection.cursor()
        ###obtengo mail
        result=cur.execute("SELECT * FROM users WHERE mail=%s",[username])
        if result>0:
            ###storedhash
            data=cur.fetchone()
            password=data["pass"]
            ###comparo passwords
            if password==password_candidate:
                ###
                session['logged_in']=True
                session['username']=data["nombre"]
                return redirect(url_for('preguntas'))                
            else:
                app.logger.info("PASSWORD incorrecto")
            cur.close()
        else:
            app.logger.info("nO EXISTE USUARIO")
    return render_template("index.html")

@app.route('/preguntas')
@logueado
def preguntas():
    ####cursor
    cur=mysql.connection.cursor()
    ###obtengo mail
    result=cur.execute("SELECT  PreciosMeli.Index ,Title,Price,Link from PreciosMeli WHERE Tipo='Impresoras' ORDER BY PreciosMeli.Index Desc LIMIT 0,100")
    productos=cur.fetchall()    
    prom=cur.execute("SELECT  ROUND(AVG(Price),2) as avg from PreciosMeli WHERE Tipo='Impresoras'")  
    promedio=cur.fetchone()  
    total=cur.execute("SELECT  COUNT(*) as cantidad from PreciosMeli WHERE Tipo='Impresoras'")
    publicaciones=cur.fetchone()        
    if result>0:
        return render_template('preguntas.html',
                                    productos=productos,
                                    promedio=promedio,
                                    publicaciones=publicaciones)
    else:
        return render_template('preguntas.html')
    cur.close()

@app.route('/ventas')
def ventas():
    ####cursor
    cur=mysql.connection.cursor()
    ###obtengo mail
    result=cur.execute("SELECT Tipo,count(*) as cantidad from PreciosMeli GROUP BY Tipo;")
    productos=cur.fetchall()    
    prom=cur.execute("SELECT  ROUND(AVG(Price),2) as avg from PreciosMeli WHERE Tipo='Impresoras'")  
    promedio=cur.fetchone()  
    total=cur.execute("SELECT  COUNT(*) as cantidad from PreciosMeli WHERE Tipo='Impresoras'")
    publicaciones=cur.fetchone() 
    porcent=cur.execute("SELECT Tipo, ROUND(count(*) * 100 / (select count(*) FROM PreciosMeli),2)AS 'Porcentaje' FROM PreciosMeli group by Tipo")
    porcentaje=cur.fetchall()        
    if result>0:
        return render_template('ventas.html',
                                    productos=productos,
                                    promedio=promedio,
                                    publicaciones=publicaciones,
                                    porcentaje=porcentaje,
                                    set=porcentaje)
    else:
        return render_template('ventas.html')
    cur.close()

@app.route('/envios')
def envios():
    ####cursor
    cur=mysql.connection.cursor()
    ###obtengo mail
    result=cur.execute("SELECT  PreciosMeli.Index ,Title,Price,Link from PreciosMeli WHERE Tipo='Plotters' ORDER BY PreciosMeli.Index Desc LIMIT 0,100")
    productos=cur.fetchall()    
    prom=cur.execute("SELECT  ROUND(AVG(Price),2) as avg from PreciosMeli WHERE Tipo='Plotters'")  
    promedio=cur.fetchone()  
    total=cur.execute("SELECT  COUNT(*) as cantidad from PreciosMeli WHERE Tipo='Plotters'")
    publicaciones=cur.fetchone()        
    if result>0:
        return render_template('envios.html',
                                    productos=productos,
                                    promedio=promedio,
                                    publicaciones=publicaciones)
    else:
        return render_template('envios.html')
    cur.close()

@app.route('/reclamos')
def reclamos():
    ####cursor
    cur=mysql.connection.cursor()
    ###obtengo mail
    result=cur.execute("SELECT  PreciosMeli.Index ,Title,Price,Link from PreciosMeli WHERE Tipo='Proyectores' ORDER BY PreciosMeli.Index Desc LIMIT 0,100")
    productos=cur.fetchall()    
    prom=cur.execute("SELECT  ROUND(AVG(Price),2) as avg from PreciosMeli WHERE Tipo='Proyectores'")  
    promedio=cur.fetchone()  
    total=cur.execute("SELECT  COUNT(*) as cantidad from PreciosMeli WHERE Tipo='Proyectores'")
    publicaciones=cur.fetchone()        
    if result>0:
        return render_template('reclamos.html',
                                    productos=productos,
                                    promedio=promedio,
                                    publicaciones=publicaciones)
    else:
        return render_template('reclamos.html')
    cur.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))




labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/pie')
def pie():
    cur=mysql.connection.cursor()
    porcent=cur.execute("SELECT Tipo, ROUND(count(*) * 100 / (select count(*) FROM PreciosMeli),2)AS 'Porcentaje' FROM PreciosMeli group by Tipo")
    porcentaje=cur.fetchall()
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=porcentaje)













 



if __name__=='__main__':
    app.secret_key="secreto"
    app.config['TESTING'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True  
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
    
    
    
    
