import argparse

class Main(object):
    
    def printMe(self,STR='default'):

        strToprint=f"runMe func printed requested string '{STR}'"
        print (strToprint)


if __name__ == "__main__":
    print('run_through_main')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*', type=str)
    args = parser.parse_args()
    main=Main()
    main.printMe(*args.args)
