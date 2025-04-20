import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar datos y preprocesado básico
df_instagram = pd.read_csv("C:\\Users\\thesa\\Downloads\\comments.csv")
df_instagram["text_clean"] = df_instagram["comment_text"].fillna("")

# 2. Configurar VADER
analyzer = SentimentIntensityAnalyzer()

# 3. Función de clasificación con umbrales ajustables
def clasificar_sentimiento(texto):
    scores = analyzer.polarity_scores(texto)
    if scores['compound'] >= 0.05:
        return 'Positive'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# 4. Aplicar a todos los comentarios
df_instagram['sentiment'] = df_instagram['text_clean'].apply(clasificar_sentimiento)

# 5. Visualización
plt.figure(figsize=(10,6))
ax = sns.countplot(
    data=df_instagram,
    x='sentiment',
    order=['Negative', 'Neutral', 'Positive'],
    palette={'Negative':'#ff9999', 'Neutral':'#66b3ff', 'Positive':'#99ff99'}
)

plt.title('Distribución de Sentimientos en Comentarios', fontsize=14)
plt.xlabel('Tipo de Sentimiento', fontsize=12)
plt.ylabel('Cantidad de comentarios', fontsize=12)

total = len(df_instagram)

# Mostrar conteo + % encima de cada barra
for p in ax.patches:
    count = int(p.get_height())
    percentage = 100 * count / total
    label = f'{count} - {percentage:.1f}%'
    x = p.get_x() + p.get_width() / 2
    y = count + total * 0.001  
    ax.annotate(label, (x, y), ha='center', fontsize=12)

plt.show()

