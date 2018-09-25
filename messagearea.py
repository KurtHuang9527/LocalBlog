#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtGui, QtCore
import base64
import sqlite3
from datetime import datetime, date




class Form(QtGui.QWidget):
	
	def createdb(self):
		conn = sqlite3.connect('messagearea.db')
		c = conn.cursor()
		c.execute('''CREATE TABLE if not exists MESSAGEAREA
			(ID INTEGER PRIMARY KEY,
			TITLE           TEXT    NOT NULL,
			CONTENT            TEXT     NOT NULL,
			PICTURE        TEXT	NOT NULL,
			DATE         DATE);''')

		conn.commit()
		conn.close()
	
	def __init__(self):
	
		self.createdb()
		super(Form, self).__init__()
#主畫面UI
		wg1_label_title = QtGui.QLabel('Title')
		self.wg2_inputarea_title = QtGui.QLineEdit()
		wg3_label_content = QtGui.QLabel('Content')
		self.wg4_inputarea_content = QtGui.QTextEdit()
		wg5_label_upload = QtGui.QLabel('Upload Picture')
		wg6_pbutton_upload = QtGui.QPushButton("Select your file")
		wg7_pbutton_cancel = QtGui.QPushButton("View")
		self.wg8_pbutton_ok = QtGui.QPushButton("OK")
		self.wg10_label_displayPic = QtGui.QLabel('Picture')
		
#主畫面按鈕		
		wg6_pbutton_upload.clicked.connect(self.uploadpic)
		wg7_pbutton_cancel.clicked.connect(self.press_cancel)
		self.wg8_pbutton_ok.clicked.connect(self.press_ok)
		
#綁定		
		layout1 = QtGui.QFormLayout()
		layout1.addRow(wg1_label_title, self.wg2_inputarea_title)
		layout1.addRow(wg3_label_content, self.wg4_inputarea_content)
		layout1.addWidget(self.wg10_label_displayPic)
		layout1.addRow(wg5_label_upload, wg6_pbutton_upload)
		layout1.addRow(wg7_pbutton_cancel, self.wg8_pbutton_ok)
		layout = QtGui.QVBoxLayout()
		layout.addLayout(layout1)
		
#輸出
		self.setLayout(layout)
		self.setGeometry(400, 400, 800, 500)
		self.setWindowTitle("Write Something")
		self.show()

#取消按鈕的功能
	def press_cancel(self):
		self.close()
		self.browse_area()	
		
#上傳照片功能		
	def uploadpic(self):
		self.pname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.gif *.png)")
		self.wg10_label_displayPic.setPixmap(QtGui.QPixmap(self.pname))
		self.image_64_encode = base64.encodestring(open(self.pname, "rb").read()) #圖片轉base64

#主UI的OK功能
	def press_ok(self):
		if self.wg2_inputarea_title.text() and self.wg4_inputarea_content.toPlainText() != "": #判斷是否全部欄位都有填
			conn = sqlite3.connect('messagearea.db') #連接DB寫入資料
			self.c = conn.cursor()
			self.c.execute('INSERT INTO MESSAGEAREA(TITLE,CONTENT,PICTURE,DATE) VALUES (?,?,?,?)',(self.wg2_inputarea_title.text(),self.wg4_inputarea_content.toPlainText(),self.image_64_encode,datetime.now()))
			conn.commit()
			conn.close()
			self.close()
			self.browse_area()

		else:
			message = QtGui.QMessageBox()
			message.setIcon(QtGui.QMessageBox.Information)
			message.setWindowTitle("Oops!")
			message.setText("All Fields are must filled.")
			message.setStandardButtons(QtGui.QMessageBox.Close)
			message.exec_()

#瀏覽所有文章			
	def browse_area(self):
		
		super(Form, self).__init__()
		conn = sqlite3.connect('messagearea.db')
		self.c = conn.cursor()
		id = self.c.execute("SELECT ID From MESSAGEAREA")
		self.all_id = id.fetchall()
		rlayout1 = QtGui.QFormLayout()
		rlayout = QtGui.QVBoxLayout()
		windows = QtGui.QWidget()
		pe = QtGui.QPalette()

#從DB撈出資料並建立UI		
		for count in self.all_id:
			count_num = int(count[0])
			show_title = self.c.execute("SELECT TITLE From MESSAGEAREA WHERE ID={s}".format(s=count_num))
			self.show_title_f = show_title.fetchone()[0]
			show_content = self.c.execute("SELECT CONTENT From MESSAGEAREA WHERE ID={s}".format(s=count_num))
			self.show_content_f = show_content.fetchone()[0]
			show_date = self.c.execute("SELECT DATE From MESSAGEAREA WHERE ID={s}".format(s=count_num))
			self.show_date = show_date.fetchone()[0]
			show_pic = self.c.execute("SELECT PICTURE From MESSAGEAREA WHERE ID={s}".format(s=count_num))
			self.show_pic_f = show_pic.fetchone()[0]
			self.rwg1_label_displayPic = QtGui.QLabel("Picture")
			self.image_64_decode = base64.decodestring(self.show_pic_f)
			self.image64 = QtGui.QImage.fromData(self.image_64_decode)
			self.rwg1_label_displayPic.setPixmap(QtGui.QPixmap.fromImage(self.image64))
			self.rwg2_label_title = QtGui.QLabel(self.show_title_f)
			self.rwg2_label_title.setFont(QtGui.QFont("Arial",20,QtGui.QFont.Bold))
			self.rwg3_label_date = QtGui.QLabel(self.show_date)
			self.rwg3_label_date.setFont(QtGui.QFont("Arial",10))
			self.rwg4_label_content = QtGui.QLabel(self.show_content_f)
			self.rwg4_label_content.setFont(QtGui.QFont("Arial",13))
			self.rwg4_label_content.setAutoFillBackground(True)  
			pe.setColor(QtGui.QPalette.Window,QtCore.Qt.white) #設定label背景
			self.rwg4_label_content.setPalette(pe) #設定label背景
			self.rlabel_split = QtGui.QLabel("===========================================================================================================================================================================================================================================")
			self.rlabel_title = QtGui.QLabel("Title: ")
			self.rlabel_title.setFont(QtGui.QFont("Arial",20,QtGui.QFont.Bold))
			self.rlabel_date = QtGui.QLabel("TIME: ")
			self.rlabel_date.setFont(QtGui.QFont("Arial",10,QtGui.QFont.Bold))
			self.rlabel_content = QtGui.QLabel("CONTENT: ")
			self.rlabel_content.setFont(QtGui.QFont("Arial",10,QtGui.QFont.Bold))
			self.del_btn = QtGui.QPushButton(str(count_num))
			icon1 = QtGui.QIcon()
			icon1.addPixmap(QtGui.QPixmap("b_delete.png"))
			self.del_btn.setIcon(icon1)
			self.del_btn.setIconSize(QtCore.QSize(90, 40))
			font=QtGui.QFont()
			font.setPointSize(1)
			self.del_btn.setFont(font)
			self.mod_btn = QtGui.QPushButton(str(count_num))
			icon2 = QtGui.QIcon()
			icon2.addPixmap(QtGui.QPixmap("b_ok.png"))
			self.mod_btn.setIcon(icon2)
			self.mod_btn.setIconSize(QtCore.QSize(90, 40))
			self.mod_btn.setFont(font)
			self.del_btn.clicked.connect(self.press_delete)
			self.mod_btn.clicked.connect(self.press_modify)
			rlayout1.addWidget(self.rlabel_split)
			rlayout1.addRow(self.rlabel_title, self.rwg2_label_title)
			rlayout1.addRow(self.rlabel_date, self.rwg3_label_date)
			rlayout1.addWidget(self.rwg1_label_displayPic)
			rlayout1.addRow(self.rlabel_content, self.rwg4_label_content)
			rlayout1.addRow(self.del_btn, self.mod_btn)
						
		conn.close()
		self.rwg5_pbutton_close = QtGui.QPushButton("Close")
		self.rwg6_pbutton_write = QtGui.QPushButton("Write Something")
		self.rwg5_pbutton_close.clicked.connect(self.close)
		self.rwg6_pbutton_write.clicked.connect(self.press_write)
		
		rlayout2 = QtGui.QHBoxLayout()
		rlayout2.addWidget(self.rwg5_pbutton_close)
		rlayout2.addWidget(self.rwg6_pbutton_write)

		windows.setLayout(rlayout1)
		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setWidget(windows)
		self.scrollArea.setAutoFillBackground(True)
		
		rlayout.addWidget(self.scrollArea)
		rlayout.addLayout(rlayout1)
		rlayout.addLayout(rlayout2)

		self.setLayout(rlayout)
		self.setGeometry(100, 100, 1200, 800)
		self.setWindowTitle("Pic Show")
		self.show()
	
	def press_write(self):
		self.close()
		self.__init__()
		
#刪除文章功能
	def press_delete(self):
		sender = self.sender()		
		conn = sqlite3.connect('messagearea.db')
		self.c = conn.cursor()
		self.c.execute("DELETE FROM MESSAGEAREA WHERE ID={s}".format(s=sender.text()))
		conn.commit()
		conn.close()
		self.close()
		self.browse_area()
		print('%s is pressed' % sender.text())
		del sender
#修改文章功能		
	def press_modify(self):
		self.close()
		self.sender = self.sender()
		conn = sqlite3.connect('messagearea.db')
		self.c = conn.cursor()
		data = self.c.execute("SELECT * From MESSAGEAREA WHERE ID={s}".format(s=self.sender.text()))
		dataintable = data.fetchone()
		m2_inputarea_title = dataintable[1]
		m4_inputarea_content = dataintable[2]
		self.m10_label_displayPic = dataintable[3]
		image_64_decode = base64.decodestring(self.m10_label_displayPic)
		image64 = QtGui.QImage.fromData(image_64_decode)
		conn.close()
		
		super(Form, self).__init__()
#主畫面UI
		m1_label_title = QtGui.QLabel('Title')
		self.m2_inputarea_title = QtGui.QLineEdit(m2_inputarea_title)
		m3_label_content = QtGui.QLabel('Content')
		self.m4_inputarea_content = QtGui.QTextEdit(m4_inputarea_content)
		m5_label_upload = QtGui.QLabel('Upload Picture')
		m6_pbutton_upload = QtGui.QPushButton("Select your file")
		m7_pbutton_cancel = QtGui.QPushButton("Cancel")
		self.m8_pbutton_ok = QtGui.QPushButton("OK")
		self.m10_label_displayPic_w = QtGui.QLabel("Picture")
		self.m10_label_displayPic_w.setPixmap(QtGui.QPixmap.fromImage(image64))
		
#主畫面按鈕		
		m6_pbutton_upload.clicked.connect(self.mod_uploadpic)
		m7_pbutton_cancel.clicked.connect(self.press_cancel)
		self.m8_pbutton_ok.clicked.connect(self.mod_ok)
		
#綁定		
		layout1 = QtGui.QFormLayout()
		layout1.addRow(m1_label_title, self.m2_inputarea_title)
		layout1.addRow(m3_label_content, self.m4_inputarea_content)
		layout1.addWidget(self.m10_label_displayPic_w)
		layout1.addRow(m5_label_upload, m6_pbutton_upload)
		layout1.addRow(m7_pbutton_cancel, self.m8_pbutton_ok)
		layout = QtGui.QVBoxLayout()
		layout.addLayout(layout1)
		
#輸出
		self.setLayout(layout)
		self.setGeometry(100, 100, 800, 500)
		self.setWindowTitle("Modify")
		self.show()
		
#修改頁面的上傳
	def mod_uploadpic(self):
		self.pname_mod = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.gif *.png)")
		self.m10_label_displayPic_w.setPixmap(QtGui.QPixmap(self.pname_mod))
		self.m10_label_displayPic = base64.encodestring(open(self.pname_mod, "rb").read()) #圖片轉base64

#修改頁面的OK
	def mod_ok(self):
		if self.m2_inputarea_title.text() and self.m4_inputarea_content.toPlainText() != "": #判斷是否全部欄位都有填
			conn = sqlite3.connect('messagearea.db') #連接DB寫入資料
			self.c = conn.cursor()
			self.c.execute('UPDATE MESSAGEAREA SET TITLE=?, CONTENT=?, PICTURE=?, DATE=? WHERE ID=?', (self.m2_inputarea_title.text(), self.m4_inputarea_content.toPlainText(), self.m10_label_displayPic, datetime.now(), self.sender.text()))
			conn.commit()
			conn.close()
			self.close()
			self.browse_area()
			del self.sender
		else:
			message = QtGui.QMessageBox()
			message.setIcon(QtGui.QMessageBox.Information)
			message.setWindowTitle("Oops!")
			message.setText("All Fields are must filled.")
			message.setStandardButtons(QtGui.QMessageBox.Close)
			message.exec_()
		

		
		
		


app = QtGui.QApplication(sys.argv)
mainWindow = Form()
status = app.exec_()
sys.exit(status)