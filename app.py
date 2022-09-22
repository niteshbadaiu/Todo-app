import re
from flask import Flask,render_template,redirect,url_for,request
import pymysql
app=Flask(__name__)

con=None
cur=None



def connectToDb():
    global con,cur
    con=pymysql.connect(host="localhost",user="root",password="",database="portal_todo")
    cur=con.cursor()
    createQuery="create table if not exists todo(sno int primary key auto_increment,title varchar(100),des varchar(500))"
    cur.execute(createQuery)
    con.commit()

def disconnectDb():
    cur.close()
    con.close()

def insertToTodoTable(title,des):
    try:
        connectToDb()
        insertQuery="insert into todo (title,des) values(%s,%s)"
        cur.execute(insertQuery,(title,des))
        con.commit()
        disconnectDb()
        return True
    except:
        disconnectDb()
        return False

def getAllTodo():
    connectToDb()
    selectQuery="select * from todo"
    cur.execute(selectQuery)
    con.commit()
    data=cur.fetchall()
    disconnectDb()
    return data

def getOneTodo(sno):
    connectToDb()
    selectQuery="select * from todo where sno=%s"
    cur.execute(selectQuery,(sno,))
    con.commit()
    data=cur.fetchone()
    disconnectDb()
    return data

def updateTodoToTable(sno,title,des):
    try:
        connectToDb()
        updateQuery="update todo set title=%s,des=%s where sno=%s"
        cur.execute(updateQuery,(title,des,sno))
        con.commit()
        disconnectDb()
        return True
    except Exception as e:
        print(e)
        disconnectDb()
        return False

def deleteTodoFromTable(sno):
    try:
        connectToDb()
        deleteQuery="delete from todo where sno=%s"
        cur.execute(deleteQuery,(sno,))
        con.commit()
        disconnectDb()
        return True
    except:
        disconnectDb()
        return False
    

@app.route("/")
@app.route("/index")
def index():
    data=getAllTodo()
    return render_template("index.html",data=data)



@app.route("/add/",methods=["GET","POST"])
def addTodo():
    if request.method=="POST":
        data=request.form
        if insertToTodoTable(data["txtTitle"],data["txtDes"]):
            message="Inserted successfully"
        else:
            message="Something went wrong"
        return render_template("insert.html",message=message)
    return render_template("insert.html")





@app.route("/update/",methods=["GET","POST"])
def updateTodo():
    sno=request.args.get("id",type=int,default=1)
    data=getOneTodo(sno)
    if request.method=="POST":
        fdata=request.form
        if updateTodoToTable(sno,fdata["txtTitle"],fdata["txtDes"]):
            message="Updated successfully"
        else:
            message="Something went wrong"
        return render_template("insert.html",message=message)
    return render_template("update.html",data=data)

@app.route("/delete/")
def deleteTodo():
    sno=request.args.get("id",type=int,default=1)
    deleteTodoFromTable(sno)
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)