from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieDb.db'
db = SQLAlchemy(app)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'genre': fields.String
}

class MovieDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Titulo:{self.title} Gênero:{self.genre}"


class Movies(Resource):
    @marshal_with(resource_fields)
    def get(self):
        movies = MovieDb.query.all()
        return movies
    
    @marshal_with(resource_fields)
    def post(self):
        data = request.json
        movie = MovieDb(title=data['title'], genre=data['genre'])
        db.session.add(movie)
        db.session.commit()

        movies = MovieDb.query.all()
        return movies


class Movie(Resource):
    @marshal_with(resource_fields)
    def get(self, pk):
        movie = MovieDb.query.filter_by(id=pk).first()
        return movie
    
    @marshal_with(resource_fields)
    def put(self, pk):
        data = request.json
        movie = MovieDb.query.filter_by(id=pk).first()
        movie.title = data['title']
        movie.genre = data['genre']
        db.session.commit()

        return movie
    
    @marshal_with(resource_fields)
    def delete(self, pk):
        movie = MovieDb.query.filter_by(id=pk).first()
        db.session.delete(movie)
        db.session.commit()

        movies = MovieDb.query.all()
        return movies
    

api.add_resource(Movies, "/movies")
api.add_resource(Movie, "/movies/<int:pk>")


if __name__ == "__main__":
    app.run(debug=True)