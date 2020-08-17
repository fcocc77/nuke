#!/usr/bin/python
import os
import shutil
from sys import platform

path = os.path.dirname(os.path.abspath(__file__))


class gizmos_setup():
    def __init__(self, action):

        # Versiones de Nuke
        nuke_versions = ['Nuke9.0v9', 'Nuke10.5v8']

        for nv in nuke_versions:
            if platform == "win32":
                self.plugins = "C:/Program Files/"+nv+"/plugins/"
            if platform == "linux2":
                self.plugins = "/usr/local/"+nv+"/plugins/"

            self.menu = self.plugins+"menu.py"
            self.gizmos_src = path+"/gizmos/"
            self.icon_src = path+"/icons/"
            self.gizmos = os.listdir(self.gizmos_src)
            self.icons = os.listdir(self.icon_src)

            if os.path.isfile(self.menu):
                if action:
                    self.install()
                else:
                    self.uninstall()

    def install(self):

        # lee el menu_jc
        script_list = []
        menu_jc = open(path+"/menu/menu_jc.py", "r")
        for l in menu_jc.readlines():
            l = l.rstrip('\n')
            script_list.append((l))
        menu_jc.close()
        # -------------------------------------

        # crea lista de menus a partir de los gizmos que hay en la carpeta gizmos
        m1 = '# j_gizmos_start'
        m2 = 'menubar=nuke.menu("Nodes")'
        m3 = 'm=menubar.addMenu(("Gizmos"), icon="Gizmos-JC.png")'

        menu_list = [m1, m2, m3, ""]

        list = os.listdir(self.gizmos_src)
        for l in list:
            name_gizmo = l.split(".")[0]

            add_menu = 'm.addCommand("' + name_gizmo+'", "nuke.createNode (' + \
                "'" + name_gizmo+".nk"+"'" + ')", icon="Gizmo-JC.png")'
            menu_list.append((add_menu))

        for l in script_list:
            menu_list.append((l))

        menu_list.append("# j_gizmos_end")
        # ---------------------------------------------------------------------------

        # agrega la lista creada al final de archivo menu.py del nuke
        files = open(self.menu, 'a')
        for w in menu_list:

            files.write(w+'\n')
        files.close()
        # --------------------------------------------------------------

        # copia los .nk al la carpeta de nuke
        for g in self.gizmos:
            if not os.path.isfile(self.plugins+g):

                src = self.gizmos_src+g
                shutil.copy(src, self.plugins)
                print "installing...   "+g
        # --------------------------------------------------------------

        # copia los icono al la carpeta de nuke
        for i in self.icons:
            if not os.path.isfile(self.plugins+"icons/"+i):

                src = self.icon_src+i
                shutil.copy(src, self.plugins+"icons")
                print "installing...   "+i
        # --------------------------------------------------------------

        # copia script y menu
        for l in os.listdir(path+"/script"):
            src = path+"/script/"+l
            dst = self.plugins+l
            shutil.copy(src, dst)

        # ---------------------------------------------

    def uninstall(self):

        # lee el archivo menu.py original y crea una lista sin los archivos del menu.py del origen
        files = open(self.menu, 'r')
        menu_list = []
        delete = 0
        for f in files.readlines():

            f = f.rstrip('\n')

            start = "# j_gizmos_start"
            if f == start:
                delete = 1

            end = "# j_gizmos_end"
            if f == end:
                delete = 0

            if not f == end:
                if delete == 0:
                    menu_list.append((f))
        files.close()
        # ---------------------------------------------------------------------------------------------

        # escribe la lista creada anteriormente al archivo menu.py original
        files = open(self.menu, 'w')
        for w in menu_list:

            files.write(w+'\n')
        files.close()
        # ------------------------------------------------------------------

        # borra los gizmos de la carpeta de nuke
        for g in self.gizmos:
            dst = self.plugins+g
            if os.path.isfile(dst):
                os.remove(dst)
                print "deleting...    "+g
        # -----------------------------------------

        # borra los iconos de la carpeta de nuke
        for i in self.icons:
            dst = self.plugins+"icons/"+i
            if os.path.isfile(dst):
                os.remove(dst)
                print "deleting...    "+i
        # -----------------------------------------

        # borra los script de la carpeta de nuke
        script = os.listdir(path+"/script")
        for s in script:
            dst = self.plugins+"/"+s

            if os.path.isfile(dst):
                os.remove(dst)
                print "deleting...    "+s
        # -----------------------------------------


gizmos_setup(1)
