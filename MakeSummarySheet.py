#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 08:15:14 2023

@author: jasonsteffener
"""
import fpdf

class PDF(fpdf.FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Neuropsychological Testing Summary Report', 1, 1, 'C')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Neurocognitive Mapping Laboratory, University of Ottawa, Canada', 1, 0, 'C')

''' Normative data
Stroop_VictoriaInter_NCM_Young_RawMean = 1.415801766
Stroop_VictoriaInter_NCM_Young_RawSTD = 0.205181135
Stroop_VictoriaInter_NCM_Young_RawN = 50
Stroop_VictoriaInter_NCM_Old_RawMean = 1.615588408
Stroop_VictoriaInter_NCM_Old_RawSTD = 0.247573225
Stroop_VictoriaInter_NCM_Old_RawN = 42
Stroop_VictoriaInter_CLSA_Old_RawMean = 2.159
Stroop_VictoriaInter_CLSA_Old_RawNSTD = 0.731
Stroop_VictoriaInter_CLSA_Old_RawN = 29675
Stroop_NCMInter_NCM_Young_RawMean = 1.318152463
Stroop_NCMInter_NCM_Young_RawSTD = 0.165441421
Stroop_NCMInter_NCM_Young_RawN = 50
Stroop_NCMInter_NCM_Old_RawMean = 1.390883002
Stroop_NCMInter_NCM_Old_RawSTD = 0.370165985
Stroop_NCMInter_NCM_Old_RawN = 45
'''


def MakeSummaryPDF(results):    
    ch = 6
    pdf = PDF() # Instance of custom class
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(w=0, h=20, txt=results['subid'], ln=1)
    pdf.set_font('Arial', '', 16)
    pdf.cell(w=30, h=ch, txt="Date: ", ln=0)
    pdf.cell(w=30, h=ch, txt= results['visitid'], ln=1)

    pdf.set_font('Arial', 'B', 16)
    pdf.ln(ch)
    pdf.cell(w = 50, h = ch, txt="Stroop", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# of trials", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Accuracy", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Resp. Time", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt = "   Color", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['StrpC_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['StrpC_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3}'.format(results['StrpC_RT']), ln = 1)
    pdf.cell(w = 50, h = ch, txt = "   Word", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['StrpW_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['StrpW_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['StrpW_RT']), ln = 1)
    pdf.cell(w = 50, h = ch, txt = "   Color/Word", ln = 1)
    pdf.cell(w = 50, h = ch, txt = "     Congruent", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['StrpCW_Con_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['StrpCW_Con_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['StrpCW_Con_RT']), ln = 1)
    pdf.cell(w = 50, h = ch, txt = "     Incongruent", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['StrpCW_Incon_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['StrpCW_Incon_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['StrpCW_Incon_RT']), ln = 1)
    pdf.ln(ch)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Antonyms", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# Attempted", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Accuracy", ln = 1)
    pdf.cell(w = 50, h = ch, txt="", ln = 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['Ant_NResp']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['Ant_Acc']), ln = 1)
    pdf.ln(ch)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="NART (max 45)", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Accuracy", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# Errors", ln = 1)
    pdf.cell(w = 50, h = ch, txt="", ln = 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['NART_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['NART_NErrors']), ln = 1)
    pdf.ln(ch)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Digit Span", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# of Trials", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Capacity", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt="   Forward", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['DSFor_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['DSFor_Capacity']), ln = 1)
    pdf.cell(w = 50, h = ch, txt="   Backward", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['DSBack_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['DSBack_Capacity']), ln = 1)
    pdf.ln(ch)
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Patt. Comparison", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# of trials", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Accuracy", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Resp. Time", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt = "   Load 1", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['PComp_Load01_NResp']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['PComp_Load01_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['PComp_Load01_RT']), ln = 1)
    pdf.cell(w = 50, h = ch, txt = "   Load 2", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['PComp_Load02_NResp']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['PComp_Load02_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['PComp_Load02_RT']), ln = 1)
    pdf.cell(w = 50, h = ch, txt = "   Load 3", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['PComp_Load03_NResp']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['PComp_Load03_Acc']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.3f}'.format(results['PComp_Load03_RT']), ln = 1)

    pdf.ln(ch)    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Matrix Reas.", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "# of Trials", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Acc.", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt="", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['Matr_NTrials']), ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['Matr_Acc']), ln = 1)
    
    pdf.ln(ch)    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Verbal DMS", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Capacity", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt="", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['DMSBeh1_DMS_Cap']), ln = 1)
    
    pdf.ln(ch)    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 50, h = ch, txt="Spatial DMS", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Capacity", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 50, h = ch, txt="", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:0.2f}'.format(results['VSTMBeh1_VSTM_Cap']), ln = 1)    
    
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 80, h = ch, txt="Selective Reminding Task", ln = 0)
    pdf.cell(w = 50, h = ch, txt = "Score", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 80, h = ch, txt="   Total Recall", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTImm_TotRecall']), ln = 1)
    pdf.cell(w = 80, h = ch, txt="   Long Term Recall", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTImm_LTR']), ln = 1)
    pdf.cell(w = 80, h = ch, txt="   Long Term Storage", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTImm_LTS']), ln = 1)
    pdf.cell(w = 80, h = ch, txt="   Consistent Long Term Retrieval", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTImm_CLTR']), ln = 1)
    pdf.cell(w = 80, h = ch, txt="   # of Intrusions", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTImm_Nintr']), ln = 1)    
    pdf.cell(w = 80, h = ch, txt="   Delayed Recall (max 12)", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTDel_Recall']), ln = 1)    
    pdf.cell(w = 80, h = ch, txt="   # of Intrusions", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTDel_Nintr']), ln = 1)        
    pdf.cell(w = 80, h = ch, txt="   Recognition (max 12)", ln = 0)
    pdf.cell(w = 50, h = ch, txt = '{:d}'.format(results['SRTRecog_Hits']), ln = 1)    
    pdf.ln(ch)    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 80, h = ch, txt="W Card Sorting Task", ln = 0)
    pdf.cell(w = 40, h = ch, txt = "# Trials", ln = 0)
    pdf.cell(w = 40, h = ch, txt = "# Errors", ln = 0)
    pdf.cell(w = 40, h = ch, txt = "# Pers Errors", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 80, h = ch, txt = '', ln = 0)    
    pdf.cell(w = 40, h = ch, txt = '{:d}'.format(results['WCST_NTrials']), ln = 0)    
    pdf.cell(w = 40, h = ch, txt = '{:d}'.format(results['WCST_NErrors']), ln = 0)    
    pdf.cell(w = 40, h = ch, txt = '{:d}'.format(results['WCST_NPersErrors']), ln = 1)    
    pdf.ln(ch)    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w = 30, h = ch, txt="N Back", ln = 0)
    pdf.cell(w = 30, h = ch, txt = "# of trials", ln = 0)
    pdf.cell(w = 30, h = ch, txt = "Hit Rate", ln = 0)
    pdf.cell(w = 30, h = ch, txt = "Hit RT", ln = 0)
    pdf.cell(w = 30, h = ch, txt = "F.A. Rate", ln = 0)
    pdf.cell(w = 30, h = ch, txt = "F.A. RT", ln = 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w = 30, h = ch, txt = "   Load 0", ln = 0)
    try:
        pdf.cell(w = 30, h = ch, txt = '{:0.1f}'.format(results['NBack_Load00_N']), ln = 0)        
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load00_HIT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load00_HitRT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load00_FA']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load00_FaRT']), ln = 1)
        pdf.cell(w = 30, h = ch, txt = "   Load 1", ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.1f}'.format(results['NBack_Load01_N']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load01_HIT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load01_HitRT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load01_FA']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load01_FaRT']), ln = 1)
        pdf.cell(w = 30, h = ch, txt = "   Load 2", ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.1f}'.format(results['NBack_Load02_N']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load02_HIT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load02_HitRT']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.2f}'.format(results['NBack_Load02_FA']), ln = 0)
        pdf.cell(w = 30, h = ch, txt = '{:0.3f}'.format(results['NBack_Load02_FaRT']), ln = 1)    
    except:
        pass
    
    fname_out = './' + results['subid'] + '_' + results['visitid'] + '.pdf'
    pdf.output(fname_out, 'F')
    
