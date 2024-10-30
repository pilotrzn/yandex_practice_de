import os


def main(a, b):
    return a + b


if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{parent_dir}/input.txt', 'r') as file_in:
        a = int(file_in.readline())
        b = int(file_in.readline())
    result = main(a, b)

    with open('output.txt', 'w') as file_out:
        file_out.write(str(result))