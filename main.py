import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

def interpolate_nan(dataframe):
    if dataframe.isna().any().any() == True:
        dataframe = dataframe.interpolate(method='polynomial', order=2)
    return dataframe

st.header("Визуализация даных об электропотреблении")
st.write("Выполнено как дополнение к проекту в рамках программы Сириус.Лето")
st.write("*Лазарева Л., Власов А.*")
st.markdown("""---""")

uploaded_file = st.file_uploader("Выберите файл Excel", type=["xlsx", "xls"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file, engine='openpyxl', usecols = [0, 1, 2], nrows = 24)
    df['dif'] = df.Q1.values - df.Q1.mean()

    df = interpolate_nan(df)

    st.write("Данные о потреблении электроэнергии за 24 часа")
    st.table(df)

    if not df.empty:
        st.write(f"Среднее значение потребления {round(df.Q1.mean(), 2)} кВт")

        fig = px.bar(df, x=df.Hour.to_list(), y="Q1", 
                    title="График потребления")

        fig.add_scatter(x=df.Hour.to_list(), y=[df.Q1.mean()]*len(df.Q1),
                        mode='lines', name = 'Среднее значение')
        
        fig.update_layout( xaxis_title="Часы", yaxis_title="Потребление Q1, кВт",
                           legend=dict(yanchor="top", y=0.99, xanchor="center", x=0.5))

        st.plotly_chart(fig, use_container_width=True)
        
        fig1 = px.bar(df, x=df.Hour.to_list(), y=df['dif'], 
                    title="График потребления относительно среднего значения")
        fig1.update_layout( xaxis_title="Часы", yaxis_title="Потребление, кВт")
        
        st.plotly_chart(fig1, use_container_width=True)

        st.header("Рекомендации")
        st.markdown("""---""")
        st.write(f"- Необходимая емкость накопителя **{round(df.dif[df['dif']>0].sum(),2)}** А*ч")
        st.write(f"- Необходимая мощность накопителя **{round(df.dif[df['dif']>0].max(),2)}** кВт")
        st.write("- Часы зарядки накопителя")
        st.write(str(list(df.Hour[df['dif']<0])))
        st.write("- Часы разрядки накопителя")
        st.write(str(list(df.Hour[df['dif']>0])))

    else:
        st.error("Пустой файл")