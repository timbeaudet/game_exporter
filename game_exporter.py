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

	objects_empty = [obj for obj in scene.objects if obj.is_visible(scene) and "EMPTY" == obj.type]
	objects_curve = [obj for obj in scene.objects if obj.is_visible(scene) and "CURVE" == obj.type]

	json_out = {
		"objects": [],
		"paths": [],
	}

	for o in objects_empty:
		objdata = {
			"name": o.name,
			"type": o.empty_draw_type,
			"size": o.empty_draw_size,
			"transform": serialize_matrix4(o.matrix_world),
			"position": serialize_vector3(o.matrix_world.to_translation()),
			"properties": {k:v for k,v in o.items()[1:]},
		}

		json_out["objects"].append(objdata)

	for o in objects_curve:
		curve_type = o.data.splines.active.type

		points = []
		if "BEZIER" == curve_type:
			for _, point in o.data.splines.active.bezier_points.items():
				points.append({
					"position": serialize_vector3(point.co),
					"handle_left": serialize_vector3(point.handle_left),
					"handle_right": serialize_vector3(point.handle_right),
				})
		else:
			for _, point in o.data.splines.active.points.items():
				points.append({"position": serialize_vector3(point.co)})

		objdata = {
			"name": o.name,
			"type": o.data.splines.active.type,
			"properties": {k:v for k,v in o.items()[1:]},
			"points": points,
		}

		json_out["paths"].append(objdata)

	with open(filepath, "w", encoding="utf-8") as file:
		file.write(json.dumps(json_out, sort_keys=True, indent=4, separators=(',', ': ')))

	return {"FINISHED"}
