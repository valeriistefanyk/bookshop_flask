from flask import Blueprint, render_template, redirect, request, url_for
from bookshop.models import Book
from bookshop.extenstions import db

books = Blueprint('books', __name__)


@books.route('/')
def index():
    all_book = Book.query.all()
    return render_template('books/index.html', books=all_book)

@books.route('/<int:book_id>')
def details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/detail.html', book=book)

@books.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        book = Book(title=request.form['title'], description=request.form['description'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.details', book_id=book.id))
    return render_template('books/create.html')

@books.errorhandler(404)
def not_found(exception):
    return render_template('books/404.html'), 404
