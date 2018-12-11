#!/usr/bin/env python

""" Data Extraction"""

_author_ ="Hector H Corzo"
_copyright_ = "Copyright 2018, Boston, MA"

import os
import re
import openpyxl 
import sys
import collections
import json
import copy
import stat

'''Input to  generate'''
input_gen=False
Basis_Traslation={'6-311++g**':'6311ppGdp'}
CompR={'Memory':'%mem=80GB','CPU':'%nprocshared=12'}
CompRSTR='%mem=80GB\n%nprocshared=12\n'
Input1={'Basis':'6-311++g**','Method':'B3LYP','Charge':0,'Multy':1,'Extra':'opt freq=noraman','Overlays':'No','Name_extention':'B3LYP_6311ppGdp_01.gjf'}
Input2={'Basis':'6-311++g**','Method':'B3LYP','Charge':1,'Multy':2,'Extra':'opt freq=noraman','Overlays':'No','Name_extention':'B3LYP_6311ppGdp_12.gjf'}
Input3={'Basis':'6-311++g**','Method':'M06','Charge':0,'Multy':1,'Extra':'opt freq=noraman','Overlays':'No','Name_extention':'M06_6311ppGdp_01.gjf'}
Inputs=[Input1,Input2,Input3]

print(Inputs[0])





'''path to this file'''
path=os.path.dirname(os.path.realpath(__file__))
pathorigin=path     #used to save workbook in this location

'''path of the log files'''
logFilesFolder='/Logs_Test2'
excelName='Test_Data.xlsx'
excelName_Logs_Status='Log_Status.xlsx'
excelName_Logs_Data='Log_General_Data.xlsx'
print('Inputs will be located at:',path)


################ General  Dictionaries ################ 

Status_Data={'Dir':'',
    'JobType':'',
    'Stoichiometry':'',  
    'Version':'',         
    'JobKeys':'',
    'CharMult':'',
    'Standard basis':'',     
    'Generals_E':{'PG':''},         
    'Geom':'',
    'Normal':'NO',
    'Date':0,
    'CPU_Time':{'Days':0,'Hrs':0,'Min':0,'Sec':0},
    'Elapsed_Time':{'Days':0,'Hrs':0,'Min':0,'Sec':0}
}



General_Data={'Dir':'',
              'Molecule':'',
              'Basisset':'',          
              'Frequencies':'None',        
              'SymmFull':'',
              'SymmLA':'',
              'SymmLCA':'',
              'Charge':'',
              'Multy':'',
              'Geom':'None',
              'GeomRF':'None',
              'MxForce':'No',
              'MDisp':'No',         
              'RMSForce':'No',
              'RMSDisp':'No',
              'ZPC':0,
              'TCE':0,
              'TCH':0,
              'TCG':0,
              'SEZPC':0,
              'SETCE':0,
              'SETCH':0,
              'SETCG':0,
              'TotE':0,
              'TotCV':0,
              'TotS':0
}



Basis_ID={'STO-3G':'P01', 
          '3-21G':'P02',
          '6-21G':'P03',
          '4-31G':'P04',
          '6-31G':'P05',
          '6-311G':'P06',
          '6-311++G**':'P07',
          '6-311++G(2df,2pd)':'P08',
          '6-311++G(3df,3pd)':'P09',
          '6-v':'10',
          '6-w':'11',
          '6-x':'12',
          '6-y':'13',
          '6-z':'14',
          '6-z1':'15',
          'cc-pVDZ':'D16',
          'cc-pVTZ':'D17',
          'cc-pVQZ':'D18',
          'cc-pV5Z':'D19',
          'cc-pV6Z':'D20',
          'cc-v':'21',
          'cc-w':'22',
          'cc-x':'23',
          'cc-y':'24',
          'cc-z':'25',
          'Aug-cc-pVDZ':'D26',
          'Aug-cc-pVTZ':'D27',
          'Aug-cc-pVQZ':'D28',
          'Aug-cc-pV5Z':'D29',
          'Aug-cc-pV6Z':'D30',
          'Aug-v':'31',
          'Aug-w':'32',
          'Aug-x':'33',
          'Aug-y':'34',
'Aug-z':'35'}


########### General Routines ####################################################


def Input_Dir_gen(Intname):
    if input_gen:
        print('Directories for the input files are about to be created')
        for n, Inptx in enumerate(Inputs):
            Dir_name='/Input'+str(n+1)
            if not os.path.exists(pathorigin+Dir_name):#Checking if the directory already exist
                os.makedirs(pathorigin+Dir_name)#Create the directory if it does not exist
                print('The directory: ',Dir_name,' was created')
    return  print('The path of the directories is ',pathorigin)

#######################################################################################################

def Input_file(Keyname,StrGeom,Inputs):
    for n, Inptx in enumerate(Inputs):
        Dir_name='/Input'+str(n+1)
        print(Dir_name)
        print(pathorigin)
        if not os.path.exists(pathorigin+Dir_name):#Checking if the directory already exist
            print('The directory ', Dir_name, 'does not exist')
            break
            #os.makedirs(path+Dir_name)#Create the directory if it does not exist
        elif os.path.exists(pathorigin+Dir_name):
            
            print('Info for the input ',Inptx)

            Chr=Inptx['Charge']
            Mult=Inptx['Multy']
            Meth=Inptx['Method']
            Baset=Inptx['Basis']
            ExtJob=Inptx['Extra']
            NExtention=Inptx['Name_extention'] 
            Add_Name=Keyname[:-4]+'_input_'+NExtention
            L1=CompRSTR # This line can be done by a diccionary
            L2='#p '+Meth+' '+Baset+ ' '+ExtJob+'\n'
            L3='\n'
            L4='Geom from '+ Keyname[:-4]+'\n'
            L5='\n'
            L6=str(Chr)+' '+str(Mult)+'\n'

            InputInfom=L1+L2+L3+L4+L5+L6+StrGeom+'\n'
            GauInpfile=open(pathorigin+Dir_name+'/'+Add_Name, "w")
            GauInpfile.write(InputInfom)
            GauInpfile.close()
            #print(Add_Name)
        #else:
         #   file_Run=open(path+Dir_name+'/'+Intname, "w")
    return

Input_Dir_gen('test')    









def makehash():
    return collections.defaultdict(makehash)
##############Keys###########################################################

Status_keys=['Normal termination','Job cpu','Elapsed','Version']
Job_keys=['Opt','Freq','MP2','HF','UHF','M06','OVGF','Extraoverlay']
#General_Data_Keys=[Molecule,Basisset,Freque
GeneralE_Keys=['HF','State','MP2','PG','S2','S2A']
Gen_Data={'Molecule':0,'Charge':0,'Multy':0,'Basisset':0,'Symm':0, 'Frequencies':0}
Energy_Data={'HF':0,'CCSD':0,'CCSD(T)':0,'State':0,'MP2':0, 'PG':0}
Energy_keys={'HF','State','MP2','PG'}
#Status_Data={'Normal':0,'Days':0,'Hrs':0,'Min':0,'Sec':0, 'Date':0}
Symm_Keys=['Full point group', 'Largest Abelian subgroup', 'Largest concise Abelian subgroup']
#Kserch={'State=':(1,State),'MP2=':(1,E_MP2),'HF=':(1,E_HF),'PG=':(1,PG),'Stoichiometry':(1,Molecule),'(AMU),':(1,Freq),'basis:':(1,Basis),'Multiplicity':(2,(Charg,Mult)),'Elapsed':(4,(Day,Hrs,Min,Sect))}


#############################################################################
def adjust_column_width(worksheet):
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.1
        worksheet.column_dimensions[column].width = adjusted_width        
################################################################################

def reverse(xfile):
   ''' This report lines in reverse with an extra empty line between line'''  
   xfile.seek(0, os.SEEK_END)
   position = xfile.tell()
   line = ''
   while position >= 0:
      xfile.seek(position)
      next_char = xfile.read(1)
      if next_char == "\n":
         yield line[::-1]
         line = ''
      else:
          line += next_char
      position -= 1
   yield line[::-1]

################################################################################
''' This report two lines at the time without a empty line between them''' 
def reversex2(xfile):
    ''' This report two lines in reverse at the time without an empty line between them'''    
    xfile.seek(0, os.SEEK_END)
    position = xfile.tell()
    line = ''
    L2=False
    while position >= 0:
       xfile.seek(position)
       next_char = xfile.read(1)
       if next_char == "\n":
          if L2:
            yield line[::-1]
            line = ''
            L2=False
          else:
            L2=True 
       elif next_char == " ": 
            line +=''  
       else:
          line += next_char 
       position -= 1
    yield line[::-1]        

################################################################################
def reverse2x(xfile):
    linex=''
    position1=xfile.tell()
    line=reverse_position(xfile)
    print('position1',position1)
    if position1 >= 0:
     line1= (next(reverse_position(xfile)))
     print(line1)
     position2=xfile.tell()
     print('position2',position2)
     if position2 >= 0:
      line2=next(reverse_position(xfile))
      print(line2)
     else:
         line2=''
     linex=line1+line2
     position = xfile.seek(position1)
    return linex
################################################################################
def reverse_position(xfile):
#   xfile.seek(0, os.SEEK_END)
   position = xfile.tell()
   line = ''
   while position >= 0:
      xfile.seek(position)
      next_char = xfile.read(1)
      if next_char == "\n":
         yield line[::-1]
         line = ''
      else:
          line += next_char
      position -= 1
   yield line[::-1]
   
################################################################################   
''' Transforming data to have the right format'''            
def Ext_X(Xword,Xwords,xfile,Kserch,DicData):
    (INo,Elems)=Kserch[Xword]
    if INo==1:
        (name,y,x,Type)=Elems
        if y!=0:
           Xwords=Jump_Line(y,xfile)  
        if Type=='R':
            DicData[name]=float(Xwords[x])
        elif Type=='S':    
            DicData[name]=Xwords[x]
    elif INo>1:    
      for elem in Elems:
        (name,y,x,Type)=elem
        if y!=0:
           Xwords=Jump_Line(y,xfile)
        if Type=='R':
            DicData[name]=float(Xwords[x])
        elif Type=='S':    
            DicData[name]=Xwords[x]
################################################################################  

def Trans_type(S,S_type):
    
    if S_type=="S":
       Sval=S 
    elif S_type=="R":
        Sval= float(S)
    elif S_type=="I":
        Sval= int(S)
    return Sval                
################################################################################

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

################################################################################


def Geom_Coor_Extraction(Filex,DataDic):

 ''' This routine extract the coordenarte format geometry after an optimization job'''

 OptConv=[]
 GxoptConv=['MxForce','MDisp','RMSForce','RMSDisp']
# First Checking that the all covergence criteria were met 
 for i in GxoptConv:
     OptConv.append(DataDic[i])
 if all(x=='YES'for x in OptConv):
     GeomD={}
     GFound=False
     while not GFound:
        Line_next=Filex.readline()
        if 'Input orientation' in Line_next:
            Line_next=Filex.readline()
            while not GFound:
                Line_next=Filex.readline()
                if '-------' in Line_next: #Checking where the geom block starts
                    while not GFound:
                        Line_next=Filex.readline()
                        if '-------' in Line_next: #checking if the geom blocks ends
                            DataDic['Geom']=GeomD #Saving the geometry in the main diccionary 
                            GFound=True
                            return
                        else:    
                            Lstr=Line_next.split()
                            #PosKey=Lstr[0]
                            GeomD[Lstr[0]]=Lstr[1:]
                            
 else:
     print('The Geomatry optimization criteria were not met')
 return    #    print('line3',line)

################################################################################
''' Extracts the lines between two matches and return them in a list''' 
def lines_between(S_start,S_end,Filex,option):
    Return_List=[]
    Line_next=Filex.readline()# This is the first line that is exactly the next line of the current position in the file
    if option==1: # the Starting match was already found
        while S_end not in Line_next:
        #if S_end not in Line_next:
            Return_List.append(Line_next)
            Line_next=Filex.readline()
        if S_end in Line_next:
            return Return_List
    elif option==2: #we need to add the option where the starting line has not be found yet
        return
        print(Line_next)
    

################################################################################
"Pulling Frequencies and their symmetries, they are returned into a diccionary"

def Extract_Freq(Filex):
    Retun_Dic={}
    Line1=Filex.readline()
    Line2=Filex.readline()
    Line3=Filex.readline()
    while ' -------------------' not in Line3:
        if ' Frequencies --' in Line3:
            for no,sym,freq in zip(Line1.split(),Line2.split(),Line3.split()[2:]):
                Retun_Dic[no]=(sym,float(freq))
        Line1=Line2
        Line2=Line3
        Line3=Filex.readline()
    return Retun_Dic


################################################################################

"Pulling E, CV, S totals  and their units, they are returned into a diccionary"
def Extract_TermTotals(Filex):
    Retun_Dic={}
    Equival_Dic={'(Thermal)':'TotE','CV':'TotCV','S':'TotS'}
    Line1=Filex.readline()
    Line2=Filex.readline()
    Line3=Filex.readline()
    while ' Electronic' not in Line3:
        if ' Total' in Line3:
            #Zipit=list(zip(Line1.split(),Line2.split(),Line3.split()[2:]))
            for key,Unit,Val in zip(Line1.split()[1:],Line2.split(),Line3.split()[1:]):
               # print(no,sym,freq)
                no=Equival_Dic[key]
                Retun_Dic[no]=(float(Val),Unit)
        Line1=Line2
        Line2=Line3
        Line3=Filex.readline()
    return Retun_Dic    

#############################################################################

'''Saving the information related to the status into the excel file
Option 1 : Sets the data for Status
Option 2 : Sets the data for General data '''
def workbook_add_info(worksheet,Status_Inf,ID,headers,Opt):
    
    
    lstexcel=[ID]
   
    if Opt==1:
      Info_excel=['Stoichiometry','CharMult','JobType','Normal','Dir']  
      for Keyinf in Info_excel:
          Info=Status_Inf[Keyinf]
          if Keyinf=='JobType':
              Info=Status_Inf[Keyinf].replace("\n","")
          lstexcel.append(Info)
     

    elif Opt==2:
        #Headers=['ID Name','Stoichiometry','Basis','Freq','SymmFull','ZPC','Directory']
        Info_excel=['Molecule','Basisset','Frequencies','SymmFull','ZPC','Dir']
        for Keyinf in Info_excel:
          Info=Status_Inf[Keyinf]
          if Keyinf=='Frequencies':
              Info=Status_Inf[Keyinf]['1'][1]
              #Info=Status_Inf[Keyinf].replace("\n","")
          lstexcel.append(Info)
    worksheet.append(lstexcel)    
    return

#############################################################################
        
def adjust_column_width(worksheet):
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.1
        worksheet.column_dimensions[column].width = adjusted_width    

#############################################################################
def workbook_prep_status(worksheet):
    #Headers=['Stoichiometry','CharMult','Calculation Type','Normal Termination?','Job routing','Directory']
    Headers=['ID Name','Stoichiometry','CharMult','Job Routing','Normal Termination?','Directory']
    worksheet.append(Headers)
    return

def workbook_prep_Data(worksheet):
    #You can choose what you want to display in your excel file here
    #Headers=['Stoichiometry','CharMult','Calculation Type','Normal Termination?','Job routing','Directory']
    Headers=['ID Name','Stoichiometry','Basis set','Freq','Point group','ZP Correction','Directory']
    worksheet.append(Headers)
    return

#############################################################################
'''This set up the excel file if it does not exist or open it if it does
option 1 : Generaltes the status data
option 2 : Generates the General data''' 
def excel_file_setup(pathorigin,ExcelName,opt):
     if not os.path.exists(pathorigin+'/'+ExcelName):#Checking if the directory already exist
         print('************************create',pathorigin,ExcelName) 
         workbook = openpyxl.Workbook()
         General_worksheet = workbook.active
         if opt==1:
             General_worksheet.title = 'Status'         
             workbook_prep_status(General_worksheet)
         elif opt==2:
             General_worksheet.title = 'Generals'         
             workbook_prep_Data(General_worksheet)             
     else:
         print('************************load')
         workbook =openpyxl.load_workbook(pathorigin + '/' +ExcelName)
         General_worksheet = workbook.active
     return workbook,General_worksheet
############################################################################# 

''' Transforming data from line to have the right format
opt=1: The unique value to extrac from a line
opt=2 Several values to extract from a line, for this the keys for the different values are in Keys_Dic'''      

class LineExtractionError_Y(ValueError):
    pass
            
def  Extract_LineX(line,Keys_Dic,Coltor_Dic,opt):
 Line_spliting=line.split()
 if opt==1:
    for i in Coltor_Dic:
       Dic_Inf=Keys_Dic[i]
       D_y=Dic_Inf['y'] # number of rows to move, for a single line this is 0
       if D_y!=0:
          raise LineExtractionError_Y(Dic_Inf)
           
       D_ty=Dic_Inf['t'] #Type of the data 
       
       D_x=Dic_Inf['x'] # number of cols to move 
       
        #Saving value  
       Coltor_Dic[i]=Trans_type(Line_spliting[D_x],D_ty)       

 if opt==2:      
    for i in Keys_Dic:
        
        
       Dic_Inf=Keys_Dic[i]
       #print(i,Dic_Inf)
       D_y=Dic_Inf['y'] # number of rows to move, for a single line this is 0
       if D_y!=0:
          raise LineExtractionError_Y(Dic_Inf)
           
       D_ty=Dic_Inf['t'] #Type of the data 
       
       D_x=Dic_Inf['x'] # number of cols to move 
       
        #Saving value
#       print('lll',Line_spliting)
       Coltor_Dic[i]=Trans_type(Line_spliting[D_x],D_ty)        


################################################################################ 

def Geom_Dic_to_String(Geom_Dic):
    ''' This routine transform a Geometry dictionary where each line is a list into a string '''
    Nlines=len(Geom_Dic)
    Geomstr=''
    for nx in range(1,Nlines+1):
        Geomline=' '.join(Geom_Dic[str(nx)])+'\n'
        Geomstr=Geomstr+Geomline
    return Geomstr    
    
with open(pathorigin+'/ksearch.json') as kfile: # Open the json with the keys
    json_decoded = json.load(kfile)                                        

    
def Status_Data_Extraction(Xfile,Status_K,Status_D):
    '''This extracts the information about the status from the log file and fills out the Status_D(Status_Data) Dictionary'''
    TimeK=1
    GeneralK=1
    GeneralEDic=Status_D['Generals_E']
    Linex=''
    Line1=''
    LComman=0
    Pfound=False    
    #Job Type:
    Pline = Xfile.readline()
    while not Pfound:
        line = Xfile.readline()
        if '#' in line:
          Status_D['JobType']=line
          Job_lst=[]
          General_lst=[]
          LComman=Xfile.tell()
          for Jobx in Job_keys:
              if Jobx.lower() in line.lower(): 
                  Job_lst.append(Jobx)  
                  words=line.split()
          Status_D['JobKeys']=Job_lst
        elif 'Stoichiometry' in line:
          words=line.split()
          Status_D['Stoichiometry']=words[1]
        elif 'Standard basis:' in line:
          words=line.split()
          print(words)
          Status_D['Standard basis']=words[2]
          Pfound=True
          break
      
    #Job Times #############################################################  
    for no,line in enumerate(reverse(Xfile)):
        if TimeK==0:
            break 
        elif any(x in line for x in Status_K):
            if 'Normal termination' in line:
                Status_K.remove('Normal termination')
                words=line.split()
                Status_D['Normal']='Yes'
                valuesBlock='/'.join(words[6:])  
                Status_D['Date']=valuesBlock
            elif 'Elapsed time:' in line:  
                    Status_K.remove('Elapsed')
                    #Pulling dict of keys 
                    XKeysD=json_decoded['Elapsed time']
                    #Pulling dict to fill 
                    XDataD=Status_D['Elapsed_Time']
                    Extract_LineX(line,XKeysD,XDataD,1)
            elif 'Job cpu time:' in line:
                Status_K.remove('Job cpu')
                # If "Job cpu" is found, chances are that Elapsed time was not reported 
                # therefore I remove the Elapsed time key                  
                if 'Elapsed' in Status_K:
                    Status_K.remove('Elapsed')
                    #Pulling dict of keys
                XKeysD=json_decoded['Job cpu time']
                    #Pulling dict to fill 
                XDataD=Status_D['CPU_Time']
                #Extracting the information we need from the line
                Extract_LineX(line,XKeysD,XDataD,1)
                TimeK=0
                break

    #Job Generals #########################################################

    for no,line in enumerate(reversex2(Xfile)):
            Linex=line+Line1
            Line1=line
            if GeneralK==0:
                return LComman
                break
    
            ValuesBLK=''.join(Linex)
            #print('Block',ValuesBLK)
            if any(x in ValuesBLK for x in GeneralE_Keys):
                ValuesBLK_s=re.split(r'[\\\s]\s*',ValuesBLK)
                for vK in GeneralE_Keys:
                    if vK in ValuesBLK:
                        Element_fnd=[k for k in ValuesBLK_s if vK in k]
                        Element_line=Element_fnd[0]
                        if vK=='PG': #Point Group
                             PG_Line=find_between(Element_line,'PG=','[')
                             GeneralEDic[vK]=PG_Line
                             #print(PG_Line)

                        elif vK=='S2':#<S2>
                            S2_Line=Element_line.split('S2=',1)[1]
                            GeneralEDic[vK]=float(S2_Line)
                        elif vK=='S2A':#<S2> after projection
                            S2A_Line=Element_line.split('S2A=',1)[1]
                            GeneralEDic[vK]=float(S2A_Line)
                        elif vK=='HF':# HF or DFT energy
                            HF_Line=Element_line.split('HF=',1)[1]
                            GeneralEDic[vK]=float(HF_Line)                            
                        elif vK=='State': #State
                            State_Line=Element_line.split('State=',1)[1]
                            GeneralEDic[vK]=State_Line
############ I am adding this as an extra I need to check this at some point
                        elif vK=='MP2': #State
                            MP2_Line=Element_line.split('MP2=',1)[1]
                            GeneralEDic[vK]=float(MP2_Line)
                            
            if '\\Version=' in ValuesBLK:
               
                            Status_K.remove('Version')

                            #Extracting the Gaussaian version 
                            Version_Line=find_between(line,'Version=','\Sta')
                            Status_D['Version']=Version_Line
                            Geom_List=['\\Version'.join(line.split("\\Version")[:1])]
                            Geom_List[0]=Geom_List[0].replace(' ','')
                            for no2,line2 in enumerate(reverse_position(Xfile)):                    
                                Geom_List.insert(0,line2)
                                if '\\\\' in line2:
                                    print('line2',line2)
                                    break
                            LLCnt=Geom_List[0].count('\\\\')
                            Geom_List[0]=Geom_List[0].split("\\",LLCnt)[2:][0]
                            Status_D['CharMult']=Geom_List[0].split("\\")[2:][0]
                            Geom_List[0]=Geom_List[0].split("\\")[3:][0]
                            Geom_List2=list(filter(lambda a: a != '', Geom_List))
                            Geom_List3=''.join(Geom_List2)
                            Geom_List3.replace(' ','')
                            Geom_List3.replace(' ','')
                            Geom_List3=Geom_List3.split('\\')
                            if Geom_List3[-1] =='':
                                    Geom_List3= Geom_List3[:-1]
                            Geom_List3=[StrinX.replace(' ','') for StrinX in Geom_List3]
                            Status_D['Geom']=Geom_List3
                            #If we found the version already chances are that we would not find more General information
                            GeneralK=0  
                            #break 

    return LComman 



    
def General_Data_Extraction(Xfile,LzCn,JobType,General_D):
    
    '''This extracts the information about the status from the log file and fills out the General_D(General_Data) Dictionary'''

    #RedantGeom=True
    Thermal=['ZPC','TCE','TCH','TCG','SEZPC','SETCE','SETCH','SETCG','TotE','TotCV','TotS']
    List_Keys=[*General_D]
#    print(List_Keys)
    List_Keys.remove('Dir')
#    print(JobType)
    if 'opt' not in JobType:
        List_Keys.remove('Geom')
        List_Keys.remove('GeomRF')
        List_Keys.remove('MxForce')
        List_Keys.remove('MDisp')
        List_Keys.remove('RMSForce')
        List_Keys.remove('RMSDisp')
        
    if 'freq' not in JobType:
        List_Keys.remove('Frequencies')
        for i in Thermal:# If there are not freq there are not termal corrections 
            List_Keys.remove(i)
        if 'GeomRF' in List_Keys:
            List_Keys.remove('GeomRF')
            
        #RedantGeom=False
    GxkeysL=[]
    GxkeysD={}
    GxoptL=['Maximum Force','RMS     Force','Maximum Displacement','RMS     Displacement']
    GxoptConv=['MxForce','MDisp','RMSForce','RMSDisp']
    with open(pathorigin+'/ksearch.json') as kfile:
            json_decoded = json.load(kfile)
            for i in List_Keys:
                keywrd=json_decoded[i]['k']
                GxkeysL.append(keywrd)
                GxkeysD[keywrd]={i:json_decoded[i]}
    Ctrl_GxkeysL=list(GxkeysL)
    Ctrl_List_Key=list(List_Keys)
    Xfile.seek(LzCn)
    #Searching in file:
    for no,line in enumerate(Xfile):
        if any(x in line for x in GxkeysL):
            if 'Frequencies' in  Ctrl_List_Key:
                if 'reduced masses (AMU), force constants' in line:
                   General_D['Frequencies']=Extract_Freq(Xfile)
                   Ctrl_GxkeysL.remove('(AMU), force')
                   Ctrl_List_Key.remove('Frequencies')
                   GxkeysL=Ctrl_GxkeysL[:]
            if 'GeomRF' in Ctrl_List_Key:#Extraction of the redundant geometry if there is a freq calculation 
                if  'Redundant internal' in line:
                    GeomL=lines_between('Redundant internal','Recover connectivity',Xfile,1)#Extracting redundant geometry
                    General_D['GeomRF']=GeomL #saving the geometry
                    Ctrl_GxkeysL.remove('Redundant internal')
                    Ctrl_List_Key.remove('GeomRF')
                    GxkeysL=Ctrl_GxkeysL[:]
            if 'Geom' in Ctrl_List_Key:
                if 'Optimization completed.' in line:
                    Geom_Coor_Extraction(Xfile,General_D)
                    Ctrl_GxkeysL.remove('Optimization completed.')
                    for xkey in GxoptL:
                        Ctrl_GxkeysL.remove(xkey)
                    Ctrl_GxkeysL=Ctrl_GxkeysL+Symm_Keys #add Symm parameters for new geom
                    GxkeysL=Ctrl_GxkeysL[:]
                    Ctrl_List_Key.remove('Geom')
            for vK in GxkeysL: # General one line key-y=0 extractor 
                if vK in line:
                    XKeysD=GxkeysD[vK]
                    Extract_LineX(line,XKeysD,General_D,2)
                    if vK not in GxoptL:
                        Ctrl_GxkeysL.remove(vK)
            if 'Sum of electronic and thermal Free Energies=' in line:
                Totals=Extract_TermTotals(Xfile)
                for Totkey in Totals:
                    General_D[Totkey]=Totals[Totkey]
                    Ctrl_List_Key.remove(Totkey)
                Ctrl_GxkeysL.remove('NoneCtr-TE') # we are control specific in case there are more NoneCtr in the future
                Ctrl_GxkeysL.remove('NoneCtr-CV')
                Ctrl_GxkeysL.remove('NoneCtr-S')
            #Updating Keys
            if len(Ctrl_GxkeysL)==0:
#                print ('Ctrl_Gxkeys', Ctrl_GxkeysL)
                return
            GxkeysL=Ctrl_GxkeysL[:]
            #print('line5',line)
#            print('GxkeysL end',GxkeysL)
    return


############################################################################# 

'''Save the information collected in the dictionary into a JSON file
Option 0 is for the Scratch.json
Option 1 is for the Log_status.json
Option 2 is for the Log_general.json
option 3 is for the User_name.json'''
def Json_saving(Key_Name,pathorigin,Final_Dic,Opt,User_name):

            # Let's choose the JSON file
            Options=('/Scratch.json','/Log_status.json','/Log_general.json','/'+str(User_name))
            JsonfileName=Options[Opt]
            # Let's check if the JSON file exist already

            if not os.path.exists(pathorigin+JsonfileName):#Checking if the JSON file already exist
                JSONfile=open(pathorigin+JsonfileName, "w")
                JSONfile.write('{ }')
                JSONfile.close()
                print('The ', JsonfileName[1:], ' file was created')
            
            # Let's now save the info in the JSON file:
            with open(pathorigin+JsonfileName) as jsonfile:
                Status_decoded = json.load(jsonfile)
            if Key_Name  in Status_decoded:
                print (40 * '*')
                print('Data for ID:\n\n',Key_Name,'\n\n already exist in',JsonfileName[1:],'\n')
                print (40 * '-')
                print('\nChoose between the following options:\n')
                print('1).- Display current JSON file info')
                print('2).- Display current extracted info')
                print('3).- Remplace old info with new info')
                print('4).- Ignore current info')
                print (40 * '*')
                is_valid=0
                while not is_valid :
                    try :
                        choice = int (input('Enter your choice [1-4] : ') )
                        ### Take action as per selected menu-option ###
                        if choice == 1:
                            print ('Info of this key in the JSON file:\n')
                            print(Status_decoded[Key_Name])
                            is_valid = 0
                        elif choice == 2:
                            print ('Current info for this key:\n')
                            print(Final_Dic[Key_Name])
                            is_valid = 0
                        elif choice == 3:
                            print ('The JSON file will be updated with the new information')
                            Status_decoded.update(Final_Dic)
                            with open(pathorigin+'/Log_status.json', 'w') as jsonfile:
                                json.dump(Status_decoded,jsonfile)
                            is_valid = 1
                            return
                        elif choice == 4:
                            print ('The information extracted will be ignored\n')
                            is_valid = 1
                            return 
                        else:
                                print ("Invalid number. Try again...")
                                is_valid = 0                 
                    except ValueError as e :
                        print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
            else:    
                Status_decoded.update(Final_Dic)
                with open(pathorigin+JsonfileName, 'w') as jsonfile:
                    json.dump(Status_decoded,jsonfile)
            return




############################################################################# 
'''This generates ID name for the logFiles based on the status information the ID has the following form STE-ABE-CM-B_ID-HFV'''
def Name_ID_Gen(Status_Inf):
    STE=Status_Inf['Stoichiometry']
    GEINF=Status_Inf['Generals_E']
    ABE=GEINF['PG']
    HFV='-000.000'
    if "HF" in GEINF:
        HFV=GEINF["HF"]
    CM=Status_Inf['CharMult']
    Base=Status_Inf['Standard basis']
    B_ID=Basis_ID[Base]
    return str(STE)+'-PG'+str(ABE)+'-CM'+str(CM[0])+str(CM[2])+'-B'+str(B_ID)+'-HF' +str(HFV)
#############################################################################    
            
    #Info_sets=['Stoichiometry','JobType','Normal','JobKeys','Normal','Dir']

    #Info_sets=['CharMult','JobType','Normal','JobKeys','Normal','Dir']

#############################################################################

'''General Extraction routine'''
def Extraction_Logs(logFiles,worksheet1,worksheet2):
    #final = makehash()

    Status_Inf=copy.deepcopy(Status_Data)
    print(logFiles)
    for file_y in logFiles:
        final={}
        final2={}
        Status_keys_ctr=Status_keys[:]
        Status_Inf=copy.deepcopy(Status_Data)
        #print('00file',file_y)
        # Setting the Directory of the log file:
        Status_Inf["Dir"]=file_y
        with open(file_y, 'r') as f:
            # Extract the Status data:
            LNComman=Status_Data_Extraction(f,Status_keys_ctr,Status_Inf)
            print("Status_Data",Status_Inf,LNComman)
            # Setting the key of this entry, the key is it just the name of the file: 
            Key_Name=os.path.basename(f.name)
            #print(Key_Name,'Key_Name\n\n')
            Status_Inf['FileName']=Key_Name
            Name_ID=Name_ID_Gen(Status_Inf)
            final[Name_ID]=Status_Inf
            # Let's now save the info in the Log_status JSON file:
            Json_saving(Name_ID,pathorigin,final,1,0)
            # Saving the information in the excel file:
            workbook_add_info(worksheet1,Status_Inf,Name_ID,0,1)
            # If status reported Normal termination we can start the search of the information we need
            if Status_Inf['Normal'] =='Yes':# Normal termination then we can get the data
                General_Inf=copy.deepcopy(General_Data)
                General_Inf["Dir"]=file_y
                JobTkeys= Status_Inf['JobType']  
                General_Data_Extraction(f,LNComman,JobTkeys,General_Inf)
                print('Final_Dic\n',General_Inf)
                final2[Name_ID]=General_Inf
                #Save the data in a JSON file
                Json_saving(Name_ID,pathorigin,final2,2,0)
                # Saving the information in the excel file:
                workbook_add_info(worksheet2,General_Inf,Name_ID,0,2)
                
             # if the user ask to generate inputs with this optimized geometry   
            if input_gen:

                Geominput=General_Inf['Geom']
                #print(Geominput)
                #print('size', len(Geominput))
                String_Geom=Geom_Dic_to_String(Geominput) 
                Input_file(Key_Name,String_Geom,Inputs)
                break
                print( Status_Inf['JobKeys'] ,'Here')
                print('f',f)
    
                for no,line in enumerate(f):
                    print( Status_Inf['Normal'] ,'Here')
                    print('lineeeee',line)
                    
                    if '#' in line:
                        print('lineeeee',line)
                        
                    
    return





def new_dictionary(logFiles):
  for file_y in logFiles:  
    with open(file_y, 'r') as f:
        ###Starting from the end###
# Status data
       Status_Data_Extraction(f,Status_keys,Status_Data)
       #print('OutData*****',Status_Data)
       #print('OUTTTTTTEXT')
       
       for no,line in enumerate(reverse(f)):
            if len(Status_keys)==0:
               break 
            if any(x in line for x in Status_keys):
               Xkeys=[]
               if 'Normal termination' in line:
                   Status_keys.remove('Normal termination')
                   words=line.split()
                   #print(words)
                   #break
                   Status_Data['Normal']='Yes'
                   valuesBlock='/'.join(words[6:])  
                   Status_Data['Date']=valuesBlock                 
               elif 'Job cpu time:' in line:
                   Status_keys.remove('Job cpu')
                   # If "Job cpu" is found already chances are that Elapsed time was not reported 
                   # therefore I remove the Elapsed time                   
                   if 'Elapsed' in Status_keys.keys():
                       Status_keys.remove('Elapsed')
                   #Pulling dict of keys
                   XKeysD=json_decoded['Job cpu time']
                   
                   #Pulling dict to fill 
                   XDataD=Status_Data['CPU_Time']
                                      
                   # Extracting the information we need from the line
                   Extract_LineX(line,XKeysD,XDataD,1)  
               elif 'Elapsed time:' in line:  
                   Status_keys.remove('Elapsed')
                    #Pulling dict of keys 
                   XKeysD=json_decoded['Elapsed time']
#                   print('Xkeys***',XKeysD) 
                    #Pulling dict to fill 
                   XDataD=Status_Data['Elapsed_Time']
                   
                   Extract_LineX(line,XKeysD,XDataD,1)  
                   break 

               words=line.split()
  return





logFiles=[]              
for path, subdirs, files in os.walk(path+logFilesFolder):     
        for name in files:
            if os.path.join(path, name)[len(os.path.join(path, name))-4:len(os.path.join(path, name))]=='.log':
                logFiles.append(os.path.join(path,name))

           # logdata=new_dictionary(logFiles)
        workbook1,worksheet1=excel_file_setup(pathorigin,excelName_Logs_Status,1)
        workbook2,worksheet2=excel_file_setup(pathorigin,excelName_Logs_Data,2)
        Extraction_Logs(logFiles,worksheet1,worksheet2)
        adjust_column_width(worksheet1)
        adjust_column_width(worksheet2)
        workbook1.save(pathorigin + '/' + excelName_Logs_Status)
        workbook2.save(pathorigin + '/' + excelName_Logs_Data)
#print(path)
#print(logFiles)
#print(logdata)

Ekeys=[]
Gkeys=[]


with open(pathorigin+'/ksearch.json') as kfile:
            json_decoded = json.load(kfile)
            for i in Energy_keys:
                Ekeys.append(json_decoded[i]['k'])
            for i in  GeneralE_Keys:
                Gkeys.append(json_decoded[i]['k'])
#print( Gkeys)                
#print( Ekeys)  
