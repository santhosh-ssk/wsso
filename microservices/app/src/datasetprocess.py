import pandas as pd
import numpy as np



df=pd.read_csv("/home/santhosh/codeutsava/dataset/report.csv",header=None)
columns=["S.No",'State','District','Block','Panchayat','Village','Habitation','Location/SourceId & Main Scheme Name ','Type of Source','Laboratory Name','Testing Date [DD/MM/YY]','Sample Number/ Name','Above Permissible Limit (Mandatory*)','Below Permissible Limit (Mandatory*)','Above Permissible Limit (Emerging /Other**)','Below Permissible Limit (Emerging /Other**)','Testid']
df.columns=columns
df=df[np.isnan(df['S.No'])==False]
columns.remove('S.No')
df=df[columns]

import requests
import json

def checkparameters(key,parameter):
	parameter=parameter.split()[0]
	parameter=float(parameter)
	if(key=='pH' or key=='PH'):
		if(parameter>8.5):
			return ["high","bitter/soda taste, deposits","Decrease pH with white vinegar / citric acid"]
		elif(parameter>=6.5):
			return ["safe"]
		else:
			return ["low","corrosion, metallic taste","pH by soda ash"]
	elif(key=='TDS'):
		if(parameter>2000):
			return ["high","Hardness, scaly deposits, sediment, cloudy colored water,staining, salty or bitter taste, corrosion of pipes and fittings","Reverse Osmosis, Distillation, deionization by ion exchange"]
		elif(parameter>=500):
			return ["permisible"]
		else:
			return ["safe"]
			
	elif(key=='Hardness'):
		if(parameter>600):
			return ["high","Scale in utensils and hot water system, soap scums","Water Softener Ion Exchanger , Reverse Osmosis"]
		elif(parameter>=300):
			return ["permisible"]
		else:
			return ["safe"]

	elif(key=='Iron'):
		if(parameter>1.0):
			return ["high","Brackish color, rusty sediment, bitter or metallic taste, brown-green stains, iron bacteria, discolored beverages","Oxidizing Filter , Green-sand Mechanical Filter"]
		elif(parameter>0.35):
			return ["permisible"]
		else:
			return ["safe"]

	elif(key=='Manganese'):
		if(parameter>0.3):
			return ["high","Brownish color, black stains on laundry and fixtures at .2 mg/l, bitter taste, altered taste of water-mixed beverages","Ion Exchange , Chlorination, Oxidizing Filter , Green-sand Mechanical Filter"]
		elif(parameter>0.1):
			return ["permissible"]
		else:
			return ["safe"]

	elif(key=='Sulphates'):
		if(parameter>400):
			return ["high","Bitter, medicinal taste, scaly deposits, corrosion, laxative effects, \"rotten-egg\" odor from hydrogen sulfide gas formation","Ion Exchange , Distillation , Reverse Osmosis"]
		elif(parameter>200):
			return ["permissible"]
		else:
			return ["safe"]

	elif(key=='Nitrate'):
		if(parameter>100):
			return ["high","Methemoglobinemia or blue baby disease in infants","Ion Exchange, Distillation, Reverse Osmosis"]
		elif(parameter>45):
			return ["permissible"]
		else:
			return ["safe"]
	
	elif(key=='Chloride'):
		if(parameter>1000):
			return ["high","High blood pressure, salty taste, corroded pipes, fixtures and appliances, blackening and pitting of stainless steel","Ion Exchange, Distillation, Reverse Osmosis","Reverse Osmosis , Distillation, Activated Carbon"]
		elif(parameter>250):
			return ["permissible"]
		else:
			return ["safe"]

	elif(key=='Fluoride'):
		if(parameter>1.5):
			return ["high","Brownish discoloration of teeth, bone damage","Activated Alumina, Distillation, Reverse Osmosis, Ion Exchange"]
		elif(parameter>1.0):
			return ["permissible"]
		else:
			return ["safe"]
	
	elif(key=='Alkalinity'):
		if(parameter>600):
			return ["high"]
		elif(parameter>400):
			return ["permissible"]
		elif(parameter>=200):
			return ["safe"]
		else:
			return ["low","Low Alkalinity (i.e. high acidity) causes deterioration of plumbing and increases the chance for many heavy metals in water are present in pipes, solder or plumbing fixtures.","Neutralizing agent"]

	elif(key=='Turbidity'):
		if(parameter>5.0):
			return ["high","increases the level of disinfections with pathogens"]
		elif(parameter>3.0):
			return ["permissible"]
		else:
			return ["safe"]

	elif(key=='Calcium'):
		if(parameter>80000):
			return ["high","increases the level of disinfections with pathogens"]
		elif(parameter>40000):
			return ["safe"]
		else:
			return ["low","pain in kiddneys,low blood pressure","reverse osmosis"]
	
	elif(key=='Magnesium'):
		if(parameter>30000):
			return ["high","it causes laxative effect"]
		elif(parameter>20000):
			return ["safe"]
		else:
			return ["low","sleep problems,hormone problems,muscle cramps,hyper tension","reverse osmosis"]

	elif(key=='E-Coli (MPN /100 Ml)' or key=='Coliform'):
		if(parameter>5):
			return ["high","Gastrointestinal illness","Chlorination , Ultraviolet, Distillation, Iodination"]
		elif(parameter>3.0):
			return ["permissible"]
		else:
			return ["safe"]
	

	else:
		return ["unknown"]



def data_seperate(index_list,testsample):
    params=list()
    for data in index_list:
        data=str(data)
        params=params +(data.split(","))
        
    for i in range(0,len(params)):
        if(params[i]=='nan'):
            continue
        else:
            sample=params[i].split('[')
            parameters=list()
            parameters.append(sample[0])
            if(testsample=='PH'):
                testsample='pH'
            if(testsample != parameters[0]):
            	continue
            parameters.append(sample[1].split("]")[0])
            params[i]=parameters
            parameters+=checkparameters(params[i][0],params[i][1])
            return("@".join(parameters[1:]))
    return "Not measured"
para=['Chloride',
 'Sulphates',
 'E-Coli (MPN /100 Ml)',
 'Alkalinity',
 'Manganese',
 'Calcium',
 'Nitrate',
 'Magnesium',
 'Iron',
 'Coliform',
 'TDS',
 'PH',
 'Turbidity',
 'Fluoride',
 'pH',
 'Hardness']

for params in para:
    df[params]=df.apply(lambda row: data_seperate([row['Above Permissible Limit (Mandatory*)'],row['Below Permissible Limit (Mandatory*)'],row['Above Permissible Limit (Emerging /Other**)'],row['Below Permissible Limit (Emerging /Other**)']],params)
,axis=1)
columns=list(df.columns)
columns.remove('PH')
columns
df=df[columns]
columns=list(df.columns)
datass=df[columns].values.tolist()


print([len(df)," page loaded"])

# This is the url to which the query is made
url = "https://data.annulment76.hasura-app.io/v1/query"


count=712
for j in [i for i in range(2000,46500,500)]:
    sending=list()
    # This is the json payload for the query
    for districsdata in datass[j:j+500]:
        record=(dict(zip(columns,districsdata)))
        #print(record.keys())
        sending_data={
                    "State": record["State"],
                    "District": record["District"],
                    "Block": record["Block"],
                    "Panchayat": record["Panchayat"],
                    "Village": record["Village"],
                    "Habitation": record["Habitation"],
                    "Location/SourceId & Main Scheme Name ": record["Location/SourceId & Main Scheme Name "],
                    "Type of Source": record["Type of Source"],
                    "Laboratory Name": record["Laboratory Name"],
                    "Testing Date [DD/MM/YY]": record["Testing Date [DD/MM/YY]"],
                    "Sample Number/ Name": record["Sample Number/ Name"],
                    "Above Permissible Limit (Mandatory*)": str(record["Above Permissible Limit (Mandatory*)"]),
                    "Below Permissible Limit (Mandatory*)": str(record["Below Permissible Limit (Mandatory*)"]),
                    "Above Permissible Limit (Emerging /Other**)": str(record["Above Permissible Limit (Emerging /Other**)"]),
                    "Below Permissible Limit (Emerging /Other**)": str(record["Below Permissible Limit (Emerging /Other**)"]),
                    "Testid": record["Testid"],
                    "Chloride":record["Chloride"],
                    "Sulphates": record["Sulphates"],
                    "E-Coli (MPN /100 Ml)": record["E-Coli (MPN /100 Ml)"],
                    "Alkalinity": record["Alkalinity"],
                    "Manganese": record["Manganese"],
                    "Calcium": record["Calcium"],
                    "Nitrate": record["Nitrate"],
                    "Magnesium": record["Magnesium"],
                    "Iron": record["Iron"],
                    "Coliform": record["Coliform"],
                    "TDS": record["TDS"],
                    "Turbidity": record["Turbidity"],
                    "Fluoride": record["Fluoride"],
                    "pH": record["pH"],
                    "Hardness": record["Hardness"]
                    }
        sending.append(sending_data)		    
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "record",
            "objects": sending
        }
    }


    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 60bcda7f858ca2dd9d5cf503cdb7aeeafcc997f6c469c66a"
    }
    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    print(resp.content)	
    print(count)
    count=count+500
    #print(requestPayload)