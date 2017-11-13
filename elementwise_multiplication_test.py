import numpy as np


def main():
    a = np.array([[1,2],[3,4]])
    b = np.array([[1,2],[3,4]])

    print(np.multiply(a,b))
    print(a*b)

    print(a.dot(b))  # Dot product

    print(a**b)  # Element-wise exponentiation





if __name__ == '__main__':
    main()