from flask import Blueprint, render_template
from bookshop.models import Book


books = Blueprint('books', __name__)


@books.route('/')
def index():
    all_book = Book.query.all()
    return render_template('books/index.html', books=all_book)

@books.route('/<int:book_id>')
def details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/detail.html', book=book)

@books.errorhandler(404)
def not_found(exception):
    return render_template('books/404.html'), 404
