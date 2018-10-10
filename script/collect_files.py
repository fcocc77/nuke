import nuke
import os
import time
import shutil
import re
import fnmatch  
import thread

class collect_files():
	def __init__(self):

		### Crea Panel y botones	
		p = nuke.Panel('Collect Files')

		p.addEnumerationPulldown('Action', "Copy Move")
		result = p.show()

		self.move = p.value('Action')
		#-------------------------------------------

		self.task = nuke.ProgressTask("CollectFiles")
		script_dir=os.path.dirname(nuke.root().name())
		self.project_dir= os.path.dirname(os.path.dirname(script_dir))

		if result:
			thread.start_new_thread(self.collect, ())

	def collect(self):

		### Cuenta todos los archivos que se van a copiar, es necesarion para calcular el porcentaje de progreso      
		box_file=['file','proxy']
		count_total=0

		for node in nuke.selectedNodes():        
			for box in box_file:
				try:
					file_path = node[box].value()
					self.fila_path_modify(file_path)
					count_total = len(self.sequence_find)+count_total		
				except:pass
		#------------------------------------------------------------------------

		#------------------------------------------------------
		count_left=0
		for node in nuke.selectedNodes():           
			for box in box_file:

				try:
					file_path = node[box].value()
					self.fila_path_modify(file_path)

					if not os.path.isdir(self.dst_dir):
						os.makedirs(self.dst_dir)

					for files in self.sequence_find:

						# imprime porcentage a la barra de progreso
						count_left=count_left+1
						porcent = (count_left*100)/count_total

						self.task.setProgress(porcent)
						self.task.setMessage("Collecting file:   " + files)
						#---------------------------------------------------

						# si el archivo esta dentro de las carpetas del projecto no lo copia
						if self.action==1:

							src=self.src_dir+"/"+files
							dst=self.dst_dir+"/"+files

							try:
								if self.move =="Move":
									shutil.move(src,dst)
								else:
									shutil.copy(src,dst)
							except:
								pass
						#-------------------------------------------------------------------------

						if self.task.isCancelled():
							break                            
							del self.task

					if not self.task.isCancelled():
						### Agrega el nombre de root a los nodos
						print self.dst_box
						node[box].setValue(self.dst_box)
						#------------------------------------- 
				except:
					pass

			if self.task.isCancelled():
				break                            
				del self.task

	def fila_path_modify(self,file_path):

		rootname = "[file dirname [value root.name]]/../.."

		assets_dir=self.project_dir+"/"+"assets"
		file=file_path.split("/")[-1]

		# Padding y extension
		padding = re.search('(#+)|(%\d\d?d)', file_path)
		padding = padding.group(0) if padding else "" 
		extencion = file_path.split(".")[-1]
		pad_ext = padding+"."+extencion
		#-----------------------------------------------

		base_name = file.replace(pad_ext, "")
		self.src_dir=os.path.dirname(file_path)
		name_folder=os.path.basename(self.src_dir)
		self.dst_dir = assets_dir+"/"+name_folder

		self.sequence_find = sorted(fnmatch.filter(os.listdir(self.src_dir), base_name+"*"))

		self.action=1

		self.dst_box=rootname+"/assets/"+name_folder+"/"+file

		# si el archivo esta dentro de las carpetas
 		if os.path.normpath(self.project_dir) in os.path.normpath(self.src_dir):

 			# crea ruta internas del projecto
			inside_file=file_path.replace(self.project_dir,"")		
			inside_path=inside_file.replace(file,"")[:-1]
			inside_path_dir= file_path.replace(inside_file,"")[:-1]
			#------------------------------------------------------

			self.dst_box=rootname+inside_file
			self.action=0
		#-------------------------------------------------------------

