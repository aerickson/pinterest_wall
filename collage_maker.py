import os
import shutil
import urllib
import Image, ImageOps #add border to each image
from config import *

class collage_maker(object):
  def __init__(self):
    """
    initalize with the temppath
    """
    self.collage_width = config['width']
    self.collage_height = config['height']
    self.image_border = config['bordersize'] 
    self.image_border_color = config['bordercolor']
    self.path = config['temppath']
    self.validate_path()

  def download_and_collage(self,imgsrc_list):
    #empty the temp path folder
    self.delete_images()

    #collage image object
    collage = Image.new('RGB',(self.collage_width, self.collage_height))

    #calculate the number of images that fit horizontally
    effective_img_width = 192 + self.image_border*2
    no_of_columns = (self.collage_width / effective_img_width)
    col_index = [0]*no_of_columns

    for i,each in enumerate(imgsrc_list):
      #fetch the image from the list
      img_fn = os.path.join(self.path, str(i)+".jpg")
      urllib.urlretrieve(each, img_fn)
      orig_img = Image.open(img_fn)
      #add border to it
      bordered_img = ImageOps.expand(orig_img, border=self.image_border, fill=self.image_border_color)
      width, height = bordered_img.size
      collage.paste(bordered_img, ((i%no_of_columns)*width, col_index[i%no_of_columns]))
      col_index[i%no_of_columns] += height
    collage_fn = os.path.join(self.path, 'collage.jpg')
    collage.save(collage_fn)
    return collage_fn

  def delete_images(self):
    shutil.rmtree(self.path)
    os.makedirs(self.path)


  def validate_path(self):
    """
    validates the temppath
    """
    #check if the temppath exists if not, then create the path
    abs_temppath = os.path.abspath(self.path)
    self.path = abs_temppath
    if not os.path.exists(abs_temppath):
      os.makedirs(abs_temppath)