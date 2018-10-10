import collect_files
import card_to_track
import reduce_project
import edl_import

menuBar = nuke.menu("Nuke")
menuBar.addCommand('J_Script/CollectFiles...', 'collect_files.collect_files()', 'Ctrl+F')
menuBar.addCommand('J_Script/Project Reduce.', 'reduce_project.reduceProject()', 'Ctrl+D')
menuBar.addCommand('J_Script/CardtoTrack','card_to_track.corn3D()',icon="Camera.png")
menuBar.addCommand('J_Script/Edl Import', 'edl_import.edlImport()')

import autosave_backup
autosave_backup.start_subprocess()
