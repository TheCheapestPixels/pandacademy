from panda3d.core import (
    GraphicsPipeSelection,
    GraphicsPipe,
    GraphicsEngine,
    FrameBufferProperties,
    WindowProperties,
    NodePath,
    Camera,
    Loader,
    LoaderOptions,
    Filename,
)


# This will be a quick end-to-end tour through Panda3D, the ends being the
# scenery to be rendered on one side, and the graphics API on the other. We will
# start at the latter and build towards the former, and then switch over to the
# former and let the pieces meet up in the middle. And yes, there is method to
# this madness.
# Also, this is a kind if "ShowBase under the hood", for a small selection of
# what ShowBase does.


# First, we need to know what graphics pipelines (OpenGL, DirectX, Vulkan, etc.)
# are available on the system.
selection = GraphicsPipeSelection.getGlobalPtr()
# NOTES
#   Some methods of interest:
#     selection.print_pipe_types()
#     selection.get_num_pipe_types()
#     selection.get_pipe_types()
#     selection.get_pipe_type(0)

# Then we need to create an instance of at least one. It is possible to create
# one instance of each.
# A pipeline is an abstraction of the OS' windowing system and graphics API.
# Which pipeline is the default one is set in Config.prc and accessed
# transparently here.
pipe = selection.make_default_pipe()
# NOTES
#   Pipelines of non-default type can be made like this:
#     selection.make_module_pipe('pandagl')
#   It should be possible to create more than one instance of one pipe.
#     Use case: Multiple X11 display servers
#   More methods of interest:
#     pipe.get_type().get_name()
#     pipe.get_interface_name()

# Now we need a window to draw to, for which we need the graphics engine. It is
# a factory for graphics outputs (both visible and invisible framebuffers, and
# the windows that are used to display the former; n.b.: There's the
# intermediate step of the drawing region, explained later), and used to manage
# the process of rendering, which means iterating over all buffers (display
# regions) and rendering them. As such, it also manages the threading model used
# for rendering.
graphics_engine = GraphicsEngine()
# NOTES
#   The graphics engine is typically a singleton:
#     graphics_engine = GraphicsEngine.getGlobalPtr()

# So, let's create a window! This will also create a few things implicitly:
# * A framebuffer. This is a set of images stored in memory, each consisting of
#   a set of channels; red, green, blue, transparency, depth, and so on. By
#   default, a window's framebuffer will have two images, the front buffer and
#   the back buffer. The Why of this will be explained below, after rendering
#   the frame.
# * A graphics state guardian (GSG), which is the abstraction of the graphics
#   API. Panda3D will "draw" to the GSG, and it in turn will issue the actual
#   draw commands to the driver, and transmit resources like meshes, textures,
#   and shaders to it. For that, the GSG needs prepared graphics objects (PGO),
#   which are resources that have been processed for the GPU's consumption. More
#   on that in the rendering section as well.
#   Several buffers can share the same GSG (by passing it as an additioanl
#   argument to graphics_engine.make_output()), and thus the same PGOs,
#   resulting in an efficient reuse of resources. The only reason to use several
#   GSGs is when you absolutely, positively, need to isolate graphics resources
#   from each other, for instance when writing to GSGs from different threads.
fbprops = FrameBufferProperties.getDefault()
wprops = WindowProperties.getDefault()
flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BFRequireWindow
sort = 0
window = graphics_engine.make_output(pipe, "name", sort, fbprops, wprops, flags)
# NOTES
#   graphics_engine.make_buffer() is a syntactic sugar for .make_output() that
#     you give an already existing output to, so that as many resources as
#     possible are shared automatically (i.e. the GSG), and the same framebuffer
#     properties are applied. .make_parasite() is similarly syntactic sugar.
#   Outputs can be set active or inactive, which controls whether they will be
#     refreshed when the frame is rendered. There's a convenience method that
#     makes them active only for the next frame.

# And now for something completely different: The scene graph.
# The scene graph is a directed acyclic graph where each node is related to its
# parent by a transformation, consisting of translation, rotation, and scale.
# Nodes may contain models or cameras, or be there just for the purpose of
# organizing the scene structure to make it easier to work with. Each node may
# also a whole plethora of render attributes which will affect the whole subtree
# below it as well, unless overridden in a part of that subtree.
# Any structure of nodes is a scene graph. While not strictly necessary,
# we'll use an otherwise empty node as the root of the scene graph that we will
# use.
scene_graph = NodePath("scene graph root")
# NOTE
#   Since the scene graph is a DAG, and not a tree, there may be multiple paths
#     from the tree's root to any given node. Since on these paths, different
#     transformations may be applied and different attributes may be set, there
#     may be several ways for a node to be rendered. To disambiguate them,
#     NodePaths represent the individual paths from root to node.
# FIXME
#   Is that correct?
#   Can I exemplify it? (see manual)
#   Since I create the root node here, why don't I use a PandaNode instead?

# To get anything visibly rendered, we need a camera in the scene graph. We also
# need to adjust its lens, so that the camera "records" the scene graph in the
# aspect ratio that its output will be displayed in.
camera = Camera("camera")
cam_node_path = scene_graph.attach_new_node(camera)
camera.get_lens().set_aspect_ratio(
    float(window.get_x_size()) /
    float(window.get_y_size())
)
# NOTES
#   The camera has only "by coincidence" the right lens type by default.
#     lens = PerspectiveLens()
#     camera.set_lens(lens)
#   camera = self.render.attachNewNode(ModelNode('camera'))
#   camera.node().setPreserveTransform(ModelNode.PTLocal)

# For purposes of rendering something interesting, and seeing that we have
# indeed set up everything correctly, we need to add a model to the scene and
# place it in front of the camera, so that we have something to actually look
# at.
# When assets are loaded, they are stored in resource pools, which are
# singletons that are created implicitly when used. Most pools store them only
# temporarily, until the resource is uploaded to VRAM, at which point it is
# removed from RAM. A reference to the file is retained, however, so that it
# can be reloaded, should it be removed from VRAM, but later is needed again.
loader = Loader.getGlobalPtr()
loader_options = LoaderOptions()
model = loader.load_sync(Filename("models/smiley"), loader_options)
model_node = NodePath(model)
model_node.reparent_to(scene_graph)
model_node.set_pos(0, 10, 0)

# And now we link scene graph and window together by creating a display region.
# A display region is simply the area of a window (or, more specifically, of a
# framebuffer) that a camera draws to. A window can have multiple display
# regions, arranged and stacked in arbitrary ways; they are merely mappings. By
# default, it covers the complete window area that the window has at the time
# that the display area is created. If the window size changes later on, the
# display region (and the underlying framebuffer) will have to be updated.
display_region = window.make_display_region()
display_region.set_camera(cam_node_path)
# NOTES
#   Currently, windows are created with a default display region, which is
#     probably just a hack. It shouldn't exist.
#   Even more methods of interest:
#     display_region.setSort(sort)
#     display_region.setClearDepthActive(1)
#     display_region.setClearColorActive(1)
#     display_region.setClearColor(clearColor)

# With everything in place now, it's time to render the scene.
# To render a frame means that the graphics engine will
# * flip the double-buffer. Rendering writes to the back-buffer, so we're now
#   presenting the results of the last frame's render, and write into the buffer
#   that is *not* displayed anymore. This is done so that drawing happens
#   off-screen, and in this order so as to maximize the time that the GPU has to
#   do the actual graphics generation.
# * step through all windows
# * step through the window's display regions
# * find the root of the scene graph that the display region's camera is in
# * perform culling
# * prepare the resources that are found to be needed, creating PGOs for them.
#   This can be preempted by calling node.prepareScene(gsg), for instance during
#   a loading screen.
# * issue the relevant draw calls to the window's GSG
# With all of this being done, the GPU can now draw the scene into the back-
# buffer without further attention of the CPU, and thus, as far as Panda3D and
# applications built on it are concerned, the frame has been rendered.
graphics_engine.render_frame()

# Now that the frame is stored in the backbuffer, it would be displayed
# automatically when the buffers are flipped again at the beginning of the next
# frame rendering.
# Since we're not in a hurry here, we'll flip the buffer explicitly. This is not
# representative of what Panda3D would or should do in production. If you still
# want it to, you can set "auto-flip true" in Config.prc to make the graphics
# engine flip the buffers after rendering the frame, instead of before it.
graphics_engine.flip_frame()

# TODO
#   Now break it all down again.
#     window.set_active(False)
#     display_region.set_camera(NodePath())
#     cam_node_path.remove_node()
#     window.remove_display_region(display_region)
#     graphics_engine.remove_window(window)
#   Some related experiments and problems
#     wp = WindowProperties.get_default()
#     wp.set_undecorated(True)
#     window.request_properties(wp)
#     graphics_engine.render_frame()
#     # Now the window just vanishes? No rejection of props, or other error?
#     # <rdb> You don't directly modify properties; you "request" properties you
#     #       want to change, and then Panda kindly asks the window manager to
#     #       apply those the next time it gets the opportunity to do so.  If it
#     #       works, it updates get_properties().  If it does not work, it puts
#     #       the rejected properties in get_rejected_properties().
#     window.get_properties().set_title("foo")
#     TypeError: Cannot call WindowProperties.set_title() on a const object.
#     # Am I supposed to copy all other properties by hand into the new props?
