from flask import Flask,redirect,render_template,request
import mysql.connector
#to make flask know where to look for resources like templates and static files.
app = Flask(__name__)
conn = mysql.connector.connect(host='localhost',user='NirajBasnet',password='Niraj_009',database='nirajbasnet')
cursor = conn.cursor()
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/add_user',methods=['POST'])
def add_user():
    regis_name = request.form.get('name')
    regis_email = request.form.get('email')
    regis_password = request.form.get('password')
    checked = request.form.get('checkbox')
    rp_password = request.form.get('rp_password')
    query = """INSERT INTO `users` (`name`, `email`, `password`) VALUES('{}', '{}', '{}')""".format(regis_name,regis_email,regis_password)
    cursor.execute(query)
    conn.commit()
    print('User added successfully')

    return redirect('/todo')
    
@app.route('/form_validation',methods=['POST'])
def form_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    query = """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password)
    cursor.execute(query)
    users = cursor.fetchall()
    print(users)
    if(len(users)>0):
        return redirect('/todo')
    else:
        return redirect('/')
    
@app.route('/todo')
def todo():
    query = """SELECT * FROM `todos`"""
    cursor.execute(query)
    todos = cursor.fetchall()
    print(todos)
    return render_template('todo.html',todos=todos)

@app.route('/add_item',methods=['POST'])
def add_item():
    task_name = request.form.get('task_name')
    query = """INSERT INTO `todos` (`todo_text`) VALUES('{}')""".format(task_name)
    cursor.execute(query)
    conn.commit()
    print('item added successfully')
    return redirect('/todo')

@app.route('/update_status/<id>')
def update_status(id):
    query = """UPDATE `todos` SET current_status='{}' WHERE item_no = '{}'""".format("Completed",id)
    cursor.execute(query)
    conn.commit()
    return redirect('/todo')

@app.route('/delete_item/<id>')
def delete_item(id):
    query = """DELETE FROM `todos` WHERE item_no = '{}'""".format(id)
    cursor.execute(query)
    conn.commit()
    return redirect('/todo')
if __name__ == '__main__':
    app.run(debug=True)

