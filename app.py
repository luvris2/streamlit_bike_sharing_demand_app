import streamlit as st
import app_home
import app_eda
import app_ml

def main() :
    st.header('자전거 수요 데이터 분석 앱')
    menu = ['Home', 'EDA', 'ML']
    choice = st.sidebar.selectbox('메뉴', menu)
    if choice == menu[0] :
        app_home.run_home()
    elif choice == menu[1] :
        app_eda.run_eda()
    elif choice == menu[2] :
        app_ml.run_ml()

if __name__ == '__main__' :
    main()