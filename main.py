try:
	import wx
except ImportError:
	import pip
	pip.main(['install', '--upgrade', '--trusted-host', 'wxpython.org', '--pre', '-f', 'http://wxpython.org/Phoenix/snapshot-builds/', 'wxPython_Phoenix'])
	import wx


from wx import adv

TRAY_TOOLTIP = 'KA Lite GUI'
TRAY_ICON = 'logo48.ico'

TRAY_START_BUTTON_ENABLED = True
TRAY_STOP_BUTTON_ENABLED = False
TRAY_LOAD_BUTTON_ENABLED = False
TRAY_EXIT_BUTTON_ENABLED = True

TRAY_START_BUTTON_ID = 1
TRAY_STOP_BUTTON_ID = 2
TRAY_LOAD_BROWSER_BUTTON_ID = 3
TRAY_OPTIONS_BUTTON_ID = 4
TRAY_EXIT_BUTTON_ID = 5
TRAY_OPTION_RUN_ON_WINDOWS_STARTUP_ID = 6
TRAY_OPTION_AUTO_START_SERVER_ID = 7

TRAY_START_BUTTON_LABEL = "Start Server"
TRAY_STOP_BUTTON_LABEL = "Stop Server"
TRAY_LOAD_BROWSER_BUTTON_LABEL ="Load in browser"
TRAY_OPTIONS_BUTTON_LABEL = "Options"
TRAY_EXIT_BUTTON_LABEL = "Exit KA Lite"
TRAY_OPTION_RUN_ON_WINDOWS_STARTUP_LABEL = "Run on Windows Startup."
TRAY_OPTION_AUTO_START_SERVER_LABEL = "Auto Start the server."

TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS = False
TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS = False

def add_menu_item(menu, button_id, label, enabled, checkable=False):
    if checkable:
        item = wx.MenuItem(menu, button_id, label, "", wx.ITEM_CHECK)
    else:
        item = wx.MenuItem(menu, button_id, label)

    item.Enable(enabled)
    menu.Append(item)
    return item

def get_run_on_windows_startup_checked_status():
    global TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS
    TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS = not(TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS)
    return TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS

def get_auto_start_server_checked_status():
    global TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS
    TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS = not(TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS)
    return TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS

class TaskBarIcon(adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def build_menu(self, start_enabled, stop_enabled, load_enabled, exit_enabled):
        menu = wx.Menu()

        tray_start_button = add_menu_item(menu, TRAY_START_BUTTON_ID, TRAY_START_BUTTON_LABEL, start_enabled)
        menu.Bind(wx.EVT_MENU, self.on_server_start, tray_start_button)
        menu.AppendSeparator()

        tray_stop_button = add_menu_item(menu, TRAY_STOP_BUTTON_ID, TRAY_STOP_BUTTON_LABEL, stop_enabled)
        menu.Bind(wx.EVT_MENU, self.on_server_stop, tray_stop_button)
        menu.AppendSeparator()

        tray_load_browser_button = add_menu_item(menu, TRAY_LOAD_BROWSER_BUTTON_ID, TRAY_LOAD_BROWSER_BUTTON_LABEL, load_enabled)
        menu.Bind(wx.EVT_MENU, self.on_browser_load, tray_load_browser_button)
        menu.AppendSeparator()

        options_menu = wx.Menu()
        menu.AppendSubMenu(options_menu, TRAY_OPTIONS_BUTTON_LABEL)
        menu.AppendSeparator()

        tray_exit_button = add_menu_item(menu, TRAY_EXIT_BUTTON_ID, TRAY_EXIT_BUTTON_LABEL, exit_enabled)
        menu.Bind(wx.EVT_MENU, self.on_exit, tray_exit_button)

        # Options
        tray_run_startup = add_menu_item(options_menu, TRAY_OPTION_RUN_ON_WINDOWS_STARTUP_ID, TRAY_OPTION_RUN_ON_WINDOWS_STARTUP_LABEL, True, True)
        menu.Bind(wx.EVT_MENU, self.on_run_on_startup_check, tray_run_startup)
        options_menu.AppendSeparator()
        global TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS
        tray_run_startup.Check(TRAY_OPTION_RUN_ON_WINDOWS_CHECKED_STATUS)

        tray_auto_start = add_menu_item(options_menu, TRAY_OPTION_AUTO_START_SERVER_ID, TRAY_OPTION_AUTO_START_SERVER_LABEL, True, True)
        menu.Bind(wx.EVT_MENU, self.on_auto_start_server_check, tray_auto_start)
        global TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS
        tray_auto_start.Check(TRAY_OPTION_AUTO_START_SERVER_CHECKED_STATUS)

        return menu

    def CreatePopupMenu(self):
        global TRAY_START_BUTTON_ENABLED
        global TRAY_STOP_BUTTON_ENABLED
        global TRAY_LOAD_BUTTON_ENABLED
        global TRAY_EXIT_BUTTON_ENABLED
        menu = self.build_menu(TRAY_START_BUTTON_ENABLED, TRAY_STOP_BUTTON_ENABLED, TRAY_LOAD_BUTTON_ENABLED, TRAY_EXIT_BUTTON_ENABLED)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print 'Clicked...'

    def on_server_start(self, event):
        print "Server is starting..."
        global TRAY_START_BUTTON_ENABLED
        global TRAY_STOP_BUTTON_ENABLED
        global TRAY_LOAD_BUTTON_ENABLED
        TRAY_START_BUTTON_ENABLED = False
        TRAY_STOP_BUTTON_ENABLED = True
        TRAY_LOAD_BUTTON_ENABLED = True

    def on_server_stop(self, event):
        print "Server is stopping..."
        global TRAY_START_BUTTON_ENABLED
        global TRAY_STOP_BUTTON_ENABLED
        global TRAY_LOAD_BUTTON_ENABLED
        TRAY_START_BUTTON_ENABLED = True
        TRAY_STOP_BUTTON_ENABLED = False
        TRAY_LOAD_BUTTON_ENABLED = False

    def on_browser_load(self, event):
    	print "Loading KA Lite on browser..."

    def on_run_on_startup_check(self, event):
        if get_run_on_windows_startup_checked_status():
            print "Run at startup checked..."
        else:
            print "Run at startup unchecked..."

    def on_auto_start_server_check(self, event):
        if get_auto_start_server_checked_status():
            print "Auto start server checked..."
        else:
            print "Auto start server unchecked..."

    def on_exit(self, event):
    	print "Exiting KA Lite..."
    	wx.CallAfter(self.Destroy)

app = wx.App()
y = TaskBarIcon()
app.MainLoop()