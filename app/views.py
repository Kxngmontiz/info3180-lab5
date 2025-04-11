"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, flash, send_from_directory
import os

from .forms import MovieForm
from app import db
from app.models import Movie

from werkzeug.utils import secure_filename
from datetime import datetime, timezone

from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
@app.route("/api/v1/movies", methods=["POST"])
def movies():
    
    if request.method == "POST":
        
        form = MovieForm()
        print("this is title: ", form.title.data)
        print("this is desc: ", form.description.data)
        print("this is poster: ", form.poster.data)
        
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            
            poster = form.poster.data
            poster_filename = secure_filename(poster.filename)
            
            created_at = datetime.now(timezone.utc)
            
            movie = Movie(title, description, poster_filename, created_at)
            
            db.session.add(movie)
            db.session.commit()
            
            # flash("New Movie Successully Added To The Database","success")
            
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
            
            # flash("Poster Successfully Saved To The Uploads Folder")
            
            return jsonify({"message": "Movie Successfully added",
                            "title": title,
                            "poster": poster_filename,
                            "description": description})
        
        return form_errors(form)
    
@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()})             
            

@app.route("/api/v1/movies", methods=["GET"])
def add_movies():
    
    movies = db.session.execute(db.select(Movie)).scalars().all()
    
    movies_list = [
        {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": f"/api/v1/posters/{movie.poster}"  # Ensure `movie.poster` stores the filename
        }
        for movie in movies
    ]
    return jsonify({"movies": movies_list})
    

@app.route("/api/v1/posters/<filename>")
def get_image(filename):
    upload_folder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])

    # print("this is uplaod folder", upload_folder)
    # print("get image route was reached")

    return send_from_directory(upload_folder, filename)
    
    

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404