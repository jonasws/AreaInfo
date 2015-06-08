#!/usr/bin/env python
import argparse
from area_info import app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-debug', dest='disable_debug', type=bool, default=False,
                        help='Run app with debugger disabled')

    args = parser.parse_args()

    if args.disable_debug:
        app.debug = False

    app.run()
