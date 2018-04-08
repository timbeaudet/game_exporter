import bpy
import json

serialise_matrices_as_column_major = None

def serialize_vector3(vector):
	return (vector[0], vector[1], vector[2])

def serialize_matrix4(matrix):
	mtrx_data = getattr(matrix, "col" if serialise_matrices_as_column_major else "row")

	return (
		mtrx_data[0][0], mtrx_data[0][1], mtrx_data[0][2], mtrx_data[0][3],
		mtrx_data[1][0], mtrx_data[1][1], mtrx_data[1][2], mtrx_data[1][3],
		mtrx_data[2][0], mtrx_data[2][1], mtrx_data[2][2], mtrx_data[2][3],
		mtrx_data[3][0], mtrx_data[3][1], mtrx_data[3][2], mtrx_data[3][3],
	)

def save(context,
		filepath,
		matrices_as_column_major=True,
		):

	global serialise_matrices_as_column_major
	serialise_matrices_as_column_major = matrices_as_column_major

	from mathutils import Quaternion

	scene = context.scene
	world = context.scene.world

	objects_empty = [obj for obj in scene.objects if obj.is_visible(scene) and "EMPTY" == obj.type]
	objects_curve = [obj for obj in scene.objects if obj.is_visible(scene) and "CURVE" == obj.type]

	json_out = {
		"matrices_as_column_major": matrices_as_column_major,
		"objects": [],
		"paths": [],
		"trigger_areas": [],
	}

	for o in objects_empty:
		obj_size = o.empty_draw_size
		obj_scale = o.matrix_world.to_scale()

		size_vector = obj_size * obj_scale

		objdata = {
			"name": o.name,
			"type": o.empty_draw_type,
			"transform": serialize_matrix4(o.matrix_world),
			"position": serialize_vector3(o.matrix_world.to_translation()),
			"size": serialize_vector3(size_vector),
			"properties": {k:v for k,v in o.items()[1:]},
		}

		if o.empty_draw_type in ["SPHERE","CUBE"]:
			list_to_add_to = "trigger_areas"

			if "CUBE" == o.empty_draw_type:
				has_rotation = Quaternion((1, 0, 0, 0)) != o.matrix_world.to_quaternion()

				objdata["type"] = "OOBB" if has_rotation else "AABB"

		else:
			list_to_add_to = "objects"

		json_out[list_to_add_to].append(objdata)

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
