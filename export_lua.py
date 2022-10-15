

bl_info = {
	"name": "Export LUA format",
	"author": "Kenny Pang (pke1029)",
	"version": (0, 0, 2),
	"blender": (2, 80, 0),
	"location": "File > Import-Export",
	"description": "Export mesh data to Lua format",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"}


# TODO
# export scene/selected object
# export uvs, face normals
# bake texture
# smart materials (choose between texture or flat color)


def float2string(x, p):
    return ('%.*f' % (p, x)).rstrip('0').rstrip('.')


def write_verts(obj, p=2):
	faces = obj.mesh.polygons[:]
	l = "\tverts = {"
	for v in verts:
		v = [v.co[1], v.co[2], v.co[0]]
		l += '{' + ','.join(float2string(i, p) for i in v) + '},'
	l += "},\n"
	return l


def write_faces(obj):
	faces = obj.mesh.polygons[:]
	l = "\tfaces = {"
	for f in faces:
		l += '{' + ','.join(str(i+1) for i in f.vertices) + '},'
	l += "},\n"
	return l


def write_cols(obj):
	l = "\tcols = {"
	materials = [i.material for i in obj.material_slots]
	for mat in materials:
		nodes = [i.type for i in mat.node_tree.nodes]
		if 'RGB' in nodes:
			c = mat.node_tree.nodes['RGB'].outputs[0].default_value[0:3]
		elif 'EMISSION' in nodes:
			c = mat.node_tree.nodes['EMISSION'].inputs[0].default_value[0:3]
		else:
			c = (0.0, 0.0, 0.0)
		rgb = tuple(round(255*i**(1.0/2.2)) for i in c) 
		l += '{%d,%d,%d},' % rgb
	l += "},\n"
	return l


def write_fcols(obj):
	faces = obj.mesh.polygons[:]
	l = '\tfcols = {' + ','.join(str(f.material_index+1) for f in faces) + '},\n'
	return l


def write_fcenters(obj, p=2):
	faces = obj.mesh.polygons[:]
	l = "\tfcenters = {" 
	for f in faces:
		v = [f.center[1], f.center[2], f.center[0]]
		l += '{' + ','.join(float2string(i, p) for i in v) + '},'
	l += "},\n"
	return l


def write_fnormals(obj, p=2):
	faces = obj.mesh.polygons[:]
	l = "\tfnormals = {" 
	for f in faces:
		v = [f.normal[1], f.normal[2], f.normal[0]]
		l += '{' + ','.join(float2string(i, p) for i in v) + '},'
	l += "},\n"
	return l


def write_uvs(obj):
	mesh = obj.data
	


import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty, IntProperty


class ExportLUA(bpy.types.Operator, ExportHelper):
	"""Save a LUA File"""

	bl_idname = "export_scene.lua"
	bl_label = "Export LUA"

	filename_ext = ".lua"

	use_selection: BoolProperty(name="Selection Only", description="Export selected objects only", default=True)
	precision: IntProperty(name="Precision", description="Precision for floating point values", default=2, min=1, max=6)

	def execute(self, context):
		filepath = self.filepath
		f = open(filepath, 'w')
		fw = f.write

		obj = context.selected_objects[0]
		fw(obj.name + ' = {\n')

		fw(write_verts(obj, p=self.precision))
		fw(write_faces(obj))
		fw(write_cols(obj))
		fw(write_fcols(obj))
		
		fw('}')
		f.close()
		return {'FINISHED'}

	# def draw(self, context):
		# pass


def register():
	bpy.utils.register_class(ExportLUA)
	bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
	bpy.utils.unregister_class(ExportLUA)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func)


def menu_func(self, context):
	self.layout.operator(ExportLUA.bl_idname, icon='MESH_CUBE')

