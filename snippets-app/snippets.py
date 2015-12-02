#this module will allow you to track what happens in the application and help you identify problems in the code


import logging
import argparse
import sys

#set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):

    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    #will report the log, FIXME identifies the problem both in the source and the log, !r modifer means that the repr() funtions runs, the repr() function returns a string containing printable version of the object
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name,snippet

def get(name):
    """
    Retrieve the snippet with a given name.

    If there is no such snippet...

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))

    return ""


def main():
    """Main Function"""
    logging.info("Constructing parser")
    #describes the interface and parses the list of arguments
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    argument = parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()





