import webbrowser
from dataclasses import dataclass
import wx
import wx.html
from pathlib import Path


# a dataclass to store, row metadata and user selections
@dataclass
class H2Fpdata():
    key: str
    clivar: str
    vardescrip: str
    pointval: int
    std_range: tuple[int, int] | str
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


        self.AF = H2Fpdata(key='F', clivar='Atrial Fibrillation', vardescrip='Paroxysmal or Persistent A. Fib',
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
        self.main_panel = self.create_main_panel()

    def create_menu(self):
        """
        Build / set up the menu bar
        """

        menu_bar = wx.MenuBar()

        # About Menu
        aboutMenu = wx.Menu()

        about_menu_item = aboutMenu.Append(wx.ID_ANY, '&About', 'About the H2FpEF')
        self.Bind(wx.EVT_MENU, self.on_about, about_menu_item)

        # Citation Menu and Submenu
        citationMenu = wx.Menu()
        cit_circulation_item = citationMenu.Append(wx.ID_ANY, 'Circulation 2018', 'Journal Circulation 2018')
        self.Bind(wx.EVT_MENU, self.on_circulation, cit_circulation_item)
        cit_circulation_item = citationMenu.Append(wx.ID_ANY, 'AAFP 2025', 'AAFP journal 2025')
        self.Bind(wx.EVT_MENU, self.on_aafp, cit_circulation_item)
        aboutMenu.AppendSubMenu(citationMenu, '&Citation')

        # License menu
        lis_menu_item = aboutMenu.Append(wx.ID_ANY, 'License', 'Application License / Disclaimer')
        self.Bind(wx.EVT_MENU, self.on_license, lis_menu_item)

        aboutMenu.AppendSeparator()

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


    def on_license(self, event):
        self.show_html_dialog("MIT_License.html", title="License and Disclaimer", size=(800,450))


    def on_exit(self, event):
        self.Close()

    def show_html_dialog(self, html_filename, title="HTML Viewer", size=(800,600)):
        """
        Helper function to display HTML files as info for the user.
        It iss called w/the file name w/file to be in the same directory level as the app code
        and the title of the dialog
        some_on_event(self.event):
            show_html_dialog(parent, html_filename, title="HTML Viewer")
        :param html_filename: name of the HTML file
        :param title: title of the dialog
        :param size: defaulted
        :return: None
        """
        dlg = wx.Dialog(self, title=title, size=size, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        html_win = wx.html.HtmlWindow(dlg)
        html_path = Path(__file__).resolve().parent / html_filename
        print(html_path)

        """
        not clear why the .as_uri works but seems stable 
        file:///{html_path}
        and (html_path.as_uri)  <- old school ? deprecated
        
        """
        html_win.LoadPage(f'file:///{html_path}')
        #html_win.LoadPage(html_path.as_uri())

        # Layout
        btn = wx.Button(dlg, wx.ID_OK, label='&OK')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html_win, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        dlg.SetSizer(sizer)

        dlg.ShowModal()
        dlg.Destroy()

    def on_about(self, event):
        self.show_html_dialog("About_text.html", title="About H2FpEF")

    def on_circulation(self, event):
        url = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6202181/'
        webbrowser.open(url)

    def on_aafp(self, event):
        url = 'https://www.aafp.org/pubs/afp/issues/2025/1000/heart-failure-preserved-ejection-fraction.html'
        webbrowser.open(url)

    def on_gdmt_gdmt(self, event):
        self.show_html_dialog("GDMT_Tx.html", title='GDMT - Meds / comorbidities', size=(500, 450))

    def on_gdmt_sympt(self, event):
        self.show_html_dialog("Signs_Symptoms.html", title="Signs and Symptoms", size=(550,600))



    # and now some sizers for the mainpanel plan is a 5 column x 10 row gridbagsizer
    def create_main_panel(self):
        self.main_panel = wx.Panel(self)
        self.mp_sizer = wx.GridBagSizer(10,10)

        self.colblk = wx.StaticText(self.main_panel, label='  ')
        self.mp_sizer.Add(self.colblk, pos=(0,0), flag=wx.ALL, border=5)
        self.colclivar = wx.StaticText(self.main_panel, label='Clinical Variable')
        self.mp_sizer.Add(self.colclivar, pos=(0,1), flag=wx.ALL, border=5)
        self.colvalue = wx.StaticText(self.main_panel, label='Values')
        self.mp_sizer.Add(self.colvalue, pos=(0,2), flag=wx.ALL, border=5)
        self.colpoints = wx.StaticText(self.main_panel, label='Points\nScore')
        self.mp_sizer.Add(self.colpoints, pos=(0,3), flag=wx.ALL, border=5)
        self.colreg = wx.StaticText(self.main_panel, label='Regression\nequation')
        self.mp_sizer.Add(self.colreg, pos=(0,4), flag=wx.ALL, border=5)


        self.keyH2 = wx.StaticText(self.main_panel, label='H2')
        self.mp_sizer.Add(self.keyH2, pos=(1,0), span= (2,1), flag=wx.ALL, border=5)
        self.cvheavy = wx.StaticText(self.main_panel, label='Heavy')
        self.mp_sizer.Add(self.cvheavy, pos=(1,1), flag=wx.ALL, border=5)
        self.valheavy = wx.StaticText(self.main_panel, label='Body mass index > 30 kg/m**2')
        self.mp_sizer.Add(self.valheavy, pos=(1,2), flag=wx.ALL, border=5)
        self.pointheavy = wx.CheckBox(self.main_panel, -1, label='2')
        self.mp_sizer.Add(self.pointheavy, pos=(1,3), flag=wx.ALL, border=5)
        self.regheavy = wx.SpinCtrlDouble(self.main_panel, -1, value='0')
        self.regheavy.SetMinSize((60,-1))
        self.regheavy.SetDigits(2)
        self.regheavy.SetToolTip(self.regValToolTip('BMI'))
        self.mp_sizer.Add(self.regheavy, pos=(1,4), flag=wx.ALL, border=5)

        self.cvhtn = wx.StaticText(self.main_panel, label='Hypertension')
        self.mp_sizer.Add(self.cvhtn, pos=(2,1), flag=wx.ALL, border=5)
        self.valhtn = wx.StaticText(self.main_panel, label='2 or more antihypertensive medicines')
        self.mp_sizer.Add(self.valhtn, pos=(2,2), flag=wx.ALL, border=5)
        self.pointhtn = wx.CheckBox(self.main_panel, -1, label='1')
        self.mp_sizer.Add(self.pointhtn, pos=(2,3), flag=wx.ALL, border=5)
        self.reghtn = wx.StaticText(self.main_panel, label='NA')
        self.reghtn.SetToolTip(self.regValToolTip('HTN'))
        self.mp_sizer.Add(self.reghtn, pos=(2,4), flag=wx.ALL, border=5)

        self.keyaf = wx.StaticText(self.main_panel, label='F')
        self.mp_sizer.Add(self.keyaf, pos=(3,0), flag=wx.ALL, border=5)
        self.cvaf = wx.StaticText(self.main_panel, label='Atrial Fibrillation')
        self.mp_sizer.Add(self.cvaf, pos=(3,1), flag=wx.ALL, border=5)
        self.valaf = wx.StaticText(self.main_panel, label='Paroxysmal or Persistent A. Fib')
        self.mp_sizer.Add(self.valaf, pos=(3,2), flag=wx.ALL, border=5)
        self.pointaf = wx.CheckBox(self.main_panel, -1, label='3')
        self.mp_sizer.Add(self.pointaf, pos=(3,3), flag=wx.ALL, border=5)
        self.regaf = wx.ToggleButton(self.main_panel, -1, label='No A. Fib')
        self.regaf.SetToolTip(self.regValToolTip('AF'))
        self.regaf.Bind(wx.EVT_TOGGLEBUTTON, self.regaf_on_toggle)
        self.mp_sizer.Add(self.regaf, pos=(3,4), flag=wx.ALL, border=5)

        self.keyph = wx.StaticText(self.main_panel, label='P')
        self.mp_sizer.Add(self.keyph, pos=(4,0), flag=wx.ALL, border=5)
        self.cvph = wx.StaticText(self.main_panel, label='Pulmonary Hypertension')
        self.mp_sizer.Add(self.cvph, pos=(4,1), flag=wx.ALL, border=5)
        self.valph = wx.StaticText(self.main_panel, label='Doppler Echocardiographic\nestimated Pulmonary Artery Systolic\nPressure > 35mmHg')
        self.mp_sizer.Add(self.valph, pos=(4,2), flag=wx.ALL, border=5)
        self.pointph = wx.CheckBox(self.main_panel, -1, label='1')
        self.mp_sizer.Add(self.pointph, pos=(4,3), flag=wx.ALL, border=5)
        self.regph = wx.SpinCtrlDouble(self.main_panel, -1, value='0')
        self.regph.SetMinSize((60,-1))
        self.regph.SetDigits(2)
        self.regph.SetToolTip(self.regValToolTip('PH'))
        self.mp_sizer.Add(self.regph, pos=(4,4), flag=wx.ALL, border=5)

        self.keyold = wx.StaticText(self.main_panel, label='E')
        self.mp_sizer.Add(self.keyold, pos=(5,0), flag=wx.ALL, border=5)
        self.cvold = wx.StaticText(self.main_panel, label='Elder')
        self.mp_sizer.Add(self.cvold, pos=(5,1), flag=wx.ALL, border=5)
        self.valold = wx.StaticText(self.main_panel, label='Age > 60 years (years for regression)')
        self.mp_sizer.Add(self.valold, pos=(5,2), flag=wx.ALL, border=5)
        self.pointold = wx.CheckBox(self.main_panel, -1, label='1')
        self.mp_sizer.Add(self.pointold, pos=(5,3), flag=wx.ALL, border=5)
        self.regold = wx.SpinCtrlDouble(self.main_panel, -1, value='0')
        self.regold.SetMinSize((60, -1))
        self.regold.SetDigits(2)
        self.regold.SetToolTip(self.regValToolTip('Elder'))
        self.mp_sizer.Add(self.regold, pos=(5,4), flag=wx.ALL, border=5)

        self.keyf = wx.StaticText(self.main_panel, label='F')
        self.mp_sizer.Add(self.keyf, pos=(6,0), flag=wx.ALL, border=5)
        self.cvf = wx.StaticText(self.main_panel, label='Filling Pressure')
        self.mp_sizer.Add(self.cvf, pos=(6,1), flag=wx.ALL, border=5)
        self.valf = wx.StaticText(self.main_panel, label='Doppler Echocardiographic E/e` > 9')
        self.mp_sizer.Add(self.valf, pos=(6,2), flag=wx.ALL, border=5)
        self.pointf = wx.CheckBox(self.main_panel, -1, label='1')
        self.mp_sizer.Add(self.pointf, pos=(6,3), flag=wx.ALL, border=5)
        self.regf = wx.SpinCtrlDouble(self.main_panel, -1, value='0')
        self.regf.SetMinSize((60, -1))
        self.regf.SetDigits(2)
        self.regf.SetToolTip(self.regValToolTip('FP'))
        self.mp_sizer.Add(self.regf, pos=(6,4), flag=wx.ALL, border=5)

        # score total rows
        self.pntscore = wx.StaticText(self.main_panel, label='Point - Score: 0 - 9')
        self.mp_sizer.Add(self.pntscore, pos=(7, 2), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        self.pntvalue = wx.StaticText(self.main_panel, label='0 - 9')
        self.mp_sizer.Add(self.pntvalue, pos=(7, 3), flag=wx.ALL, border=5)

        self.regscore = wx.StaticText(self.main_panel, label='Regression - Score: 0.0 - 1.0')
        self.mp_sizer.Add(self.regscore, pos=(8, 2), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        self.regvalue = wx.StaticText(self.main_panel, label='0.0 - 1.0')
        self.mp_sizer.Add(self.regvalue, pos=(8, 4), flag=wx.ALL, border=5)

        # the scoring nomogram
        # need to scale for inital display and w/resize events
        frame_width, frame_height = (550, 100)
        self.nomo_img = wx.Image('nihms_score_1.png', wx.BITMAP_TYPE_PNG)
        self.nomo_img = self.nomo_img.Rescale(frame_width, frame_height, quality=wx.IMAGE_QUALITY_HIGH)
        self.nomo_bitmap = wx.StaticBitmap(self.main_panel, -1, wx.Bitmap(self.nomo_img))
        self.mp_sizer.Add(self.nomo_bitmap, pos=(9,0), span=(1,9), flag=wx.ALL, border=5)

        #add cal / reset buttons
        self.pointcalc = wx.Button(self.main_panel, -1, "Points Calculate")
        self.pointcalc.Bind(wx.EVT_BUTTON, self.calc_points)
        self.mp_sizer.Add(self.pointcalc, pos=(10,1), flag=wx.ALL, border=5)

        self.regcalc = wx.Button(self.main_panel, -1, "Regression Calculate")
        self.regcalc.Bind(wx.EVT_BUTTON, self.reg_calc_score)
        self.mp_sizer.Add(self.regcalc, pos=(11,1), flag=wx.ALL, border=5)

        self.reset = wx.Button(self.main_panel, -1, "Reset")
        self.reset.Bind(wx.EVT_BUTTON, self.on_reset)
        self.mp_sizer.Add(self.reset, pos=(10,2), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)

        self.main_panel.SetSizer(self.mp_sizer)
        #return main_panel

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
        :return: pointscore - - the points calculated / score
        name is the Key for the dict datarows and datapoint is the dataclass H2pdata data
        """
        self.pointscore = 0

        for name, datapoint in self.datarows.items():
            if self.statckbx(datapoint.ckboxname):
                self.pointscore += int(datapoint.pointval)
        self.pntvalue.SetLabel(str(self.pointscore))
        return self.pointscore

    ##########  calc using regression formula

    def reg_calc_score(self, event):
        """
        Again iterate through the GUI via datarows, validate the user inputs and feedback / updated as needed
        compounded by 3 different ctrls, SpinCtrlDouble (may need to change for now just using the ranges used by the
        study but will have to open up possible values (but compatible with life!)
        :param event: button event
        :return: ProbHFpEF
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
        C5 - Filling pressure (E/e`) from Echocardiogram
        But all these vales are in the dataclass for each element - regvalue

            regdata = datapoint.regval
            regctrl = datapoint.regctrltype
            print( regdata, regctrl)

        Have to use the getattr again (see above) seems a bit convoluted, and need to read about this more

        So while calculating the risk score will also be building the report string output as well
        want to try to build as an HTML string
        """
        self.regstr = ''
        logOdds = -9.19174463966566
        for key, datapoint in self.datarows.items():
            ctrl = getattr(self, datapoint.regname, None)
            if ctrl:
                if isinstance(ctrl, wx.SpinCtrlDouble):
                    datapoint.userreg = ctrl.GetValue()
                    self.regstr += f'{datapoint.vardescrip} = {datapoint.userreg}, <br>'
                    #print(f'for {datapoint.vardescrip} = {datapoint.userreg} <br>,')
                elif isinstance(ctrl, wx.ToggleButton):
                    datapoint.userreg = ctrl.GetValue()
                    datapoint.userreg = 1 if datapoint.userreg else 0
                    self.regstr += f'{datapoint.vardescrip} = {'has' if datapoint.userreg else 'dose not have'} A. Fib,<br>'
                elif isinstance(ctrl, wx.StaticText):
                    datapoint.userreg = ctrl.GetLabel()
                    datapoint.userreg = 0

            # add the product of each of these to get the final Log Odds value (F2 in comment above)
            logOdds += float(datapoint.userreg) * datapoint.regval

        G2 = 2.71828182845904**logOdds

        self.ProbHFpEF = G2 / (1 + G2) * 100

        self.regvalue.SetLabel(f'{self.ProbHFpEF:.3f}')

        self.regrptstr = (f'<p>Using the regression equation to calculate the H2FpEF risk score = {self.ProbHFpEF:.3f}</p> <br>' 
                     f'{self.regstr}<p>')
        print (self.regrptstr)

        return (self.ProbHFpEF, self.regstr)

    def on_reset(self, event):
        # reset all the control
        for key, datapoint in self.datarows.items():
            ctrl = getattr(self, datapoint.regname, None)
            if ctrl:
                if isinstance(ctrl, wx.SpinCtrlDouble):
                    ctrl.SetValue(0.0)
                elif isinstance(ctrl, wx.ToggleButton):
                    ctrl.SetValue(False)
                    ctrl.SetLabel("No A. Fib")
            ctrl = getattr(self, datapoint.ckboxname, None)
            if ctrl:
                if isinstance(ctrl, wx.CheckBox):
                    ctrl.SetValue(False)

        # now clear  the StaticText in the GUI
        self.pntvalue.SetLabel('0-9')
        self.regvalue.SetLabel('0-1')



if __name__ == "__main__":
    app = wx.App()
    frm = Main_Frame()
    frm.Show()
    app.MainLoop()

