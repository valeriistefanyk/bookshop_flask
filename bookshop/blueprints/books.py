from flask import Blueprint, render_template, redirect, request, url_for
from bookshop.models import Book
from bookshop.extenstions import db
from bookshop.forms import BookForm

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
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, description=form.description.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.details', book_id=book.id))
    return render_template('books/create.html', form=form)

@books.route('/<int:book_id>/edit', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.description = form.description.data
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.details', book_id=book.id))
    return render_template('books/edit.html', book=book, form=form)


@books.errorhandler(404)
def not_found(exception):
    return render_template('books/404.html'), 404
