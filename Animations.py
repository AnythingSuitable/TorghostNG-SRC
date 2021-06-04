#
# Follow on GitHub : https://github.com/AnythingSuitable
#

import tkinter as tk
import time

def Header_Menu_Animation(app, color):
	
	Header_Frame = tk.Frame(app, background = color)
	Header_Frame.place(relx=0.0 , rely= 0.0 , relheight= 1 ,relwidth= 0 )
	n = 0.0
	while True:
		n += 0.08
		time.sleep(0.024)
		Header_Frame.place(relx=0.0 , rely= 0.0 , relheight= 1 ,relwidth= n )
		Header_Frame.update()
		if n >= 1.0:
			return Header_Frame
			break


def Screen_Changing_Animations(app, ColorFront, ColorBack):
	
	Frame_ = tk.Frame(app, background=ColorBack)
	Frame_.place(relx=0.0 , rely= 0.2 , relheight= 0.8 ,relwidth= 1 )

	Header_Frame = tk.Frame(app, background = ColorFront)
	Header_Frame.place(relx=0.0 , rely= 0.0 , relheight= 0 ,relwidth= 1 )

	n = 0.0
	while True:
		n += 0.08
		time.sleep(0.024)
		Header_Frame.place(relx=0.0 , rely= 0.0 , relheight= n ,relwidth= 1 )
		Header_Frame.update()
		if n >= 1.0:
			#return Header_Frame
			break
	n = 1.0
	while True:
		
		n -= 0.08
		time.sleep(0.024)
		Header_Frame.place(relx=0.0 , rely= 0.0 , relheight= n ,relwidth= 1 )
		Header_Frame.update()
		if n <= 0.4:
			return Header_Frame, Frame_
			break