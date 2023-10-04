from flask import Flask,render_template,url_for,redirect,request
from flask_mysqldb import MySQL
app=Flask(__name__)

#MYSQL CONNECTION
app.config["MYSQL_HOST"]="mysql"
app.config["MYSQL_USER"]="flask"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_PORT"]= 5010
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#Loading home page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM new_table1"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#new user
@app.route("/addusers",methods=['GET','POST'])
def addusers():
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        age= request.form['age']
        city= request.form['city']
        con=mysql.connection.cursor()
        sql="insert into new_table1(ID,NAME,AGE,CITY) value (%s,%s,%s,%s)"
        con.execute(sql,[id,name,age,city])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))

    return render_template("addusers.html")

#update user
@app.route("/edituser/<string:id>",methods=['GET','POST'])

def edituser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name= request.form['name']
        age= request.form['age']
        city= request.form['city']
        sql="update new_table1 set NAME=%s,AGE=%s,CITY=%s where ID=%s"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
    sql="select * from new_table1 where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("edituser.html",datas=res)

#Delete user
@app.route("/deleteuser/<string:id>",methods=['GET','POST'])
def deleteuser(id):
    con=mysql.connection.cursor()
    sql="delete from new_table1 where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))



if(__name__=='__main__'):
     app.run(debug=True,host='0.0.0.0')
