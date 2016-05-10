import os, sys, getopt, csv

###  Help message function  ###
def usage(progname):
  print("Usage:", progname, "-h")
  print("Usage:", progname, "-r|--reffile <csv reference file> -c|--chkfile <csv file to check>")
  return

###  Parse command-line arguments function  ###
def parseargs(argv):
  progpath = ''                     # declare progpath and initialize to NULL
  progname = ''                     # declare progpath and initialize to NULL
  reffile = ''                      # declare reffile and initialize to NULL
  chkfile = ''                      # declare chkfile and initialize to NULL

  prognamewithpath = argv.pop(0)    # pop program name (with path) off the sys.argv list
  (progpath, progname) = os.path.split(prognamewithpath)  # split program into path and name
  try:                              # grab arguments via getopt
    (opts, args) = getopt.getopt(argv, "hr:c:",["reffile=","checkfile="])  # ':' and '=' indicate arg following
  except getopt.GetoptError:        # bail if error with getopt
    usage(progname)
    sys.exit(2)
  else:                             # if getopt successful
    for opt, arg in opts:           # iterater over arguments
      if opt == '-h':               # if -h, print usage statements
        usage(progname)
        sys.exit(0)
      elif opt in ("-r", "--reffile"):   # if -r, set next arg to reffile
        reffile = arg
      elif opt in ("-c", "--checkfile"):  # if -c, set next arg to chkfile
        chkfile = arg
  finally:                           # after iterating over all arguments
    if reffile == '' or chkfile == '':  # bail if we don't have both a ref file and a check file
      usage(progname)
      sys.exit(3)
  return (progname, reffile, chkfile)

###  Open files function  ###
def openfiles(progname, reffile, chkfile):
  try:                                # attempt to open ref file in read mode
    reffh = open(reffile, 'r') 
  except:                             # bail if open is unsuccessful
    print(progname, "- unable to open reference file:", reffile)
    sys.exit(10);
  else:                               # if ref file open is successful
    namebyrefid = {}                  # declare hash array
    statusbyrefid = {}                # declare hash array
    slurpedinfile = csv.reader(reffh) # use csv.reader function to slurp in the ref file
    next(slurpedinfile)               # ignore headers; could assign to a variable to capture headers
    for row in slurpedinfile:         # iterate over slurped in ref file
      namebyrefid[row[0]] = row[1:4]  # key is id, value stored is in columns 1, 2, 3
      statusbyrefid[row[0]] = row[4]  # key is id, value stored is in column 4
  finally:                            # when done, close ref file
    reffh.close()
  try:                                # do essentially the same as above on the check file
    chkfh = open(chkfile, 'r') 
  except:
    print(progname, "- unable to open check file:", chkfile)
    sys.exit(11);
  else:
    infobychkid = {}
    slurpedinfile = csv.reader(chkfh)
    next(slurpedinfile)               # ignore headers; could assign to a variable to capture headers
    for row in slurpedinfile:
      infobychkid[row[0]] = row[1:4]
  finally:
    chkfh.close()
  return (namebyrefid, statusbyrefid, infobychkid)

###  Check IDs function  ###
def checkids(infobychkid, namebyrefid):
  for key in infobychkid.keys():        # iterate over all ids to be checked
    if namebyrefid.get(key) is None:    # print a message if an id in the chk file is not found in the ref file
      print("Employee ID of", key, "could not be found in reference file", infobychkid[key])
  return


###  MAIN  ###
def main(argv):
  (progname, reffile, chkfile) = parseargs(argv)                                     # parse arguments
  (namebyrefid, statusbyrefid, infobychkid) = openfiles(progname, reffile, chkfile)  # open and read files
  checkids(infobychkid, namebyrefid)                                                 # check employee IDs
  return 0

if __name__ == "__main__":
  main(sys.argv)


