from flask import *
from flask import request
import requests
import bd
import os
import psycopg2
import datetime
__key=''
app=Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=1)
app.secret_key=os.urandom(30)

@app.route("/",methods=['GET','POST'])
def started(messages={'vhod':''}):
    if request.method=='GET':
        if 'username' in session:
            session.pop('username')
        if 'IP' not in session:
            session['IP']=request.remote_addr
        return render_template('enty.html',messages=messages)
    if request.method=='POST':
        if request.form.get('entry'):
            username=request.form['log']
            password=request.form['passw']
            if bd.__login(username,password):
                return redirect(url_for('login',username=username))
            else:return render_template('enty.html',messages={'vhod':'Не правельный логин/пароль'})
        if request.form.get('regi'):
            return redirect(url_for('register'))


#########
@app.route('/session',methods=['GET','POST'])
def ses():
    if request.method=='GET':
        return render_template('session.html',mess={'main':str(session)+' ■ '+str(request.remote_addr)})
#########


@app.route('/login/<username>',methods=['GET'])
def login(username=''):
    if request.method=='GET':
        if username not in session:
            session['username']=username
        return redirect(url_for('user',username=username))

    
@app.route('/logout/<username>',methods=['GET'])
def logout(username=''):
    if request.method=='GET':
        session.pop('username')
        return redirect(url_for('started'))


@app.route('/registration', methods=['GET','POST'])
def register(error={'er':''}):
    if request.method=='GET':
        if request.remote_addr in session['IP']:
            return  render_template('regestration.html',error=error)
        else:return redirect(url_for('started'))
    if request.method=='POST':
        username=request.form['nm']
        if bd.new_user(request.form['fnam'],request.form['lnam'],username,request.form['ps']):
            return redirect(url_for('login',username=username))
        else: return render_template('regestration.html',error={'er':'Пользователь с таким никнеймом уже существует'})


@app.route('/<username>',methods=['GET','POST'])
def user(username):
    if request.method=='GET':
        try:
            if username in session['username'] and request.remote_addr in session['IP']:
                return render_template('user.html',url={'url':username})
            else: return redirect(url_for('started'))
        except:return redirect(url_for('logout'))
    if request.method=='POST':
        if request.form.get('subm1'):
            return redirect(url_for('logout',username=username))
        if request.form.get('subm2'):
            return render_template('user.html',url={'url':username})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)