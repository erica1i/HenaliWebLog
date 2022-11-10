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
def load_def_blog_page():
    return load_blog_page("test", 1)

@app.route("/blog/<name>/<id>")
def load_blog_page(name, id):
    db = sqlite3.connect(db_name)
    c =  db.cursor()
    blog_id = int(id)
    blog_info = c.execute("SELECT id, name, user_name FROM blogs WHERE id="+str(blog_id)).fetchall() # Grabs the exact blog by id
    blog_entries = c.execute("SELECT id, name, contents FROM entries WHERE blog_id="+str(blog_id)+" ORDER BY id").fetchall()  # Selects all entries on this blog and orders them by id
    blog_name = blog_info[0][1]
    blog_creator = blog_info[0][2]
    session['last_page'] = ["/blog", blog_id, blog_name] # Sets the last_page variable to the current page
    db.close()
    print(blog_entries)

    if len(blog_entries) == 0 :
        blog_entries = [[0, "Nothing here yet", "Create the first entry below"]]
    return render_template('blog_page.html', blog_name=blog_name, entries=blog_entries)

@app.route("/edit_page", methods = ["POST"])
def load_edit_page():
    blog_id = session['last_page'][1]
    blog_name = session['last_page'][2] # Gets last page visited data
    #check to see if user is correct one

    session['last_page'] = ["/edit_page", blog_id, blog_name] # Sets the last_page variable to the current page
    return render_template('edit_page.html', blog_name=blog_name)

@app.route("/create_post", methods = ["POST"])
def save_new_post():
    if request.method == "POST" :
        blog_id = session['last_page'][1]
        blog_name = session['last_page'][2] # Gets last page visited data
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        num_blog_entries = len(c.execute("SELECT id FROM entries").fetchall()) # Gets the number of current entries as to create a new unique entry id
        #c.execute("CREATE TABLE entries (name TEXT, contents TEXT, blog_id INT, id INT PRIMARY KEY);")
        c.execute("INSERT INTO entries VALUES ('"+str(request.form.get("name"))+"', '"+str(request.form.get("change"))+"', "+str(blog_id)+", "+str(num_blog_entries)+");")
        db.commit()
        db.close()
        return redirect(url_for('load_blog_page', name=blog_name, id=blog_id)) # Returns to previous blog page
    return "ERROR - NOT POST!"

@app.route("/edit_entry/<id>", methods = ["POST"])
def load_edit_entry_page(id):
    blog_id = session['last_page'][1]
    blog_name = session['last_page'][2] # Gets last page visited data
    entry_id = id
    db = sqlite3.connect(db_name)
    c =  db.cursor()
    entry_info = c.execute("SELECT id, name, contents FROM entries WHERE id="+str(entry_id)).fetchall()
    entry_name = entry_info[0][1]
    entry_contents = entry_info[0][2]
    db.close()
    #check to see if user is correct one
    print([entry_name, entry_contents])
    session['last_page'] = ["/edit_entry", blog_id, blog_name, entry_id] # Sets the last_page variable to the current page
    return render_template('edit_entry.html', blog_name=blog_name, name=entry_name, contents=entry_contents)

@app.route("/save_edit", methods = ["POST"])
def save_edit():
    if request.method == "POST" :
        blog_id = session['last_page'][1]
        blog_name = session['last_page'][2]
        entry_id = session['last_page'][3]
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        c.execute("DELETE FROM entries WHERE id="+str(entry_id)) # Deletes the current entry
        #c.execute("CREATE TABLE entries (name TEXT, contents TEXT, blog_id INT, id INT PRIMARY KEY);")
        c.execute("INSERT INTO entries VALUES ('"+str(request.form.get("name"))+"', '"+str(request.form.get("change"))+"', "+str(blog_id)+", "+str(entry_id)+");")
        db.commit()
        db.close()
        return redirect(url_for('load_blog_page', name=blog_name, id=blog_id)) # Returns to previous blog page
    return "ERROR - NOT POST!"

@app.route("/delete_entry", methods = ["POST"])
def delete_entry():
    if request.method == "POST" :
        blog_id = session['last_page'][1]
        blog_name = session['last_page'][2]
        entry_id = session['last_page'][3]
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        c.execute("DELETE FROM entries WHERE id="+str(entry_id)) # Deletes the current entry
        db.commit()
        db.close()
        return redirect(url_for('load_blog_page', name=blog_name, id=blog_id)) # Returns to previous blog page
    return "ERROR - NOT POST!"
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

@app.route("/blog", methods = ['POST'])
def view_blog_section():
    return render_template('blog_page.html')

# @app.route("/test")
# def test():
#     return "test"

if __name__ == "__main__":
    app.debug = True
    app.run(port=1026)

# db.commit()
# db.close()
