# game_exporter
Export information from Blender to a json format to process as game information.

## How to use / install
Clone the repository in the Blender addons directory for your system.
Turn on the add-on in Blender user preferences.

## Planned Features:
- Exporting of `objects` including
  - world `transform` (4x4 row or column based matrix)
  - world `position` (1x3 vector)
  - custom `properties` which have name:value format
- Exporting of `paths` which take curves and output a line list
- Exporting of `triggers` or `areas` ??
  - Could be AABB, OOBB, or Sphere
