import streamlit as st
import app_home
import app_eda
import app_ml
from streamlit_option_menu import option_menu

def main() :
    st.header('🚴🏻‍♀️ 자전거 수요 데이터 분석 앱')
    with st.sidebar:
        st.image('data/bike_img01.png')
        menu = option_menu("App Menu", ["Home", "EDA", "ML"],
                            icons=['house', 'bar-chart', 'kanban'],
                            menu_icon="bi bi-menu-up", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"}, })
    if menu == 'Home' :
        app_home.run_home()
    elif menu == 'EDA' :
        app_eda.run_eda()
    elif menu == 'ML' :
        app_ml.run_ml()

if __name__ == '__main__' :
    main()