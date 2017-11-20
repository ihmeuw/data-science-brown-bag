import sys


def func(arg1, arg2):
    print(arg1)
    print(arg2)


def main():
    args = sys.argv[1:]
    func(args[0], args[1])


if __name__ == "__main__":
    main()
