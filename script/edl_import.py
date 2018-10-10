from timecode import Timecode
import nuke
def edl_create( edl, frameRate ):
    # crea lista de shots con los timecode
    shots = []
    _edl = open( edl, "r" )
    for e in _edl.readlines():
        if ( "C     " in e ):
            line = e.replace("\n", "").split(" ")
            shots.append(( line[-4], line[-3], line[-2], line[-1] ))
    #------------------------------    
    dot = nuke.createNode ("Dot", inpanel=False)
    for shot in shots:
        first = Timecode(frameRate, shot[2]).frames
        last = Timecode(frameRate, shot[3]).frames - 1
        timeclip = nuke.createNode ("TimeClip")
        timeclip.setInput(0,dot)
        timeclip["first"].setValue(first)
        timeclip["last"].setValue(last)

        timeclip.hideControlPanel()

def edlImport():
	### Crea Panel y botones    
	p = nuke.Panel('Collect Files')
	p.addEnumerationPulldown('Frame Rate', "24 29.97")
	p.addClipnameSearch('Edl', '.edl')
	result = p.show()
	#-------------------------------------------

	if result:
	    edl_create( p.value('Edl'), p.value('Frame Rate') )

