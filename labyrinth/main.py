import argparse
from time import perf_counter

import params
import maze

# Тестовая стока
# python main.py -wh 30 40 -sol -sp 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-wh', '--size', nargs=2, type=int, required=True,
                        help='Maze width and height (from 3 to 200)')
    parser.add_argument('-sol', '--solution', action="store_true",
                        help="Do you need a solution?")
    parser.add_argument('-l', '--load', type=str,
                        help="Path to the file which stores a maze"
                             "(txt / png / jpg)")
    parser.add_argument('-st', '--save_text', type=str,
                        help="Name of the file that will store maze as text"
                             "(txt)")
    parser.add_argument('-si', '--save_image', type=str,
                        help="Name of the file that will store maze as image"
                             "(png / jpg)")
    parser.add_argument('-sp', '--speed', type=int,
                        help='Speed for solution visualisation(1-10)')
    args = vars(parser.parse_args())

    args = params.check_args(args)
    if args:
        start_time = perf_counter()
        print(f'{args=}')
        maze.start_maze(args[0], args[1], args[2], args[3], args[4], args[5],
                        args[6])

        # Время работы
        print(f"Work time: {perf_counter() - start_time} seconds")
    else:
        print("Maze wasn't created")

    print("Program completed")
