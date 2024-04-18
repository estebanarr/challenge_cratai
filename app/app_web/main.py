import sys
from streamlit.web import cli as stcli
import streamlit as st
from utils import func
from utils.mongo_connection import MongoDBConnection
import requests
import datetime
    
def main():

    st.set_page_config(layout="wide",page_title='SUSTAINABILITY PREDICTION', page_icon='📊')

    st.header(" :deciduous_tree: Sustainability prediction :deciduous_tree:")

    st.subheader("Please enter the company description to predict sustainability")

    company_name = st.text_input('Company name:')
    company_description = st.text_area('Company description:')

    if st.button("Predict", type="primary"):
    
        text_processed = func.preprocess_text(company_description)
   
        response = requests.post("http://api/sustainability/analyze", json={'text_description':text_processed})
     
        try:
            response = response.json()

            st.subheader("Results:")

            if response['prediction_class']:
                st.write(f":green[The company is focused on sustainability goals with a probability of **{response['prob_label_1']*100:.2f}** %]")
            else:
                st.write(f":red[The company is not focused on sustainability goals with a probability of **{response['prob_label_0']*100:.2f}** %]")

            with MongoDBConnection() as mongo:

                mongo._col_evaluation.insert_one({'date': datetime.datetime.now(),
                                                  'companyName': company_name,
                                                  'description':company_description,
                                                  'prob_label_0':response['prob_label_0'],
                                                  'prob_label_1':response['prob_label_1']})


        except requests.exceptions.JSONDecodeError:
            print("Error JSON")


if __name__ == '__main__':
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())