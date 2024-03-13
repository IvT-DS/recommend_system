import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_csv("kino_mail_proc.csv")
random_digits = np.random.choice(len(df), size=10, replace=False)


# Создать текстовое поле для ввода названия фильма
# title = st.text_input('Что хотите посмотреть сегодня?')

# if len(title) != 0:
#     st.header('Я пока что в разработке 😬😬😬😬')


if st.button("Выбрать случайно"):

    for i in random_digits:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(df["poster"][i])

        with col2:
            genre = f"Нет данных" if pd.isna(df["genres"].iloc[i]) else df["genres"][i]

            st.markdown(
                f"<h4 style='font-weight:bold;display:inline;'>Название сериала:</h4> {df['title'][i]}<br>"
                f"<h6 style='font-weight:bold;display:inline;'>Страна:</h6> {df['country'][i]}<br>"
                f"<h6 style='font-weight:bold;display:inline;'>Год выпуска:</h6> {df['year1'][i]}<br>"
                f"<h6 style='font-weight:bold;display:inline;'>Жанр:</h6> {genre}<br>"
                unsafe_allow_html=True,
            )

            st.markdown(
                "<h6 style='font-weight:bold;'>В ролях:</h6>", unsafe_allow_html=True
            )
            st.write(df["cast1"][i])

            st.markdown(
                "<h6 style='font-weight:bold;'>Описание:</h6>", unsafe_allow_html=True
            )
            st.write(df["description"][i])

            # st.write("Нет данных" if pd.isna(df['genres'].iloc[i]) else df['genres'][i] )
            # st.title('Оценка')
            # imb = 'Нет оценки' if df['imdb'][i] == 0 else str(df['imdb'][i])
            # kinopoisk = 'Нет оценки' if df['kinopoisk'][i] == 0 else str(df['kinopoisk'][i])
            # st.write(f'Рейтинг imdb: {imb}')
            # st.write(f'Рейтинг кинопоиск: {kinopoisk}')
        st.markdown("---")
