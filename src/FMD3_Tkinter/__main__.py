import argparse
from FMD3_Tkinter.run_local import run_local
from FMD3_Tkinter.run_web_client import run_web


def main():
    parser = argparse.ArgumentParser(description='Specify API type.')
    parser.add_argument('--web', action='store_true', help='Use WebApi')
    parser.add_argument('--local', action='store_true', help='Use LocalApi')
    args = parser.parse_args()

    if args.web:
        run_web()
    else:
        run_local()

if __name__ == "__main__":
    main()
