import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns

def preprocess_data(dataset):
    """
    Preprocessa il dataset meteorologico
    """
    dataset = pd.read_csv('../dataset/stazione_molfetta_anno_2023.csv', sep=';', header=0)

    # Converti la colonna data in datetime
    dataset['data'] = pd.to_datetime(dataset['data'])
    
    # Aggiungi feature temporali
    dataset['hour'] = dataset['data'].dt.hour
    dataset['month'] = dataset['data'].dt.month
    
    # Seleziona le feature rilevanti
    features = ['temperatura', 'umr', 'vvento', 'dvento', 'radsolare', 'pressione', 
                'hour', 'month']
    
    X = dataset[features]
    
    # Converti precipitazione in classificazione binaria (pioggia/non pioggia)
    y = (dataset['precipitazione'] > 0).astype(int)
    
    return X, y

def train_and_evaluate_model(X, y):
    """
    Addestra e valuta il modello
    """
    # Split dei dati
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Crea e addestra il modello
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X_train, X_test, y_train, y_test

def plot_learning_curves(model, X, y):
    """
    Genera le curve di apprendimento
    """
    train_sizes, train_scores, valid_scores = learning_curve(
        model, X, y,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5,
        scoring='accuracy'
    )
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
    plt.plot(train_sizes, np.mean(valid_scores, axis=1), label='Cross-validation score')
    plt.xlabel('Training examples')
    plt.ylabel('Score')
    plt.title('Learning Curves')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

def plot_feature_importance(model, X):
    """
    Visualizza l'importanza delle feature
    """
    importance = model.feature_importances_
    feat_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feat_importance)
    plt.title('Feature Importance')
    plt.show()

def plot_confusion_matrix_custom(y_true, y_pred):
    """
    Visualizza la matrice di confusione
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def analyze_precipitation_prediction(dataset):
    """
    Analisi completa del modello di predizione precipitazioni
    """
    # Preprocessamento
    X, y = preprocess_data(dataset)
    
    # Training
    model, X_train, X_test, y_train, y_test = train_and_evaluate_model(X, y)
    
    # Valutazione
    y_pred = model.predict(X_test)
    
    # Stampa report di classificazione
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Visualizzazioni
    print("\nGenerating visualizations...")
    plot_learning_curves(model, X, y)
    plot_feature_importance(model, X)
    plot_confusion_matrix_custom(y_test, y_pred)
    
    return model