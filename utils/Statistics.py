import pandas as pd
class FindStats:    
    def __init__(self, branch_code) -> None:
        self.overall_data=pd.DataFrame(columns=["Branch","Registered","Appeared","Absent","Failed","Passed","Percentage"])
        self.branch_code=branch_code
        self.stats_df=pd.DataFrame(columns=["subject","Registered","Appeared","Absent","Failed","Passed","Pass Percentage"])
        self.topper_df=pd.DataFrame(columns=["Place","Roll No","Points","SGPA"])
        
    def statsCal(self,result_df,grades,branch_code):
        pass_grades=[]
        fail_grades=[]
        absent_grades=[]

        #For finding the grades that represent pass,fail and absent
        for i in range(len(grades)):
            if grades[i][1] !=0 and grades[i][2].capitalize()=="P":
                pass_grades.append(grades[i][0])
            elif grades[i][1] ==0 and grades[i][2].capitalize()=="P":
                pass_grades.append(grades[i][0])
            else:
                if grades[i][3].upper()=="ABSENT":
                    absent_grades.append(grades[i][0])
                else:
                    fail_grades.append(grades[i][0])      
        
        #To find the pass percentages for each subject
        for i in list(result_df.columns)[1:-7]:
            pass_count=0
            fail_count=0
            absent_count=0
            temp_list=[i]
            subject_analysis=result_df[i].tolist()
            temp_list.append(len(subject_analysis)-subject_analysis.count("-"))
            for j in absent_grades:
                absent_count+=subject_analysis.count(j)
            temp_list.append(temp_list[1]-absent_count)
            temp_list.append(absent_count)
            for j in pass_grades:
                pass_count+=subject_analysis.count(j)
            for j in fail_grades:
                fail_count+=subject_analysis.count(j)
            temp_list.append(fail_count)
            temp_list.append(pass_count)
            temp_list.append(pass_count/temp_list[2]* 100)
            self.stats_df.loc[len(self.stats_df)]=temp_list

        #Over analysis calculation            
        fail_count=0
        absent_count=0
        for i in range(len(result_df)):
            grades_list=result_df.iloc[i,1:-7]
            grades_list=list(set(grades_list))
            if len(grades_list)==1:
                for j in absent_grades:
                    if grades[0]==j:
                        absent_count+=1
            elif len(grades_list)!=1:
                for j in fail_grades:
                    for k in grades_list:
                        if j==k:
                            fail_count+=1
                for j in absent_grades:
                    for k in grades_list:
                        if j==k:
                            fail_count+=1
        temp_list=["Total",len(result_df),len(result_df)-absent_count,absent_count,fail_count]
        temp_list.append(temp_list[2]-fail_count)
        temp_list.append(temp_list[5]*100/temp_list[2])
        self.stats_df.loc[len(self.stats_df)]=temp_list
        temp_list.pop(0)
        temp_list.insert(0,branch_code)
        self.overall_data.loc[len(self.overall_data)]=temp_list

    def toppersCal(self,result_df):
        data=result_df.sort_values(by=["Points"])
        position=1
        temp=data.iloc[-1,-1]
        for i in range(1,len(data)):
            if position<3 or temp==data.iloc[-i,-1]:
                if temp!=data.iloc[-i,-1]:
                    position+=1
                temp_data=[position,data.iloc[-i,0],data.iloc[-i,-2],data.iloc[-i,-1]]
                temp=data.iloc[-i,-1]
                self.topper_df.loc[len(self.topper_df.index)]=temp_data     
            elif position==3:
                break