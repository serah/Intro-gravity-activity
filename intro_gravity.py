#  gcompris - intro_gravity.py
#
# Copyright (C) 2003, 2008 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# intro_gravity activity.
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import goocanvas
import pango
import time
import gcompris.bonus

from gcompris import gcompris_gettext as _

class Gcompris_intro_gravity:
  """Empty gcompris python class"""


  def __init__(self, gcomprisBoard):
    print "intro_gravity init"

    # Save the gcomprisBoard, it defines everything we need
    # to know from the core
    self.gcomprisBoard = gcomprisBoard

    # Needed to get key_press
    gcomprisBoard.disable_im_context = True

  def start(self):
    print "intro_gravity start"

    # Set the buttons we want in the bar
    gcompris.bar_set(0)


    # Create our rootitem. We put each canvas item in it so at the end we
    # only have to kill it. The canvas deletes all the items it contains
    # automaticaly.
    self.rootitem = goocanvas.Group(parent =
                                    self.gcomprisBoard.canvas.get_root_item())
    
    gcompris.set_background(self.gcomprisBoard.canvas.get_root_item(),"intro_gravity/solar_system.svgz")

    svghandle = gcompris.utils.load_svg("intro_gravity/solar_system.svgz")
    self.selection = goocanvas.Svg(
      parent = self.rootitem,
      svg_handle = svghandle,
      svg_id = "#selected"
      )
      
    self.selection.connect("button_press_event", self.game)
    gcompris.utils.item_focus_init(self.selection, None)
    
    self.text = goocanvas.Text(parent=self.rootitem,
      x = 400,
      y = 400,
      fill_color = "yellow",
      font = gcompris.skin.get_font("gcompris/title"),
      text = _("The Solar System"))


  def game(self,a,b,c):
    gcompris.utils.item_focus_remove(self.selection, None)
    self.text.remove()
    goocanvas.Text(
      parent = self.rootitem,
      x=400.0,
      y=100.0,
      text=_("Mass is directly proportional to gravitational force"),
      font = gcompris.skin.get_font("gcompris/subtitle"),
      fill_color="red",
      anchor = gtk.ANCHOR_CENTER,
      alignment = pango.ALIGN_CENTER
      )

    # Set a background image
    gcompris.set_background(self.gcomprisBoard.canvas.get_root_item(),
                           "intro_gravity/background.svg")

    pixbuf = gcompris.utils.load_pixmap("intro_gravity/uranus.png")
    self.mid_planet = goocanvas.Image(
      parent = self.rootitem,
      pixbuf = pixbuf,
      height = 50,
      width = 50,
      x = 375,
      y = 220)


    self.pixbuf_saturn = gcompris.utils.load_pixmap("intro_gravity/saturn.png")
    self.saturn_x = 30
    self.saturn_y = 170
    self.saturn_size = 110
    self.planet_load_saturn(self.saturn_size,self.saturn_x,self.saturn_y)
    
    self.pixbuf_neptune = gcompris.utils.load_pixmap("intro_gravity/neptune.png")
    self.neptune_x = 630
    self.neptune_y = 170
    self.neptune_size= 120
    self.planet_load_neptune(self.neptune_size,self.neptune_x,self.neptune_y)
   
    self.neptune.connect("button_press_event",self.increase_neptune)
    self.saturn.connect("button_press_event",self.increase_saturn)
      
  def end(self):
    print "intro_gravity end"
    # Remove the root item removes all the others inside it
    self.rootitem.remove()


  def ok(self):
    print("intro_gravity ok.")


  def repeat(self):
    print 'repeat'
    gcompris.bonus.display(gcompris.bonus.LOOSE,gcompris.bonus.SMILEY)
    self.neptune.remove()
    self.saturn.remove()
    self.mid_planet.remove()
    self.game(1,2,3)


  #mandatory but unused yet
  def config_stop(self):
    pass

  # Configuration function.
  def config_start(self, profile):
    print("intro_gravity config_start.")

  def key_press(self, keyval, commit_str, preedit_str):
    utf8char = gtk.gdk.keyval_to_unicode(keyval)
    strn = u'%c' % utf8char

    print("Gcompris_intro_gravity key press keyval=%i %s" % (keyval, strn))

  def pause(self, pause):
    print("intro_gravity pause. %i" % pause)


  def set_level(self, level):
    print("intro_gravity set level. %i" % level)
  
  
  def increase_neptune(self,a,b,c):
    if self.neptune_size < 171:
      self.neptune_size += 10
      self.neptune_x -=5
      self.neptune_y -=4
      self.neptune.remove()
  		 		
      self.planet_load_neptune(self.neptune_size,self.neptune_x,self.neptune_y)
      self.mid_planet.animate(30,0,1,0,False,900,50,goocanvas.ANIMATE_FREEZE)
  
    else:
      self.neptune_decrease()

    self.neptune.connect("button_press_event",self.increase_neptune)
    self.mid_planet_move()
      
  def increase_saturn(self,a,b,c):  	
    if self.saturn_size < 171:
      self.saturn_size += 12
      self.saturn_x -=5
      self.saturn_y -=4
      self.saturn.remove()
  		
      self.planet_load_saturn(self.saturn_size,self.saturn_x,self.saturn_y)

      self.mid_planet.animate(-30,0,1,0,False,900,50,goocanvas.ANIMATE_FREEZE)
 
    else:
      self.saturn_decrease()
        
    self.saturn.connect("button_press_event",self.increase_saturn)
    self.mid_planet_move()
    
  def mid_planet_move(self):
    self.position = self.mid_planet.get_bounds().x1
    if self.position > 495:
        self.mid_planet.animate(100,0,1,0,False,400,50,goocanvas.ANIMATE_FREEZE)
        self.repeat()
        
    elif self.position < 200:
      self.mid_planet.animate(-100,0,1,0,False,400,50,goocanvas.ANIMATE_FREEZE)
      self.repeat()
      
  def saturn_decrease(self):
    self.saturn.remove()
    self.saturn_size = 100
    self.saturn_x = 30
    self.saturn_y = 170
    
    self.planet_load_saturn(self.saturn_size,self.saturn_x,self.saturn_y)

    self.mid_planet.animate(140,0,1,0,False,900,50,goocanvas.ANIMATE_FREEZE)
    
    
  def neptune_decrease(self):
    self.neptune.remove()
    self.neptune_size = 120
    self.neptune_x = 630
    self.neptune_y = 170

    self.planet_load_neptune(self.neptune_size,self.neptune_x,self.neptune_y)
    self.mid_planet.animate(-140,0,1,0,False,900,50,goocanvas.ANIMATE_FREEZE)
    
  def planet_load_neptune(self,size,x,y):
    self.neptune = goocanvas.Image(
      parent = self.rootitem,
      pixbuf=self.pixbuf_neptune,
      height=size,
      width=size,
      x=x,
      y=y)

  def planet_load_saturn(self,size,x,y):
    self.saturn = goocanvas.Image(
      parent = self.rootitem,
      pixbuf=self.pixbuf_saturn,
      height=size,
      width=size,
      x=x,
      y=y)
    
