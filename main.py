#!/usr/bin/env python3
from stdlib import *
from os import path, mkdir
from time import sleep
from datetime import datetime, date
from inspect import stack as funcname

arg = arg()
arg.add_argument('-q', '--quiet', help="Make program output be as quiet as possible")
args = arg.parse_args()

defaultarchive = True
defaultarget = "/mnt/backup"
defaultformat="%Y/%m/%d %H:%M:%S"
defaultarchiveformat = 'targz'
supportedarchiveformat = ['zip', 'targz', 'gz', 'tar', 'bz2', 'rar', 'tbz2', 'Z', '7z']



def backup(target_so, multiso: bool, target: str, format, archive: bool, archiveformat: str):
    # verify configuration
    if args.q:
        from sys import stdout, stderr
        from os import devnull
        stdout = open(devnull, 'w')
        stderr = open(devnull, 'w')
    printinfo(f"backup(): recive infomation/configuration: \ttarget_so: {target_so}, target: {target}, multi-target_so: {multi-target_so}, format: {format}, archive: {archive}, archive-format: {archiveformat}")
    if not args.q:
        if 'n' in ainputf("[?] Is this Correct?(Y/n):: ").lower():
            main()
    # start copying operations
    from shutil import copy, copytree
    target += f'/{date.today().strftime(format)}'
    mkdir(target)
    if multiso:
        for l in target_so:
            if path.isdir(l):
                printinfo(f"Copying Directory {path.abspath(l)} -> {target}")
                copytree(l, target)
            elif path.isfile(l):
                printinfo(f"Copying File {path.abspath(l)} -> {target}")
                copytree(l, target)
    else:
        if path.isdir(target_so):
            printinfo(f"Copying Directory {path.abspath(l)} -> {target}")
            copytree(l, target)
        elif path.isfile(target_so):
            printinfo(f"Copying File {path.abspath(l)} -> {target}")

    if archive:
        from shutil import make_archive
        make_archive(f"{target}.{archiveformat}", archiveformat, target)


def main():
    # get configuration
    target_so = ''
    while target_so == '':
        target_so = ainputf(f"{ascii.color.green}[*] What do you want to backup(files or directory):: ")
        if ',' in target_so:
            localtarget_so = target_so.split(',')
            for l in localtarget_so:
                if l == '' or not path.exists(l):
                    printerror("Please enter a valid file")
                    exit(1)
            multiso = True
        else:
            l = target_so
            if target_so == '' or not path.exists(l):
                printerror("Please enter a valid file")
                exit(1)
            multiso = False


    target = None
    while target == None:
        target = ainputf(f"{ascii.color.green}[*] Where do you want to place them(default /mnt/backup):: ")
        if target == '':
            target = defaultarget
        elif not path.exists(target):
            printerror("Please enter a valid or folder")
            exit(1)


    format = ainputf(f"{ascii.color.green}[*] What format do you want it to be(default %Y/%m/%d%H:%M:%S):: ")
    if format == '':
        format = defaultformat

    archive = None
    while archive == None or archive.lower() not in ['y', 'n', 'yes', 'no']:
        if archive == None or archive.lower() not in ['y', 'n', 'yes', 'no']:
            printerror("Please enter yes or no")
        ainputf("[*] Do you want to archive it after backing it up:: ")
    if archive.lower() in ['y', 'yes']:
        archive = True
    elif archive.lower() in ['n', 'no']:
        archive = False

    if archive:
        archiveformat = None
        while archiveformat == None or archiveformat not in supportedarchiveformat and not archiveformat == '':
            if archiveformat == '':
                archiveformat = defaultarchiveformat
            elif archiveformat not in supportedarchiveformat:
                printerrorf(f"Please enter a valid archive format {supportedarchiveformat}")
            archiveformat = ainputf("[*] Please enter a archive format::")


    printwarning("System will start backing up in ", end='')
    countdown(3)
    printwarning(f"{ascii.color.green}[*] System backup started in {datetime.now()}")
    
    backup(target_so, multiso, target, format, archive, archiveformat)


if __name__ == "__main__":
    main()
