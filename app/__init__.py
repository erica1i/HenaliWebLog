'''
Henali: Erica (hugo), Henry (e), Aahan (spikes)

SoftDev
2022-11-03
time spent:
'''

from flask import Flask, session, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'foo'

db_name = "test.db"


# @app.route("/create_user", methods = ["POST"])
# def register():
#     if request.method == "POST" :
#         name = request.form.get('username')
#         passwd = request.form.get('password')
#
#         if name is in #Retrive from database
#
#         else :
#             c.execute("INSERT INTO users VALUES ('"+name+"', '"+passwd+"');")

@app.route("/blog")#, methods = ["POST"])
#@app.route("/blog/<name>", methods = ["POST"])
def load_blog_page():
    db = sqlite3.connect(db_name)
    c =  db.cursor()
    id_number = 1
    #print(c.execute("SELECT * FROM blogs;").fetchall())
    #c.execute("INSERT INTO blogs VALUES ('blog1', 'Foo', 2);")
    #blogs_data = c.execute("SELECT * FROM blogs;")
    blogs_data = c.execute("SELECT id, name FROM blogs ORDER BY id")
    blog_info = blogs_data.fetchall()[id_number-1]
    blog_name = blog_info[1]
    db.close()
    return render_template('blog_page.html', blog_name=blog_name)

@app.route("/edit_page", methods = ["POST"])
def load_edit_page():
    return render_template('edit_page.html', blog_name="test blog")

@app.route("/save_edit", methods = ["POST"])
def save_edit():
    return redirect(url_for('load_blog_page'))


#FROM 19_SESSION!!!!!!!!!!!

@app.route("/") #, methods = ['POST'])
def login():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return render_template('login.html')

@app.route("/welcome", methods = ['POST'])
def welcome():
    if request.method == "POST" :
        if request.form.get('username') == "Foo" and request.form.get('password') == "Bar" :
            session['username'] = request.form.get('username')
            return render_template('welcome.html', username=session['username'])
    return render_template('login.html', additional="Incorrect Username or Password")

@app.route("/logout", methods = ['POST'])
def logout():
    session.pop('username')
    return redirect(url_for('login'))

# @app.route("/test")
# def test():
#     return "test"

if __name__ == "__main__":
    app.debug = True
    app.run(port=1026)

# db.commit()
# db.close()
