#!/bin/bash

###############################################################################
# A example of how to use getopt to parse command line options.
#
# name:     getopt-example.sh
# author:   Ryan Chapin
# created:  2014-11-11
################################################################################
# USAGE:

function about {
   cat << EOF
getopt-example.sh - An example of how to use the getopt command to parse
                    command line arguments.
EOF
}

function usage {
   cat << EOF
Usage: getopt-example.sh [OPTIONS] -a file_path_a -b file_path_b

  -a A_FILE_PATH  Path to the file a.

  -b B_FILE_PATH  Path to the file b.

Options:
  -h HELP
      Outputs this basic usage information.

  -v VERBOSE
      Output additional feedback/information during runtime.

  --more-help EXTENDED HELP
      Extended help and documentation.
EOF
}

function extended_usage {
cat << EOF
Extended Usage:
       file_path_a : The path to some file that should contain something.

       file_path_b : The path to some file that should contain something else.

Here is where we would put additional information about the program and  how  to
to use it.  Perhaps we could even include an example.

Example:
   $ ./getopt-example.sh -a /some/path/a_file -b /some/path/b_file -v

   Will run the program passing in the path to  a_file  and  b_file  and  output
   verbose feedback during runtime.
EOF
}

################################################################################
#
# A sample function to provide verbose output during runtime.
#
function ddt {
   if [ "$VERBOSE" -eq 1 ];
   then
      echo "$1"
   fi
}

################################################################################
#
# Here we define variables to store the input from the command line arguments as
# well as define the default values.
#
HELP=0
VERBOSE=0
MORE_HELP=0

PARSED_OPTIONS=`getopt -o hv -l more-help,version:,build-type: -- "$@"`

# Check to see if the getopts command failed
if [ $? -ne 0 ];
then
   echo "Failed to parse arguments"
   exit 1
fi

eval set -- "$PARSED_OPTIONS"

# Loop through all of the options with a case statement
while true; do
   case "$1" in
      -h)
         HELP=1
         shift
         ;;

      -v)
         VERBOSE=1
         shift
         ;;

      --version)
         VERSION=$2
         shift 2
         ;;

      --build-type)
         BUILD_TYPE=$2
         shift 2
         ;;

      --more-help)
         MORE_HELP=1
         shift 
         ;;

      --)
         shift
         break
         ;;
   esac
done

if [ "$MORE_HELP" -eq 1 ];
then
   about
   usage
   echo ""
   extended_usage
   exit
fi

if [ "$HELP" -eq 1 ];
then
   usage
   exit
fi

#
# Do a check that the input arguments are actual files
#
if [ "$VERSION" == "0" ];
then
   echo "ERROR: you must specify a version"
   usage
   exit 1
fi

ddt "Building with version=$VERSION"

