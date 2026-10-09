"""Small training/inference fixture with explicit parameter updates."""


class LinearModel:
    def __init__(self, weight=0.0, bias=0.0):
        self.weight = weight
        self.bias = bias

    def forward(self, x):
        return self.weight * x + self.bias


def train_step(model, x, target, learning_rate):
    prediction = model.forward(x)
    error = prediction - target
    loss = error * error
    model.weight -= learning_rate * 2 * error * x
    model.bias -= learning_rate * 2 * error
    return loss


def predict(model, x):
    return model.forward(x)
