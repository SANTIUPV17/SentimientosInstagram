import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Descargar recursos de nltk 
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Cargar el dataset de entrenamiento
df_train = pd.read_csv("C:\\Users\\thesa\\Downloads\\dataset_entrenamiento.csv", encoding='latin-1', header=None)

# Asignar nombres a las columnas
df_train.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']

# Nos quedamos solo con texto y sentimiento (0 negativo, 4 positivo)
df_train = df_train[df_train['target'].isin([0, 4])]
df_train['label'] = df_train['target'].map({0: 'negative', 4: 'positive'})

# Preprocesamiento
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    tokens = nltk.word_tokenize(str(text).lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

df_train["text_clean"] = df_train["text"].apply(clean_text)

# Separar entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(df_train["text_clean"], df_train["label"], test_size=0.2, random_state=42)

# Pipeline con Naive Bayes
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', MultinomialNB())
])

pipeline.fit(X_train, y_train)

# Evaluar
y_pred = pipeline.predict(X_test)
print("== Evaluación del modelo ==")
print(classification_report(y_test, y_pred))

# Aplicar nuestro dataset de nintendo
df_instagram = pd.read_csv("C:\\Users\\thesa\\Downloads\\comments.csv")
df_instagram["text_clean"] = df_instagram["comment_text"].fillna("").apply(clean_text)
df_instagram["sentiment"] = pipeline.predict(df_instagram["text_clean"])

# Visualización
plt.figure(figsize=(10,6))
ax = sns.countplot(
    data=df_instagram,
    x='sentiment',
    order=['negative', 'positive'],
    palette={'negative':'#ff9999', 'positive':'#99ff99'}
)

plt.title('Distribución de Sentimientos (Naive Bayes)', fontsize=14)
plt.xlabel('Sentimiento', fontsize=12)
plt.ylabel('Cantidad', fontsize=12)

total = len(df_instagram)

# Mostrar conteo + %
for p in ax.patches:
    count = int(p.get_height())
    percentage = 100 * count / total
    label = f'{count} - {percentage:.1f}%'
    x = p.get_x() + p.get_width() / 2
    y = count + total * 0.001
    ax.annotate(label, (x, y), ha='center', fontsize=12)

plt.tight_layout()
plt.show()
