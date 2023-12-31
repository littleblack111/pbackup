#!/usr/bin/env python3
from stdlib import *
from os import path, mkdir
from time import sleep
from datetime import datetime, date
from inspect import stack as funcname

defaultarchive = True
defaultarget = "/mnt/backup"
defaultformat="%Y/%m/%d %H:%M:%S"
defaultarchiveformat = 'zip'
supportedarchiveformat = ['zip', 'tgz', 'gz', 'tar', 'bz2', 'rar', 'tbz2', 'Z', '7z']
successbanner = "=====================SUCCESS====================="



def backup(target_so, multiso: bool, target: str, format, archive: bool, archiveformat: str):
    # verify configuration
    printinfo(f"backup(): recive infomation/configuration: \ttarget_so: {target_so}, target: {target}, multi-target_so: {multiso}, format: {format}, archive: {archive}, archive-format: {archiveformat}")
    if 'n' in ainputf("[?] Is this Correct?(Y/n):: ").lower():
        main()

    printwarning("System will start backing up in ", end='')
    countdown(3)
    printwarning(f"{ascii.color.green}[*] System backup started in {datetime.now()}")


    from shutil import copy, copytree
    # Start copying operations
    target = path.abspath(target)
    target += f'/{date.today().strftime(format)}'.replace('/', '_').replace(' ', '_')
    mkdir(target)
    
    if multiso:
        for l in target_so:
        	if path.isdir(l):
        		printinfo(f"Copying Directory {path.abspath(l)} -> {target}")
        		copytree(l, target)
                printinfo(successbanner)
        	elif path.isfile(l):
        		printinfo(f"Copying File {path.abspath(l)} -> {target}")
        		copy(l, target)
                printinfo(successbanner)
    else:
        if path.isdir(target_so):
        	printinfo(f"Copying Directory {path.abspath(target_so)} -> {target}")
        	copytree(target_so, target)
        elif path.isfile(target_so):
        	printinfo(f"Copying File {path.abspath(target_so)} -> {target}")
        	copy(target_so, target)

    printinfo(successbanner)

    if archive:
        from shutil import make_archive
        printinfo("Making archive")
        make_archive(f"{target}", archiveformat, target)

    printinfo(successbanner)

    printinfo(f"Summary: Created backup - copied {target_so} into {target}\t", end='')
    if archive:
        printinfo(f"Created archive - created {target}.{archiveformat}", end='')
    printf('\n')


def main():
    # get configuration
    target_so = ''
    while target_so == '':
        target_so = ainputf(f"{ascii.color.green}[*] What do you want to backup(files or directory):: ")
        if ',' in target_so:
        	localtarget_so = target_so.split(',')
        	for l in localtarget_so:
        		if l == '' or not path.exists(l):
        			printerror("Please enter a valid file or directory")
        			exit(1)
        	multiso = True
        else:
        	l = target_so
        	if target_so == '' or not path.exists(l):
        		printerror("Please enter a valid file or directory")
        		exit(1)
        	multiso = False


    target = None
    while target == None:
        target = ainputf(f"{ascii.color.green}[*] Where do you want to place them(default {defaultarget}):: ")
        if target == '':
            if path.exists(defaultarget):
                target = defaultarget
        elif not path.exists(target):
        	printerror("Please enter a valid or folder")
        	exit(1)


    format = ainputf(f"{ascii.color.green}[*] What format do you want it to be(default {defaultformat}):: ")
    if format == '':
        format = defaultformat

    archive = None
    try:
        while archive == None or archive.lower() not in ['y', 'n', 'yes', 'no']:
        	if archive.lower() == 'y' or archive.lower() == 'yes':
        		archive = True
        	elif archive.lower() == 'n' or archive.lower() == 'no':
        		archive = False
        	elif archive == '':
        		archive = defaultarchive
        	else:
        		printerror("Please enter yes or no")
        	ainputf("[*] Do you want to archive it after backing it up:: ")

    except AttributeError:
        archive = defaultarchive
           
    try:
        if archive.lower() in ['y', 'yes']:
        	archive = True
        elif archive.lower() in ['n', 'no']:
        	archive = False
    except AttributeError:
        archive = defaultarchive

    if archive:
        archiveformat = None
        while archiveformat == None or archiveformat not in supportedarchiveformat and not archiveformat == '':
        	if archiveformat == '':
        		archiveformat = defaultarchiveformat
        	elif archiveformat == None:
        		archiveformat = ainputf("[*] Please enter a archive format::")
        	elif archiveformat not in supportedarchiveformat:
        		printerror(f"Please enter a valid archive format {supportedarchiveformat}")
        if archiveformat == '' or archiveformat == None:
            archiveformat =defaultarchiveformat

    
    backup(target_so, multiso, target, format, archive, archiveformat)


if __name__ == "__main__":
    main()
