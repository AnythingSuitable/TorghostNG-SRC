#
# Follow on GitHub : https://github.com/AnythingSuitable
#

import tkinter as tk
from tkinter.ttk import *
import threading
from os import path, geteuid, mkdir, getcwd, system
from sys import exit
import wget

try:
	from Animations import Screen_Changing_Animations, Header_Menu_Animation
	from ColorScheme import Theme
	from Configs import *
	from Backend import Get_Interface_List, Get_MAC_Address, Change_MAC_Address, Check_Update, DNS_Fix, DNS_Restore, Connect_Tor, Disconnect_Tor, Renew_Tor_Circuit, Check_Tor

except Exception as e:
	print("TorghostNg/GUI Lacking some Files... Kindly Download again from GitHub.\nExitting...")
	exit()

if geteuid() != 0:
	print("Program requires Super-User Access.\nRun with 'sudo' privileges...\nExiting :/")
	exit()

GUI_VERSION = 'GUI Version : 0.1'
MAINTAINER = 'Maintainer : @AnythingSuitable'
TWITTER = '[ Twitter : @WhatIsSuitable ]'
PACKAGED = False

Theme_Mode, MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText = Theme()

app = tk.Tk()
app.title('TorghostNG - GUI')
app.geometry('600x400')
app.resizable(0,0)

try:
	SRC_FILE = 'torngSRC/'
	ICON = tk.PhotoImage(file = f'{SRC_FILE}Logo_{Theme_Mode.upper()}.png')
	app.iconphoto(False, ICON)

except Exception as e:
	print("TorghostNg/GUI Lacking some Files... Kindly Download again from GitHub.\nExitting...")
	exit()

################################################### ~ <GLOBAL> ~ #########################################################################

def Back_To_Home():
	Frame_ = Header_Menu_Animation(app, MainBackground)
	HomePage()

def Global_Option_Frame(heading, info=None):

	Header_Frame, Main_Frame = Screen_Changing_Animations(app, MainForeground, MainBackground)

	Header_Label = tk.Label(Header_Frame, text=heading, bg=MainForeground, fg=MainBackground, font=('Helvetica', 38, 'bold'), bd=0,)
	Header_Label.place(relx=0.04, rely=0.14)
	Header_Label_Info = tk.Label(Header_Frame, text=info, bg=MainForeground, fg=MainBackground, font=('Helvetica', 12,), bd=0,)
	Header_Label_Info.place(relx=0.06, rely=0.58)

	btn = tk.Button(Header_Frame,text='<',command=Back_To_Home, bd = 0, bg = MainBackground, fg=MainForeground, font=('Helvetica', 14,'bold'), highlightthickness=0,)
	btn.place(relx=0.84 , rely= 0.12 , relwidth=0.14, relheight=0.16)

	return Header_Frame, Main_Frame

################################################### ~ <PAGES> ~ #########################################################################

def TorPage():
	
	def Tor_Disonnect():

		Disconnect_Tor()
		Label_ = tk.Label(Tor_Main_Frame, text='Stopped Tor services.', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
		Label_.place(relx=0.04, rely=0.86)
		Tor_Start_Button = tk.Button(Tor_Main_Frame,text='Start', command=Tor_Connect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		Tor_Start_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
	
	def Tor_Connect():

		Connect_Tor()
		Label_ = tk.Label(Tor_Main_Frame, text='Started Tor services.', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
		Label_.place(relx=0.04, rely=0.86)
		Tor_Stop_Button = tk.Button(Tor_Main_Frame,text='Stop', command=Tor_Disonnect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		Tor_Stop_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
		Tor_Renew_Button = tk.Button(Tor_Main_Frame,text='Renew', command=Tor_Renew, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		Tor_Renew_Button.place(relx=0.64 , rely= 0.62 , relwidth=0.32, relheight=0.14)

	def Tor_Renew():
		try:
			Renew_Tor_Circuit()
			Label_ = tk.Label(Tor_Main_Frame, text='Renewed Tor Circuit.', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
			Label_.place(relx=0.04, rely=0.86)

		except Exception as e:
			Label_ = tk.Label(Tor_Main_Frame, text='Error Renewing Tor Circuit.', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
			Label_.place(relx=0.04, rely=0.86)
		Tor_Stop_Button = tk.Button(Tor_Main_Frame,text='Stop', command=Tor_Disonnect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		Tor_Stop_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
		Tor_Renew_Button = tk.Button(Tor_Main_Frame,text='Renew', command=Tor_Renew, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		Tor_Renew_Button.place(relx=0.64 , rely= 0.62 , relwidth=0.32, relheight=0.14)

	Tor_Header_Frame, Tor_Main_Frame = Global_Option_Frame('Tor Service.', 'Start connecting to Tor')

	def Tor_Current_Status():
		Label_ = tk.Label(Tor_Header_Frame, text = 'Getting Tor status...', font=('calibre', 12,), bd=0, bg=MainForeground, fg=MainBackground)
		Label_.place(relx=0.72 , rely= 0.82 )
		Tor_Status = Check_Tor()
		Label_.destroy()

		if Tor_Status.upper() == "CONNECTED":
			Tor_Stop_Button = tk.Button(Tor_Main_Frame,text='Stop', command=Tor_Disonnect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
			Tor_Stop_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
			Tor_Renew_Button = tk.Button(Tor_Main_Frame,text='Renew', command=Tor_Renew, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
			Tor_Renew_Button.place(relx=0.64 , rely= 0.62 , relwidth=0.32, relheight=0.14)
		if Tor_Status.upper() == "DISCONNECTED":
			Tor_Start_Button = tk.Button(Tor_Main_Frame,text='Start', command=Tor_Connect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
			Tor_Start_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
		if Tor_Status.upper() == "ERROR":
			Tor_Stop_Button = tk.Button(Tor_Main_Frame,text='Stop', command=Tor_Disonnect, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
			Tor_Stop_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)
			Label_ = tk.Label(Tor_Main_Frame, text="Either you aren't\nconnected to \ninternet or your \nTor circuit isn't \nworking properly.\npress 'Stop' to\ndisconnect :v", bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
			Label_.place(relx=0.02, rely=0.44)

	_ = threading.Thread(target=Tor_Current_Status,)
	_.start()


def MACPage():

	Interface_List = Get_Interface_List()

	MAC_Header_Frame, MAC_Main_Frame = Global_Option_Frame('MAC Changer.', 'Randomly change MAC address')

	def Current_MAC_Address():
		Selected_Interface = Interface_Selected.get()
		Current_MAC_Address = Get_MAC_Address(Selected_Interface)
		#print(Current_MAC_Address)
		Current_MAC_Address_Label.set(f'Current MAC Address : \n{Current_MAC_Address}')

	def Change_MAC():
		Selected_Interface = Interface_Selected.get()
		Change_MAC_Address(Selected_Interface)
		Current_MAC_Address()

	MAC_Change_Button = tk.Button(MAC_Main_Frame,text='Change',command=Change_MAC, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	MAC_Change_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)

	Interface_Selected = tk.StringVar()
	Interface_Selected.set( Interface_List[0] )
	  
	Interface_Dropdown = tk.OptionMenu( MAC_Main_Frame , Interface_Selected , *Interface_List )
	Interface_Dropdown.place(relx=0.08 , rely= 0.34, relwidth=0.32 )

	Get_MAC_Current_Address_Button = tk.Button(MAC_Main_Frame,text='Current Address',command=Current_MAC_Address, bd = 0, bg = SecondaryBlack, fg=SecondaryText, font=('Helvetica', 12,'bold'), highlightthickness=0,)
	Get_MAC_Current_Address_Button.place(relx=0.08 , rely= 0.48 , relwidth=0.32, relheight=0.16)

	Current_MAC_Address_Label = tk.StringVar()
	Current_MAC_Address_Label.set('Current MAC Address : \n__:__:__:__:__:__')

	MAC_Current_Label = tk.Label(MAC_Main_Frame, textvariable=Current_MAC_Address_Label, bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
	MAC_Current_Label.place(relx=0.58, rely=0.32)


def DNSPage():

	DNS_Header_Frame, DNS_Main_Frame = Global_Option_Frame('DNS.', "Use this to fix DNS when website address can't be resolved")

	def Restore_DNS():	
		_ = threading.Thread(target=DNS_Restore,)
		_.start()
		_.join()
		Label_ = tk.Label(DNS_Main_Frame, text='Done Restoring Original', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
		Label_.place(relx=0.04, rely=0.86)
		Label_.after(6000 , lambda: Label_.destroy())

	def Fix_DNS():	
		_ = threading.Thread(target=DNS_Fix,)
		_.start()
		_.join()
		Label_ = tk.Label(DNS_Main_Frame, text='DNS Fixed', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 16,), bd=0,)
		Label_.place(relx=0.04, rely=0.86)
		Label_.after(6000 , lambda: Label_.destroy())
	
	if path.isfile(resolv_b) == True:
		DNS_Restore_Button = tk.Button(DNS_Main_Frame,text='Restore Original',command=Restore_DNS, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
		DNS_Restore_Button.place(relx=0.64 , rely= 0.6 , relwidth=0.32, relheight=0.14)

	DNS_Fix_Button = tk.Button(DNS_Main_Frame,text='Fix',command=Fix_DNS, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	DNS_Fix_Button.place(relx=0.64 , rely= 0.8 , relwidth=0.32, relheight=0.14)


def AboutPage():

	About_Header_Frame, About_Main_Frame = Global_Option_Frame('About.', "(^_^)")

	def UpdatePage():

		def Check_For_Update(Label_):

			Current_Version, Latest_Version, Update_Available = Check_Update()

			def Back_To_About():
				Frame_ = Header_Menu_Animation(app, MainBackground)
				AboutPage()

			btn = tk.Button(Frame_,text='<',command=Back_To_About, bd = 0, bg = MainBackground, fg=MainForeground, font=('Helvetica', 14,'bold'), highlightthickness=0,)
			btn.place(relx=0.82 , rely= 0.08 , relwidth=0.08, relheight=0.08)

			Label_.destroy()

			if Current_Version == Latest_Version == float(0.0):
				Update_Label = tk.Label(Frame_, text='Error Retrieving', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label.place(relx=0.04, rely=0.06)

				Update_Label_ = tk.Label(Frame_, text='Update info...', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label_.place(relx=0.04, rely=0.22)

			elif Update_Available  == True:

				Update_Label = tk.Label(Frame_, text='Update', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label.place(relx=0.04, rely=0.06)

				Update_Label_ = tk.Label(Frame_, text='Available', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label_.place(relx=0.04, rely=0.22)

				Update_Frame = tk.Frame(Frame_, background=PrimaryPurple)
				Update_Frame.place(relx=0.04 , rely= 0.56 , relwidth=0.48, relheight=0.4)

				
				Update_Version_Header_Label = tk.Label(Update_Frame, text='TorghostNg - GUI', bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 18, 'bold'), bd=0,)
				Update_Version_Header_Label.place(relx=0.12, rely=0.12)
				Version_Current_Label = tk.Label(Update_Frame, text= f'Current Version : {Current_Version}', bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 14, ), bd=0,)
				Version_Current_Label.place(relx=0.04, rely=0.58)
				Version_Latest_Label = tk.Label(Update_Frame, text= f'Latest Version : {Latest_Version}', bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 14, ), bd=0,)
				Version_Latest_Label.place(relx=0.04, rely=0.78)

				def Download_Update():

					URL = 'https://github.com/AnythingSuitable/raw/raw/main/torghostng'

					if path.exists('/usr/bin/torghostng_tmp_update_files') == False:
						mkdir('/usr/bin/torghostng_tmp_update_files')

					Download_Dir_Final = f'/usr/bin/torghostng_tmp_update_files/'

					Downloading_Label = tk.Label(Frame_, text = 'Downloading...', font=('calibre', 12,), bd=0, bg=MainBackground, fg=PrimaryText)
					Downloading_Label.place(relx=0.62 , rely= 0.52 )
					progress_ = Progressbar(Frame_, orient = tk.HORIZONTAL,length = 100, mode = 'determinate')
					progress_.place(relx=0.62 , rely= 0.6, relheight= 0.08 ,relwidth= 0.24)

					perc = tk.StringVar()
					perc.set('0')

					Downloaded_Percentage_Label = tk.Label(Frame_, text = f'{perc}% Completed', font=('calibre', 12,), bd=0, bg=MainBackground, fg=PrimaryText)
					Downloaded_Percentage_Label.place(relx=0.62 , rely= 0.7 )

					def Download_Indicator(current, total, width=80):

						Download_Completed_Percentage = round((current / total * 100),2)
						progress_['value'] = Download_Completed_Percentage
						perc.set(Download_Completed_Percentage)
						Downloaded_Percentage_Label.config(text=f'{Download_Completed_Percentage}% Completed')
						Frame_.update_idletasks()
						if int(Download_Completed_Percentage) == 100:
							Downloading_Label.destroy()
							Installing_Label = tk.Label(Frame_, text = 'Installing...', font=('calibre', 12,), bd=0, bg=MainBackground, fg=PrimaryText)
							Installing_Label.place(relx=0.62 , rely= 0.52 )

					wget.download(URL, bar=Download_Indicator, out=Download_Dir_Final)
					system(f'sudo rm -rf /usr/bin/torghostng ')
					system(f'sudo cp {Download_Dir_Final}torghostng /usr/bin/')
					system(f'sudo rm -rf {Download_Dir_Final}')
					system(f'sudo chmod +x /usr/bin/torghostng')

					Frame__ = Header_Menu_Animation(app, MainBackground)

					Label_ = tk.Label(Frame__, text='Kindly Restart the app\nto see new Features...', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 14,), bd=0,)
					Label_.place(relx=0.04, rely=0.18)

				Update_Proceed_Button = tk.Button(Frame_,text='Update',command=Download_Update, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
				Update_Proceed_Button.place(relx=0.6 , rely= 0.8 , relwidth=0.28, relheight=0.12)
			else:
				Update_Label = tk.Label(Frame_, text='No Updates', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label.place(relx=0.04, rely=0.06)

				Update_Label_ = tk.Label(Frame_, text='Available', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 32, 'bold'), bd=0,)
				Update_Label_.place(relx=0.04, rely=0.22)


		Frame_ = Header_Menu_Animation(app, MainBackground)
		Update_Check_Status_Label = tk.StringVar()
		Update_Check_Status_Label.set('Checking for Update...')
		Label_ = tk.Label(Frame_, textvariable=Update_Check_Status_Label, bg=MainBackground, fg=PrimaryText, font=('Helvetica', 24, 'bold'), bd=0,)
		Label_.place(relx=0.04, rely=0.08)
		_ = threading.Thread(target=Check_For_Update, args=(Label_,),)
		_.start()

	About_Version_Frame = tk.Frame(About_Main_Frame, background=PrimaryPurple)
	About_Version_Frame.place(relx=0.48 , rely= 0.28 , relwidth=0.48, relheight=0.66)
	About_Version_Header_Label = tk.Label(About_Version_Frame, text='TorghostNg - GUI', bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 22, 'bold'), bd=0,)
	About_Version_Header_Label.place(relx=0.06, rely=0.12)
	About_Version_Current_Label = tk.Label(About_Version_Frame, text= GUI_VERSION, bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 12, ), bd=0,)
	About_Version_Current_Label.place(relx=0.02, rely=0.66)
	About_Version_Maintainer_Label = tk.Label(About_Version_Frame, text= MAINTAINER, bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 12, ), bd=0,)
	About_Version_Maintainer_Label.place(relx=0.02, rely=0.76)
	About_Version_Twitter_Label = tk.Label(About_Version_Frame, text= TWITTER, bg=PrimaryPurple, fg=SecondaryText, font=('Helvetica', 12, ), bd=0,)
	About_Version_Twitter_Label.place(relx=0.02, rely=0.86)

	About_Version_Info_Frame = tk.Frame(About_Main_Frame, background=MainBackground)
	About_Version_Info_Frame.place(relx=0.0 , rely= 0.28 , relwidth=0.48, relheight=0.66)
	About_Version_Info_Label = tk.Label(About_Version_Info_Frame, text='Just a GUI implementation\nof TorghostNG scripted\nby @GitHackTools', bg=MainBackground, fg=MainForeground, font=('Helvetica', 14, 'bold'), bd=0,)
	About_Version_Info_Label.place(relx=0.08, rely=0.08)
	About_Update_Button = tk.Button(About_Version_Info_Frame,text='Update',command=UpdatePage, bd = 0, bg = SecondaryBlack, fg=SecondaryText, font=('Helvetica', 12,'bold'), highlightthickness=0,)
	About_Update_Button.place(relx=0.2 , rely= 0.74 , relwidth=0.6, relheight=0.2)


def HomePage():

	Home_Frame = tk.Frame(app, background=MainBackground)
	Home_Frame.place(relx=0, rely=0, relwidth=1, relheight=1)

	Home_Label = tk.Label(Home_Frame, text='TorghostNG', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 42, 'bold'), bd=0,)
	Home_Label.place(relx=0.04, rely=0.06)

	Home_Label_V = tk.Label(Home_Frame, text='2.0', bg=MainBackground, fg=PrimaryText, font=('Helvetica', 42, 'bold'), bd=0,)
	Home_Label_V.place(relx=0.04, rely=0.22)

	def Toggle_Theme():
		Theme_Mode, _, _, _, _, _, _, _, _ = Theme()
		New_Theme_Label = tk.StringVar()
		
		if Theme_Mode.upper() == 'LIGHT':
			with open('__ThemeMode__.txt', 'w') as Theme_Mode_File:
				Theme_Mode_File.write('dark')
				Theme_Mode_File.close()
				New_Theme_Label.set('Dark mode will be applied\nafter you restart.')
				
		else:
			with open('__ThemeMode__.txt', 'w') as Theme_Mode_File:
				Theme_Mode_File.write('light')
				Theme_Mode_File.close()
				New_Theme_Label.set('Light mode will be applied\nafter you restart.')

		Label_ = tk.Label(Home_Frame, textvariable=New_Theme_Label, bg=MainBackground, fg=PrimaryText, font=('Helvetica', 14,), bd=0,)
		Label_.place(relx=0.64, rely=0.16)
		Label_.after(6000 , lambda: Label_.destroy())

	Theme_Button = tk.Button(Home_Frame,text=(Theme_Mode[0].upper() + Theme_Mode[1:]),command = Toggle_Theme, bd = 0, bg = SecondaryBlack, fg=SecondaryText, font=('Helvetica', 12,'bold'), highlightthickness=0,)
	Theme_Button.place(relx=0.82 , rely= 0.04 , relwidth=0.16, relheight=0.08)

	Home_Tor_Button = tk.Button(Home_Frame,text='Tor Service',command=TorPage, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	Home_Tor_Button.place(relx=0.32 , rely= 0.66 , relwidth=0.3, relheight=0.12)
	Home_MAC_Button = tk.Button(Home_Frame,text='MAC',command=MACPage, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	Home_MAC_Button.place(relx=0.66 , rely= 0.66 , relwidth=0.3, relheight=0.12)
	Home_DNS_Button = tk.Button(Home_Frame,text='DNS',command=DNSPage, bd = 0, bg = PrimaryBlue, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	Home_DNS_Button.place(relx=0.32 , rely= 0.82 , relwidth=0.3, relheight=0.12)
	Home_About_Button = tk.Button(Home_Frame,text='About',command=AboutPage, bd = 0, bg = PrimaryGreen, fg=SecondaryText, font=('Helvetica', 16,'bold'), highlightthickness=0,)
	Home_About_Button.place(relx=0.66 , rely= 0.82 , relwidth=0.3, relheight=0.12)

HomePage()

app.mainloop()