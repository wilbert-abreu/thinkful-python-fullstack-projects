#this module will allow you to track what happens in the application and help you identify problems in the code


import logging
import argparse
import sys
import psycopg2

#set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established")


def put(name, snippet):

    """Store a snippet with an associated name."""
    #will report the log, FIXME identifies the problem both in the source and the log, !r modifer means that the repr() funtions runs, the repr() function returns a string containing printable version of the object
    # logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    # cursors allow you to run SQL commands in the postgress session
    cursor = connection.cursor()

    """old code
    #save sql statement
    try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
    except:
        #connection.rollback() undue, gets database to original state
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s)"
        cursor.execute(command, (snippet, name))
    connection.commit()
"""
    with connection, connection.cursor() as cursor:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))

    # save changes to the database

    logging.debug("Snippet stored successfully")
    return name,snippet

def get(name):
    """
    Retrieve the snippet with a given name.

    If there is no such snippet...

    Returns the snippet.
    """
    # logging.error("FIXME: Unimplemented - get({!r})".format(name))
    with connection, connection.cursor() as cursor:
        command = "select message FROM snippets WHERE keyword= %s"
        cursor.execute(command, (name,))
        message = cursor.fetchone()
    logging.info("Retrieving snippet {!r}".format(name))

    """old code
        # cursors allow you to run SQL commands in the postgress session
        cursor = connection.cursor()
        #save sql statement
        command = "select message FROM snippets WHERE keyword= %s"
        cursor.execute(command, (name,))
        # fetchone() returns a tuple of values for each field.
        message = cursor.fetchone()
    """

    if not message:
        name = input("Snippet not found, please input another: ")#no snippet was found with that name
        with connection, connection.cursor() as cursor:
            command = "select message FROM snippets WHERE keyword= %s"
            cursor.execute(command, (name,))
            message = cursor.fetchone()
    logging.debug("Snippet Retrieved successfully")

    return message

def catalog():
    logging.info("Retrieving catalog")

    with connection, connection.cursor() as cursor:
        command = "select keyword FROM snippets order by keyword"
        cursor.execute(command)
        catalog = cursor.fetchall()
    logging.debug("Retrieved catalog successfully")

    return catalog

def search(query):
    logging.info("Searching snippets")

    with connection, connection.cursor() as cursor:
        command = "select * from snippets where keyword like '%%'||%s||'%%' OR message like '%%'||%s||'%%'"
        cursor.execute(command, (query,query))
        search_result = cursor.fetchall()
    if not search_result:
        next_query = input("Nothing to see here..Please enter another search query: ")
        with connection, connection.cursor() as cursor:
            command = "select * from snippets where keyword like '%%'||%s||'%%' OR message like '%%'||%s||'%%'"
            cursor.execute(command, (next_query,next_query))
            search_result = cursor.fetchall()

    logging.debug("Retrieved search result")

    return search_result

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

    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")

    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve the catalog")

    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve the catalog")
    search_parser.add_argument("query", help="Search query")

    arguments = parser.parse_args(sys.argv[1:])

    #convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        # **arguments is the same as put(name="list", snippet="A sequence of things - created using []")
        print("Stored {!r} as {!r}".format(snippet,name))
    elif command == "catalog":
        full_catalog = catalog()
        print("Retrieved catalog: {!r}".format(full_catalog))
    elif command == "search":
        search_request = search(**arguments)
        print("Retrieved snippet: {!r}".format(search_request))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))





if __name__ == '__main__':
    main()





