import webbrowser
import wx


class Main_Frame(wx.Frame):
    """
    main frame for the H2FpEF calculator
    """

    def __init__(self):
        super().__init__(None, title='H2FpEF - risk calculator', size=(550, 400))

        self.create_menu()
        self.CreateStatusBar()
        self.create_main_panel()


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


    # and now some sizers for the mainpanel plan is a 5 column x 10 row gridbagsizer
    def create_main_panel(self):
        main_panel = wx.Panel(self)
        mp_sizer = wx.GridBagSizer(0,0)

        colblk = wx.StaticText(main_panel, label='  ')
        mp_sizer.Add(colblk, pos=(0,0), flag=wx.ALL, border=5)
        colclivar = wx.StaticText(main_panel, label='Clinical Variable')
        mp_sizer.Add(colclivar, pos=(0,1), flag=wx.ALL, border=5)
        colvalue = wx.StaticText(main_panel, label='Values')
        mp_sizer.Add(colvalue, pos=(0,2), flag=wx.ALL, border=5)
        colpoints = wx.StaticText(main_panel, label='Points')
        mp_sizer.Add(colpoints, pos=(0,3), flag=wx.ALL, border=5)
        colreg = wx.StaticText(main_panel, label='Regression')
        mp_sizer.Add(colreg, pos=(0,4), flag=wx.ALL, border=5)


        keyH2 = wx.StaticText(main_panel, label='H2')
        mp_sizer.Add(keyH2, pos=(1,0), span= (2,1), flag=wx.ALL, border=5)
        cvheavy = wx.StaticText(main_panel, label='Heavy')
        mp_sizer.Add(cvheavy, pos=(1,1), flag=wx.ALL, border=5)
        valheavy = wx.StaticText(main_panel, label='Body mass index > 30 kg/m**2')
        mp_sizer.Add(valheavy, pos=(1,2), flag=wx.ALL, border=5)
        pointheavy = wx.CheckBox(main_panel, -1, label='2')
        mp_sizer.Add(pointheavy, pos=(1,3), flag=wx.ALL, border=5)
        regheavy = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(regheavy, pos=(1,4), flag=wx.ALL, border=5)

        cvhtn = wx.StaticText(main_panel, label='Hypertension')
        mp_sizer.Add(cvhtn, pos=(2,1), flag=wx.ALL, border=5)
        valhtn = wx.StaticText(main_panel, label='2 or more antihypertensive medicines')
        mp_sizer.Add(valhtn, pos=(2,2), flag=wx.ALL, border=5)
        pointhtn = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(pointhtn, pos=(2,3), flag=wx.ALL, border=5)
        reghtn = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(reghtn, pos=(2,4), flag=wx.ALL, border=5)

        keyaf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(keyaf, pos=(3,0), flag=wx.ALL, border=5)
        cvaf = wx.StaticText(main_panel, label='Atrial Fibrillation')
        mp_sizer.Add(cvaf, pos=(3,1), flag=wx.ALL, border=5)
        valaf = wx.StaticText(main_panel, label='Paroxysmal or Persistent')
        mp_sizer.Add(valaf, pos=(3,2), flag=wx.ALL, border=5)
        pointaf = wx.CheckBox(main_panel, -1, label='3')
        mp_sizer.Add(pointaf, pos=(3,3), flag=wx.ALL, border=5)
        regaf = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(regaf, pos=(3,4), flag=wx.ALL, border=5)

        keyph = wx.StaticText(main_panel, label='P')
        mp_sizer.Add(keyph, pos=(4,0), flag=wx.ALL, border=5)
        cvph = wx.StaticText(main_panel, label='Pulmonary Hypertension')
        mp_sizer.Add(cvph, pos=(4,1), flag=wx.ALL, border=5)
        valph = wx.StaticText(main_panel, label='Doppler Echocardiographic\nestimated Pulmonary Artery Systolic\nPressure > 35mmHg')
        mp_sizer.Add(valph, pos=(4,2), flag=wx.ALL, border=5)
        pointph = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(pointph, pos=(4,3), flag=wx.ALL, border=5)
        regph = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(regph, pos=(4,4), flag=wx.ALL, border=5)

        keyold = wx.StaticText(main_panel, label='E')
        mp_sizer.Add(keyold, pos=(5,0), flag=wx.ALL, border=5)
        cvold = wx.StaticText(main_panel, label='Elder')
        mp_sizer.Add(cvold, pos=(5,1), flag=wx.ALL, border=5)
        valold = wx.StaticText(main_panel, label='Age > 60 years')
        mp_sizer.Add(valold, pos=(5,2), flag=wx.ALL, border=5)
        pointold = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(pointold, pos=(5,3), flag=wx.ALL, border=5)
        regold = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(regold, pos=(5,4), flag=wx.ALL, border=5)

        keyf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(keyf, pos=(6,0), flag=wx.ALL, border=5)
        cvf = wx.StaticText(main_panel, label='Filling Pressure')
        mp_sizer.Add(cvf, pos=(6,1), flag=wx.ALL, border=5)
        valf = wx.StaticText(main_panel, label='Doppler Echocardiographic E/e`')
        mp_sizer.Add(valf, pos=(6,2), flag=wx.ALL, border=5)
        pointf = wx.CheckBox(main_panel, -1, label='a')
        mp_sizer.Add(pointf, pos=(6,3), flag=wx.ALL, border=5)
        regf = wx.StaticText(main_panel, label='??')
        mp_sizer.Add(regf, pos=(6,4), flag=wx.ALL, border=5)






        main_panel.SetSizer(mp_sizer)




if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

