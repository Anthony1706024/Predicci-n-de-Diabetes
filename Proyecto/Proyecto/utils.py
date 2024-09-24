import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

def diabetes_prediction_model( new_data):
    # Carga los datos

    df = pd.read_csv('C:\\Users\\toni_\\OneDrive\\Desktop\\Analitica\\Proyecto\\Proyecto\\Media\\Obj3.csv')
    # Mapeo de categorías a valores numéricos
    ordinal_mapping1 = {
        '18-24': 1,
        '25-29': 2,
        '30-34': 3,
        '35-39': 4,
        '40-44': 5,
        '45-49': 6,
        '50-54': 7,
        '55-59': 8,
        '60-64': 9,
        '65-69': 10,
        '70-74': 11,
        '75-79': 12,
        '80+': 13
    }

    ordinal_mapping = {
        'Poor': 1,
        'Fair': 2,
        'Good': 3,
        'Very Good': 4,
        'Excellent': 5
    }

    # Aplicar el mapeo
    df.iloc[:, 7] = df.iloc[:, 7].map(ordinal_mapping)
    df['Age_Category'] = df.iloc[:, 2].map(ordinal_mapping1)
    df.iloc[:, 8] = df.iloc[:, 8].map({'Yes': 1, 'No': 0})
    df.iloc[:, 0] = df.iloc[:, 0].map({'Yes': 1, 'No': 0})
    df.iloc[:, 1] = df.iloc[:, 1].map({'Yes': 1, 'No': 0})
    df.iloc[:, 4] = df.iloc[:, 4].map({'Yes': 1, 'No': 0})
    df.iloc[:, 6] = df.iloc[:, 6].map({'Yes': 1, 'No': 0})

    # Asegurarse de que todas las columnas numéricas sean enteros
    df = df.apply(lambda x: x.astype(int) if x.dtype in ['float64', 'int64'] else x)

    # Definir las variables independientes y dependientes
    x = df.iloc[:, [1,2,3,4,5,6,7,8]].values
    y = df.iloc[:, 0].values

    # Asegurarse de que `y` sea un array de enteros
    y = y.astype(int)

    # Dividir el conjunto de datos
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Escalar las características
    st_x = StandardScaler()
    x_train = st_x.fit_transform(x_train)
    x_test = st_x.transform(x_test)

    # Crear y entrenar el modelo
    clf = LogisticRegression()
    clf.fit(x_train, y_train)

    # Hacer predicciones en los datos de prueba
    y_pred = clf.predict(x_test)
    
    # Calcular la matriz de confusión y la precisión
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    # Imprimir resultados del entrenamiento
    print("Matriz de Confusión:\n", cm)
    print("Precisión del modelo:", accuracy)

    # Escalar los nuevos datos con el mismo escalador usado para el entrenamiento
    new_data_scaled = st_x.transform([new_data])

    # Realizar la predicción
    prediction = clf.predict(new_data_scaled)
    prediction_prob = clf.predict_proba(new_data_scaled)

    # Resultados de la predicción
    resultado = "Presentara Enfermedad al corazon" if prediction[0] == 1 else "No Presentara enfermedad al corazon"
    probabilidad = prediction_prob[0][prediction[0]] * 100

    return resultado, probabilidad

# Ejemplo de uso

