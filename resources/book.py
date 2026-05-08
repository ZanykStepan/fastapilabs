from flask_restful import Resource, reqparse
from flask import request
import uuid
from models import books

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help="Назва обов'язкова")
parser.add_argument('author', required=True)
parser.add_argument('year', type=int, required=True)
parser.add_argument('status', default="available")

class BookListResource(Resource):
    def get(self):
        """
        Отримати список всіх книг
        ---
        responses:
          200:
            description: Список книг
        """
        return books, 200

    def post(self):
        """
        Додати нову книгу
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Book
              properties:
                title: {type: string}
                author: {type: string}
                year: {type: integer}
        responses:
          201:
            description: Книгу створено
        """
        args = parser.parse_args()
        new_book = {
            "id": str(uuid.uuid4()),
            "title": args['title'],
            "author": args['author'],
            "year": args['year'],
            "status": args['status']
        }
        books.append(new_book)
        return new_book, 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Книга знайдена
          404:
            description: Не знайдено
        """
        book = next((b for b in books if b["id"] == book_id), None)
        if book:
            return book, 200
        return {"message": "Книгу не знайдено"}, 404

    def delete(self, book_id):
        """
        Видалити книгу (ідемпотентно)
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Видалено
        """
        global books
        books = [b for b in books if b["id"] != book_id]
        return '', 204