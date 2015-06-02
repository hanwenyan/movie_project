import webbrowser
import os
import re

# Styles and scripting for the page
# TODO: move all of the HTML to separate files and read using os
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Movie Trailer Project</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 20%;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.view-trailer', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        // Added jQuery to trigger modal for more movie information
        $(document).ready(function () {
          $('#movieInfo').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget) // Button that triggered the modal
            
            // Extract info from data-* attributes
            var title = button.data('title') 
            var storyline = button.data('storyline')
            var year = button.data('year')
            var rating = button.data('rating')
            var duration = button.data('duration')
            var genre = button.data('genre')
            var director = button.data('director')
            var actors = button.data('actors')
            var metascore = button.data('metascore')
            var imdbRating = button.data('imdb-rating')
            var imdbID = button.data('imdb-id')


            var modal = $(this)
            modal.find('.modal-title').text(title + ' ('+year+')' ) // Add the title and year of the movie
            // Add year, rating, duration, and storyline to modal body
            modal.find('.modal-body').html(
              '<p><b>Plot:</b> ' +storyline+ '</p>' + 
              '<p><b>Rating:</b> ' +rating+ '</p>' + 
              '<p><b>Duration:</b> ' +duration+ '</p>' + 
              '<p><b>Genres:</b> ' +genre+ '</p>' +
              '<p><b>Director(s):</b> ' +director+ '</p>' + 
              '<p><b>Actor(s):</b> ' +actors+ '</p>' + 
              '<p><b>Metascore:</b> <a href="http://www.metacritic.com/about-metascores" target="_blank">' +metascore+ '</a></p>' + 
              '<p><b>IMDb Rating:</b> <a href="http://www.imdb.com/title/' +imdbID+ '/" target="_blank">' +imdbRating+ '</a></p>'
              )
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Movie Information Modal -->
    <div class="modal fade" id="movieInfo" tabindex="-1" role="dialog" aria-labelledby="movieInfoLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h3 class="modal-title" id="movieInfoLabel">Movie Title</h3>
          </div>
          <div class="modal-body">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  
  <footer class="navbar navbar-default navbar-fixed-bottom">
    <div class="container">
      <p class="navbar-text pull-right">Movie information from:
        <a href="http://www.omdbapi.com/" target="_blank">The Open Movie Database</a>.
      </p>
    </div>
  </footer>

  </body>
</html>
'''

# A single movie entry html template. Added a link which will trigger a modal popup for more information on the movie itself.
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" >
    <img class="view-trailer" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer" src="{poster_image_url}" width="220" height="342">
    <br>
    <button type="button" class="btn btn-link" data-toggle="modal" data-target="#movieInfo" data-title="{movie_title}" data-year="{movie_year}"
    data-rating="{movie_rating}" data-duration="{movie_duration}" data-genre="{movie_genre}" data-director="{movie_director}" data-actors="{movie_actors}"
    data-metascore="{movie_metascore}" data-imdb-rating="{movie_imdbRating}" data-imdb-id="{movie_imdbID}" data-storyline="{movie_storyline}">
      {movie_title}
    </button>
</div>

'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title = movie.title,
            movie_year = movie.year,
            movie_rating = movie.rating,
            movie_duration = movie.duration,
            movie_genre = movie.genre,
            movie_director = movie.director,
            movie_actors = movie.actors,
            movie_metascore = movie.metascore,
            movie_imdbRating = movie.imdbRating,
            movie_imdbID = movie.imdbID,
            poster_image_url = movie.poster_image_url,
            movie_storyline = movie.storyline,
            trailer_youtube_id = trailer_youtube_id
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible