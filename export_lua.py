

bl_info = {
	"name": "Export LUA format",
	"author": "Kenny Pang (pke1029)",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"location": "File > Import-Export",
	"description": "Export mesh data to Lua format",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"}


def f2s(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')


import bpy
from bpy_extras.io_utils import (ExportHelper)


class ExportLUA(bpy.types.Operator, ExportHelper):
	"""Save a Wavefront LUA File"""

	bl_idname = "export_scene.lua"
	bl_label = "Export LUA"

	filename_ext = ".lua"

	def execute(self, context):
		filepath = self.filepath
		f = open(filepath, 'w')
		obj = context.selected_objects[0]
		f.write(obj.name + ' = {\n')
		mesh = obj.data
		
		# vertices
		verts = "\tverts = {"
		mesh_verts = mesh.vertices[:]
		for v in mesh_verts:
			# verts += '{%.3f,%.3f,%.3f},' % (v.co[1], v.co[2], v.co[0])
			verts += '{' + f2s(v.co[1]) + ',' + f2s(v.co[2]) + ',' + f2s(v.co[0]) + '},'
		verts += "},\n"
		f.write(verts)

		# faces
		faces = "\tfaces = {"
		mesh_faces = mesh.polygons[:]
		for p in mesh_faces:
			faces += '{' + ','.join(str(i+1) for i in p.vertices) + '},'
		faces += "},\n"
		f.write(faces)

		# colors
		cols = "\tcols = {"
		materials = obj.material_slots
		for c in materials:
			cols += '{%.4f,%.4f,%.4f},' % c.material.node_tree.nodes.active.outputs[0].default_value[0:3]
		cols += "},\n"
		f.write(cols)

		# face colors
		fcols = '\tfcols = {' + ','.join(str(p.material_index+1) for p in mesh_faces) + '},\n'
		f.write(fcols)

		f.write('}')
		f.close()
		return {'FINISHED'}


def register():
	bpy.utils.register_class(ExportLUA)
	bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
	bpy.utils.unregister_class(ExportLUA)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func)


def menu_func(self, context):
	self.layout.operator(ExportLUA.bl_idname, icon='MESH_CUBE')

