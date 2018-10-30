import sys
sys.path.insert(0, '../predict')
from predict import Model

model = Model()


def main():

    # Load keras model
    model.load()
    print(model.predictTest())


if __name__ == '__main__':
    main()
