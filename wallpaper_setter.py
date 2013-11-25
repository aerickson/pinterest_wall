import os
from importlib import import_module

class wallpaper_setter(object):
  def __init__(self, img_path):
    self.env = self.environment()
    # load corresponding plugin
    active_plugin = import_module('wpplugins.%s' % self.env)

    # set image as wallpaper using plugin
    setimage = active_plugin.set_wallpaper(img_path)

    if setimage:
        # success
        self.log.debug('successfully set wallpaper from %s' % (save_to))

    else:
        # fail
        self.log.error('error while setting wallpaper from %s' % (save_to))
        print 'cannot set wallpaper, check log for details. Exiting'
        sys.exit(1)


  #https://github.com/lunemec/wpchanger/blob/master/lib/environment.py
  def environment(self):
    if os.name == 'nt':
        env = 'windows'
    elif os.name == 'posix':
        if os.uname()[0] == 'Linux':
            env = self.detect_wm()
        elif os.uname()[0] == 'Darwin':
            env = 'mac'

    return env

  #https://github.com/lunemec/wpchanger/blob/master/lib/environment.py
  def detect_wm(self):
    ''' tries to detect user's window manager on linux, if fail, reverts to using regular Xserver
    @return string

    usage: detect_wm()
    returns "xorg" or "kde" or "gnome" or wm type'''
    ps = []

    # detect running processes
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

    for pid in pids:
        try:
            ps.append(open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().strip())
        except Exception:
            # since we don't mind that some processes might not be in list, do nothing on error
            pass

    # now compare running processes to known window managers
    prepared_dict = {}
    for wm_key in settings.window_managers:
        for wm_string in settings.window_managers[wm_key]:
            prepared_dict[wm_string] = wm_key

    for proc in ps:
        for key in prepared_dict:
            if key in proc:
                return prepared_dict[key]

    # all loops ended and no match, revert to Xserver
    return 'xorg'

