import pandas as pd
import json
import os

abs_path = os.path.dirname(__file__)

class Employee_Search:

    def __init__(self,):
       print(os.getcwd())
       return None

    #Read csv files into memory
    def load_csv(self,):
        df_us = pd.read_csv(os.path.join(abs_path,"../employees/us.csv"))
        df_us["Country"] = "USA"
        df_uk = pd.read_csv(os.path.join(abs_path,"../employees/uk.csv"))
        df_uk["Country"] = "UK"
        merged_df = pd.concat([df_us,df_uk],axis=0)
        return df_us,df_uk,merged_df

    #Extract employee details from csv file based on the keystring of the format first_name+last_name
    def get_employee_data(self,keywords,df_us,df_uk,merged_df):
        if len(keywords) == 1:
            employee_data = merged_df.loc[(merged_df['first_name'] == keywords[0]) + (merged_df['last_name'] == keywords[0])]
        else:
            employee_data = merged_df.loc[(merged_df['first_name'] == keywords[:-1][0]) + (merged_df['last_name'] == keywords[:1][0])]

        #Store data as dictionary to be returned as json by endpoint
        employee_data_dict = {k:"" for k in ["name", "company", "address", "phone", "email"]}
        employee_data_dict["name"] = employee_data['first_name'].iloc[0] + " " + employee_data['last_name'].iloc[0]
        employee_data_dict["company"] = employee_data["company_name"].iloc[0]
        employee_data_dict["email"] = employee_data["email"].iloc[0]
        print(employee_data_dict)
        if employee_data["Country"].iloc[0] == "USA":
            employee_data_dict["address"] = employee_data[["address","city","state","zip","Country"]].iloc[0,:].to_dict()
            employee_data_dict["phone"] = employee_data["phone2"].iloc[0]
        else:
            employee_data_dict["address"] = employee_data[["address","city","county","postal","Country"]].iloc[0,:].to_dict()
            employee_data_dict["phone"] = employee_data["phone1"].iloc[0]
        return json.dumps(employee_data_dict)


    #Display information for all employees in the format{region, count, employees}
    def get_all_employees(self,df_us,df_uk,merged_df):
        state_dict = {k:{"count":0,"employees":[]} for k in df_us.groupby("state").groups.keys()}
        county_dict = {k:{"count":0,"employees":[]} for k in df_uk.groupby("county").groups.keys()}
        for k in state_dict.keys():
            state_dict[k]["count"] = int(df_us.groupby("state")["first_name","last_name"].get_group(k).count()[0])
            emp_names = df_us.groupby("state")["first_name","last_name"].get_group(k)
            emp_names["full_name"] = emp_names["first_name"] +" "+ emp_names["last_name"]
            state_dict[k]["employees"] = list(emp_names["full_name"])
        for k in county_dict.keys():
            county_dict[k]["count"] = int(df_uk.groupby("county")["first_name","last_name"].get_group(k).count()[0])
            emp_names = df_uk.groupby("county")["first_name","last_name"].get_group(k)
            emp_names["full_name"] = emp_names["first_name"] + " " + emp_names["last_name"]
            county_dict[k]["employees"] = list(emp_names["full_name"])
        return json.dumps([state_dict,county_dict])



if __name__=="__main__":
    #get_all_employees()
    es_obj = Employee_Search()
    df_us,df_uk,merged_df = es_obj.load_csv()
    es_obj.get_employee_data("Gail",df_us,df_uk,merged_df)