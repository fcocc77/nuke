## copiar las siguientes lineas en init.py

## import autosave_backup
## autosave_backup.start_subprocess()

import thread
import nuke
import os
import time

def autosave_backup():
    munutes = 10

    while(1):

        project = nuke.root().knob( 'name' ).value() ### ruta y nombre del proyecto abierto
        project_name_ex = project.split("/")[-1]   ### nombre con la extension del proyecto
        project_name = project_name_ex.split(".nk")[0]  ### nombre del proyecyo
        project_path = project.replace(project_name_ex,"")  ### ruta del proyeco
        backup_folder =project_path+"backup"  ### nueva ruta del proyecto

        try:

            if not os.path.isdir(backup_folder):
                os.makedirs(backup_folder)

            version=1

            while(1):### antepone un 0 antes del numero

                if version > 9:
                    ante=""
                else:
                    ante="0"

                ver_number = "backup_"+ante+str(version)

                new_project = project_path+"backup/"+project_name+"_"+ver_number+".nk"
                check_file = os.path.isfile(new_project)  ### chequea si el archivo existe

                try: ### si los proyectos pesan lo mismo, este no guarda la version

                    ver_number2 = "v"+ante+str(version-1)
                    out_project = project_path+"backup/"+project_name+"_"+ver_number2+".nk"

                    in_size = str(os.path.getsize(project)) ### obtiene el peso del archivo
                    out_size = str(os.path.getsize(out_project))

                    in_size = in_size.replace(' ', '')[:-2].upper() ### borra los 2 ultimos digitos
                    out_size = out_size.replace(' ', '')[:-2].upper()

                    if in_size == out_size:
                        break

                except:
                    pass

                if check_file == 0:### si el archivo no exite crea una version
                    nuke.scriptSave(new_project)
                    version=1
                    break
                else:
                    version=version+1
        except:
            pass

        time.sleep(munutes*60)

def start_subprocess():
    thread.start_new_thread(autosave_backup, ())

