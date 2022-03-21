# Blender addon for exporting to LUA syntax 

An addon for Blender to export meshes to Lua format

## Format
Format of the 
```
Cube = {
    verts = {{0,0,0},{0,0,1},{0,1,0}...},
    faces = {},
    cols = {},
    fcols = {},
}
```

## Installation
Download `export_lua.py`. In Blender, go to `Edit > Preference > Addon > Install` and choose `export_lua.py`. Tick the checkbox in the addon pannel to activate it. The option for exporting to LUA is located in `File > Export > Export LUA`. 
