import os
import re
import fnmatch  
import nuke
import time
import thread

class reduceProject():
	def __init__(self):

		if nuke.ask('Reduce Project... \nAre you sure you want to erase the files permanently?'):

			self.task = nuke.ProgressTask("Reducing Project...")
			thread.start_new_thread(self.reduce, ())

	def reduce(self):

		dirname="[file dirname [value root.name]]/../.."
		projectDir= os.path.dirname(os.path.dirname(os.path.dirname(nuke.root().name())))

		script_list=[]

		for node in nuke.allNodes():
			if node.Class() =="Group":

				node.begin()

				for n in nuke.allNodes():
					if n.Class() =="Group":
						node.begin()
						for n2 in nuke.allNodes():
							try:
								file=n2["file"].value()
								script_list.append(file)
							except:pass		
						node.end()

					else:
						try:
							file=n["file"].value()
							script_list.append(file)
						except:pass
				node.end()

			else:

				try:
					file=node["file"].value()
					script_list.append(file)
				except:pass

		project_list=[]
		for folder in ["/assets","/footage"]:
			for root, dir, file in os.walk(projectDir+folder):
				for f in file:
					project_list.append(root+"/"+f)

		script_list_project=[]
		for f in script_list:
			try:
				f=f.replace(dirname,projectDir)
				padding = re.search('(#+)|(%\d\d?d)', f)
				padding = padding.group(0) if padding else ""

				f=f.split(padding)[0]

				base_name=os.path.basename(f)
				base_path=os.path.dirname(f)

				sequence_find = sorted(fnmatch.filter(os.listdir(base_path), base_name+"*"))

				for name in sequence_find:
					final_file=base_path+"/"+name
					script_list_project.append(final_file)
			except:
				script_list_project.append(f)

		remove_list=[]

		for f in project_list:
			if not f in script_list_project:
				remove_list.append(f)

		count_total=len(remove_list)
		count_left=0
		for f in remove_list:
			if os.path.isfile(f):

				# imprime porcentage a la barra de progreso
				count_left=count_left+1
				porcent = (count_left*100)/count_total

				self.task.setProgress(porcent)
				self.task.setMessage("Erasing file:   " + f)
				#---------------------------------------------------

				if self.task.isCancelled():
					break                            
					del self.task

				os.remove(f)

		for dir, subdirs, files in os.walk(projectDir):
			if len(os.listdir(dir)) == 0: 
				os.rmdir(dir)

