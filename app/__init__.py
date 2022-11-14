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

#load blog_list
@app.route("/blog", methods = ['POST'])
def load_blog_list():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    blog_list = c.execute("SELECT name, user_name, id FROM blogs").fetchall()
    # print(blog_list)
    db.close()
    return render_template('blog_list.html', blogs = blog_list)

@app.route("/new_blog")
def new_blog():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    new_blog_id = str(len(c.execute("SELECT id FROM blogs").fetchall()) + 1)
    blog_name = request.form.get('blog_name')
    creator = session['username']
    c.execute("INSERT INTO blogs VALUES ('"+blog_name+"', '"+creator+"', '"+new_blog_id+"');")
    
    db.commit()
    db.close()
    return redirect(url_for('load_blog_list'))

# Load Pages :
@app.route("/blog/<name>/<id>", methods = ['POST'])
def load_blog_page(name, id):
    db = sqlite3.connect(db_name)
    c =  db.cursor()
    blog_id = int(id)
    blog_info = c.execute("SELECT id, name, user_name FROM blogs WHERE id="+str(blog_id)).fetchall() # Grabs the exact blog by id
    blog_entries = c.execute("SELECT id, name, contents FROM entries WHERE blog_id="+str(blog_id)+" ORDER BY id").fetchall()  # Selects all entries on this blog and orders them by id
    try :
        blog_name = blog_info[0][1]
        if blog_name != name :
            return present_error("Apologies, it seems that blog does not exist.")
            #Maybe have info to get to the blog they probably wanted (same name / id for example)?
        blog_creator = blog_info[0][2]
    except :
        return present_error("Apologies, it seems that blog does not exist.")
    db.close()
    if len(blog_entries) == 0 :
        blog_entries = [[-1, "Nothing here yet", "Create the first entry below"]]
    session['last_page'] = ["/blog", blog_id, blog_name, blog_creator] # Sets the last_page variable to the current page
    return render_template('blog_page.html', blog_name=blog_name, creator=blog_creator, entries=blog_entries)

@app.route("/edit_page", methods = ["POST"])
def load_edit_page():
    (name, blog_id, blog_name, blog_creator) = session['last_page'] # Gets last page visited data
    if 'username' not in session :
        return present_error("Apologies, you need to log in to edit pages.")
    if session['username'] != blog_creator :
        return present_error("Apologies, only a blog's creator can edit it.")
    session['last_page'] = ["/edit_page", blog_id, blog_name, blog_creator] # Sets the last_page variable to the current page
    return render_template('edit_page.html', blog_name=blog_name)

@app.route("/edit_entry/<id>", methods = ["POST"])
def load_edit_entry_page(id):
    (name, blog_id, blog_name, blog_creator) = session['last_page'] # Gets last page visited data
    if 'username' not in session :
        return present_error("Apologies, you need to log in to edit pages.")
    if session['username'] != blog_creator :
        return present_error("Apologies, only a blog's creator can edit it.")
    entry_id = id
    db = sqlite3.connect(db_name)
    c =  db.cursor()
    entry_info = c.execute("SELECT id, name, contents FROM entries WHERE id="+str(entry_id)).fetchall()
    try :
        entry_name = entry_info[0][1]
        entry_contents = entry_info[0][2]
    except :
        return present_error("Apologies, it seems that entry does not exist.")
    db.close()
    session['last_page'] = ["/edit_entry", blog_id, blog_name, blog_creator] # Sets the last_page variable to the current page
    session['entry'] = entry_id
    return render_template('edit_entry.html', blog_name=blog_name, name=entry_name, contents=entry_contents)

@app.route("/")
def load_main_page():
    if 'username' in session:
        session['last_page'] = ["/", "na", "na", "na"]
        return render_template('main_page.html', username=session['username'])
    return redirect(url_for('load_login_page'))

@app.route("/login")
def load_login_page():
    if 'username' in session:
        return redirect(url_for('load_main_page'))
    session['last_page'] = ["/login", "na", "na", "na"]
    return render_template('login.html')

@app.route("/register", methods=["POST"])
def load_register_page():
    session['last_page'] = ["/register", "na", "na", "na"]
    return render_template("register.html")

# Functions :
@app.route("/create_post", methods = ["POST"])
def save_new_post():
    if request.method == "POST" :
        (name, blog_id, blog_name, blog_creator) = session['last_page'] # Gets last page visited data
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        blog_entries = c.execute("SELECT id FROM entries ORDER BY id").fetchall() # Gets the number of current entries as to create a new unique entry id
        num_blog_entries = blog_entries[-1][0]+1
        #c.execute("CREATE TABLE entries (name TEXT, contents TEXT, blog_id INT, id INT PRIMARY KEY);")
        c.execute("INSERT INTO entries VALUES ('"+str(request.form.get("name"))+"', '"+str(request.form.get("change"))+"', "+str(blog_id)+", "+str(num_blog_entries)+");")
        db.commit()
        db.close()
        return redirect(url_for('load_blog_page', name=blog_name, id=blog_id)) # Returns to previous blog page
    return "ERROR - NOT POST!"

@app.route("/save_edit", methods = ["POST"])
def save_edit():
    if request.method == "POST" :
        (name, blog_id, blog_name, blog_creator) = session['last_page'] # Gets last page visited data
        entry_id = session['entry']
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
        (name, blog_id, blog_name, blog_creator) = session['last_page'] # Gets last page visited data
        entry_id = session['entry']
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        c.execute("DELETE FROM entries WHERE id="+str(entry_id)) # Deletes the current entry
        db.commit()
        db.close()
        return redirect(url_for('load_blog_page', name=blog_name, id=blog_id)) # Returns to previous blog page
    return "ERROR - NOT POST!"

def present_error(message):
    print(message)
    return render_template("error.html", error=message)

@app.route("/logout", methods = ['POST'])
def logout():
    session.pop('username')
    return redirect(url_for('load_login_page'))

@app.route("/activate_login", methods = ["POST"])
def login():
    if request.method == "POST" :
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        username = request.form.get('username')
        user = c.execute("SELECT name, passwd FROM users WHERE name='"+str(username)+"'").fetchall()
        db.close()
        if len(user) == 1 : # Checks to make sure username exists
            if user[0][1] == str(request.form.get('password')) :
                session['username'] = username # Logins in user
                return redirect(url_for('load_main_page'))
            else :
                return render_template('login.html', additional="ERROR: Incorrect password for "+username)
        else :
            return render_template('login.html', additional="ERROR: No User with that Username exists")
    return "ERROR - NOT POST!"

@app.route("/create_user", methods=["POST"])
def create_user():
    if request.method == "POST" :
        db = sqlite3.connect(db_name)
        c =  db.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        users = c.execute("SELECT name FROM users WHERE name='"+str(username)+"'").fetchall()
        if len(users) == 0 : # Checks to make sure username doesn't already exist
            c.execute("INSERT INTO users VALUES ('"+username+"', '"+password+"');") # Adds user to database
            db.commit()
            db.close()
            session['username'] = username # Logins in user
            return redirect(url_for('load_main_page'))
        else :
            db.close()
            return render_template('register.html', additional="ERROR: Username already taken")
    return "ERROR - NOT POST!"

# @app.route("/back", methods = ["POST"])
# def back():
#     (page, blog_id, blog_name, blog_creator) = session['last_page']
#     if page == "/":
#         return redirect(url_for('load_main_page'))
#     elif page == "/login":
#         return redirect(url_for('load_login_page'))
#     elif page == "/register":
#         return redirect(url_for('load_register_page'))
#     elif page == "/blog":
#         return redirect(url_for('load_blog_page', name=blog_name, id=blog_id))
#     elif page == "/edit_page":
#         return redirect(url_for('load_edit_page'))
#     elif page == "/edit_entry":
#         return redirect(url_for('load_edit_entry_page', id=session['entry']))
#     else :
#         return "ERROR - Incorrect Last Page in Session! "+request.path()

if __name__ == "__main__":
    app.debug = True
    app.run(port=1026)
