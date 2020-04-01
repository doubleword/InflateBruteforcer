# Description

Inflate Bruteforcer extracts information from files which use Deflate compression algorithm. It attempts to decompress data from each offset in a target file and stores decompressed data in separate files.

**NOTE:** the script was originally made for solving steganography CTF challenges which require extracting data from corrupted .zip/.png/.docx and other relatively small files. Thus, it is based on the assumption that the compressed file can fully fit in your RAM.

# Install

Requires Python3

No external Python3 dependencies required.

```
git clone https://github.com/doubleword/InflateBruteforcer.git
cd InflateBruteforcer
```
# Usage

```
python inflate.py [options] compressed_file
```

**-h, --help**

Display help:
```
python inflate.py -h
usage: inflate.py [-h] [-w wrapper_type] [-l max_attempts] [-o file_offset]
                  [-e file_extension] [-d output_directory] [-v]
                  compressed_file

positional arguments:
  compressed_file       File to decompress

optional arguments:
  -h, --help            show this help message and exit
  -w wrapper_type, --wrapper wrapper_type
                        Raw, Zlib, Gzip (default: Raw)
  -l max_attempts, --limit max_attempts
                        Stop bruteforcing after max_attempts
  -o file_offset, --offset file_offset
                        Start bruteforce from file_offset (Must be positive:
                        HEX or Decimal)
  -e file_extension, --extension file_extension
                        Output file extension (default: .inf)
  -d output_directory, --directory output_directory
                        Output directory path (default: Current directory)
  -v, --verbose         Verbose output
```

**-w, --wrapper**

There are two popular wrappers around raw Deflate data which add additional information to it (header and trailer). Those are zlib and gzip wrappers.

If this option is set to other than "raw", which is a default value, during bruteforcing, data will be successfully decompressed only if it has an appropriate wrapper.

**Raw Deflate data:**
```
python inflate.py -w raw example.zip
python inflate.py example.zip
```
**Zlib wrapper:**
```
python inflate.py -w zlib example.png
```
**Gzip wrapper:**
```
python inflate.py -w gzip example.gz
```

**-l, --limit**

This option limits the amount of bruteforcing attempts.

```
python inflate.py -w gzip -l 1 example.gz
```

**-o, --offset**

Sets the starting offset at which to begin bruteforcing a target file.

The value must be a positive hex or decimal number.

```
python inflate.py -o 0x2A example.png
```

**-e, --extension**

Extension to use when saving decompressed data to disk (default: .inf).

```
python inflate.py -e xml example.docx
```

**-d, --directory**

Set the output directory for decompressed data (default: current working directory)

```
python inflate.py -e xml -d /home/user/inflated example.docx
```

**-v, --verbose**

Produces more verbose output. Prints offsets at which it couldn't decompress the data.

```
python inflate.py -v example.zip
```