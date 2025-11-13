import webbrowser
from collections import namedtuple
from dataclasses import dataclass
from operator import itemgetter
from typing import Tuple

import wx

# a dataclass to store, row metadata and user selections
@dataclass
class H2Fpdata():
    key: str
    clivar: str
    vardescrip: str
    pointval: int
    std_range: Tuple[int, int] | str
    ckboxname: str
    ckboxval: bool
    regname: str
    regval: float
    userreg: str
    name: str
    regctrltype: str
    #ctrlname: str




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
        super().__init__(None, title='H2FpEF - risk calculator  (patients with EF >= 50%)', size=(600, 700), style= wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)

        # table data
        # not done yet but may use the metadata to automate the build of the initial GUI rows :-)
        self.BMI = H2Fpdata(key="H2", clivar="Heavy", vardescrip='Body mass index > 30 kg/m**2',
                            pointval=2, std_range=(22.8, 40.4), ckboxname = 'pointheavy', ckboxval='False', regname='regheavy',
                            userreg='0', regval=0.130730156015681,name='BMI', regctrltype="SpinCtrlDouble")

        # had to get a little tricky here as std_range expects 2 values so :-)
        self.HTN = H2Fpdata(key='H2', clivar='Hypertension', vardescrip='2 or more antihypertensive medicines',
                            pointval='1', ckboxname='pointhtn', std_range=('Not', 'Applicable'),
                            ckboxval='False', regname='reghtn', userreg='0', regval=0, name='HTN', regctrltype='StaticTxt')


        self.AF = H2Fpdata(key='F', clivar='Atrial Fibrillation', vardescrip='Paroxysmal or Persistent',
                            pointval='3', std_range=('Toggle for ', 'present or not'), ckboxname="pointaf", ckboxval='False',
                           regname='regaf', userreg=False, regval=1.69968057294513, name='AF', regctrltype='ToggleButton')

        self.PH = H2Fpdata(key='P', clivar='Pulmonary Hypertension',
                           vardescrip='Doppler Echocardiographic estimated Pulmonary Artery Systolic Pressure > 35mmHg',
                            pointval='1', std_range=(25,50), ckboxname='pointph', regctrltype= 'SpinCtrlDouble',
                            ckboxval='False', regname='regph', userreg='0', regval=0.051963758732548, name='PH')

        self.Elder = H2Fpdata(key='E', clivar='Elder', vardescrip='Age > 60 years',
                            pointval='1', std_range=(41, 79), ckboxname='pointold', regctrltype='SpinCtrlDouble',
                            ckboxval='False', regname='regold', userreg='0', regval=0.0451129471272832, name='Elder')

        self.FP = H2Fpdata(key='F', clivar='Filling Pressure', vardescrip='Doppler Echocardiographic E/e` > 9',
                            pointval='1', std_range=(6,21), ckboxname='pointf', regctrltype='SpinCtrlDouble',
                            ckboxval='False', regname='regf', userreg='0', regval=0.0858634402456586, name='FP')

        # now to put these into a dict so I can iterate threw for calculating scores, resets, validation
        # key will be a hash of the string name and item will beh the dataclass
        self.datarows = {
            'BMI': self.BMI, 'HTN': self.HTN, 'AF': self.AF,'PH': self.PH, 'Elder': self.Elder, 'FP': self.FP
        }
        #print(datarows)

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
        self.regheavy = wx.SpinCtrlDouble(main_panel, -1, value='0')
        self.regheavy.SetMinSize((60,-1))
        self.regheavy.SetDigits(2)
        self.regheavy.SetToolTip(self.regValToolTip('BMI'))
        mp_sizer.Add(self.regheavy, pos=(1,4), flag=wx.ALL, border=5)

        self.cvhtn = wx.StaticText(main_panel, label='Hypertension')
        mp_sizer.Add(self.cvhtn, pos=(2,1), flag=wx.ALL, border=5)
        self.valhtn = wx.StaticText(main_panel, label='2 or more antihypertensive medicines')
        mp_sizer.Add(self.valhtn, pos=(2,2), flag=wx.ALL, border=5)
        self.pointhtn = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointhtn, pos=(2,3), flag=wx.ALL, border=5)
        self.reghtn = wx.StaticText(main_panel, label='NA')
        self.reghtn.SetToolTip(self.regValToolTip('HTN'))
        mp_sizer.Add(self.reghtn, pos=(2,4), flag=wx.ALL, border=5)

        self.keyaf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(self.keyaf, pos=(3,0), flag=wx.ALL, border=5)
        self.cvaf = wx.StaticText(main_panel, label='Atrial Fibrillation')
        mp_sizer.Add(self.cvaf, pos=(3,1), flag=wx.ALL, border=5)
        self.valaf = wx.StaticText(main_panel, label='Paroxysmal or Persistent')
        mp_sizer.Add(self.valaf, pos=(3,2), flag=wx.ALL, border=5)
        self.pointaf = wx.CheckBox(main_panel, -1, label='3')
        mp_sizer.Add(self.pointaf, pos=(3,3), flag=wx.ALL, border=5)
        self.regaf = wx.ToggleButton(main_panel, -1, label='No A. Fib')
        self.regaf.SetToolTip(self.regValToolTip('AF'))
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
        self.regph = wx.SpinCtrlDouble(main_panel, -1, value='0')
        self.regph.SetMinSize((60,-1))
        self.regph.SetDigits(2)
        self.regph.SetToolTip(self.regValToolTip('PH'))
        mp_sizer.Add(self.regph, pos=(4,4), flag=wx.ALL, border=5)

        self.keyold = wx.StaticText(main_panel, label='E')
        mp_sizer.Add(self.keyold, pos=(5,0), flag=wx.ALL, border=5)
        self.cvold = wx.StaticText(main_panel, label='Elder')
        mp_sizer.Add(self.cvold, pos=(5,1), flag=wx.ALL, border=5)
        self.valold = wx.StaticText(main_panel, label='Age > 60 years (years for regression)')
        mp_sizer.Add(self.valold, pos=(5,2), flag=wx.ALL, border=5)
        self.pointold = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointold, pos=(5,3), flag=wx.ALL, border=5)
        self.regold = wx.SpinCtrlDouble(main_panel, -1, value='0')
        self.regold.SetMinSize((60, -1))
        self.regold.SetDigits(2)
        self.regold.SetToolTip(self.regValToolTip('Elder'))
        mp_sizer.Add(self.regold, pos=(5,4), flag=wx.ALL, border=5)

        self.keyf = wx.StaticText(main_panel, label='F')
        mp_sizer.Add(self.keyf, pos=(6,0), flag=wx.ALL, border=5)
        self.cvf = wx.StaticText(main_panel, label='Filling Pressure')
        mp_sizer.Add(self.cvf, pos=(6,1), flag=wx.ALL, border=5)
        self.valf = wx.StaticText(main_panel, label='Doppler Echocardiographic E/e`')
        mp_sizer.Add(self.valf, pos=(6,2), flag=wx.ALL, border=5)
        self.pointf = wx.CheckBox(main_panel, -1, label='1')
        mp_sizer.Add(self.pointf, pos=(6,3), flag=wx.ALL, border=5)
        self.regf = wx.SpinCtrlDouble(main_panel, -1, value='0')
        self.regf.SetMinSize((60, -1))
        self.regf.SetDigits(2)
        self.regf.SetToolTip(self.regValToolTip('FP'))
        mp_sizer.Add(self.regf, pos=(6,4), flag=wx.ALL, border=5)

        # score total rows
        self.pntscore = wx.StaticText(main_panel, label='Point - Score: 0 - 9')
        mp_sizer.Add(self.pntscore, pos=(7, 2), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        self.pntvalue = wx.StaticText(main_panel, label='0 - 9')
        mp_sizer.Add(self.pntvalue, pos=(7, 3), flag=wx.ALL, border=5)

        self.regscore = wx.StaticText(main_panel, label='Regression - Score: 0.0 - 1.0')
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
        self.pointcalc.Bind(wx.EVT_BUTTON, self.calc_points)
        mp_sizer.Add(self.pointcalc, pos=(10,1), flag=wx.ALL, border=5)

        self.regcalc = wx.Button(main_panel, -1, "Regression Calculate")
        self.regcalc.Bind(wx.EVT_BUTTON, self.reg_calc_score)
        mp_sizer.Add(self.regcalc, pos=(11,1), flag=wx.ALL, border=5)

        self.reset = wx.Button(main_panel, -1, "Reset")
        mp_sizer.Add(self.reset, pos=(10,2), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)

        main_panel.SetSizer(mp_sizer)

    def regaf_on_toggle(self, event):
        if self.regaf.GetValue():
            self.regaf.SetLabel("Has A. Fib")
            self.userreg = 1
        else:
            self.regaf.SetLabel("No A. Fib")
            self.userreg = 0

    def regValToolTip(self, name) -> str:
        """
        helper function to generate the tooltips for each of the regression data entry controls
        :param name: of the dataclass H2pdata element
        :return: str - The range of values in the study population for this clinical element was from x to y
        """
        x, y = self.datarows[name].std_range
        return f"The range of values in the study population\nfor this clinical element was from {x} to {y}\n(allows 2 decimal digits)"

    ########### score for points screening

    def statckbx(self, checkboxname) -> bool:
        """helper function to get the value of a checkbox - calc_points function
        it returns a bool True / False - depending onn if the checkbox is checked or unchecked
        the checkboxes are unchecked by default and on reset
        -
        :param checkboxname:
        :return: bool
        """
        ckbx = getattr(self, checkboxname, None)
        if isinstance(ckbx, wx.CheckBox):
            is_checked = ckbx.GetValue()
            return is_checked


    def calc_points(self, event):
        """
        Iterate through the datarows adding up the points and calculate the score
        :param event: from Points Calculate button
        :return: the points calculated / score
        name is the Key for the dict datarows and datapoint is the dataclass H2pdata data
        """
        pointscore = 0

        for name, datapoint in self.datarows.items():
            if self.statckbx(datapoint.ckboxname):
                pointscore += int(datapoint.pointval)
        self.pntvalue.SetLabel(str(pointscore))
        return pointscore

    ##########  calc using regression formula

    def reg_calc_score(self, event):
        """
        Again iterate through the GUI via datarows, validate the user inputs and feedback / updated as needed
        compounded by 3 different ctrls, SpinCtrlDouble (may need to change to SpinCtrlDoubleDouble
        for now just using the ranges used by the study but will have to open up possible values (but compatible
        with life!)
        :param event: button event
        :return: regressionscore
        The regression equation from the 2018 article; a grip for me is that none of data point has more then
        3 significant digits while equation circa 18 digits?  See the excel/calc spreadsheet

        Probability of HFpEF = G2 / (1 + G2) * 100

        G2 = 2.71828182845904^F2 (where F2 is the Logs odds)
        F2 = =-9.19174463966566
            + 0.0451129471272832*C4
            + 0.130730156015681*C1
            + 0.0858634402456586*C5
            + 0.051963758732548*C3
            + 1.69968057294513*C2

        C1 - BMI in Kg/m^2
        C2 - A. Fib a 0 if present or 1 if present
        C3 - PASP in mmHg
        C4 - age in years
        C5 - Filling pressure (E/e`)
        But all these vales on the the dataclass for each element - regvalue

            regdata = datapoint.regval
            regctrl = datapoint.regctrltype
            print( regdata, regctrl)

        Have to use the getattr again (see above) seems a bit convoluted, and need to read about this more
        """
        logOdds = -9.19174463966566
        for key, datapoint in self.datarows.items():
            ctrl = getattr(self, datapoint.regname, None)
            if ctrl:
                if isinstance(ctrl, wx.SpinCtrlDouble):
                    datapoint.userreg = ctrl.GetValue()
                elif isinstance(ctrl, wx.ToggleButton):
                    datapoint.userreg = ctrl.GetValue()
                    datapoint.userreg = 1 if datapoint.userreg else 0
                elif isinstance(ctrl, wx.StaticText):
                    datapoint.userreg = ctrl.GetLabel()
                    datapoint.userreg = 0
            print(f'{datapoint.regval}  {datapoint.userreg}')
            # add the product of each of these to get the final Log Odds value (F2 in comment above)
            logOdds += float(datapoint.userreg) * datapoint.regval
            print(f'{datapoint.userreg:.2f}')
        print(f'log Odds: {logOdds:.3f}')
        G2 = 2.71828182845904**logOdds
        print(f'G2: {G2:.3f}')
        ProbHFpEF = G2 / (1 + G2) * 100
        print(f'ProbHFpEF: {ProbHFpEF:.3f}')
        self.regvalue.SetLabel(f'{ProbHFpEF:.3f}')




if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

