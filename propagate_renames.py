#!/usr/bin/env python

import argparse 
import os
import hashlib

parser = argparse.ArgumentParser(description="Mirror name and path changes in mirrored directory trees.")
parser.add_argument('master', metavar="master", help="path to the master tree's root directory")
parser.add_argument('slave', metavar="slave", help="path to the slave tree's root directory")
parser.add_argument('-n', '--dry-run', dest='dry_run', action='store_true', help="dry run (print moves instead of moving files)")
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="be verbose (print moves as they're made)")

master_files = {}

def md5sum(filename, blocksize=65536):
	hash = hashlib.md5()
	with open(filename, 'r+b') as f:
		for block in iter(lambda: f.read(blocksize), ''):
			hash.update(block)
	return hash.hexdigest()

def create_dir_with_tree(path):
	if not os.path.exists(path):
		create_dir_with_tree(os.path.dirname(path))
		os.mkdir(path)

args = parser.parse_args()
moved = 0

for dirpath, dirs, files in os.walk(args.master):
	for name in files:
		path = os.path.join(dirpath, name)
		checksum = md5sum(path)
		if checksum not in master_files:
			master_files[checksum] = os.path.relpath(path, args.master)
		else:
			del master_files[checksum]
		# let's just skip anything duplicated in master tree--you're on your own
for dirpath, dirs, files in os.walk(args.slave, topdown=False):
	for name in files:
		path = os.path.join(dirpath, name)
		checksum = md5sum(path)
		fullname = os.path.relpath(path, args.slave)
		master_fullname = master_files[checksum]
		if checksum in master_files and fullname != master_fullname:
			if not args.dry_run:
				dest = os.path.join(args.slave, master_fullname)
				create_dir_with_tree(os.path.dirname(dest))
				os.rename(path, dest)
				moved += 1
			if args.dry_run or args.verbose:
				print fullname, "->", master_fullname
	if (not args.dry_run) and (dirs or files) and not os.listdir(dirpath):
		# this directory had something in it when we started, but it's empty now
		os.rmdir(dirpath)
if not args.dry_run:
	print moved, "files moved."
