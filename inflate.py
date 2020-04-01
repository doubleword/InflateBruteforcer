import argparse
import zlib
import sys
import os

parser=argparse.ArgumentParser()

parser.add_argument(metavar="compressed_file",
                    dest="cfile",
                    help="File to decompress",
                    type=argparse.FileType("rb")
                    )

parser.add_argument("-w","--wrapper",
                    metavar="wrapper_type",
                    help="Raw, Zlib, Gzip\t (default: Raw)",
                    default="Raw",
                    choices=["Raw","raw","Zlib","zlib","Gzip","gzip"]
                    )

def limit_validator(x):

    limit=int(x)
    
    if limit>=0:
        return limit
    raise argparse.ArgumentTypeError("negative int value: {}".format(limit))

parser.add_argument("-l","--limit",
                    type=limit_validator,
                    default=0,
                    metavar="max_attempts",
                    help="Stop bruteforcing after max_attempts"
                    )

def offset_validator(x):
    sub=x.find("0x")
    if sub==0:
        return int(x,0)
    elif sub!=-1:
        raise argparse.ArgumentTypeError("invalid int value: {}".format(x))
    else:
        off=int(x)
        if off>=0:
            return off
        raise argparse.ArgumentTypeError("invalid int value: {}".format(x))

parser.add_argument("-o","--offset",
                    type=offset_validator,
                    default=0,
                    metavar="file_offset",
                    help="Start bruteforce from file_offset\t (Must be positive: HEX or Decimal)"
                    )

parser.add_argument("-e","--extension",
                    metavar="file_extension",
                    default=".inf",
                    help="Output file extension\t (default: .inf)",
                    type=lambda x: x if x.startswith(".") else "."+x
                    )

parser.add_argument("-d","--directory",
                    metavar="output_directory",
                    help="Output directory path\t (default: Current directory)",
                    default="./",
                    type=lambda x: x if x.endswith("/") else x+"/"
                    )

parser.add_argument("-v","--verbose",
                    action="store_true",
                    help="Verbose output"
                    )


args=parser.parse_args()



if args.offset:
    args.cfile.seek(args.offset)

compressed_data=args.cfile.read()

if args.wrapper=="Zlib" or args.wrapper=="zlib":
    wbits=15
elif args.wrapper=="Gzip" or args.wrapper=="gzip":
    wbits=31
else:#Raw DEFLATE stream
    wbits=-15


try:
    os.mkdir(args.directory)
except FileExistsError:
    pass

for i in range(len(compressed_data) if not args.limit else args.limit):
    data_chunk=compressed_data[i:]
    current_offset=args.offset+i

    if not data_chunk:
        print("[!] -l/--limit exceeds file's length. Reached the end of file.")
        sys.exit(0)
    try:
        decompressed=zlib.decompress(data_chunk,wbits)
    except zlib.error:
        if args.verbose:
            print("{:#x} - Failed".format(current_offset))
        continue
    else:
       print("{:#x} - Decompressed {} byte(s)".format(current_offset,len(decompressed)))
    
    try:
        with open(args.directory+hex(current_offset)+args.extension,"wb") as f:
            f.write(decompressed)
    except OSError:
        print("[!] Couldn't open the file.")
        sys.exit(1)
