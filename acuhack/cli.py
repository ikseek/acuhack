from argparse import ArgumentParser
from asyncio import get_event_loop
from logging import basicConfig

from .spoof import spoof
from .web import run


def main():
    parser = ArgumentParser("Acurite Smart Hub hack")
    parser.add_argument('-i', '--interface', type=str, help='Interface directly connected to Acurite Smart Hub')
    parser.add_argument('-v', '--verbosity', type=str, help='Logging level')
    args = parser.parse_args()
    if args.verbosity:
        basicConfig(level=args.verbosity.upper())
    if args.interface:
        get_event_loop().create_task(spoof(args.interface))
    run(host='0.0.0.0', port=80)
