import os
import sys


def func(arg1, arg2):
    print(arg1)
    print(arg2)


def main():
    """There are lots of ways to write a single script that can handle both
    using SGE_TASK_ID and command line arguments. This is just one example.
    """
    try:
        task_id = int(os.environ.get("SGE_TASK_ID")) - 1
        locations = [6, 97, 102, 156]
        years = [2000, 2005, 2010, 2015]

        location = locations[task_id // len(locations)]
        year = years[task_id % len(years)]
    except TypeError:
        args = sys.argv[1:]
        location = args[0]
        year = args[1]

    func(location, year)


if __name__ == "__main__":
    main()
