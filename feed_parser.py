from BeautifulSoup import BeautifulStoneSoup
import urllib2
import sys

class feed_parser(object):
  def __init__(self, username, boardname="feed"):
    """
    INPUT:
      -url: url to the rss feed to be parsed
    """
    self.url = "http://www.pinterest.com/"+username+'/'+boardname+'.rss'

  def parse_item_tag(self,item_tag):
    """
    takes in the item tag from the rss feed and parses out the imporant information to a dictionary
    INPUT:
      -item_tag: beautiful soup object of the tag
      -settings: dictioanry of settings as listed below'
        -width: minimum width of the image
        -height: minimum height of the image
    OUTPUT:
      -dict(): dictioanry of the listed attributes assosicated with the pins
        -link 
        -img_src
        -title
    """
    pin_dict = dict()
    pin_dict['link'] = item_tag.find('link').getText()
    pin_dict['title'] = item_tag.find('title').getText()

    #TODO: find a better way to extract the image src
    description_string = item_tag.find('description').getText()
    description_string = description_string.split("img src=\"", 2)[1]
    description_string = description_string.split("\"",2)[0]
    pin_dict['img_src'] = description_string

    return pin_dict

  def get_blob(self):
    """
    INPUT:
    OUTPUT:
      -string: blob of the rss feed of the requested user and his board if boardname is provided
    SIDE-EFFECT:
      -accesses the interwebs for getting the feed, expect and catch those 404s
    """
    print self.url
    try:
      response = urllib2.urlopen(self.url)
    except:
      print "Can't access the username+boardname"
      sys.exit(0)
    self.blob = response.read()
    return self.blob

  def parse_pin_attr(self):
    """
    INPUT:
    OUTPUT:
      -[list]: list of wallpaper urls that pass the criteria
    SIDE-EFFECT:
      -Not much error checking happening so expect parsing error in case incorrect blob is passed
      -wrap the call to the function in a try block
    """
    #get the blob if it hasn't been requested yet
    if not self.blob:
      self.get_blob()
    feed_soup = BeautifulStoneSoup(self.blob)
    pins_soup = feed_soup.findAll("item")
    self.pins_attr_list = list()
    for each_pin in pins_soup:
      self.pins_attr_list.append(self.parse_item_tag(each_pin))
    return self.pins_attr_list

  def get_imgsrc_list(self):
    """
    INPUT:
    OUTPUT:
      -list of imgsrc parsed from the rss feed url
    """
    self.get_blob()
    self.parse_pin_attr()
    self.imgsrc_list = list()
    for pin in self.pins_attr_list:
      self.imgsrc_list.append(pin['img_src'])

    return self.imgsrc_list
