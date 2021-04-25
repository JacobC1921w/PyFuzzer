#!/usr/bin/env python3

from PyNetTools.PyNetTools import *
from PyPrintSystem.PyPrintSystem import *
from sys import argv
from os import linesep
from time import sleep as delay

def doHelp(errorMessage, exitCode=1, verbose=False):
    if(exitCode != 0):
        p(errorMessage, 'e')

    p(argv[0] + " <opts>")
    print()
    
    p("<opts>:")
    p("\t-(-h)elp\t\t\tShow this help message")
    p("\t-(-v)erbose\t\t\tTurns on verbose messaging (like this one!)", 'v', True)
    p("\t-(t)arget-mode <targetMode>\tTarget mode to use (see <targetMode>)")
    p("\t-(-o)utput <outputMode>\t\tOutput mode to use (see <outputMode>)")
    print()

    p("<targetMode>:")
    p("\tscan\t\t\t\tScans the networks subnet for online hosts")
    p("\t<ip>\t\t\t\tSkips the scan and uses the specified <ip> instead (FASTER)")
    print()

    p("<outputMode>:")
    p("\tSTDOUT\t\t\t\tPrint any results to STDOUT")
    p("\t<logFile>\t\t\tWrite any output result to <logFile>")
    print()

    p("Exitting with code: " + str(exitCode), 'v', verbose)
    exit(exitCode)

verbose = False
skipThisIteration = False

if len(argv) == 1:
    doHelp("Argumental error", 1)
else:
    commandLineOptions = argv[1:]
    p("Checking command line arguments", 'v', verbose)
    for option in commandLineOptions:
        if skipThisIteration:
            skipThisIteration = False
            continue

        p("Iterating over option: " + option, 'v', verbose)

        if option.lower() in ["-h", "--help"]:
            doHelp("", 0, verbose)
        elif option.lower() in ["-v", "--verbose"]:
            p("Setting verbose to true", 'v', verbose)
            verbose = True
        elif option.lower() in ["-t", "--target-mode"]:
            p("Setting target mode", 'v', verbose)
            skipThisIteration = True
            try:
                if commandLineOptions[commandLineOptions.index(option) + 1].lower() == "scan":
                    p("Target mode set to scan", 'v', verbose, "", linesep + linesep)
                    targetHost = ""
                else:
                    p("Target host set manually to " + commandLineOptions[commandLineOptions.index(option) + 1], 'v', verbose, "", linesep + linesep)
                    targetHost = commandLineOptions[commandLineOptions.index(option) + 1]
            except IndexError:
                doHelp("Expected <targetMode> after: " + option, 2, verbose)
        elif option.lower() in ["-o", "--out"]:
            p("Setting output mode", 'v', verbose)
            skipThisIteration = True
            try:
                if commandLineOptions[commandLineOptions.index(option) + 1].lower() == "stdout":
                    p("Output mode set to STDOUT", 'v', verbose, "", linesep + linesep)
                    outputFile = "STDOUT"
                else:
                    p("Outputting to file: " + commandLineOptions[commandLineOptions.index(option) + 1], 'v', verbose, "", linesep + linesep)
                    outputFile = commandLineOptions[commandLineOptions.index(option) + 1]
            except IndexError:
                doHelp("Expected <outputMode> after: " + option, 3, verbose)

p("ToDo:")
p("- Scan network (or add host manually)")
p("- Port scan host")
p("- Select ports to fuzz, or all")
p("- Send all data to port, or autodetect service")
p("- Print responses to STDOUT or to log file")
p("- Jacob, you need to dump network data, like http packets and whatnot, and save them to a temporary directory, to analyze!", 'w')
