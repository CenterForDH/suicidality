import pickle
import streamlit as st
import time
from datetime import datetime #add for time
import pytz #add for time
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

#st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

footerText = """
<style>
#MainMenu {
visibility:hidden ;
}

footer {
visibility : hidden ;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>

<div class='footer'>
<p> Copyright @ 2023 Center for Digital Health <a href="mailto:iceanon1@khu.ac.kr"> iceanon1@khu.ac.kr </a></p>
</div>
"""

st.markdown(str(footerText), unsafe_allow_html=True)

@st.cache_data
#suicidalthinking_finalized_model_adb predict_suicidalthinking_model
def model_file():
    mfile = str(Path(__file__).parent) + '/suicialthinking_finalized_model.pkl'
    with open(mfile, 'rb') as file:
        model = pickle.load(file)
    return model


def prediction(X_test):
    model = model_file()
    result = model.predict_proba([X_test])

    return result[0][1]


def set_bmi(BMI):
    x = 4
    if   BMI <  18.5           : x = 1
    elif BMI >= 18.5 and BMI < 23: x = 2
    elif BMI >= 23   and BMI < 25: x = 3
    elif BMI >= 25             : x = 4
    else : x = 0

    return x


def input_values():
    Region of residence  = st.radio('Region of regidence', ('Urban','Rural'), horizontal=True)
    Region of residenceDict = {'Urban':1,'Rural':2}
    Region of residence  = Region of residence[Region of residenceDict]

    Age   = st.radio('Age(year)',(13,14,15,16,17,18), horizontal=True)

    Sex     = st.radio('Sex',('Male','Female'), horizontal=True)
    SexDict = {'Male':1,'Female':2}
    Sex = SexDict[Sex]

    height  = st.number_input('Height (cm)', min_value=80, max_value=190, value=130)
    weight  = st.number_input('Weight (kg)', min_value=30, max_value=100, value=50)
    bmiv = weight/((height/100)**2)
    bmi_2 = set_bmi(bmiv)
    BMI groupDict = {1:'Underweight',2:'Normal',3:'Overweight',4:'Obese'}
    st.write('BMI: ', BMI groupDict[bmi_2], round(bmiv,2))
    
    Parents highest educational level = st.radio('Academic achievement', ('Low','Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    Parents highest educational levelDict = {'Low':1, 'Low-middle':2,'Middle':3,'Upper-middle':4,'Upper':5}
    Parents highest educational level = Parents highest educational levelDict[Parents highest educational level]

    Household income  = st.radio('Household income', ('Low','Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    Household incomeDict = {'Low':1, 'Low-middle':2,'Middle':3,'Upper-middle':4,'Upper':5}
    Household income  = household_incomeDict[household_income]

    Smoking status   = st.radio('Smoking status', ('No','Yes'), horizontal=True)
    Smoking statusDict = {'No':0,'Yes':1}
    Smoking status   = Smoking statusDict[Smoking status]
    
    Alcohol consumption = st.radio('Acohol consumption status', ('No','Yes'), horizontal=True)
    Alcohol consumptionDict = {'No':0,'Yes':1}
    Alcohol consumption = Alcohol consumptionDict[Alcohol consumption]
    
    Stress status  = st.radio('Stress status', ('Low to moderate','High to severe'), horizontal=True)
    Stress statusDict = {'Low to moderate':1,'High to severe':2}
    Stress status = Stress statusDict[Stress status]

    Sadness and despair = st.radio('Sadness and despair', ('Low to moderate','High to severe'), horizontal=True)
    Sadness and despairDict = {'Low to moderate':0,'High to severe':1}
    Sadness and despair = Sadness and despairDict[Sadness and despair]

    Atopic dermatitis   = st.radio('Atopic dermatitis', ('No','Yes'), horizontal=True)
    Atopic dermatitisDict = {'No':0,'Yes':1}
    Atopic dermatitis   = Atopic dermatitisDict[Atopic dermatitis]

    Asthma  = st.radio('Asthma', ('No','Yes'), horizontal=True)
    AsthmaDict = {'No':0,'Yes':1}
    Asthma  = AsthmaDict[Asthma] 

    
    X_test = [Age, Sex, Region of residence, BMI group,
             School performance, Parents highest educational level, Household income,
             Alcohol consumption, Smoking status, Stress status, Atopic dermatitis,
             Asthma, Sadness and despair]
    result = prediction(X_test)

    return result


def main():
    result = input_values()    

    with st.sidebar:
        st.markdown(f'# Probability for suicide')
        st.markdown(f'# {result*100:.2f} %')
        
        st.markdown(f'## {danger_level}')
    
    now = datetime.now(pytz.timezone('Asia/Seoul'))  # 한국 시간대로 변경
    current_time = now.strftime('%Y-%m-%d %H:%M')
    st.write(f"Current Time: {current_time}")



if __name__ == '__main__':
    main()
