from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords

# Загружаем стоп-слова для русского языка
nltk.download('stopwords')
russian_stopwords = stopwords.words('russian')

products_df = pd.read_excel('data/Список товаров.xlsx')
categories_df = pd.read_excel('data/Дерево категорий.xlsx')
supplier_data = pd.read_excel('data/Данные поставщика.xlsx')

vectorizer = TfidfVectorizer(stop_words=russian_stopwords)

categories = categories_df['Дочерняя категория'].tolist()
types = categories_df['Тип товара'].tolist()

category_vectors = vectorizer.fit_transform(categories)


def get_product_type(product_name):
    # Векторизация названия товара
    product_vector = vectorizer.transform([product_name])

    # Вычисляем косинусное сходство между вектором товара и векторами категорий
    cosine_similarities = cosine_similarity(product_vector, category_vectors)

    # Находим индекс наиболее похожей категории
    most_similar_index = cosine_similarities.argmax()

    # Возвращаем соответствующий тип товара
    return types[most_similar_index]


# Применяем функцию ко всем товарам
products_df['Предсказанный тип товара'] = products_df['Наименование'].apply(get_product_type)

correct_predictions = products_df[products_df['Предсказанный тип товара'] == products_df['Тип товара']]
products_df.to_excel('Результаты предсказаний_nlp_russian.xlsx', index=False)
print(f"Правильных предсказаний: {len(correct_predictions)} из {len(products_df)}")
