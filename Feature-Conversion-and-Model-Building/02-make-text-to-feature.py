from sklearn.preprocessing import MaxAbsScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = pd.read_csv('New_Merge_Data_Comment.csv')

# Tf-idf
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
X = tfidf_vectorizer.fit_transform(df['Comment'])

# MaxAbs scaling directly on sparse matrix
scaler = MaxAbsScaler()
X = scaler.fit_transform(X)

# Label Encoding
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['Class'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# HyperParameter Tuning
param_grid = {
    'C': [0.1, 1, 10],
    'penalty': ['l2']  # Only 'l2' penalty is supported by LBFGS solver
}

model = LogisticRegression(max_iter=1000)  # Increase max_iter
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best parameters for Logistic Regression:", best_params)
print("Best score for Logistic Regression:", best_score)



# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best parameters for Random Forest:", best_params)
print("Best score for Random Forest:", best_score)