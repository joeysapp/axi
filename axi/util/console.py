# for COLOR in {0..255} 
# do
#     for STYLE in "38;5" ;; or 48;5
#     do 
#         TAG="\033[${STYLE};${COLOR}m"
#         STR="${STYLE};${COLOR}"
#         echo -ne "${TAG}${STR}${NONE}  "
#     done
#     echo
# done

class Console():
    def __init__(self, **kwargs):
        print("util/Console.py init", kwargs);

red   = "\033[1;31m"  
blue  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
