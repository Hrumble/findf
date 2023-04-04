import os, sys, getopt, stat    

argv = sys.argv[1:]

opts, args = getopt.getopt(argv, "hvn:d:ce:p")

directory = os.path.expanduser("~")
found_n = 0
file_name = " "
p_match = False
found_path = []
verbose = False
exclude_name = []
sub_directories = []
star_index = -1

def Help():
    print("usage:\n"+
        "     find -n <filename> [options]\n\n"+
        "Options:\n"+
        "     -v   Verbose mode\n"+
        "     -e <directory_name1; directory_name2; ...>   Exclude directories from Scan\n"+
        "     -c   Use current directory as a scan start\n"+
        "     -d <directory>   Specify a directory to start the scan in\n\n"+
        "Examples:\n"+
        "     find -n myfile.txt -d C:/Users\n"+
        "     find -n myfile.txt -c -e 'MyDirectory; MyOtherDirectory' -v\n"+
        "Run command as administrator for more results")
    sys.exit()


if len(opts) == 0:
    Help()

for opt, arg in opts:
    if (opt == "-h"):
            print("usage:\n"+
                "     findf -n <filename> [options]\n\n"+
                "Options:\n"+
                "     -v   Verbose mode\n"+
                "     -e <directory_name1; directory_name2; ...>   Exclude directories from Scan\n"+
                "     -p   Perfect match"+
                "     -c   Use current directory as a scan start\n"+
                "     -d <directory>   Specify a directory to start the scan in\n\n"+
                "Examples:\n"+
                "     findf -n myfile.txt -d C:/Users\n"+
                "     findf -n myfile.txt -c -e 'MyDirectory; MyOtherDirectory' -v\n"+
                "     findf -n myfile.* -c\n\n"+
                "Run command as administrator for more results")
            sys.exit()
    elif (opt == "-n"):
        file_name = arg
        split_args = arg.split(".")
        if "*" in split_args:
            star_index = split_args.index("*")
            
    elif (opt == "-d"):
        directory = arg
    elif (opt == "-v"):
        verbose = True
    elif (opt == "-c"):
        directory = os.getcwd()
    elif (opt == "-e"):
        exclude_name.append(arg.split("; "))
    elif (opt == "-p"):
        p_match = True
    else:
        Help()


def AddPath(entry, directory_name):
    global found_n
    found_n += 1
    print(f"Found {found_n} file(s) matching the description")
    found_path.append(entry.path)
    if verbose:print(f"Found match {file_name} with {entry.name} in {directory_name}\\-")

def Output():
    if len(found_path) != 0: 
        print(f"{found_n} file(s) found in:")
        for dir in found_path:
            print("   ", dir)

    else: 
        print(f"Could not locate a file called {file_name}")

def Scan(directory):
    global found_n
    if verbose:print(f"Scanning {directory}-")
    directory_name = directory.split("\\")[-1]
    sub_directories = []
    try:
        with os.scandir(directory) as dir_contents:
            for entry in dir_contents:
                if entry.is_dir():
                    if (entry.name in exclude_name):
                        if verbose:print(f"directory: {entry.name} in {directory_name}\\ is excluded-")
                        continue
                    sub_directories.append(entry.path)
                    if verbose:print(f"directory: {entry.name} found in {directory_name}\\-")
                elif entry.is_file():
                    if verbose:print(f"checking {file_name} for match with {entry.name} in {directory_name}\\-")
                    if p_match:
                        if entry.name == file_name:
                            AddPath(entry, directory_name)
                        continue

                    if star_index != -1:
                        if entry.name.split(".")[star_index-1].lower() == file_name.split(".")[star_index-1].lower():
                            AddPath(entry, directory_name)
                        continue
                    if entry.name.lower() == file_name.lower():
                        AddPath(entry, directory_name)
                    

        for dir in sub_directories:
            Scan(dir)
    except PermissionError:
        if verbose:print(f"directory: {entry.name} in {directory_name}\\ Permission Denied-")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        Output()
        sys.exit()

Scan(directory)
Output()


                    
