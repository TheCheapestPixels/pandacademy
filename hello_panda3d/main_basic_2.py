from direct.showbase.ShowBase import ShowBase


ShowBase()
# Don't you hate having to go to stop your program the difficult way,
# wasting several seconds that could be spent coding? Wouldn't it be
# much easier if the program stopped itself when we slam the `Esc` key?
# Well, let's make it so! When we press the key, `dataLoop` throws an
# `'escape'` event; Let's register a function that will be called when
# the `eventManager` processes that task. For our purposes, we can
# simply take the function that stops the task manager after the current
# loop run-through.
base.accept('escape', base.task_mgr.stop)
# We should also disable the second big idiosyncracy of Panda3D: By
# default, you can control the camera with the mouse, but don't ask me
# how, just build something new, for which you need to disable these
# default controls; They were built by and for people who sat down at
# the DISH CAVE and went right into experimenting with new amusement
# park rides.
base.disable_mouse()
base.run()
