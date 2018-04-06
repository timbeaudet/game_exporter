bl_info = {
	"name": "Game Exporter",
	"author": "Timmy Sjöstedt",
	"category": "Import-Export"
}

import bpy
from bpy_extras.io_utils import ExportHelper

class GameExporter(bpy.types.Operator, ExportHelper):
	bl_idname = "export_game.json"
	bl_label = "Export Game Data"
	filename_ext = ".game.json"

	def execute(self, context):
		return {"FINISHED"}

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
