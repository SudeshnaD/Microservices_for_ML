import pandas as pd
import json

#Read csv files into memory
df_us=pd.read_csv("../employees/us.csv")
df_us["Country"]="USA"
df_uk=pd.read_csv("../employees/uk.csv")
df_uk["Country"]="UK"
merged_df=pd.concat([df_us,df_uk],axis=0)

#Extract employee details from csv file based on the keystring of the format first_name+last_name
def get_employee_data(keystring):
    keywords=keystring.split(' ')
    if len(keywords==1):
        employee_data=merged_df.loc[(merged_df['first_name']==keywords[0])+(merged_df['last_name']==keywords[0])
    elif:
        employee_data=merged_df.loc[(merged_df['first_name']==keywords[:len(keywords)])+(merged_df['last_name']==keywords[:-1])

    #Store data as dictionary to be returned as json by endpoint
    employee_data_dict={k:"" for k in ["name", "company", "address", "phone", "email"]}
    employee_data_dict["name"]=employee_data['first_name']+employee_data['last_name']
    employee_data_dict["company"]=employee_data["company_name"]
    employee_data_dict["email"]=employee_data["email"]
    if employee_data["Country"=="USA"]:
        employee_data_dict["address"]=employee_data[["address","city","state","zip","Country"]].iloc[0,:].to_dict()
        employee_data_dict["phone"]=employee_data["phone2"]
    else:
        employee_data_dict["address"]=employee_data[["address","city","upper_case(county)","postal","Country"]].iloc[0,:].to_dict()
        employee_data_dict["phone"]=employee_data["phone1"]

    return json.dumps(employee_data_dict)




