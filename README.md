# Blender addon for exporting to LUA syntax 

An addon for Blender to export meshes and materials to Lua format

## Format
Format follows a similar structure as a Wavefront OBJ file: 
```
Cube = {
    verts = {{0,0,0},{0,0,1},{0,1,0},...},
    faces = {{1,5,7,3},{4,3,7,8},...},
    cols = {{175,187,227}},
    fcols = {1,1,1,1,1,1},
}
```

## Installation
Download `export_lua.py`. In Blender, go to `Edit > Preference > Addon > Install` and choose `export_lua.py`. Tick the checkbox in the addon pannel to activate it. The option for exporting to LUA is located in `File > Export > Export LUA`. 
