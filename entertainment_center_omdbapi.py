# Importing the modules which we are required for this project
import fresh_tomatoes # contains functions to create the webpage
import omdbapi # contains the class Movie

# Create instances of the class Movie for each of the favorite movies
desperado = omdbapi.Movie("Desperado","www.youtube.com/watch?v=MdZaOB03b1U")
ratatouille = omdbapi.Movie("Ratatouille","www.youtube.com/watch?v=c3sBBRxDAqk")
unforgiven = omdbapi.Movie("Unforgiven","www.youtube.com/watch?v=XDAXGILEdro")
tangled = omdbapi.Movie("Tangled","www.youtube.com/watch?v=ip_0CFKTO9E")
matrix = omdbapi.Movie("The Matrix","www.youtube.com/watch?v=m8e-FF8MsqU")
ralph = omdbapi.Movie("Wreck-It Ralph","www.youtube.com/watch?v=87E6N7ToCxs")

# Create a list of all of the movie instances for the fresh_tomatoes.open_movies_page function
movies = [desperado, ratatouille, unforgiven, tangled, matrix, ralph]

# Run the function which creates the HTML/CSS/JS with the movie information
fresh_tomatoes.open_movies_page(movies)