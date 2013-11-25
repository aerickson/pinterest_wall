import argparse
import time
import urllib
from config import *
from feed_parser import feed_parser
from collage_maker import collage_maker
from wallpaper_setter import wallpaper_setter

def main_flow():
  """
  this is the function that controls the mainflow of the program
  -> parse the feed of user
  -> get wallpaper urls
  -> create collage
  -> set as wallpaper
  -> sleep for designated time before restarting
  INPUT:
    look at argparse settings defined in term_main()
  OUTPUT:
    sets the wallpaper on your mac with simple collage of pins from your selected board
  """
  while(1):
    #->read the feed and get image link list
    feed = feed_parser(config['username'], config['boardname'])
    imgsrc_list = feed.get_imgsrc_list()

    #->download images from the feed and create a First-Fit collage based on the config options
    img_loader = collage_maker()
    collage_fn = img_loader.download_and_collage(imgsrc_list)

    #->set as wallpaper from the image stored at temppath
    wp_set = wallpaper_setter(collage_fn)

    #->sleep for designated time before restarting
    time.sleep(config['sleeptime'])

def main():
   #argument parser
    parser = argparse.ArgumentParser(description="""parses pinterest feed to find out all the pictures from there,it prints the list of qualified image urls""")
    parser.add_argument('-u','--username', help='username for which the feed is to be accessed', required=True)

    parser.add_argument('-w','--width', type=int, help='minimum width of the background image', default=config['width'], required=False)
    parser.add_argument('-ht','--height', type=int, help='minimum height of the background image', default=config['height'], required=False)
    parser.add_argument('-b','--boardname', help='board name of the user from which the feed is to be accessed', default=config['boardname'],required=False)
    parser.add_argument('-s','--sleeptime', type=int, help='time to sleep in seconds before resetting the wallpaper', default=config['sleeptime'], required=False)
    parser.add_argument('-p','--temppath', help='temporary path that should be used to download images and output the collage to', default=config['temppath'], required=False)
    args = vars(parser.parse_args())

    config.update(args)
    main_flow()

if __name__ == "__main__":
  main()