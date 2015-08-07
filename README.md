# propagate_renames.py
Mirror renamed or moved files in mirrored directory trees.

Takes two directory trees, master and slave, scans them for identical files under different names or in different directories, and changes the names and directory structure in slave to match master. Ignores any files which differ.

Uses MD5 to determine file identity. NOT FAST. But faster than wholesale copying, and handy as a prepper for synchronization software like rsync or Unison. (rsync does something like this with the `--fuzzy` switch, but only within directories; Unison can do this per spec but in practice does not). Unlike the [hardlink method](https://lincolnloop.com/blog/detecting-file-moves-renames-rsync/), can be run *after* moving files around.

Tickets and/or objections welcome.
