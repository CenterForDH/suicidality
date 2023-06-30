import pickle
import streamlit as st
import time

st.set_page_config(layout="wide")

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
<p> Copyright @ 2023 Center for Digital Health <a href="mailto:wycho@khu.ac.kr"> wycho@khu.ac.kr </a></p>
</div>
"""

st.markdown(str(footerText), unsafe_allow_html=True)

@st.cache_data
def model_file():
    mfile = 'finalized_model_adb.pkl'
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
    sex     = st.radio('SEX',('Male','Female'), horizontal=True)
    sexDict = {'Male':1,'Female':2}
    sex = sexDict[sex]

    age     = st.radio('AGE (year)',(13,14,15,16,17,18), horizontal=True)

    height  = st.number_input('Height (cm)', min_value=80, max_value=190, value=130)
    weight  = st.number_input('Weight (kg)', min_value=30, max_value=100, value=50)
    bmiv = weight/((height/100)**2)
    bmi = set_bmi(bmiv)
    bmiDict = {1:'Underweight',2:'Normal',3:'Overweight',4:'Obesity'}
    st.write('BMI: ', bmiDict[bmi], round(bmiv,2))
    
    region  = st.radio('REGION', ('Urban','Rural'), horizontal=True)
    regionDict = {'Urban':1,'Rural':2}
    region  = regionDict[region]
    
    educa   = st.radio('EDUCATION', ('Middle school','High school'), horizontal=True)
    educaDict = {'Middle school':1,'High school':2}
    educa = educaDict[educa]
    
    acad    = st.radio('ACADEMIC ACHIEVEMENT (Grade)', ('Low', 'Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    acadDict = {'Low':10, 'Low-middle':9,'Middle':8,'Upper-middle':7,'Upper':6}
    acad = acadDict[acad]
    
    income   = st.radio('HOUSEHOLD INCOME',('1Q (Lowest)','2Q','3Q','4Q (Highest)'), horizontal=True)
    incomeDict = {'1Q (Lowest)':1,'2Q':2,'3Q':3,'4Q (Highest)':4}
    income = incomeDict[income]
    
    parent  = st.radio('PARENT EDUCATION (GRADUATION)', ('Middle school or lower','High school','University or higher','Unknown'), horizontal=True)
    parentDict = {'Middle school or lower':4,'High school':3,'University or higher':2,'Unknown':1}
    parent  = parentDict[parent]
    
    smoke   = st.radio('SMOKING STATUS', ('No','Yes'), horizontal=True)
    smokeDict = {'No':0,'Yes':1}
    smoke   = smokeDict[smoke]
    
    alcohol = st.radio('ACOHOL CONSUMPTION PER MONTH', ('No','1-2','3-5','6-9','< 10'), horizontal=True)
    alcoholDict = {'No':0,'1-2':1,'3-5':2,'6-9':3,'< 10':4}
    alcohol = alcoholDict[alcohol]
    
    stress  = st.radio('STRESS', ('Low','Moderate', 'High','Very much'), horizontal=True)
    stressDict = {'Low':1,'Moderate':2,'High':3,'Very much':4}
    stress = stressDict[stress]
    
    depress = st.radio('DEPRESSION', ('No','Yes'), horizontal=True)
    depressDict = {'No':0,'Yes':1}
    depress = depressDict[depress]
    
    derma   = st.radio('DERMATIS', ('No','Yes'), horizontal=True)
    dermaDict = {'No':0,'Yes':1}
    derma   = dermaDict[derma]
    
    asthma  = st.radio('ASTHMA', ('No','Yes'), horizontal=True)
    asthmaDict = {'No':0,'Yes':1}
    asthma  = asthmaDict[asthma] 

    aad     = derma | asthma
    
    X_test = [sex,age,bmi,region,educa,
              acad,income,parent,
              smoke,alcohol,stress,depress,derma,asthma]

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
