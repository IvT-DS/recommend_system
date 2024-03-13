import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_csv("kino_mail_proc.csv")
random_digits = np.random.choice(len(df), size=10, replace=False)


# Создать текстовое поле для ввода названия фильма
# title = st.text_input('Что хотите посмотреть сегодня?')

# if len(title) != 0:
#     st.header('Я пока что в разработке 😬😬😬😬')


# Создание списка уникальных стран
all_countries = set()
for countries_list in df["country"].dropna().str.split(", "):
    all_countries.update([country.strip() for country in countries_list])
all_countries = sorted(all_countries)

# Создание списка уникальных жанров
all_genres = set()
for genres_list in df["genres"].dropna().str.split(", "):
    all_genres.update([genre.strip() for genre in genres_list])
all_genres = sorted(all_genres)

# Виджеты для боковой панели
selected_country = st.sidebar.multiselect("Страна", all_countries)
selected_genre = st.sidebar.multiselect("Жанры", all_genres)

# Применение фильтров к DataFrame
if selected_country:
    country_filters = "|".join([rf"\b{country}\b" for country in selected_country])
    df = df[df["country"].str.contains(country_filters, regex=True, na=False)]

if selected_genre:
    genre_filters = "|".join(selected_genre)
    df = df[df["genres"].str.contains(genre_filters, regex=True, na=False)]


if selected_genre:
    df = df[df["genres"].str.contains("|".join(selected_genre))]

# Проверяем, не пустой ли отфильтрованный DataFrame
if not df.empty:
    # Преобразование year1 в числовой формат, если возможно, и обработка NaN значений
    df["year1"] = pd.to_numeric(df["year1"], errors="coerce")
    df = df.dropna(subset=["year1"])

    # Теперь безопасно ищем min и max
    min_year = int(df["year1"].min())
    max_year = int(df["year1"].max())

    # Если есть хотя бы два разных года, отображаем слайдер
    if min_year < max_year:
        selected_year_range = st.sidebar.slider(
            "Выберите диапазон лет выпуска",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
        )
        # Применяем фильтр по годам
        df = df[
            (df["year1"] >= selected_year_range[0])
            & (df["year1"] <= selected_year_range[1])
        ]
else:
    st.error(
        "После фильтрации данных не осталось. Пожалуйста, выберите другие параметры."
    )


if st.button("Выбрать случайно") and len(df) > 0:
    random_indices = np.random.choice(df.index, size=min(10, len(df)), replace=False)
    for i in random_indices:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(df["poster"][i])

        with col2:

            # Используйте loc для безопасного доступа к элементам DataFrame
            title = df.loc[df.index == i, "title"].iloc[0]
            country = df.loc[df.index == i, "country"].iloc[0]
            year = df.loc[df.index == i, "year1"].iloc[0]
            genre = df.loc[df.index == i, "genres"].iloc[0]
            cast = df.loc[df.index == i, "cast1"].iloc[0]
            description = df.loc[df.index == i, "description"].iloc[0]

            # Заголовки полей жирным шрифтом
            st.markdown(
                f"<span style='font-weight:bold; font-size:22px;'>Название сериала:</span> <span style='font-size:20px;'>«{title}»</span>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<span style='font-weight:bold; font-size:16px;'>Страна:</span> <span style='font-size:16px;'>{country}</span>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<span style='font-weight:bold; font-size:16px;'>Год выпуска:</span> <span style='font-size:16px;'>{year}</span>",
                unsafe_allow_html=True,
            )

            # genre = f"Нет данных" if pd.isna(df["genres"].iloc[i]) else df["genres"][i]

            st.markdown(
                f"<span style='font-weight:bold; font-size:16px;'>Жанр:</span> <span style='font-size:16px;'>{genre}</span>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<h6 style='font-weight:bold;'>В ролях:</h6>", unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align: justify; margin-bottom: 18px;'>{cast}</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<h6 style='font-weight:bold;'>Описание:</h6>", unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align: justify;'>{description}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
