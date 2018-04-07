import bpy
import json

def serialize_vector3(vector):
	return (vector[0], vector[1], vector[2])

def serialize_matrix4(matrix):
	return (
		matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
		matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
		matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
		matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3],
	)

def save(context,
		filepath,
		):

	scene = context.scene
	world = context.scene.world

	objects = [obj for obj in scene.objects if obj.is_visible(scene)]

	json_out = {
		"objects": [],
	}

	for o in objects:
		objdata = {
			"name": o.name,
			"type": o.type,
			"transform": serialize_matrix4(o.matrix_world),
			"position": serialize_vector3(o.matrix_world.to_translation()),
		}

		if "EMPTY" == o.type:
			objdata.update({
				"empty_type": o.empty_draw_type,
				"empty_size": o.empty_draw_size,
			})

		json_out["objects"].append(objdata)

	with open(filepath, "w", encoding="utf-8") as file:
		file.write(json.dumps(json_out, sort_keys=True, indent=4, separators=(',', ': ')))

	return {"FINISHED"}
