import argparse
import multiprocessing


def main():
    parser = argparse.ArgumentParser(description='Specify API type.')
    parser.add_argument('--web', action='store_true', help='Use WebApi')
    parser.add_argument('--local', action='store_true', help='Use LocalApi')
    args = parser.parse_args()

    if args.web:
        from FMD3_Tkinter.run_web_client import run_web
        run_web()
        # pass
    else:
        from FMD3_Tkinter.run_local import run_local
        run_local()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
