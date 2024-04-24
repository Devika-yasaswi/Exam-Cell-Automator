from pandas import *
class CGPA:
    def __init__(self,branch) -> None:
        self.branch=branch
        self.cgpa_df=DataFrame()
    def add_sem(self,sem_data):
        pass
    def cgpa_cal(self):
        self.cgpa_df["CGPA"]=0
        self.cgpa_df["Total backlogs"]=0
        x=len(self.cgpa_df.columns)//4
        value=0
        gpa=0
        backlogs=0
        for i in range(len(self.cgpa_df)):
            for j in range(x):
                gpa+=(self.cgpa_df.iloc[i,1+4*j])
                value+=(self.cgpa_df.iloc[i,2+(4*j)])
                backlogs+=self.cgpa_df.iloc[i,4+(4*j)]
            self.cgpa_df.loc[i,"CGPA"]=gpa/value
            self.cgpa_df.loc[i,"Total backlogs"]=backlogs
            value=0
            gpa=0
            backlogs=0
        self.cgpa_df=self.cgpa_df.drop(self.cgpa_df.columns[4::4],axis=1)
