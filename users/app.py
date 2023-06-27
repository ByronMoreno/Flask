from flask import Flask, jsonify, render_template,request,redirect
#Para conectar con la base de datos
from psycopg2 import connect, extras

#Instanciar la clase de flask
app = Flask(__name__)

#Contantes la base de datos
host = 'localhost'
port = 5432
dbname = 'byron'
username = 'postgres'
password = 123

#Funcion para conectar a la base de datos
def get_database():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

#Consultar todos los usuarios
@app.route('/en')
def home():
    return render_template('create.html')

@app.route('/api/users/create')
def create():
    return render_template('create.html')

#Consultar todos los usuarios
@app.get('/app/users')
def get_users():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    #Paso 5 convertir un objeto diccionario en un objeto json
    print(user)    
    return jsonify(user)

#Mostrando datos en html
#Consultar todos los usuarios
@app.route('/api/users', methods=['GET'])
def get_users_html():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    return render_template('select.html',users=user)

#Delete
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete_users(id):
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("DELETE FROM users where id = %s RETURNING *", (id,))
    #Paso 4 sacar datos a pantalla
    user_deleting = cursor.fetchone()

    if request.method == 'POST':
        if user_deleting:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/users')
        #abort(404)
    return render_template('delete.html', user=user_deleting)

#Update
@app.route('/<int:id>/edit', methods=['GET','POST'])
def update_user(id):

    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users where id = %s", (id,)) 
    # Paso 4 sacar datos a pantalla
    user_select = cursor.fetchone()
    cursor.close()
    conn.close()

    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        nombre = request.form['name1']
        edad = request.form['age']
        descripcion = request.form['description']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute("UPDATE users SET name=%s, age=%s, description=%s WHERE id=%s RETURNING *",
                    (nombre, edad, descripcion, id))
        #Paso 4 sacar datos a pantalla
        user_updating = cursor.fetchone()    
        if user_updating:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/api/users')
        #abort(404)
    return render_template('update.html', user=user_select)

#Create
@app.route("/", methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create.html')
    #Paso 1 obtenr los datos del html
    if request.method == 'POST':
        nombre = request.form['name1']
        edad = request.form['age']
        descripcion = request.form['description']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute('INSERT INTO users(name,age,description) VALUES (%s,%s,%s) RETURNING *',
                (nombre, edad, descripcion))
        #Paso 4 sacar datos a pantalla
        user_creating = cursor.fetchone()    
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
        #abort(404)
    

#Para colocar en modo debug, modo desarrallador
if __name__ == '__main__':
    app.run(debug=True)