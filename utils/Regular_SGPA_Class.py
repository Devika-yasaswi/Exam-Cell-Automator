import pandas as pd
class RegularSGPA:
    def __init__(self,branch):
        self.branch=branch
        self.subjects_list=[]
        self.subject_codes=[]
        self.credits=0
        self.final_result_df=pd.DataFrame(columns=["Roll No"])
    def subjectList(self,sub):        
        self.subjects_list.append(sub)

    def uniqueSubjectList(self):
        unique_list=[]
        final_sub=[]
        sub_count=[]
        for i in range(len(self.subjects_list)):
            if self.subjects_list[i] not in unique_list:
                unique_list.append(self.subjects_list[i])    
        for i in range(len(unique_list)):
            sub_count.append(len(unique_list[i]))
        for i in range(len(sub_count)):
            if sub_count[i] == min(sub_count):
                final_sub.append(unique_list[i])
        new_final_sub=final_sub[0]
        for i in range(1,len(final_sub)):
            for j in range(len(final_sub[i])):
                if final_sub[i][j] not in new_final_sub:
                    new_final_sub.append(final_sub[i][j])
        self.subjects_list=new_final_sub
        for i in range(len(self.subjects_list)):
            self.subject_codes.append(self.subjects_list[i].split(" ")[-1])
    def finalCredits(self,df,grades):
        fail_grades=[]
        student_data=[]
        sub=[]
        total=0
        for i in range(len(grades)):
            if grades[i][1]==0 and grades[i][2]=='F':
                fail_grades.append(grades[i][0])
        for i in range(len(df)):
            if df.iloc[i,0] not in student_data:
                if not any(grade in fail_grades for grade in student_data) and set(sub)-set(self.subjects_list)==set():
                    self.credits=total
                student_data =[df.iloc[i,0]]
                total=0
                sub=[]
            if df.iloc[i,1] not in sub:
                sub.append(df.iloc[i,2]+" "+df.iloc[i,1])
                total+=float(df.iloc[i,-1])
                student_data.append(df.iloc[i,-2])
    def regularCalculation(self,student_data,grades):
        temp_data=[student_data[0]]
        total=0
        GBM=0
        pass_status=[]
        total_subs=0
        if "SGPA" not in list(self.final_result_df):
            for i in range(len(self.subjects_list)):
                self.final_result_df[self.subjects_list[i]]=[]
            self.final_result_df['GBM']=[]
            self.final_result_df['Total Credits']=[] 
            self.final_result_df['Status']=[]
            self.final_result_df['Backlogs']=[]
            self.final_result_df['Pass Percentage']=[]
            self.final_result_df['Points']=[]
            self.final_result_df['SGPA']=[]
        subs=list(student_data[1].keys())
        for i in subs:
            if i in self.subject_codes:                
                data=student_data[1][i]
                temp_data.append(data[0])
                for i in range(len(grades)):
                    if data[0]==grades[i][0]:
                        total+=grades[i][1]*data[1]
                        GBM+=grades[i][1]*10
                        pass_status.append(grades[i][2].capitalize())
                        if (grades[i][1] !=0 and grades[i][2].capitalize()=="P") or (grades[i][2].capitalize()=="F"):
                            total_subs+=1
                        break
                else:
                    return "Details about grade "+data[0]+" is missing in the database. So update the database by logging in"
        temp_data.append(GBM)
        temp_data.append(self.credits)
        if "F" not in pass_status:
            temp_data.append("Pass")            
        else:
            temp_data.append("Fail")
        temp_data.append(pass_status.count("F"))          
        try:
            temp_data.append(GBM/total_subs)
        except ZeroDivisionError:
            temp_data.append(0)
        temp_data.append(total)
        temp_data.append(total/self.credits)
        try:
            self.final_result_df.loc[len(self.final_result_df)]=temp_data
        except:
            for i in range(len(self.subject_codes)):
                if self.subject_codes[i] not in subs:
                    temp_data.insert(i+1,"-")
            self.final_result_df.loc[len(self.final_result_df)]=temp_data
        return 0
        