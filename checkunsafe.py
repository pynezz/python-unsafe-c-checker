#! /usr/bin/python3

import os 
import re
import sys

c = ["\033[31m", "\033[32m", "\033[33m",    #  0     1       2     3     4      5
    "\033[34m", "\033[36m", "\033[1;33m"]   # red, green, orange, blue, cyan, yellow
italic = "\033[3;37m"                       # italic
q = "\033[0m"                               # end formatting


unsafe_functions_verbose = {
    "gets": f"\n\t{c[2]}This function reads input from the user and stores it into a buffer,\n\tbut it doesn't perform any bounds checking on the input.\n\tThis can result in buffer overflows and other security vulnerabilities.{q}\n\t{c[5]}Use fgets() instead{q}",
    "strcpy": f"\n\t{c[2]}This function copies a string from one buffer to another,\n\tbut it doesn't perform any bounds checking on the destination buffer.\n\tThis can result in buffer overflows and other security vulnerabilities.{q}\n\t{c[5]}Use strncpy() or strlcpy() instead{q}",
    "strcat": f"\n\t{c[2]}This function appends one string to another,\n\tbut it doesn't perform any bounds checking on the destination buffer.\n\tThis can result in buffer overflows and other security vulnerabilities.{q}\n\t{c[5]}",
    "sprintf": f"\n\t{c[2]}This function writes a formatted string to a buffer,\n\tbut it doesn't perform any bounds checking on the destination buffer.\n\tThis can result in buffer overflows and other security vulnerabilities.{q}\n\t{c[5]}",
    'scanf': f"\n\t{q}{c[0]}[SEVERE]{q}{c[2]} This function reads input from the user and stores it into variables,\n\tbut it doesn't perform any bounds checking on the variables.\n\t - Can lead to buffer overflows and other security vulnerabilities.\n\t - Prone to format string vulnerabilities, which can allow attackers to execute arbitrary code.\n\t{q}{c[5]}Use fgets(), fscanf(), or getline() instead{q}"
}

unsafe_functions = {
    "gets": "\n\tUse fgets() instead",
    'strcpy': '\n\tUse strncpy() or strlcpy() instead',
    'strcat': '\n\tUse strncat() or strlcat() instead',
    'sprintf': '\n\tUse snprintf() instead',
    'scanf': '\n\tUse fgets(), fscanf(), or getline() instead'
}

def display_help():
    print(f'+-----------------------***------------------------+')
    print(f'|  {c[1]}A python script for checking unsafe C functions{q} |')
    print(f'|  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  |')
    print(f'| Usage:                                           |')
    print(f'|        {sys.argv[0]} -f <file_path> [-fRov]   |')
    print(f'|                                                  |')
    print(f'| Example:                                         |')
    print(f'|        {sys.argv[0]} -v -r . -o result.txt    |')
    print(f'|                                                  |')
    print(f'|  Show this message    : --help, -h               |')
    print(f'|  Recursive search     :  -r <dir>                |')
    print(f'|  Save output          :  -o <file>               |')
    print(f'|  Verbose output       :  -v                      |')
    print(f'|  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  |')
    print(f'| Currently checks for:                            |')
    print(f'|  {c[2]}gets(), strcpy(), strcat(), scanf(), sprintf(){q}  |')
    print(f'|  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  |')
    print(f'|  {c[3]}To check for memory issues, use valgrind{q}        |')
    print(f'|  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  |')
    print(f'|                     {italic}Good luck on the exam! - Kev{q} |')
    print(f'+-----------------------***------------------------+')
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print(f"{c[0]}[!]{q} You must supply arguments!")
        display_help()
        sys.exit(1)

    count = 0
    files = []
    result_file = "results.txt"
    rec_file_path = ""
    write_output = False
    verbose = False

    for args in sys.argv:
        count += 1
        if (args == '-f'):
            file_path = sys.argv[count]
            files.append(sys.argv[count])
            
        if (args == '-r'):
            rec_file_path = sys.argv[count]
            print("[>] Recursive search on directory ", rec_file_path)

        if (args == '-o'):
            result_file = sys.argv[count]
            if (result_file[0] == "-"):
                print("Whoops, you must supply an output file to -o")
                print(f"Example: {sys.argv[0]} -r . -o somefile.txt")
                os.exit(1)
            write_output = True

        if (args == '-v'):
            verbose = True

        if (args == '-h' or args == '--help'):
            display_help()       
            
    if rec_file_path:
        find_command = f"find {rec_file_path} -type f -name '*.c'" # Bruker "find" og rekursivt 
                                                                   # finner alle filnavn som ender i .c
        output = os.popen(find_command).read()
        files.extend(output.splitlines())
    elif (not rec_file_path and not file_path):
        print("Whoops, I don't know where to look for errors, did you specify a path or directory?")
        print(f"Example: {sys.argv[0]} -r .")
        os.exit(1)


    results = []

    tot_issues = 0
    file_w_no_issues = 0
    for f in files:
        res_string = ""
        issues = 0
        with open(f, 'r') as file:
            try:
                for line_num, line in enumerate(file, start=1):
                    for unsafe_func in unsafe_functions:
                        match = re.search(rf'\b{unsafe_func}\b', line)
                        if match:
                            issues += 1
                            if (verbose):
                                results.append(f'{c[2]}[!]{q} Unsafe function {c[0]} "{unsafe_func}" {q} found on line {line_num} in file {f}: {unsafe_functions_verbose[unsafe_func]}\n')
                                print(f'{c[2]}[!]{q} Unsafe function {c[0]}{unsafe_func}{q} found on line {line_num} in file {f}: {c[2]}{unsafe_functions_verbose[unsafe_func]}{q}\n')
                            else: 
                                results.append(f'{c[2]}[!]{q} Unsafe function {c[0]} "{unsafe_func}" {q} found on line {line_num} in file {f}: {unsafe_functions[unsafe_func]}\n')
                                print(f'{c[2]}[!]{q} Unsafe function {c[0]}{unsafe_func}{q} found on line {line_num} in file {f}: {c[2]}{unsafe_functions[unsafe_func]}{q}\n')
                                
                        
                if (issues == 0):
                    file_w_no_issues += 1
                    if (verbose):
                        results.append(f'{c[1]}[+]{q} No issues found in {f}')
                        print(f'{c[1]}[+]{q} No issues found in {f}')
                    
            except UnicodeDecodeError:
                            print(f'{c[2]}[!]{q} UnicodeDecodeError in {file} line {line_num}')
                            continue
        tot_issues += issues

    tot_files_w_issues = len(files) - file_w_no_issues
    
    if (tot_issues == 0):
        res_string = f"| {c[1]} No common issues found in {len(files)} files!{q} |"
    elif (tot_issues > 0):
        res_string = f"| {c[2]}{tot_issues}{q} issue(s) found in {tot_files_w_issues}/{len(files)} files   <"
        
        print("\n+------------------------------------+")
        print(res_string)
        print("+------------------------------------+")

    if (write_output):  # Write to file output, not just stdout
        with open(result_file, 'w') as f:
            f.write('\n'.join(results))

if __name__ == '__main__':
    main()
