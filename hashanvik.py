#! /usr/bin/env python
from __future__ import division;
import wx
#from wx import *
from wxPython.wx import *
import os
import os.path
import hashlib
import traceback
import math
from wx.lib import *
class TestFrame(wx.Frame):
	

	def __init__(self,parent,id):
		self.fileSelected=0     
		wx.Frame.__init__(self,parent, id, 'Hash AnviK', size=(750,450))
		wx.Frame.SetSizeHints(self,750,450,750,450)
		self.count=0
		self.filename=''
	
		''' set the menu'''

		fileMenu= wx.Menu()

		aboutMenu= fileMenu.Append(wx.ID_ABOUT, "About"," Info about this program")
		exitMenu = fileMenu.Append(wx.ID_EXIT,"Exit"," Close the program")
		

		panel=wx.Panel(self)
		
		self.gauge=wx.Gauge(panel,-1, 1000,(250,350),(200,50) )
		self.gauge.Hide()
		
		# Creating the menubar
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&File") # Adding the "fileMenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		# creating the sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)


		# Creating the labels
		self.label1 = wx.StaticText(panel, -1, "Select a file to compute Hash  ---------------------------------------> " , wx.Point(15, 30))
		self.label2 = wx.StaticText(panel, -1,"",wx.Point(15,60))
		self.label3 = wx.StaticText(panel, -1,"",wx.Point(340,400))
		self.label4 = wx.StaticText(panel, -1,"File Name: ",wx.Point(15,35))
		self.label5 = wx.StaticText(panel, -1,"Path: ",wx.Point(15,95))
		self.label6 = wx.StaticText(panel,-1,"Size:",wx.Point(15,155))
		self.label7 = wx.StaticText(panel,-1,"Hash:",wx.Point(15,215))
		self.label8 = wx.StaticText(panel,-1,"Hash Mode:",wx.Point(600,155))
		self.label9 = wx.StaticText(panel,-1,"",wx.Point(505,280))
		self.label10 = wx.StaticText(panel,-1,"Compare:",wx.Point(15,275))
		
		self.chk_compare = wx.CheckBox(panel,-1,"Compare Hash",pos=(15,350),size=(-1,-1),style=0,name="Compare")
		
		self.chk_compare.Hide()
		self.label4.Hide()
		self.label5.Hide()
		self.label6.Hide()
		self.label7.Hide()
		self.label8.Show()
		self.label9.Hide()
		self.label10.Hide()
		
		# Creating Radio Buttons
		self.md5_rad1 = wx.RadioButton ( panel, -1, 'md5 hash',pos=(600,180),style = wx.RB_GROUP )		
		self.sha1_rad2 = wx.RadioButton ( panel, -1, 'sha1 hash',pos=(600,210) )
		self.sha256_rad3 = wx.RadioButton ( panel, -1, 'sha256 hash',pos=(600,240))


		# Adding rad buttons to the view

		self.sizer.Add(self.md5_rad1, 0, wx.ALL, 5)		
		self.sizer.Add(self.sha1_rad2, 0, wx.ALL, 5)
		self.sizer.Add(self.sha256_rad3, 0, wx.ALL, 5)

		# Adding Textboxes
		self.fileName_txt = wx.TextCtrl ( panel, -1, "", style = wx.TE_READONLY,size=(400,30),pos=(100,30) )
		self.dirName_txt = wx.TextCtrl ( panel, -1, "", style = wx.TE_READONLY,size=(400,30),pos=(100,90) )
		self.size_txt = wx.TextCtrl ( panel, -1, "", style = wx.TE_READONLY,size=(400,30),pos=(100,150) )
		self.Hash_txt = wx.TextCtrl ( panel, -1, "", style = wx.TE_READONLY,size=(400,30),pos=(100,210) )

		self.Compare_Hash_txt = wx.TextCtrl ( panel, -1, "", size=(400,30),pos=(100,270))
		

		# Hiding the Textboxes after creating them
		self.fileName_txt.Hide()
		self.dirName_txt.Hide()
		self.size_txt.Hide()
		self.Hash_txt.Hide()
		self.Compare_Hash_txt.Hide()
		
		self.label10.Hide()
		


		# Binding Menu Events to functions

		self.Bind(wx.EVT_MENU, self.closeWindow, exitMenu)

		self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenu)

		self.dirname=''
		
		# Creating buttons and their position on the screen
		self.openButton=wx.Button(panel, label='Open', pos=(600, 10), size=(90,40))
		self.hashButton=wx.Button(panel, label='Hash it!!',pos=(600, 75), size=(90,40))
		self.hashButton.Disable()


		# Binding Various Events to functions		
		self.Bind(wx.EVT_BUTTON, self.onHash, self.hashButton)               
		self.Bind(wx.EVT_BUTTON, self.OnOpen,self.openButton)
	
		self.Bind(wx.EVT_CLOSE, self.closeWindow)
		
		self.Bind(wx.EVT_CHECKBOX,self.onCheck,self.chk_compare)
		
		self.Bind(wx.EVT_RADIOBUTTON,self.radClick,self.md5_rad1)
		self.Bind(wx.EVT_RADIOBUTTON,self.radClick,self.sha1_rad2)
		self.Bind(wx.EVT_RADIOBUTTON,self.radClick,self.sha256_rad3)
		self.Bind(wx.EVT_TEXT, self.texChange,self.Compare_Hash_txt) 
	
	def texChange(self,event):
		if(self.Hash_txt.GetValue()==self.Compare_Hash_txt.GetValue()):
			self.label9.SetLabel("Match")
			self.label9.Show()
		else:
			self.label9.SetLabel("")
		
	def radClick(self,event):
		self.Hash_txt.SetValue("")
		self.Compare_Hash_txt.Hide()
		self.chk_compare.SetValue(False)
		self.chk_compare.Hide()
		self.label9.Hide()
		self.label9.SetLabel("")
		self.Hash_txt.Hide()
		self.Hash_txt.SetValue("")
		self.label7.Hide()
		self.label10.Hide()
		pass
		
	def onCheck(self,event):
		if(self.chk_compare.GetValue()==True):
			
			self.Compare_Hash_txt.Show()
			self.label10.Show()
			self.label9.SetLabel("")
			self.Compare_Hash_txt.SetValue("")
		else:
			self.Compare_Hash_txt.Hide()
			self.label9.SetLabel("")
			self.label10.Hide()

	def closeButton(self,event):
		self.Close(True)
		pass
	
	def onHash(self, event):
		try:	
			self.gauge.Hide()
			self.hashButton.Disable()
			self.openButton.Disable()
			self.label3.SetLabel("")

			self.Compare_Hash_txt.SetValue("")
			self.Compare_Hash_txt.Hide()
			self.label10.Hide()
			self.chk_compare.SetValue(False)
			self.label9.SetLabel("")
			self.label9.Hide()

			if(self.md5_rad1.GetValue()==True or self.sha256_rad3.GetValue()==True or self.sha1_rad2.GetValue()==True):
				if os.path.exists(TestFrame.filename):
					self.gauge.Show()
				 	if(self.md5_rad1.GetValue()==True):
						block_size=128
					elif(self.sha256_rad3.GetValue()==True):
						block_size=256
					elif(self.sha1_rad2.GetValue()==True):
						block_size=160
					self.hash = TestFrame.hashFunc(self,self.filename,block_size)
					#print self.hash
					
					if(wx.TheClipboard.Open()):
						wx.TheClipboard.SetData(wx.TextDataObject(self.hash))
						wx.TheClipboard.Close()
					
					dialog = wx.MessageDialog(self,"Hash Copied onto Clipboard", "Hash AnviK",wx.OK)
					dialog.ShowModal() # Show it
					dialog.Destroy()
					self.chk_compare.Show()
					self.hashButton.Enable()
					self.openButton.Enable()


		
		except (Exception,IOError),e:

			dialog = wx.MessageDialog(self, str(self.filename)+"Exception in computing the Hash.\n\r Please select a valid file to hash ", "Hash AnviK",wx.OK)
			dialog.ShowModal() # Show it
			dialog.Destroy()
			print repr(traceback.extract_stack())
			print e

	def closeWindow(self,event):
		self.Destroy()

	def OnAbout(self,e):
		# Create Message Dialog Box


		dialog = wx.MessageDialog(self, " A SHA1/SHA256/MD5 Hash Generator-Checker written \n in wxPython\n\nDeveloper Site-Blog:\nhttp://developerstation.blogspot.com/", "About Hash AnviK", wx.OK)

		retCode = dialog.ShowModal() # Show it
		
		#if(retCode == wx.ID_YES):
			
			#dialog.Destroy()

		dialog.Destroy() # destroy when finished.

	def OnOpen(self,e):
		""" Open a file"""
		dialog = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dialog.ShowModal() == wx.ID_OK:

			self.filename = dialog.GetPath()
			self.dirname = dialog.GetDirectory()
			
			self.chk_compare.Hide()
			self.label1.Hide()
			self.label4.Show()
			self.label5.Show()
			self.label6.Show()

			TestFrame.filename=self.filename

			self.hashButton.Enable()

			self.fileName_txt.SetValue(dialog.GetFilename())
			self.dirName_txt.SetValue(self.dirname)
			self.Compare_Hash_txt.SetValue("")
			self.Compare_Hash_txt.Hide()
			self.label10.Hide()
			self.label9.Hide()
			
			self.Hash_txt.Hide()
			self.Hash_txt.SetValue("")
			self.label7.Hide()
			

			self.dirName_txt.SetEditable(False)
			self.fileName_txt.SetEditable(False)
			self.size_txt.SetValue(str(float(os.path.getsize(self.filename))/1000000)+" MB")
			
			self.fileName_txt.Show()
			self.dirName_txt.Show()
			self.size_txt.Show()
			
			self.dirName_txt.SetInsertionPointEnd()
			self.fileName_txt.SetInsertionPointEnd()
			self.size_txt.SetInsertionPointEnd()
			self.Hash_txt.SetValue("")
		
		dialog.Destroy()
		
	def hashFunc(self,filename,block_size):

		try:
			self.w=0
			self.x=0
			self.g=[0]
			self.i=0

			f=open(self.filename,'rb')
			if(block_size==128):
				hashObj=hashlib.md5()
			elif(block_size==160):
				hashObj=hashlib.sha1()
			elif(block_size==256):
				hashObj=hashlib.sha256()
			
			self.size=float(os.path.getsize(self.filename))
			
			while self.x<self.size:
				self.x=self.x+self.size/100
				self.g.append(self.x)

			while True:
				self.w = self.w + block_size
				data = f.read(block_size)
				if(self.w>=self.g[self.i]):
					self.i=self.i+1
					self.gauge.SetValue(self.i*10)
					self.label3.SetLabel(str(self.i-1)+" %")
				if (self.w>self.size):
					pass
					self.i=100
				if not data:
					#print "broken"
					break
					self.gauge.SetValue(1000)
				hashObj.update(data)
				wx.Yield()
			self.gauge.SetValue(1000)
			self.Hash_txt.SetValue(hashObj.hexdigest())
			self.Hash_txt.Show()
			self.label7.Show()
			return str(hashObj.hexdigest())
			
		except Exception,e:
			pass	

if __name__=='__main__':
	app=wx.PySimpleApp()
	frame=TestFrame(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
