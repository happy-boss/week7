from flask import Flask,request,render_template,redirect,session,url_for,jsonify
import mysql.connector
import json


app=Flask(
    __name__,static_folder="public",static_url_path="/")   

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase",
    buffered = True
)

mycursor = mydb.cursor()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=["POST"])
def signup():
    username=request.form['username']
    mycursor.execute("SELECT  username FROM user where username='%s'"% (username))
    user=mycursor.fetchone()

    if user!=None:
        return redirect("/error?message=帳號重複註冊")
    else:
        sql = "INSERT INTO user (name, username,password) VALUES (%s, %s,%s)"
        val = (request.form['name'],request.form['username'], request.form['password'])
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect("/")  

@app.route("/signin",methods=["POST"])
def signin():
    username=request.form['username']
    password=request.form['password']
    mycursor.execute("SELECT username,password FROM user where username='%s'and password='%s'"% (username,password))
    checkuser = mycursor.fetchone()
    if checkuser!=None:
        session['user'] = checkuser[1]
        return redirect("/member")              
    else:
        return redirect("/error?message=帳號或密碼錯誤")

@app.route("/signout")
def signout():
    session["user"]=None
    return redirect("/")

@app.route("/api/users")
def apiusers():
    username=request.args.get('username')
    print(username)
    mycursor.execute("SELECT id,username,name FROM user where username='%s'"% (username))
    myresult=mycursor.fetchone()
    print(myresult)
    if myresult!=None:
        
        return jsonify({"data":{
            'id' : myresult[0],
            'username' : myresult[1],
            'name' : myresult[2]
                }
            })
    else:
        return  jsonify({"data":myresult})
    #首先在資料後面可以改成None，結果也是一樣的，不能直接寫null顯示出來的訊息會出現名稱未定義
    # 再來再判斷的時候，邏輯是如果帳號存在的畫執行這件事，第一次寫的邏輯錯了寫在第一行
    # 在來犯的錯是沒想到說myresult=mycursor.fetchone()這句成立之後再去寫if
    # if myresult!=None:代表這個東西存在就做這件事                         

@app.route("/member")
def member():
    if session["user"]!=None:
        print(session['user'])
        mycursor.execute(f"SELECT name FROM user where username='{session['user']}'")
        name = mycursor.fetchone()
        name=name[0]
        return render_template("member.html",name=name)
    else:    
        return redirect("/")
@app.route("/error")
def error():
    message= request.args.get('message')
    print(message)
    return render_template("error.html",message=message)

app.debug=True    
app.run(port=3000,debug=True)    
