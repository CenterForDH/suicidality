import pickle
import streamlit as st
import time

st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True).
def model_file():
    mfile = 'finalized_model_adb.pkl'
    model = pickle.load(open(mfile, 'rb'))
    
    return model

def prediction(X_test):
    model = model_file()
    result = model.predict_proba([X_test])
    
    return result[0][1]


def input_values():
    sex     = st.slider('SEX',                  1,   2,   1)
    age     = st.slider('AGE',                 13,  18,  15)
    bmi     = st.slider('BMI',                  1,   4,   1)
    region  = st.slider('REGION',               1,   2,   1)
    educa   = st.slider('EDUCATION',            1,   2,   1)
    acad    = st.slider('ACADEMIC ACHIEVEMENT', 5,  10,   6)
    econo   = st.slider('ECONOMIC STATUS',      1,   4,   1)
    parent  = st.slider('PARENT EDUCATION',     1,   4,   1)
    smoke   = st.slider('SMOKING STATUS',       0,   1,   1)
    alcohol = st.slider('ACHOL CONSUMPTION',    0,   4,   0)
    stress  = st.slider('STRESS',               6,   9,   6)
    depress = st.slider('DEPRESSION',           0,   1,   0)
    derma   = st.slider('DERMATIS',             0,   1,   0)
    asthma  = st.slider('ASTHMA',               0,   1,   0)
    aad     = st.slider('AAD',                  0,   1,   0)


    cols = ['SEX', 'age', 'bmi_2', 'region', 'education',
            'academic achievement', 'economic', 'parental education',
            'smoking', 'alcoholic consumption',
            'stress', 'depression', 'derma', 'asthma', 'aad']
    
    X_test = [sex,age,bmi,region,educa,acad,econo,parent,
              smoke,alcohol,stress,depress,derma,asthma,aad]
    
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
