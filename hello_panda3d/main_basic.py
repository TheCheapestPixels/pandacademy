# So you just installed Panda3D and want to see whether it works. First,
# though: There are *two* modules that come in the `panda3d` package:
# `panda3d` and `direct`. `panda3d` contains the parts of the engine
# that are written in C++, and wrapped for use in Python by the
# Interrogate system. `direct` is a suite of tools built on top of
# `panda3d` in Python.
from direct.showbase.ShowBase import ShowBase


# `ShowBase` is a convenience class that sets up all moving parts that
# make up a running 3D engine. When instantiated, the object will
# automatically create a reference to itself in the `__builtins__`,
# meaning that it can now accessed from anywhere, just like `str` or
# `min`. This is obviously heresy to any Clean Coder, but it is
# remarkably comfortable to not have to scatter your code with
# `global base` everywhere.
# Anyway, as you just saw, the name of that reference is `base`.
ShowBase()
# At this point, a window containing a black rectangle should have
# opened up. This is the engine at rest. In any more complex
# application, we would now be starting to set up everything that we
# need. Here, we need nothing to be done either now or during the
# running of the application, so we just call...
base.run()
# Now the window should have turned grey, as Panda3D begins to render
# pure emptiness as often as your screen's frame rate allows it to. It
# will (seemingly) not react to any input, so all that is left to do is
# to close the window (or stop the process). But now you know that
# everything is working.
