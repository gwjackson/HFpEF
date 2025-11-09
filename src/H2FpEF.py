import webbrowser
from collections import namedtuple
import wx


class Main_Frame(wx.Frame):
    """
    main frame for the H2FpEF calculator

    clinic data is dic of  key : namedtuples
        {
        clinic_variable (str) : (ckbox=str, points=int, reg_value=float, std_range=str, key=str),
        ...
        {
    """


    def __init__(self):
        super().__init__(None, title='H2FpEF - risk calculator', size=(600, 700), style= wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)

        # table data
        screen_data = namedtuple('ckbox',['points', 'reg_value', 'std_range', 'row_lable'])
        tb_date = {
            'pointheavy': screen_data(2, 0.130730156015681, '22.5 - 40.4', 'H2'),
            'pointhtn'  : screen_data(1, 0, '22.5 - 40.4', 'H2'),
            'pointaf'   : screen_data(3, 1.69968057294513, '0 - 1', 'F'),
            'pointph'   : screen_data(1, 0.051963758732548, '25 - 50', 'P'),
            'pointold'  : screen_data(1, 0.0451129471272832, '41 - 79', 'E'),
            'pointf'    : screen_data(1, 0.0858634402456586, '6 - 21', 'F'),
        }
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
        mp_sizer = wx.GridBagSizer(10,10)

        self.colblk = wx.StaticText(main_panel, label='  ')
        mp_sizer.Add(self.colblk, pos=(0,0), flag=wx.ALL, border=5)
        self.colclivar = wx.StaticText(main_panel, label='Clinical Variable')
        mp_sizer.Add(self.colclivar, pos=(0,1), flag=wx.ALL, border=5)
        self.colvalue = wx.StaticText(main_panel, label='Values')
        mp_sizer.Add(self.colvalue, pos=(0,2), flag=wx.ALL, border=5)
        self.colpoints = wx.StaticText(main_panel, label='Points\nScore')
        mp_sizer.Add(self.colpoints, pos=(0,3), flag=wx.ALL, border=5)
        self.colreg = wx.StaticText(main_panel, label='Regression\nequation')
        mp_sizer.Add(self.colreg, pos=(0,4), flag=wx.ALL, border=5)


        self.keyH2 = wx.StaticText(main_panel, label='H2')
        mp_sizer.Add(self.keyH2, pos=(1,0), span= (2,1), flag=wx.ALL, border=5)
        self.cvheavy = wx.StaticText(main_panel, label='Heavy')
        mp_sizer.Add(self.cvheavy, pos=(1,1), flag=wx.ALL, border=5)
        self.valheavy = wx.StaticText(main_panel, label='Body mass index > 30 kg/m**2')
        mp_sizer.Add(self.valheavy, pos=(1,2), flag=wx.ALL, border=5)
        self.pointheavy = wx.CheckBox(main_panel, -1, label='2')
        mp_sizer.Add(self.pointheavy, pos=(1,3), flag=wx.ALL, border=5)
        self.regheavy = wx.SpinCtrl(main_panel, -1, value='0')
        self.regheavy.SetMinSize((60,-1))
        self.regheavy.SetRange(15, 50)
        mp_sizer.Add(self.regheavy, pos=(1,4), flag=wx.ALL, border=5)

        self.cvhtn = wx.StaticText(main_panel, label='Hypertension')
        mp_sizer.Add(self.cvhtn, pos=(2,1), flag=wx.ALL, border=5)
        self.valhtn = wx.StaticText(main_panel, label='2 or more antihypertensive medicines')
        mp_sizer.Add(self.valhtn, pos=(2,2), flag=wx.ALL, border=5)
        self.pointhtn = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointhtn, pos=(2,3), flag=wx.ALL, border=5)
        self.reghtn = wx.StaticText(main_panel, label='NA')
        mp_sizer.Add(self.reghtn, pos=(2,4), flag=wx.ALL, border=5)

        self.keyaf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(self.keyaf, pos=(3,0), flag=wx.ALL, border=5)
        self.cvaf = wx.StaticText(main_panel, label='Atrial Fibrillation')
        mp_sizer.Add(self.cvaf, pos=(3,1), flag=wx.ALL, border=5)
        self.valaf = wx.StaticText(main_panel, label='Paroxysmal or Persistent')
        mp_sizer.Add(self.valaf, pos=(3,2), flag=wx.ALL, border=5)
        self.pointaf = wx.CheckBox(main_panel, -1, label='3')
        mp_sizer.Add(self.pointaf, pos=(3,3), flag=wx.ALL, border=5)
        self.regaf = wx.ToggleButton(main_panel, -1, label='Toggle Me')
        self.regaf.Bind(wx.EVT_TOGGLEBUTTON, self.regaf_on_toggle)
        mp_sizer.Add(self.regaf, pos=(3,4), flag=wx.ALL, border=5)

        self.keyph = wx.StaticText(main_panel, label='P')
        mp_sizer.Add(self.keyph, pos=(4,0), flag=wx.ALL, border=5)
        self.cvph = wx.StaticText(main_panel, label='Pulmonary Hypertension')
        mp_sizer.Add(self.cvph, pos=(4,1), flag=wx.ALL, border=5)
        self.valph = wx.StaticText(main_panel, label='Doppler Echocardiographic\nestimated Pulmonary Artery Systolic\nPressure > 35mmHg')
        mp_sizer.Add(self.valph, pos=(4,2), flag=wx.ALL, border=5)
        self.pointph = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointph, pos=(4,3), flag=wx.ALL, border=5)
        self.regph = wx.SpinCtrl(main_panel, -1, value='0')
        self.regph.SetMinSize((60,-1))
        self.regph.SetRange(20, 60)
        mp_sizer.Add(self.regph, pos=(4,4), flag=wx.ALL, border=5)

        self.keyold = wx.StaticText(main_panel, label='E')
        mp_sizer.Add(self.keyold, pos=(5,0), flag=wx.ALL, border=5)
        self.cvold = wx.StaticText(main_panel, label='Elder')
        mp_sizer.Add(self.cvold, pos=(5,1), flag=wx.ALL, border=5)
        self.valold = wx.StaticText(main_panel, label='Age > 60 years (years for regression)')
        mp_sizer.Add(self.valold, pos=(5,2), flag=wx.ALL, border=5)
        self.pointold = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointold, pos=(5,3), flag=wx.ALL, border=5)
        self.regold = wx.SpinCtrl(main_panel, -1, value='0')
        self.regold.SetRange(35, 100)
        self.regold.SetMinSize((60, -1))
        mp_sizer.Add(self.regold, pos=(5,4), flag=wx.ALL, border=5)

        self.keyf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(self.keyf, pos=(6,0), flag=wx.ALL, border=5)
        self.cvf = wx.StaticText(main_panel, label='Filling Pressure')
        mp_sizer.Add(self.cvf, pos=(6,1), flag=wx.ALL, border=5)
        self.valf = wx.StaticText(main_panel, label='Doppler Echocardiographic E/e`')
        mp_sizer.Add(self.valf, pos=(6,2), flag=wx.ALL, border=5)
        self.pointf = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointf, pos=(6,3), flag=wx.ALL, border=5)
        self.regf = wx.SpinCtrl(main_panel, -1, value='0')
        self.regf.SetRange(6, 21)
        self.regf.SetMinSize((60, -1))
        self.regf.SetRange(1, 30)
        mp_sizer.Add(self.regf, pos=(6,4), flag=wx.ALL, border=5)

        # score total rows
        self.pntscore = wx.StaticText(main_panel, label='Point - Score')
        mp_sizer.Add(self.pntscore, pos=(7, 2), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        self.pntvalue = wx.StaticText(main_panel, label='0 - 9')
        mp_sizer.Add(self.pntvalue, pos=(7, 3), flag=wx.ALL, border=5)

        self.regscore = wx.StaticText(main_panel, label='Regression - Score')
        mp_sizer.Add(self.regscore, pos=(8, 2), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        self.regvalue = wx.StaticText(main_panel, label='0.0 - 1.0')
        mp_sizer.Add(self.regvalue, pos=(8, 4), flag=wx.ALL, border=5)

        # the scoring nomogram
        # need to scale for inital display and w/resize events
        frame_width, frame_height = (550, 100)
        self.nomo_img = wx.Image('nihms_score_1.png', wx.BITMAP_TYPE_PNG)
        self.nomo_img = self.nomo_img.Rescale(frame_width, frame_height, quality=wx.IMAGE_QUALITY_HIGH)
        self.nomo_bitmap = wx.StaticBitmap(main_panel, -1, wx.Bitmap(self.nomo_img))
        mp_sizer.Add(self.nomo_bitmap, pos=(9,0), span=(1,9), flag=wx.ALL, border=5)

        #add cal / reset buttons
        self.pointcalc = wx.Button(main_panel, -1, "Points Calculate")
        mp_sizer.Add(self.pointcalc, pos=(10,1), flag=wx.ALL, border=5)

        self.regcalc = wx.Button(main_panel, -1, "Regression Calculate")
        mp_sizer.Add(self.regcalc, pos=(11,1), flag=wx.ALL, border=5)

        self.reset = wx.Button(main_panel, -1, "Reset")
        mp_sizer.Add(self.reset, pos=(10,2), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)

        main_panel.SetSizer(mp_sizer)

    def regaf_on_toggle(self, event):
        if self.regaf.GetValue():
            self.regaf.SetLabel("Has A. Fib")
        else:
            self.regaf.SetLabel("No A. Fib")






if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

