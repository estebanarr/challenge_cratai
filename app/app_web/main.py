import sys
from streamlit.web import cli as stcli
import streamlit as st
from utils import func
import requests
    
def main():

    st.set_page_config(layout="wide",page_title='SUSTAINABILITY PREDICTION', page_icon='📊')

    st.subheader("Please enter the company description to predict sustainability")
    title = st.text_area('Company description:')

    if st.button("Predict", type="primary"):
    
        text_processed = func.preprocess_text(title)
        st.write(text_processed)
        response = requests.post("http://api/sustainability/analyze", json={'text_description':text_processed})

        st.write(response)



if __name__ == '__main__':
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())