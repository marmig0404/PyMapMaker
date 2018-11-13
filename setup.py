import sys


deps = ['ensurepip', 'geopy']
pypi_deps = deps
deps.extend(['mapnik', 'python-mapnik', 'mysql-connector'])


def check_dependencies():
    try:
        from address2img import render
        import database
        import mapnik
        import mysql.connector
    except ImportError:
        try:
            import helpers
            helpers.write_to_log("Error loading dependencies. Make sure they are all installed.")
            helpers.write_to_log("Dependencies: " + ','.join(deps))
            sys.exit(5)
        except ImportError:
            print("Error Loading helpers.py")
            sys.exit(6)
    return True


def install_dependencies():

    try:
        from setuptools import setup, find_packages
        setup(
            name='PyMapMaker',
            version='1.0',
            install_requires=deps,

        )
    except ImportError:
        print("Could not setup install dependencies!")


def clean():
    pass


def first_run():
    print("Preparing for first time run.")
    print("Looking for dependencies")
    if not check_dependencies():
        install_dependencies()

#/Users/martinmiglio/PycharmProjects/PyMapMaker/venv/bin/python