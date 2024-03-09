from direct.showbase.ShowBase import ShowBase


ShowBase()
base.accept('escape', base.task_mgr.stop)
base.disable_mouse()
# When loading a model, it is automatically wrapped into a NodePath.
model = base.loader.load_model("models/smiley")
# We attach it to the scene graph's root...
model.reparent_to(base.render)
# ...and move back the camera, because right now it is in the center of
# the sphere.
base.cam.set_y(-10)
base.run()
