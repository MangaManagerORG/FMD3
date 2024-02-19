# """ AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()
#
# Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
# Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md
#
# """
# import sys
# import time
# try:
# 	import Tkinter as tk  # for Python2
# except ImportError:
# 	import tkinter as tk  # for Python3
#
# from PIL import Image, ImageTk
# class AnimatedGif(tk.Toplevel):
# 	"""
# 	Class to show animated GIF file in a label
# 	Use start() method to begin animation, and set the stop flag to stop it
# 	"""
# 	def __init__(self, parent, gif_file, delay=0.04):
# 		"""
# 		:param root: tk.parent
# 		:param gif_file: filename (and path) of animated gif
# 		:param delay: delay between frames in the gif animation (float)
# 		"""
# 		tk.Toplevel.__init__(self, parent,height=295,width=295)
# 		self.attributes('-alpha',0.2)
# 		self.root = parent
# 		self.gif_file = gif_file
# 		self.delay = delay  # Animation delay - try low floats, like 0.04 (depends on the gif in question)
# 		self.stop_ = False  # Thread exit request flag
# 		self._num = 0
# 		self.overrideredirect(True)
# 		self.canvas = tk.Canvas(self, height=295,width=295)
# 		self.canvas.pack()
#
#
#
# 		# Load gif
# 		self.image = image1 = Image.open(gif_file)
# 		self.total_frames = image1.n_frames
# 		self.animation = []
# 		for x in range(image1.n_frames):
# 			frame = ImageTk.PhotoImage(image1.copy())
# 			self.animation.append(frame)
# 			image1.seek(x)
#
# 		self.image_container = None
# 		self.image.close()
# 		win = self
# 		parent.update_idletasks()
# 		width = win.winfo_width()
# 		height = win.winfo_height()
# 		x = (parent.winfo_rootx() + parent.winfo_width() // 2) - (width // 2)
# 		y = (parent.winfo_rooty() + parent.winfo_height() // 2) - (height // 2)
# 		win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
#
# 		self.withdraw()
#
# 	def show(self):
# 		self.start()
# 		self.deiconify()
#
# 	def hide(self):
# 		self.withdraw()
# 		self.stop()
#
# 	def start(self):
# 		""" Starts non-threaded version that we need to manually update() """
# 		self.gif = ImageTk.PhotoImage(file=self.gif_file, format='gif -index 0')
# 		self.image_container = self.canvas.create_image(0,0,anchor=tk.NW, image=self.gif)
#
# 		self.start_time = time.time()  # Starting timer
# 		self._animate(0)
#
# 	def stop(self):
# 		""" This stops the after loop that runs the animation, if we are using the after() approach """
# 		self.stop_ = True
#
# 	def _animate(self,index):
# 		frame = self.animation[index]
# 		self.canvas.itemconfig(self.image_container,image=frame)
#
# 		index += 1
# 		if index == self.total_frames:
# 			index = 0
# 		if not self.stop_:
# 			self.canvas.after(int(self.delay*1000), self._animate, index)
#
# if __name__ == '__main__':
# 	a = AnimatedGif(None,r"C:\Users\galla\PycharmProjects\FMD3\src\FMD3_Tkinter\assets\loading.gif")
# 	a.mainloop()