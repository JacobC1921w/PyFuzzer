#!/usr/bin/env python3

from PyNetTools.PyNetTools import *
from PyPrintSystem.PyPrintSystem import *
from sys import argv, maxsize
from os import linesep, path
from time import sleep as delay
from random import randint
from multiprocessing.dummy import Pool
from itertools import repeat

def doHelp(errorMessage, exitCode=1, verbose=False):
    if(exitCode != 0):
        p(errorMessage, 'e')

    p(argv[0] + " <opts>")
    print()
    
    p("<opts>:")
    p("\t-(-h)elp\t\t\tShow this help message")
    p("\t-(t)arget <target>\t\tTarget mode to use (see <target>)")
    p("\t-(-o)utput <outputMode>\t\tOutput mode to use (see <outputMode>)")
    p("\t-(-v)erbose\t\t\tTurns on verbose messaging (like this one!)", 'v', True)
    print()

    p("<target>:")
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
seed = str(randint(-int(maxsize)-1,int(maxsize)))
onlineHosts = 0
hosts = []
userChoice = ""
openPorts = []

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
        elif option.lower() in ["-t", "--target"]:
            p("Setting target mode", 'v', verbose)
            skipThisIteration = True
            try:
                if commandLineOptions[commandLineOptions.index(option) + 1].lower() == "scan":
                    p("Target mode set to scan", 'v', verbose, "", linesep + linesep)
                    targetHost = seed + "scan" + seed
                else:
                    p("Target host set manually to " + commandLineOptions[commandLineOptions.index(option) + 1], 'v', verbose, "", linesep + linesep)
                    targetHost = commandLineOptions[commandLineOptions.index(option) + 1]
            except IndexError:
                doHelp("Expected <targetMode> after: " + option, 1, verbose)
        elif option.lower() in ["-o", "--out"]:
            p("Setting output mode", 'v', verbose)
            skipThisIteration = True
            try:
                if commandLineOptions[commandLineOptions.index(option) + 1].lower() == "stdout":
                    p("Output mode set to STDOUT", 'v', verbose, "", linesep + linesep)
                    outputFile = seed + "STDOUT" + seed
                else:
                    p("Outputting to file: " + commandLineOptions[commandLineOptions.index(option) + 1], 'v', verbose, "", linesep + linesep)
                    outputFile = commandLineOptions[commandLineOptions.index(option) + 1]
            except IndexError:
                doHelp("Expected <outputMode> after: " + option, 2, verbose)
        else:
            doHelp("Unexpected option: " + option, 3)

p("Verifying CL arguments", 'v', verbose)
if targetHost != (seed + "scan" + seed):
    if ping(targetHost, 5):
        p(targetHost + " is up!", 's')
    else:
        doHelp(targetHost + " doesn't appear to be online", 4, verbose)

if outputFile != (seed + "STDOUT" + seed):
    if path.isfile(outputFile):
        p(outputFile + " exists, appending to file")
    else:
        p(outputFile + " doesn't exist, creating it")
        with open(outputFile, "w+") as f:
            f.write("# Start of " + outputFile)

if targetHost == (seed + "scan" + seed):
    for host in (parseScan(hostScan(getPrivateIP()), getPrivateIP())[0]):
        onlineHosts += 1
        hosts.append(host)
        p(host + " was found online", 's')

    if onlineHosts == 0:
        doHelp("No hosts appear to be online", 4, verbose)
    elif onlineHosts == 1:
        userChoice = i("One host appears to be online, would you like to use this one? [Y/n]")
        if userChoice.lower() in ["y", "yes", ""]:
            targetHost = hosts[0]
        else:
            doHelp("No host spewcified", 5, verbose)
    else:
        p("Multiple hosts appear to be online!, please choose one below:", 's')
        for host in hosts:
            p("[" + str(hosts.index(host)) + "] " + host)

        userChoice = i("Host index: ")
        if userChoice in ["{:d}".format(x) for x in range(len(hosts))]:
            targetHost = hosts[int(userChoice)]
        else:
            doHelp("Host index " + userChoice + " out of range: 0-" + str(len(hosts) - 1), 6)

p("Portscanning " + targetHost)

p("ToDo:")
p("- Add CLA parser", 's')
p("- Verify CLA variables", 's')
p("- Scan network (or add host manually)", 's')
p("- Port scan host")
p("- Select ports to fuzz, or all")
p("- Send all data to port, or autodetect service")
p("- Print responses to STDOUT or to log file")
p("- Jacob, you need to dump network data, like http packets and whatnot, and save them to a temporary directory, to analyze!", 'w')
