import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# Заголовок приложения
st.title('Анализ торгового предприятия')

# Загрузка данных
df = pd.read_csv('Products.csv')

# Создаем selectbox для выбора раздела
section = st.selectbox(
    'Выберите раздел для анализа:',
    ['Просмотр данных', 'Информация о данных', 'Анализ нулевых значений', 
     'Анализ продаж по годам основания', 'Анализ самого прибыльного магазина по году основания', 
     'Анализ по категориям продуктов', 'Самые продаваемые категории товаров', 
     'Объем выручки по категориям товаров', 'Локация магазина с самыми большими продажами', 
     'Выводы']
)

# Просмотр данных
if section == 'Просмотр данных':
    st.subheader('Просмотр данных')
    st.write(df.head(15))

# Описание столбцов
if section == 'Информация о данных':
    st.subheader('Информация о данных')
    st.markdown("""
    * **ProductID** : уникальный идентификатор товара
    * **Weight** : вес продуктов
    * **FatContent** : указывает, содержит ли продукт мало жира или нет
    * **Visibility** : процент от общей площади витрины всех товаров в магазине, отведенный для конкретного продукта
    * **ProductType** : категория, к которой относится товар
    * **MRP** : Максимальная розничная цена (указанная цена) на продукты
    * **OutletID**: уникальный идентификатор магазина
    * **EstablishmentYear** : год основания торговых точек
    * **OutletSize** : размер магазина с точки зрения занимаемой площади
    * **LocationType** : тип города, в котором расположен магазин
    * **OutletType** : указывает, является ли торговая точка просто продуктовым магазином или каким-то супермаркетом
    * **OutletSales** : (целевая переменная) продажи товара в конкретном магазине
    """)

    # Информация о данных
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

# Анализ нулевых значений
if section == 'Анализ нулевых значений':
    st.subheader('Нулевые значения в столбцах')
    st.write(df.isnull().sum())

    # Заполнение нулевых значений
    df['Weight'].fillna(df['Weight'].mean(), inplace=True)
    df['OutletSize'].fillna('Средний', inplace=True)

    # Проверка проделанной работы
    st.subheader('Проверка проделанной работы')
    st.write(df.isnull().sum())
    st.write(df.head(15))

    # Удаление дубликатов
    st.subheader('Проверка дубликатов')
    st.write(f"Количество дубликатов: {df.duplicated().sum()}")

# Анализ продаж по годам основания
if section == 'Анализ продаж по годам основания':
    st.subheader('Анализ продаж по годам основания')
    st.write(df['EstablishmentYear'].value_counts())
    st.write(df.groupby('EstablishmentYear')['OutletSales'].sum().astype(int))

# Анализ самого прибыльного магазина по году основания
if section == 'Анализ самого прибыльного магазина по году основания':
    st.subheader('Анализ самого прибыльного магазина по году основания')
    st.write(df[df['EstablishmentYear']==1985].groupby('ProductType')['OutletSales'].sum().head(16).astype(int))

    # Гистограмма объема выручки по категориям товаров для 1985 года
    st.subheader('Объем выручки по категориям товаров для 1985 года')
    product_sales1985 = df[df['EstablishmentYear'] == 1985].groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales1985.index, product_sales1985.values, color='grey')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales1985)):
        ax.text(product_sales1985.values[i], i, round(product_sales1985.values[i]), ha='left', va='center')
    st.pyplot(fig)

    # Круговая диаграмма по категориям товаров для 1985 года
    st.subheader('Круговая диаграмма по категориям товаров для 1985 года')
    fig, ax = plt.subplots()
    ax.pie(product_sales1985.values, labels=product_sales1985.index, autopct='%.0f%%')
    st.pyplot(fig)

# Анализ по категориям продуктов
if section == 'Анализ по категориям продуктов':
    st.subheader('Анализ по категориям продуктов')
    st.write(df['ProductType'].value_counts())

    # Создание новой таблицы для работы с отдельными данными
    st.subheader('Создание новой таблицы для анализа категорий товаров')
    df_product = pd.DataFrame({
        'Категория товара': [
            'Фрукты и овощи','Закуски','Товары для дома','Замороженные продукты','Молочные продукты',
            'Консервы','Выпечка','Здоровье и гигиена','Безалкогольные напитки','Мясо','Хлеб','Крепкие напитки',
            'Другое','Бакалея','Завтрак','Морепродукты'
        ],
        'Количество': [1232,1200,910,856,682,649,648,520,445,425,251,214,169,148,110,64]
    })
    st.write(df_product)

    # Гистограмма количества продаж по категориям товаров
    st.subheader('Количество продаж товара по категориям')
    fig, ax = plt.subplots()
    df_product.groupby('Категория товара')['Количество'].mean().plot(ax=ax, kind='bar', rot=45, fontsize=10, figsize=(16, 10), color='purple')
    st.pyplot(fig)

# Самые продаваемые категории товаров
if section == 'Самые продаваемые категории товаров':
    st.subheader('Самые продаваемые категории товаров')
    product_counts = df['ProductType'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.barh(product_counts.index, product_counts.values, color='red')
    ax.set_title('Самые продаваемые категории товаров')
    ax.set_xlabel('Количество продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_counts)):
        ax.text(product_counts.values[i], i, str(product_counts.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Объем выручки по категориям товаров
if section == 'Объем выручки по категориям товаров':
    st.subheader('Объем выручки по категориям товаров')
    product_sales = df.groupby('ProductType')['OutletSales'].sum().sort_values(ascending=False).head(12)
    fig, ax = plt.subplots()
    ax.barh(product_sales.index, product_sales.values, color='green')
    ax.set_title('Объем выручки')
    ax.set_xlabel('Сумма продаж')
    ax.set_ylabel('Категории товаров')
    for i in range(len(product_sales)):
        ax.text(product_sales.values[i], i, round(product_sales.values[i]), ha='left', va='center')
    st.pyplot(fig)

# Локация магазина с самыми большими продажами
if section == 'Локация магазина с самыми большими продажами':
    st.subheader('Локация магазина с самыми большими продажами')
    st.write(df['LocationType'].value_counts())
    df_location = pd.DataFrame({'Магазин': ['Локация 1', 'Локация 2', 'Локация 3'], 'Количество продаж': [2388, 2785, 3350]})
    st.write(df_location)

    ilocation = df.groupby('LocationType')['OutletSales'].sum().index
    vlocation = df.groupby('LocationType')['OutletSales'].sum().values
    fig, ax = plt.subplots()
    ax.pie(vlocation, labels=ilocation, autopct='%.0f%%')
    st.pyplot(fig)

# Выводы
if section == 'Выводы':
    st.subheader('Выводы')
    st.markdown('''
    В ходе работы с данными торгового предприятия был проведен комплексный анализ, включающий следующие этапы:
    ''')
    st.subheader('Анализ категорий товаров') 
    st.markdown('''
Выявление самых продаваемых категорий товаров:
Проведен анализ по категориям товаров, чтобы определить, какие из них приносят наибольшую прибыль. Например, категории "Фрукты и овощи" и "Закуски" оказались лидерами по объемам продаж.
Построены графики и диаграммы, иллюстрирующие количество продаж по категориям и объем выручки.
    ''')
    st.subheader('Анализ нулевых значений') 
    st.markdown('''
    Проведен анализ пропущенных значений в данных. Обнаружены нулевые значения в столбцах "Weight" и "OutletSize".
    Выполнено заполнение пропущенных значений в столбце "Weight" средним значением, а в столбце "OutletSize" — значением "Средний".
    Выполнена проверка проделанной работы, убедившись, что нулевые значения успешно заполнены.
    Проведена проверка на наличие дубликатов и было установлено, что дубликатов в данных нет.
    ''')
    st.subheader('Анализ продаж по годам основания') 
    st.markdown('''
    Проведен анализ продаж по годам основания торговых точек. Определены годы с наибольшими объемами продаж.
    Проведен анализ самого прибыльного магазина по году основания. Для года 1985 построены гистограмма и круговая диаграмма, иллюстрирующие объем выручки по категориям товаров.
    ''')
    st.subheader('Анализ по локации магазинов') 
    st.markdown('''
    Проведен анализ локаций магазинов, чтобы определить, в каких типах городов расположены магазины с самыми большими продажами.
    Построена круговая диаграмма, иллюстрирующая распределение выручки по локациям.
    ''')
    st.subheader('Выводы') 
    st.markdown('''
    Проведен комплексный анализ данных торгового предприятия, включающий анализ категорий товаров, нулевых значений, продаж по годам основания и локациям магазинов.
    Определены категории товаров, приносящие наибольшую прибыль, и локации магазинов с самыми большими продажами.
    ''')
