"""

"""

from titanic.data import load_data,clean_data,prepare_data
from titanic.registry import save_model, load_model
from titanic.train import train_model, evaluate_model


def train():
    data= load_data(train=True)
    data = clean_data(data)
    X, y = prepare_data(data, fit=True, survive=True)
    model = train_model(X, y)
    save_model(model, "best_model.pkl", cloud=True)
    import os
    os.remove("/Users/aloys.bernard/Downloads/titanic/models/best_model.pkl")
    model = load_model("best_model.pkl", cloud=True)
    data_test = load_data(train=False)
    data_test = clean_data(data_test)
    X_test, y_test = prepare_data(data_test, fit=False, survive=True)
    print(evaluate_model(X_test,y_test,model)    )
    
if __name__ == "__main__":
    train()
