from flask import Flask, render_template,request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)
#######################MODELS ###############################

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    email =  db.Column(db.String(50))
    password = db.Column(db.String(50))
    about = db.Column(db.String(50))
    genres = db.Column(db.String(50))
    image = db.Column(db.String(50))

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    possessor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(200))
    book_name = db.Column(db.String(50))
    genres = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_name = db.Column(db.String(50))
    author_image = db.Column(db.String(50))
    claps = db.Column(db.Integer, default=0)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_name = db.Column(db.String(50))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_name = db.Column(db.String(50))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    status = db.Column(db.String(50), default='Pending')
    


##########################ROUTES################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        data = User.query.filter_by(username=username,
                                    password=password).first()

        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('index'))

        return render_template('incorrectLogin.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        getGenresArray=request.form.getlist('genres')
        g=''
        for eachGenre in getGenresArray:
            g += "      "
            g += eachGenre
            g += "   |   "
        new_user = User(username=request.form['username'],
                        email=request.form['email'],
                        password=request.form['password'], about=request.form['about'],
                        genres=g, image=request.form['image']
                        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/AddReview', methods=['GET', 'POST'])
def AddReview():
    if request.method == 'POST':
        user_id = session['user']
        getGenresArray=request.form.getlist('genres')
        g=''
        for eachGenre in getGenresArray:
            g += "      "
            g += eachGenre
            g += "   |   "
        
        new_review = Review(review=request.form['review'],book_name=request.form['bookname'], 
                                genres=g, author_id=user_id,
                                author_name=User.query.get(user_id).username,
                                author_image=User.query.get(user_id).image)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('addReview.html')


@app.route('/AddBook', methods=['GET', 'POST'])
def AddBook():
    if request.method == 'POST':
        user_id = session['user']
        new_book = Book(title=request.form['bookname'],author=request.form['authorname'],
                         owner_id=user_id,
                        possessor_id=user_id)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('addBook.html')

@app.route('/profile')
def profile():
    user_id = int(request.args['id'])
    isSamePerson = request.args['user']
    person = User.query.filter_by(id=user_id).one()
    bookShelf = Book.query.filter_by(owner_id = user_id,possessor_id = user_id).all()
    nowReading = Book.query.filter(Book.possessor_id == user_id, Book.owner_id != user_id).all()
    return render_template('profile.html', j=person, bookShelf = bookShelf, nowReading = nowReading, isSamePerson = isSamePerson)

@app.route('/profileView')
def profileView():
    user_id = int(request.args['from'])
    request_id = int(request.args['id'])
    person = User.query.filter_by(id=user_id).one() 
    bookShelf = Book.query.filter_by(owner_id = user_id,possessor_id = user_id).all()
    return render_template('profileView.html', j=person, bookShelf = bookShelf, requestId = request_id)

@app.route('/index')
def index():
    user_id = session['user']
    username = User.query.get(user_id).username
    showReview = Review.query.order_by(desc(Review.id)).filter(Review.author_id != user_id).all()
    requests = Request.query.filter_by(to_id=user_id, status='Pending').all()
    return render_template('index.html', showReview = showReview, requests = requests )

@app.route('/clap')
def clap():
    review_id = int(request.args['id'])
    review =  Review.query.get(review_id)
    review.claps += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/suggestions')
def suggestions():

    book_name = request.args['bookname']
    matches = Book.query.filter(Book.title == book_name, Book.owner_id == Book.possessor_id).all()
    matchList = []
    for book in matches:
        matchList.append(User.query.get(book.owner_id))
    return render_template('suggestions.html', matchList = matchList , bookName = book_name)

@app.route('/requested')
def requested():
    user_id = session['user']
    fromname = User.query.get(user_id).username
    to = int(request.args['id']) 
    bookname = request.args['book_name']
    book = Book.query.filter_by(title = request.args['book_name'], owner_id = to).one().id

    requested = Request(from_id = user_id, from_name = fromname, to_id = to, 
                        book_name = bookname, book_id = book)
    db.session.add(requested)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/requestUpdate')
def requestUpdate():
    rid = int(request.args['requestId'])
    obj = Request.query.get(rid)
    ex_book_id = int(request.args['exchangedbook'])
    if ex_book_id == 0 :
        obj.status = 'Ignored'
    else :
        obj.status = 'Accepted'
        ex_book = Book.query.get(ex_book_id)
        ex_book.possessor_id = session['user']
        book = Book.query.get(obj.book_id)
        book.possessor_id = obj.from_id 
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/returnBook')
def returnBook():
    book_id = int(request.args['book_id'])
    book = Book.query.get(book_id)
    book.possessor_id = book.owner_id
    db.session.commit()
    return redirect(url_for('profile', id = session['user'], user = True))




######################################### MAIN ####################################


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
