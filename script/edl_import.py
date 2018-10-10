from timecode import Timecode

frame_rate = "29.97"

edl = "//192.168.10.45/server_01/2018/re-enact/shot_010/assets/cuts.edl"


# crea lista de shots con los timecode
shots = []
_edl = open( edl, "r" )
for e in _edl.readlines():
    if ( "C     " in e ):
        line = e.replace("\n", "").split(" ")
        shots.append(( line[-4], line[-3], line[-2], line[-1] ))
#------------------------------    
dot = nuke.createNode ("Dot")
for shot in shots:

    first = Timecode(frame_rate, shot[2]).frames
    last = Timecode(frame_rate, shot[3]).frames - 1 
    
    
    timeclip = nuke.createNode ("TimeClip")
    timeclip.setInput(0,dot)
    timeclip["first"].setValue(first)
    timeclip["last"].setValue(last)