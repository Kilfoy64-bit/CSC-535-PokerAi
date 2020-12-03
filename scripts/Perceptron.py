import pandas as pd
import numpy as np


class Perceptron:
    def __init__(self, wvec_size: int, lrate: float, weights = None, bias = None):
        '''
        Perceptron Constructor Function
        This program creates a perceptron and initializes a bias to a random value b_0 is in {b_0 | 0 ≤ b_0 < 1}
        and initializes a weights vector to a random value

        Parameters:
        wvec_size            int            predefined weight vector size
        lrate                float          the learn rate of the model

        Returns:
        Perceptron            The generated perceptron
        '''
        self._learn_rate = lrate

        if weights is not None and bias is not None:
            self._weights = weights
            self._bias = bias
        else:
            self._weights = np.random.random(wvec_size)
            self._bias = np.random.random()
        #print("Starting weights: " + str(self._weights))

    def weights(self):
        '''
        Getter function to return private variable self._weights
        '''
        return self._weights

    def learn_rate(self):
        '''
        Getter function to return private variable self._learn_rate
        '''
        return self._learn_rate

    def bias(self):
        '''
        Getter function to return private variable self._bias
        '''
        return self._bias

    def learn(self, point: np.array, classif: int):
        '''
        FUNCTION learn
        This function accepts an input vector and a classification and
        adjusts weights according to the algorithm as follows:
        LOOP
            IF (W_n·v + b_n ≤ 0 and k = 1) OR (W_n·v + b_n > 0 and k = -1)
                W_(n+1) = W_n + λkv
                b_(n+1) = b_n + kλ
            END IF
        END LOOP
        Where λ is in {λ | 0 ≤ λ < 1}
        k is the classification value integer representation,
        v is the input vector,
        b is the learned bias

        A special termination condition has been set to terminate weight
        updates at an arbitrarily high value (n = 100,000) because this
        value is sufficiently high enough to allow W to converge to an accurate
        target weight vector and low enough to maintain calculation speed.

        Parameters:
        point            np.array            array representation of an input vector
        classif          int                 the target classification
        '''
        iteration = 0
        while True:
            dot_product = np.dot(self._weights, point) + self._bias
            if (dot_product <= 0 and classif == -1) or iteration >= 100000:
                break
            elif dot_product > 0 and classif == 1:
                break
            else:
                self._weights = self._weights + \
                    (classif * self._learn_rate * point)
                self._bias = self._bias + (classif * self._learn_rate)
                iteration += 1

    def classify(self, point: np.array):
        '''
        FUNCTION classify
        This function returns 1 if W·v + b > 0 and -1 if W·v + b ≤ 0
        '''
        # print(point)
        # print(self._weights)
        return 1 if np.dot(self._weights, point) + self._bias > 0 else -1


def train(filename: str, threshold: float) -> (list, float, int):
    accuracy = 0
    epochs = 0
    drawPerc = Perceptron(6, 0.2)
    while accuracy < threshold:
        df = pd.read_csv(filename)
        test_data = df.sample(frac=0.2).copy()
        df.drop(test_data.index, inplace=True)
        for row in df.iterrows():
            cur_row = row[1].to_numpy()
            drawPerc.learn(cur_row[0:len(cur_row) - 1],
                           cur_row[len(cur_row) - 1])
        hits = 0
        misses = 0
        for row in test_data.iterrows():
            cur_row = row[1].to_numpy()
            if drawPerc.classify(cur_row[0:len(cur_row)-1]) == cur_row[len(cur_row) - 1]:
                hits += 1
            else:
                misses += 1
        if accuracy < hits / (hits+misses):
            accuracy = hits/(hits+misses)
        epochs += 1
    return (drawPerc.weights(), accuracy, epochs, drawPerc.bias())

def main():

    weights, accuracy, epochs, bias = train("./datasets/drawmd.csv", 0.6)
    print("Draw")
    print("Weights", weights)
    print("Bias", bias)
    print("Accuracy: %f" % accuracy)
    print("Training Epochs: %i" % epochs)

    weights, accuracy, epochs, bias = train("./datasets/flopmd.csv", 0.6)
    print("Flop")
    print("Weights", weights)
    print("Bias", bias)
    print("Accuracy: %f" % accuracy)
    print("Training Epochs: %i" % epochs)

    weights, accuracy, epochs, bias = train("./datasets/turnmd.csv", 0.6)
    print("Turn")
    print("Weights", weights)
    print("Bias", bias)
    print("Accuracy: %f" % accuracy)
    print("Training Epochs: %i" % epochs)

    weights, accuracy, epochs, bias = train("./datasets/rivermd.csv", 0.6)
    print("River")
    print("Weights", weights)
    print("Bias", bias)
    print("Accuracy: %f" % accuracy)
    print("Training Epochs: %i" % epochs)

if __name__ == "__main__":
    main()