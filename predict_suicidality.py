import pickle
import streamlit as st
import time

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
def model_file():
    mfile = 'suicidalthinking_final.pkl'
    model = pickle.load(open(mfile, 'rb'))

    return model


def prediction(X_test):
    model = model_file()
    result = model.predict_proba([X_test])

    return result[0][1]


def set_bmi(bmi):
    x = 4
    if   bmi <  18.5           : x = 1
    elif bmi >= 18.5 and bmi < 23: x = 2
    elif bmi >= 23   and bmi < 25: x = 3
    elif bmi >= 25             : x = 4

    return x


def input_values():
    Age     = st.radio('Age (year)',(13,14,15,16,17,18), horizontal=True)

    Sex     = st.radio('Sex',('Male','Female'), horizontal=True)
    SexDict = {'Male':1,'Female':2}
    Sex = SexDict[Sex]

    height  = st.number_input('Height (cm)', min_value=80, max_value=190, value=130)
    weight  = st.number_input('Weight (kg)', min_value=30, max_value=100, value=50)
    bmiv = weight/((height/100)**2)
    BMI_group = set_bmi(bmiv)
    BMI_groupDict = {1:'Underweight',2:'Normal',3:'Overweight',4:'Obesity'}
    st.write('BMI: ', BMI_groupDict[BMI_group], round(bmiv,2))
    
    Region  = st.radio('Region of regidence', ('Urban','Rural'), horizontal=True)
    RegionDict = {'Urban':1,'Rural':2}
    Region  = RegionDict[Region]
      
    School_performance    = st.radio('School performance', ('Low', 'Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    School_performanceDict = {'Low':10, 'Low-middle':9,'Middle':8,'Upper-middle':7,'Upper':6}
    School_performance = School_performanceDict[School_performance]
    
    Household_income   = st.radio('Household income',('1Q (Lowest)','2Q','3Q','4Q (Highest)'), horizontal=True)
    Household_incomeDict = {'1Q (Lowest)':1,'2Q':2,'3Q':3,'4Q (Highest)':4}
    Household_income = Household_incomeDict[Household_income]
    
    Parents_highest_educational_level  = st.radio('Parents\' highest education level', ('Middle school or lower','High school','University or higher','Unknown'), horizontal=True)
    Parents_highest_educational_levelDict = {'Middle school or lower':4,'High school':3,'University or higher':2,'Unknown':1}
    Parents_highest_educational_level  = Parents_highest_educational_levelDict[Parents_highest_educational_level]
    
    Smoking_status   = st.radio('Smoking status', ('No','Yes'), horizontal=True)
    Smoking_statusDict = {'No':0,'Yes':1}
    Smoking_status   = Smoking_statusDict[Smoking_status]
    
    Alcohol_consumption = st.radio('Acohol consumption per month', ('No','1-2','3-5','6-9','< 10'), horizontal=True)
    Alcohol_consumptionDict = {'No':0,'1-2':1,'3-5':2,'6-9':3,'< 10':4}
    Alcohol_consumption = Alcohol_consumptionDict[Alcohol_consumption]
    
    Stress_status  = st.radio('Stress status', ('Low','Moderate', 'High','Very much'), horizontal=True)
    Stress_statusDict = {'Low':1,'Moderate':2,'High':3,'Very much':4}
    Stress_status = Stress_statusDict[Stress_status]
    
    Sadness_and_despair = st.radio('Sadness and despair', ('No','Yes'), horizontal=True)
    Sadness_and_despairDict = {'No':0,'Yes':1}
    Sadness_and_despair = Sadness_and_despairDict[Sadness_and_despair]
    
    Atopic_dermatitis   = st.radio('Atopic dermatitis', ('No','Yes'), horizontal=True)
    Atopic_dermatitisDict = {'No':0,'Yes':1}
    Atopic_dermatitis   = Atopic_dermatitisDict[Atopic_dermatitis]

    Asthma  = st.radio('Asthma', ('No','Yes'), horizontal=True)
    AsthmaDict = {'No':0,'Yes':1}
    Asthma  = AsthmaDict[Asthma] 

    X_test = [Age, Sex, Region, BMI_group, School_performance, Parents_highest_educational_level,
              Household_income, Alcohol_consumption, Smoking_status, Stress_status, Atopic_dermatitis, Asthma, Sadness_and_despair]
    result = prediction(X_test)

    return result


def main():
    result = input_values()    
    
    with st.sidebar:
        st.markdown(f'# Probability for suicide')
        st.markdown(f'# {result*100:.2f} %')

    now = time
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
        

if __name__ == '__main__':
    main()
