""""
This program was written by Winkelmann17. 
Github: https://github.com/Winkelmann17

This code serves as the main entry point for WinkelBudget.

Last Updated: 29 October 2026
Recent Changes:
- Preparing for final release
"""
# ===================================================================
#           Imports
# ===================================================================
import argparse
import os
import sys

# ===================================================================
#               CONSTANTS
# ===================================================================
NUM_ARGS = 1
DESC = "Program to add pages to winkelmann17.github.io"
EPILOG = "How to use:\n" \
"python addpage.py -a <Article Name>\n" \
"python addpage.py -p <Project Name\n"

TAB = 12
VAR = "$"
TARGET = "config.html"
BLANK =  "blank.html"
TITLE = "TITLE"
NUM_VARS = 3
# ===================================================================
#               Functions
# ===================================================================
def get_inputs():
    """Function that handles command line inputs for the specific 
    months and years that will be used. Will be replaced with an
    all UI solution in a future release.
    """
    # Parser and argument setup
    parser = argparse.ArgumentParser(
        prog="python addpage.py -h",
        description=DESC,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument(
        "-a",
        "--article",
        action="store_true",
        help="The article title that you desire."
    )
    parser.add_argument(
        "-p", 
        "--project", 
        action="store_true",
        help="The project title that you desire."
    )

    # Parse the args
    args = parser.parse_args()
    article : bool = args.article
    project : bool = args.project
    total_args = len(sys.argv) - 1 # 1 is the source file, subtract that

    print(total_args)
    
    # Check all inputs are valid via a variety of checks
    errors = []
    # Arg number checks
    if total_args < NUM_ARGS:
        errors.append("Not enough args specified. Use -a or -p.") 
    elif total_args > NUM_ARGS:
        errors.append("Too many arguments specified. Use only -a or -p.")

    # Check that only one flag is set
    elif article and project:
        errors.append("Only one flag (-a OR -p) can be set.")
    elif not article and not project:
        errors.append("No flags are set (-a OR -p). Please set one.")

    # Check that file to build from is present
    elif not os.path.exists(TARGET):
        errors.append(f"Target file {TARGET} does not exist.")

    # Print the erros underneath the help message. Helps make it more clear
    # what the actual problem is.
    if errors:
        parser.print_help()
        print("\nThe following errors with your input were found:")
        for error in errors:
            print(f"- {error}")
        print()
        exit()

    # All is good, return data to main
    else:
        return article, project
    
# -------------------------------------------------------------------
def tab_content(html):
    lines = html.split("\n")
    for i in range(1, len(lines), 1):
        lines[i] = " " * TAB + lines[i]
    tabbed_html = "\n".join(lines)
    return tabbed_html

# ===================================================================
#           Main
# ===================================================================
def main():
    # Get Inputs
    article, project = get_inputs()
    print("[+] Inputs read for new page.")

    # Parse Blank and New Content
    with open(BLANK, "r") as f:
        blank = f.read()
    print("[+] Blank page read.")

    # Parse config.html
    content_vars = {}
    print(f"[+] Config file read with the following variables:")
    with open(TARGET, "r") as f:
        for i in range(NUM_VARS):
            line = f.readline().split("=")
            print(f"- {line[0]} : {line[1].strip()}")
            content_vars[line[0]] = line[1].strip()
        html = f.read()
    keys = list(content_vars.keys())

    # Iterate through and replace the $ that are not the 
    # content of the page.
    try:
        # Replace each variable if it is found
        for i in range(len(keys)):
            index = blank.index(VAR)
            var = content_vars[keys[i]]
            blank = blank[:index] + var + blank[index+1:] # Remove the $

        # Tab content and Replace final $
        tabbed_html = tab_content(html)
        index = blank.index(VAR)
        blank = blank[:index] + tabbed_html + blank[index+1:]

        print("[+] Info vars have been replaced successfully.")

    # No index is found, we are done going through the blank html string
    except ValueError:
        print("[-] No other $ variables are left to edit. Check inegrity of output HTML")
    except Exception as e:
        print(f"[-] Exception occurred (what the skib): {e}")
        print(i)
        exit()

    # Add to Article section if article        
    title = content_vars[TITLE].replace(" ", "")
    if article:
        path = f"./Articles/{title}.html"
    # Add to Project section if project
    else:
        path = f"./Projects/{title}.html"

    # Write new HTML in proper folder
    with open(path, "w") as f:
        f.write(blank)

    
if __name__ == "__main__":
    main()

# EOF