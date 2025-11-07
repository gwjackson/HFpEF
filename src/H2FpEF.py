import wx



class Main_Frame(wx.Frame):
    """
    main frame for the H2FpEF calculator
    """

    def __init__(self):
        super().__init__(None, title='H2FpEF - risk calculator')

        self.create_menu()
        self.CreateStatusBar()


    def create_menu(self):
        """
        Build / set up the menu bar
        """

        menu_bar = wx.MenuBar()

        aboutMenu = wx.Menu()

        help_menu_item = aboutMenu.Append(wx.ID_ANY, '&About', 'About the H2FpEF')
        self.Bind(wx.EVT_MENU, self.on_help, help_menu_item)

        citation_item = aboutMenu.Append(wx.ID_ANY, '&Citation', 'Citation information')
        self.Bind(wx.EVT_MENU, self.on_citation, citation_item)
        ### TO DO add citation sub-menus

        exit_menu_item = aboutMenu.Append(wx.ID_EXIT, '&Exit', 'Exit / Terminate the application')
        self.Bind(wx.EVT_MENU, self.on_exit, exit_menu_item)

        menu_bar.Append(aboutMenu, '&About')

        gdmtMenu = wx.Menu()

        gdmt_menu_item = gdmtMenu.Append(wx.ID_ANY, '&GDMT', 'Guideline Directed Medical Therapy for HFpEF')
        self.Bind(wx.EVT_MENU, self.on_gdmt_gdmt, gdmt_menu_item)

        gdmt_sympt_itme = gdmtMenu.Append(wx.ID_ANY, '&Symptoms', 'Common HFpEF Symptoms')
        self.Bind(wx.EVT_MENU, self.on_gdmt_sympt, gdmt_sympt_itme)

        menu_bar.Append(gdmtMenu, '&GDMT')

        self.SetMenuBar(menu_bar)


    def on_exit(self, event):
        pass

    def on_help(self, event):
        pass

    def on_citation(self, event):
        pass

    def on_gdmt_gdmt(self, event):
        pass

    def on_gdmt_sympt(self, event):
        pass





if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

