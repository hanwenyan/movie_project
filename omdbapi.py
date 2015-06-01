import urllib # using urllib functions for returning webpage results
import json # using json function for parsing JSON objects from webpage results

class Video():
	"""This class stores video information:
	- Title
	- Duration (in minutes)"""
	
	# Constructor to initialize an instance of class Video with a title and duration
	def __init__(self, video_title):
		self.title = video_title

class Movie(Video):
	"""This is a subclass of the class Video which stores movie information in addition to video information:
	- Storyline
	- Poster URL
	- YouTube Trailer URL"""
	
	VALID_RATINGS = ["G", "PG", "PG-13", "R"] # A list of valid ratings for movies

	# Constructor to initialize an instance of class Movie with storyline, image, and trailer
	def __init__(self, movie_title, trailer_link):
		Video.__init__(self, movie_title)
		
		# Set the movie name as the title
		self.movie_name = movie_title
		# Perform a query to omdbapi for the movie_title, this is basically the same as the check_profanity
		# from Lesson 2C
		connection = urllib.urlopen("http://www.omdbapi.com/?t="+self.movie_name+"&y=&plot=short&r=json")
		output = connection.read()
		connection.close()

		#print output # For viewing the JSON output to see which values are available in the response
		parsed_json = json.loads(output)
		
		self.storyline = parsed_json["Plot"] # Get the plot
		self.duration = parsed_json["Runtime"] # Get the length
		self.poster_image_url = parsed_json["Poster"] # Get the poster url
		self.trailer_youtube_url = trailer_link # TODO use YouTube API for searching the YT id of the movie trailer

	# Function to display the trailer for the movie. This function is not called by the Movie Trailer webpage
	# since it only uses the ID for playing the video with JavaScript
	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)

ratatouille = Movie("Ratatouille","www.youtube.com/watch?v=c3sBBRxDAqk")

print ratatouille.storyline
print ratatouille.poster_image_url