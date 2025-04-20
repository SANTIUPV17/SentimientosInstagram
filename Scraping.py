from glob import glob
from os.path import expanduser
from sqlite3 import connect
import pathlib
import csv
import emoji
from glob import glob
from os.path import expanduser
from sqlite3 import connect
from instaloader import ConnectionException, Instaloader, Post

'''
To add user and account info, make sure you are currently logged into specified account on firefox.
'''
#######################################
## 1. Autenticarse en instagram
#######################################
path_to_firefox_cookies = "C:/Users/thesa/AppData/Roaming/Mozilla/Firefox/Profiles/wexbutt3.default-release/cookies.sqlite"
FIREFOXCOOKIEFILE = glob(expanduser(path_to_firefox_cookies))[0]


## solo se permite un intento por conexión
instaloader = Instaloader(max_connection_attempts=1)

## obtener cookie id for instagram
instaloader.context._session.cookies.update(connect(FIREFOXCOOKIEFILE)
                                            .execute("SELECT name, value FROM moz_cookies "
                                                     "WHERE host='.instagram.com'"))


## comprobar connection
try:
    username = instaloader.test_login()
    if not username:
        raise ConnectionException()
except ConnectionException:
    raise SystemExit("Cookie import failed. Are you logged in successfully in Firefox?")

instaloader.context.username = username

## se guarda la sesión en instaloader para poder usarla más tarde
instaloader.save_session_to_file()

#######################################
## 2. Construir scraper
#######################################

## inicializar instaloader
instagram = Instaloader(download_pictures=False, download_videos=False,
                                    download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)

## login
instagram.load_session_from_file('jonasitovuelve43')


def scrape_data(url):
# """
# Input url in string format.
# """
	SHORTCODE = str(url[28:39])
	post = Post.from_shortcode(instagram.context, SHORTCODE)

	csvName = SHORTCODE + '.csv'
	output_path = pathlib.Path('C:\\Users\\thesa\\Downloads\\test-scrapping')
	post_file = output_path.joinpath(csvName).open("w", encoding="utf-8")

	field_names = [
			    "post_shortcode",
			    "commenter_username",
			    "comment_text",
			    "comment_likes"
			    ]

	post_writer = csv.DictWriter(post_file, fieldnames=field_names)
	post_writer.writeheader()

	## obtener comentarios del post
	for x in post.get_comments():
	    post_info = {
	    "post_shortcode":post.shortcode,
	    "commenter_username": x.owner,
	    "comment_text": (emoji.demojize(x.text)).encode('utf-8', errors='ignore').decode() if x.text else "",
	    "comment_likes": x.likes_count
	    }
     
	    post_writer.writerow(post_info)

print("Done Scraping!")

scrape_data("https://www.instagram.com/p/DDGKw3ytw6U/?igsh=MXZkeDBjMnZrOXNnMQ==")
#scrape_data("https://www.instagram.com/p/DIca0iiSbXT/?img_index=1/")	
#scrape_data("https://www.instagram.com/p/DHW_EJnS39Z/")

