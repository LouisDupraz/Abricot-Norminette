#!/usr/bin/python3

import os
from program.abriThread import Abrifast
from program.profile import rules
from abricot import getAllErrors, TokenizerObject, getSourceFileNames, prepareGetSourceFileNames, prepareGetAllLines
from program.arguments import parser
from program.output import OutputManager
from program.ignored import getIgnoredFiles
from program.configuration import Configuration
from program.print import printc, Colors
from utils import is_header_file, is_makefile, is_source_file


args = parser.parse_args()
thread = Abrifast()

config = Configuration()


if args.file:
    if os.path.isdir(args.file):
        config.dir = args.file
    elif os.path.isfile(args.file):
        config.file = args.file
    else:
        printc("ERROR: File or directory '%s' not found" %
               args.file, bold=True, color=Colors.RED)
        exit(1)


if args.update:
    from program.updater import update
    update()

if args.version:
    from __init__ import showVersion
    showVersion()

try:
    os.system("find tests/ -type f -print > .abricotbaseignore 2> /dev/null")
    os.system("find bonus/ -type f -print >> .abricotbaseignore 2> /dev/null")
    with open(".abricotbaseignore", "r") as f:
        basic_ignored = f.readlines()
    os.system("rm .abricotbaseignore")
except:
    basic_ignored = []

config.ignored = [x[2:].replace("\n", "") if x.startswith("./") else x.replace("\n", "") for x in basic_ignored]

if args.ignore:
    config.ignored += getIgnoredFiles()

prepareGetSourceFileNames(config)

parseFiles = list(filter(lambda x: is_source_file(x) or is_makefile(x) or is_header_file(x), getSourceFileNames()))

prepareGetAllLines(parseFiles)

TokenizerObject.setFiles(parseFiles)

for rule in rules.values():
    if rule.code == "C-FN" and args.nofunc:
        continue
    if not rule.optional or args.all:
        thread.add(rule.checker, (), rule.name)

thread.run()

errors = getAllErrors()
output = OutputManager(errors)
output.groupBy(args.group)
output.showAs(args.format)

if args.status:
    exit(len(errors) > 0)
