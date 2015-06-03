import urllib # using urllib functions for returning webpage results
import json # using json function for parsing JSON objects from webpage results

class Video():
	"""This class stores video information:
	* title - The title of the video
	"""
	
	# Constructor to initialize an instance of class Video with a title
	def __init__(self, video_title):
		self.title = video_title

class Movie(Video):
	"""
	This is a subclass of the class Video which stores movie information
	in addition to video information. It passes a movie title to
	www.omdbapi.com and then parses the returned JSON for the
	movie's information:
	
	Currently the movie attributes stored are:

	* year - the release year
	* rating - the MPAA rating e.g. G, PG, PG-13, R
	* duration - the length
	* genre - the genre
	* director - the list of directors
	* actors - the list of actors
	* storyline - the plot of the movie
	* metascore - the rating from Metacritic (out of 100)
	* imdbRating - the movie rating from IMDB (out of 10)
	* poster_image_url - the link to the movie's poster
	* trailer_youtube_url - the link to the movie's YouTube Trailer

	Example Usage:
	>> import omdbapi
	>> ratatouille = Movie("Ratatouille","www.youtube.com/watch?v=c3sBBRxDAqk")
	>> print ratatouille.storyline 
	>> A rat who can cook makes an unusual alliance with a young kitchen worker
	   at a famous restaurant.

	"""
	
	# Constructor to initialize an instance of class Movie with storyline,
	# image, and trailer
	def __init__(self, movie_title, trailer_link):
		Video.__init__(self, movie_title)
		
		# Set the movie name as the title
		self.movie_name = movie_title
		
		# Pass the title to omdbapi.com This is basically the same as the
		# check_profanity from Lesson 2C
		connection = urllib.urlopen("http://www.omdbapi.com/?t="+
									self.movie_name+"&y=&plot=short&r=json")
		output = connection.read()
		connection.close()

		#print output # For viewing the JSON output to see which values
		# are available in the response
		parsed_json = json.loads(output)
		
		self.year = parsed_json["Year"] # Get the movie release year
		self.rating = parsed_json["Rated"] # Get the MPAA rating
		self.duration = parsed_json["Runtime"] # Get the length
		self.genre = parsed_json["Genre"] # Get the list of genres
		self.director = parsed_json["Director"] # Get the directors
		self.actors = parsed_json["Actors"] # Get the actors
		 # Get the score from metacritic
		self.metascore = parsed_json["Metascore"]
		self.imdbRating = parsed_json["imdbRating"] # Get the score from IMDb
		 # Get the IMDb ID which can be used to find the movie
		self.imdbID = parsed_json["imdbID"]
		self.storyline = parsed_json["Plot"] # Get the plot
		self.poster_image_url = parsed_json["Poster"] # Get the poster url
		 # TODO: use YouTube API for searching the YT id of the movie trailer
		self.trailer_youtube_url = trailer_link

	# Function to display the trailer for the movie. This function is not
	# called by the Movie Trailer webpage since it only uses the ID for
	# playing the video with JavaScript but can be used to test the trailer
	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)