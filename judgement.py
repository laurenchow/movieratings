from flask import Flask, render_template, session, redirect, request
import model
import jinja2
 
 
app = Flask(__name__) 
app.secret_key = ')V\xaf\xdb\x9e\xf7k\xccm\x1f\xec\x13\x7fc\xc5\xfe\xb0\x1dc\xf9\xcfz\x92\xe8'
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route('/')
def index():
    print session

    return render_template("index.html")

    # use jquery AJAX here to add on same page
    # show some things only when logged in
    

@app.route('/signup', methods = ['GET', 'POST'])
def user_signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        return signup_user()

def signup_user():
    user_email = request.form['email']
    user_password = request.form['password']
    
    new_user = model.User(email = user_email, password = user_password)
    model.session.add(new_user)
    model.session.commit() 

    current_user = model.session.query(model.User).filter_by(email = user_email).first()
    current_user_id = current_user.id


    if "login" in session: #this adds users to session
        session["login"][current_user_id] = user_email
    else:
        session["login"] = {current_user_id: user_email}

    print session
 

    return redirect("/")
 



@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == "GET":
        return render_template("login.html")
    else: 
        return login_user()

def login_user():

    
    user_email = request.form['email']
    user_password = request.form['password']

    # use hashing here different than hashing or hashmap, use MD5 or SHA1 to store the password in the session
    #https://docs.python.org/2/library/md5.html

    current_user = model.session.query(model.User).filter_by(email = user_email).filter_by(password=user_password).first()


    #the line below checks to see if a user is already in DB -if not, it sends them to signup page
    #if they are in DB, it checks to see if they're in session -if not, it adds them
    if current_user:
        session['user_id'] = current_user.id
        session['user_email'] = current_user.email

        print session
        return redirect("/")

    else: 
        return redirect("/")
        return redirect("/signup")
            
@app.route('/logout')
def logout_user():
    session.clear()
    print "This is what session looks like now %r" % session
    return redirect("/login")
    # use g in a before_request function to check and see if a user is logged in -- if they are logged in you can save it in g
    

@app.route('/viewallusers')
def view_all_users(): 
    user_list = model.session.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)



@app.route('/user/<int:id>')
def view_single_user(id):
    single_user = model.session.query(model.Rating).filter_by(user_id = id).all()
    return render_template("user.html", user = single_user)



@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def view_single_movie(id):
   
    single_movie = model.session.query(model.Movie).get(id)
    print single_movie.ratings

    return render_template("movie.html", film = single_movie)



@app.route('/add_rating/<int:movie_id>', methods=['GET', 'POST'])
def add_rating(movie_id):
    if request.method == "GET":
        return render_template("add_rating.html", movie_id=movie_id)
    else:
        return add_your_own_rating(movie_id)

def add_your_own_rating(movie_id):
    my_own_rating = request.form['my_rating']
    current_user_id = session.get('user_id') # won't crash if doesn't exist this way
    movie_to_rate = request.form['movie_id']

    new_movie_rating = model.Rating(user_id = current_user_id, movie_id = movie_to_rate, rating = my_own_rating)
    model.session.add(new_movie_rating)
    model.session.commit()
 
    
    return render_template("add_rating.html", movie_id = movie_id)

  


    
if __name__ == "__main__":
    app.debug = True
    app.run()
