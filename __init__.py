bl_info = {
	"name": "Game Exporter",
	"author": "Timmy Sjöstedt",
	"category": "Import-Export"
}

if "bpy" in locals():
	import imp
	if "game_exporter" in locals():
		imp.reload(game_exporter)

import bpy
from bpy.props import EnumProperty
from bpy_extras.io_utils import ExportHelper, axis_conversion

class GameExporter(bpy.types.Operator, ExportHelper):
	bl_idname = "export_game.json"
	bl_label = "Export Game Data"
	filename_ext = ".gmon"

	matrix_order = EnumProperty(
		items=[
			("column", "Column Major", "Column Major"),
			("row", "Row Major", "Row Major"),
		],
		name="Matrix Order",
		description="The order matrices will be exported as",
		default="column",
	)

	def axes(axis):
		return [
			("X", "X {}".format(axis), "X {}".format(axis)),
			("-X", "-X {}".format(axis), "-X {}".format(axis)),
			("Y", "Y {}".format(axis), "Y {}".format(axis)),
			("-Y", "-Y {}".format(axis), "-Y {}".format(axis)),
			("Z", "Z {}".format(axis), "Z {}".format(axis)),
			("-Z", "-Z {}".format(axis), "-Z {}".format(axis)),
		]

	forward_axis = EnumProperty(
		items=axes("Forward"),
		name="Forward Vector",
		description="The forward vector of your desired coordinate space",
		default="-Z",
	)
	up_axis = EnumProperty(
		items=axes("Up"),
		name="Up Vector",
		description="The up vector of your desired coordinate space",
		default="Y",
	)

	def execute(self, context):
		from . import game_exporter
		keywords = self.as_keywords(ignore=("check_existing", "matrix_order", "forward_axis", "up_axis"))
		keywords.update({
			"matrices_as_column_major": "column" == self.matrix_order,
			"global_matrix": axis_conversion(to_up=self.up_axis, to_forward=self.forward_axis).to_4x4()
		})
		return game_exporter.save(context, **keywords)

def add_export_menu_item(self, context):
	self.layout.operator(
		GameExporter.bl_idname,
		text="Game Data ({})".format(GameExporter.filename_ext)
	)

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(add_export_menu_item)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(add_export_menu_item)

if __name__ == "__main__":
	register()
