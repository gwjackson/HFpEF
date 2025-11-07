import webbrowser

import wx



class Main_Frame(wx.Frame):
    """
    main frame for the H2FpEF calculator
    """

    def __init__(self):
        super().__init__(None, title='H2FpEF - risk calculator')

        self.create_menu()
        self.CreateStatusBar()
        panel = wx.Panel(self)
        self.panel = panel


    def create_menu(self):
        """
        Build / set up the menu bar
        """

        menu_bar = wx.MenuBar()

        # About Menu
        aboutMenu = wx.Menu()

        help_menu_item = aboutMenu.Append(wx.ID_ANY, '&About', 'About the H2FpEF')
        self.Bind(wx.EVT_MENU, self.on_help, help_menu_item)

        # Citation Menu and Submenu
        citationMenu = wx.Menu()
        cit_circulation_item = citationMenu.Append(wx.ID_ANY, 'Circulation 2018', 'Journal Circulation 2018')
        self.Bind(wx.EVT_MENU, self.on_circulation, cit_circulation_item)
        cit_circulation_item = citationMenu.Append(wx.ID_ANY, 'AAFP 2025', 'AAFP journal 2025')
        self.Bind(wx.EVT_MENU, self.on_aafp, cit_circulation_item)

        aboutMenu.AppendSubMenu(citationMenu, '&Citation')


        exit_menu_item = aboutMenu.Append(wx.ID_EXIT, '&Exit', 'Exit / Terminate the application')
        self.Bind(wx.EVT_MENU, self.on_exit, exit_menu_item)

        menu_bar.Append(aboutMenu, '&About')

        # GDMT menu
        gdmtMenu = wx.Menu()

        gdmt_menu_item = gdmtMenu.Append(wx.ID_ANY, '&GDMT', 'Guideline Directed Medical Therapy for HFpEF')
        self.Bind(wx.EVT_MENU, self.on_gdmt_gdmt, gdmt_menu_item)

        gdmt_sympt_itme = gdmtMenu.Append(wx.ID_ANY, '&Symptoms', 'Common HFpEF Symptoms')
        self.Bind(wx.EVT_MENU, self.on_gdmt_sympt, gdmt_sympt_itme)

        menu_bar.Append(gdmtMenu, '&GDMT')

        self.SetMenuBar(menu_bar)


    def on_exit(self, event):
        self.Close()

    def on_help(self, event):
        pass

    def on_circulation(self, event):
        url = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6202181/'
        webbrowser.open(url)

    def on_aafp(self, event):
        url = 'https://www.aafp.org/pubs/afp/issues/2025/1000/heart-failure-preserved-ejection-fraction.html'
        webbrowser.open(url)

    def on_gdmt_gdmt(self, event):
       pass

    def on_gdmt_sympt(self, event):
        pass





if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

