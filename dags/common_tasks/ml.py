import pandas as pd
from tpot import TPOTRegressor
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


def tpot_regression(data_location, output_location, target):
    print('tpot_regression')
    df = pd.read_csv(data_location)
    cols = [c for c in df.columns if c != target]
    df['x2'] = df['x'] ** 2

    X_train, X_test, y_train, y_test = train_test_split(
        df[['x', 'x2']], df[target],
        train_size=0.75, test_size=0.25)

    tpot = TPOTRegressor(
        generations=2, population_size=5, cv=5,
        random_state=42, verbosity=2, n_jobs=1)
    tpot.fit(X_train, y_train)

    print(tpot.score(X_test, y_test))
    tpot.export(output_location + '.py')
    joblib.dump(tpot.fitted_pipeline_, output_location)
