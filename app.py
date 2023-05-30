import streamlit as st
import pandas as pd
import numpy as np
import pickle
from numerize import numerize

preprocessor = pickle.load(open('resources/preprocessor.pkl','rb'))
model = pickle.load(open('resources/model.pkl','rb'))

st.title('ASFA')

columns = st.columns(4)
with columns[0]:
    size = st.selectbox('Size',['Small','Medium','Large','Extra Large'])
with columns[1]:
    if size=='Small':
        capacity=st.number_input('Capacity (m3/d)',1,999)
    elif size=='Medium':
        capacity=st.number_input('Capacity (m3/d)',1000,10000)
    elif size=='Large':
        capacity=st.number_input('Capacity (m3/d)',10000,50000)
    else:
        capacity=st.number_input('Capacity (m3/d)',50000,1000000)
with columns[2]:
    process=st.selectbox('Process',['Membrane','Thermal','Specialized'])
with columns[3]:
    if process=='Membrane':
        technology=st.selectbox('Technology',['ED','EDI','EDR','FO','NF','RO'])
    elif process=='Thermal':
        technology=st.selectbox('Technology',['MED','MSF','VC'])
    else:
        technology=st.selectbox('Technology',['NF/Sulfate Removal'],disabled=True)

columns = st.columns(2)
with columns[0]:
    units=st.number_input('Units',1,6000)
with columns[1]:
    plant_supplier_share=st.slider('Plant Supplier Share (%)',1,100)

columns = st.columns(4)
with columns[0]:
    continent=st.selectbox('Continent',['Asia', 'Europe', 'North America', 'Africa', 'Oceania',
                                         'South America', 'Antarctica'])
with columns[1]:
    location_type=st.selectbox('Location Type',['Land based','Mobile','Offshore'])
with columns[2]:
    procurement_model = st.selectbox('Procurement Model',['EPC', 'BOT', 'IWP', 'BOO', 'DB', 'DBO', 
                                                          'IWPP', 'BOOT','DBOOT'])
        
with columns[3]:
    if process=='Thermal':
        thermal_design=st.selectbox('Thermal Design', ['Flash','MVC','TVC', 'Med (Pure)'])
    else:
        thermal_design=st.selectbox('Thermal Design', ['N/A'],disabled=True)       
columns = st.columns(4)
with columns[0]:
    feedwater=st.selectbox('Feedwater',['Brackish Water','Brine (Conc. Seawater)','Pure Water (Tap Water)',
                            'River Water','Seawater','Waste Water'])
with columns[1]:
    if technology=='RO':
        ro_system=st.selectbox('RO System', ['Single Pass','Two Pass','Triple Pass'])
    else:
        ro_system=st.selectbox('RO System', ['N/A'],disabled=True)
with columns[2]:
    if technology=='RO':
        ro_membrane_type=st.selectbox('RO Membrane Type', ['Spiral Wound','Hollow Fibre','Flat','Tube','Dual','SW/FM Dual'])
    else:
        ro_membrane_type=st.selectbox('RO Membrane Type', ['N/A'],disabled=True)
with columns[3]:
    customer_type=st.selectbox('Customer Type', ['Industry','Municipalities','Tourist','Demonstration',
                                                 'Military','Irrigation','Discharge'])       
          

df = pd.DataFrame([[capacity,feedwater,size,procurement_model,process,units,plant_supplier_share,
                    thermal_design,continent,location_type,ro_system,technology,customer_type,ro_membrane_type]],
                   columns = ['capacity_(m3/d)', 'feedwater', 'size', 'procurement_model', 'process',
                                'units', 'plant_supplier_share', 'thermal_design', 'continent',
                                'location_type', 'ro_system', 'technology', 'customer_type',
                                'ro_membrane_type'])


df['size'] = df['size'].map({'Small':'s','Medium':'m','Large':'l','Extra Large':'xl'})
df.technology = df.technology.map({'ED':'ed (electrodialysis)',
                                    'EDI':'edi (electrodeionization)',
                                    'EDR':'edr (electrodialysis reversal)',
                                    'FO':'fo (forward osmosis)',
                                    'NF':'nf (nanofiltration)',
                                    'RO':'ro (reverse osmosis)',
                                    'MED':'med (multi-effect distillation)',
                                    'MSF':'msf (multi-stage flash)',
                                    'VC':'vc (vapour compression)',
                                    'NF/Sulfate Removal':'nf / sulfate removal'})
df['continent'] = df['continent'].map({'Asia':'AS',
                                        'Europe':'EU',
                                        'North America':'NA',
                                        'Africa':'AF',
                                        'Oceania':'OC',
                                        'South America':'SA'})
df.location_type = df.location_type.str.lower()
df.procurement_model = df.procurement_model.str.lower()
df['thermal_design'] = df['thermal_design'].map({'Flash':'flash',
                                                'MVC':'mvc (mechanical vapour compression)',
                                                'TVC':'tvc (thermal vapor compression)', 
                                                'Med (Pure)': 'med (pure)'})
df.feedwater = df.feedwater.map({'Brackish Water':'brackish water or inland water (tds 3000ppm - <20000ppm)',
                   'Brine (Conc. Seawater)':'brine or concentrated seawater (tds >50000ppm)',
                   'Pure Water (Tap Water)':'pure water or tap water (tds <500ppm)',
                   'River Water':'river water or low concentrated saline water (tds 500ppm - <3000ppm)',
                   'Seawater':'seawater (tds 20000ppm - 50000ppm)',
                   'Waste Water':'wastewater'})
df.ro_system = df.ro_system.str.lower()
df.ro_membrane_type = df.ro_membrane_type.map({'Spiral Wound':'spiral wound membrane',
                                                'Hollow Fibre':'hollow fibre membrane',
                                                'Flat':'flat membrane (fm)',
                                                'Tube':'tube membrane',
                                                'Dual':'dual membrane plant (hfm/swm)',
                                                'SW/FM Dual':'sw / fm dual membrane'})
df['customer_type'] = df['customer_type'].map({'Industry':'industry (tds <10ppm)',
                                'Municipalities':'municipalities as drinking water (tds 10ppm - <1000ppm)',
                                'Tourist':'tourist facilities as drinking water (tds 10ppm - <1000ppm)',
                                'Demonstration':'demonstration',
                                'Military':'military purposes (tds 10ppm- <1000ppm)',
                                'Irrigation':'irrigation (tds <1000ppm)',
                                'Discharge':'discharge'})


X_preprocessed = preprocessor.transform(df)

# predict price
log_price = model.predict(X_preprocessed)
price = round(np.expm1(log_price)[0])

if len(str(price)) > 6:
    st.markdown(f'<h1><span style="font-weight:lighter;">Minimum Investment:</span> <span style="color:rgb(255, 75, 75);">${numerize.numerize(price)}</span></h1>', unsafe_allow_html=True)
else:
    st.markdown(f'<h1><span style="font-weight:lighter;">Minimum Investment:</span> <span style="color:rgb(255, 75, 75);">${price:,}</span></h1>', unsafe_allow_html=True)
