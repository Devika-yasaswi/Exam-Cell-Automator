import tabula
import pandas as pd
import pandas as pd

def pdfToDataframe(input_file):
    print("Hi")
    global flag
    if flag==0:
        df=tabula.read_pdf(input_file,pages="all")
        data=pd.DataFrame()
        for i in range(len(df)):
            data=pd.concat([data,df[i]],ignore_index=True)
        try:
            if data[list(data.columns)[-1]].isnull().values.any():
                flag=1 
                return "The uploaded file is in incorrect format. So try uploading excel"   
            return data                                                                  
        except: 
            flag=1
            return "The uploaded file is in incorrect format. So try uploading excel"