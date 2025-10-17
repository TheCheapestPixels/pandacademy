Scene Graph Deep Dive
=====================

* Scene graphs are our tool to arrange objects in 3D space.
  * There can be several scene graphs
* Render (and other) attributes are inherited downwards.
* There are also non-graphical node types.


Scene Graph Basics
------------------

* PandaNodes (and subtypes) vs. NodePaths
* Creating hierarchies
* Instancing


NodePath States
---------------

### `TransformState`

The spatial transformation between a NodePath and its parent, expressed
as a 4x4 matrix.

* `get_transform()` returns the `TransformState`, which allows for
  direct inspection and manipulation of the matrix.
* Transforms (and the NodePaths using them) have syntactical sugar:
  * `get_pos`
  * `get_hpr`
  * `get_shear`
  * `get_scale`
* `get_net_transform()` returns the transformation from the root of the
  scene graph to the node.
* NodePaths also store the previous frame's TransformState.


### `RenderState`

* [List of all attributes](https://docs.panda3d.org/1.10/python/programming/render-attributes/list-of-all-attributes)
* NodePath has methods that correspond to arrtibutes to make working
  with them easy. E.g.: `np.setAntialias(AntialiasAttrib.MAuto)`
* Camera-managed RenderState (`camera.initial_state` and tagged nodes)
* `Attrib.make(mode, args)`
* `np.get_net_state()`

```python
from panda3d.core import CullFaceAttrib

from direct.showbase.ShowBase import ShowBase


ShowBase()
rs = base.render.get_state()
cfa = rs.get_attrib(CullFaceAttrib)
print(f"Does render cull clockwise faces? {cfa.mode == CullFaceAttrib.M_cull_clockwise}")
```

Programmatic list of all `RenderAttrib`s:
```python
from panda3d.core import TypeRegistry, TypeHandle


ra_type = TypeRegistry.ptr().find_type('RenderAttrib')
TypeHandle.get_num_child_classes(ra_type)
for idx in range(TypeHandle.get_num_child_classes(ra_type)):
    print(TypeHandle.get_child_class(ra_type, idx))
```
FIXME: This registry is more specific: https://docs.panda3d.org/1.10/cpp/reference/panda3d.core.RenderAttribRegistry

FIXME: Now set to backface culling.


### SamplerState

Deals with how textures are sampled.

https://docs.panda3d.org/1.10/python/reference/panda3d.core.SamplerState
