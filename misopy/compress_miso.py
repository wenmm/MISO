##
## Compress MISO files into a database
##
import os
import sys
import time

import sqlite3

import misopy
import misopy.misc_utils as utils
import misopy.miso_utils as miso_utils


def get_non_miso_files(filenames, miso_ext=".miso"):
    non_miso_files = []
    for fname in filenames:
        if os.path.basename(fname).endswith(miso_ext):
            non_miso_files.append(fname)
    return non_miso_files


class MISOCompressor:
    """
    Compressor/uncompressor of MISO files.
    """
    def __init__(self):
        self.input_dir = None
        self.output_dir = None


    def compress(self, miso_dirname, output_filename):
        """
        Takes a MISO input directory and compresses it
        into 'output_filename'.
        """
        if not os.path.isdir(miso_dirname):
            print "Error: %s not a directory." %(miso_dirname)
            sys.exit(1)
        if os.path.isfile(output_filename):
            print "Output file %s already exists, aborting. Please delete " \
                  "the file if you want compression to run."
            sys.exit(1)
        output_dir = os.makedirs(os.path.join(output_filename, ".dir"))
        # Keep track of paths that were already copied
        copied_paths = {}
        num_compressed_total = 0
        for dirpath, dirnames, filenames in os.walk(miso_dirname):
            # If already copied path, continue
            if dirpath in copied_paths:
                continue
            if utils.is_miso_rawdir(dirpath):
                non_miso_files = get_non_miso_files(filenames)
                miso_files = filter(lambda f: os.path.basename(f).endswith(".miso"),
                                    filenames)
                num_miso_files = len(miso_files)
                if len(non_miso_files):
                    print "WARNING: Found non-MISO files in a directory " \
                          "containing MISO output files. " \
                          "These files are being excluded: "
                    for non_miso_file in non_miso_files:
                        print " - %s" %(non_miso_files)
                    time.sleep(1)
                # It's a MISO output directory, so compress it
                print "Skipping MISO raw output directory: %s" %(dirpath)
                #self.compress_miso_dir()
                num_compressed_total += num_miso_files
            else:
                # Otherwise, copy its files and subdirectories
                shutil.copy(dirpath, output_dir)
        print "Compressed total of %d raw output files." %(num_compressed_total)


    def compress_miso_dir(miso_dirname):
        """
        Compress MISO directory.
        """
        if not os.path.isdir(miso_dirname):
            return None
        # Zip up directory at end
        # ...
        

    def uncompress(self, input_filename):
        """
        Uncompress a MISO input filename.
        """
        if not os.path.isfile(input_filename):
            print "Error: %s does not exist. Nothing to uncompress, quitting."
            sys.exit(1)
        


def compress_miso(input_dir, output_dir):
    """
    Compress a directory containing MISO files.

    Traverse directories, one by one, and look for directories
    that contain 
    """
    input_dir = utils.pathify(input_dir)
    output_dir = utils.pathify(output_dir)
    if input_dir == output_dir:
        print "Error: Cannot compress to same directory as " \
              "input directory.  Choose different output dir."
        sys.exit(1)
    t1 = time.time()
    t2 = time.time()
    print "Compression took %.2f minutes." %((t2 - t1)/60.)


def uncompress_miso(input_dir, output_dir):
    """
    Foo.
    """
    input_dir = utils.pathify(input_dir)
    output_dir = utils.pathify(output_dir)
    if input_dir == output_dir:
        print "Cannot uncompress to same directory as " \
              "input directory.  Choose different output dir."
        sys.exit(1)


def greeting():
    print "Compress/uncompress MISO output.\n"
    print "Usage: "
    print "To compress a directory containing MISO files \'inputdir\', use: "
    print "  compress_miso.py --compress inputdir outputfile"
    print "To uncompress back into a directory \'outputdir\', use: "
    print "  compress_miso.py --uncompress outputfile outputdir"


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--compress", dest="compress", nargs=2, default=None,
                      help="Compress a directory containing MISO output. "
                      "Takes as arguments: (1) the directory to be "
                      "compressed, and (2) the output filename of the compressed "
                      "representation. Example: --compress input_dir output_dir")
    parser.add_option("--uncompress", dest="uncompress", nargs=2, default=None,
                      help="Uncompress a file generated by compress_miso. "
                      "Takes as arguments: (1) the filename to be uncompressed, and "
                      "(2) the directory to place the uncompressed representation into.")
    (options, args) = parser.parse_args()

    if (options.compress is None) and (options.uncompress is None):
        greeting()
        sys.exit(1)
        
    output_dir = os.path.abspath(os.path.expanduser(options.output_dir))

    sd_max = options.sd_max

    if options.compute_insert_len != None:
        bams_to_process = [os.path.abspath(os.path.expanduser(f)) for f in \
                           options.compute_insert_len[0].split(",")]
        gff_filename = os.path.abspath(os.path.expanduser(options.compute_insert_len[1]))
        compute_insert_len(bams_to_process, gff_filename, output_dir,
                           options.min_exon_size,
                           no_bam_filter=options.no_bam_filter,
                           sd_max=sd_max)
    
    pass
    
