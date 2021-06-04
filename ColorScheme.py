#
# Follow on GitHub : https://github.com/AnythingSuitable
#

DARK_MODE = {

	'MainBackground' : '#161B22',
	'MainForeground' : '#FFFFFF',
	'SecondaryBlack' : '#30363D',
	'PrimaryBlue' : '#1F6FEB',
	'PrimaryGreen' : '#2EA043',
	'PrimaryPurple' : '#6C63FF',
	'PrimaryText' : '#FFFFFF',
	'SecondaryText' : '#FFFFFF'

}

LIGHT_MODE = {

	'MainBackground' : '#FFFFFF',
	'MainForeground' : '#161B22',
	'SecondaryBlack' : '#30363D',
	'PrimaryBlue' : '#1F6FEB',
	'PrimaryGreen' : '#2EA043',
	'PrimaryPurple' : '#6C63FF',
	'PrimaryText' : '#000000',
	'SecondaryText' : '#FFFFFF'
	
}

def ColorScheme(MODE = 'DARK'):

	if MODE.upper() == 'LIGHT':

		MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText = LIGHT_MODE['MainBackground'], LIGHT_MODE['MainForeground'], LIGHT_MODE['SecondaryBlack'], LIGHT_MODE['PrimaryBlue'], LIGHT_MODE['PrimaryGreen'], LIGHT_MODE['PrimaryPurple'], LIGHT_MODE['PrimaryText'], LIGHT_MODE['SecondaryText']
		return MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText

	else:

		MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText = DARK_MODE['MainBackground'], DARK_MODE['MainForeground'], DARK_MODE['SecondaryBlack'], DARK_MODE['PrimaryBlue'], DARK_MODE['PrimaryGreen'], DARK_MODE['PrimaryPurple'], DARK_MODE['PrimaryText'], DARK_MODE['SecondaryText']
		return MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText

def Theme():
	try:
		with open('__ThemeMode__.txt', 'r') as Theme_Mode_File:

			Theme_Mode = Theme_Mode_File.readlines()
			Theme_Mode_File.close()
			if len(Theme_Mode) == 0:
				Theme_Mode = ['Dark']
	except Exception as e:
		Theme_Mode = ['DARK']

	Theme_Mode = str(Theme_Mode[0])

	MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText = ColorScheme(Theme_Mode)
	return Theme_Mode, MainBackground, MainForeground, SecondaryBlack, PrimaryBlue, PrimaryGreen, PrimaryPurple, PrimaryText, SecondaryText