import os
import re

scale = 0.25

def postRender( _read, proxy ):
	read = nuke.toNode(_read)
	read["proxy"].setValue( proxy )
	nuke.delete( nuke.toNode("write_proxy") )
	nuke.delete( nuke.toNode("reformat_proxy") )

	nuke.root()["proxy_type"].setValue(1)
	nuke.root()["proxy_scale"].setValue(scale)

for read in nuke.selectedNodes():
	read["proxy"].setValue("")

	# Nueva ruta creacion
	file = read['file'].value()
	basename = os.path.basename(file)
	ext = basename.split(".")[-1]
	padding = re.search('(#+)|(%\d\d?d)', file)
	padding = padding.group(0) if padding else "" 
	_basename = basename.split( padding )[0]
	proxy_file = os.path.dirname(file) + "/" + _basename + "_proxy_" + padding + ".jpg"
	#---------------------------------

	reformat = nuke.createNode( "Reformat")
	reformat["name"].setValue("reformat_proxy")
	reformat["type"].setValue(2)
	reformat["scale"].setValue(scale)

	write = nuke.createNode( "Write" )
	write["name"].setValue("write_proxy")
	write["file"].setValue(proxy_file)
	write["_jpeg_quality"].setValue(1)
	write["afterRender"].setValue("postRender(\"" + read["name"].value() + "\",\"" + proxy_file + "\")")
	nuke.root().setProxy(False)

	nuke.execute(write,read.firstFrame(),read.lastFrame(),1)

	