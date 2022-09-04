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

red   = "\033[1;31m"  
blue  = "\033[1;34m"
cyan  = "\033[1;36m"
green = "\033[0;32m"
reset = "\033[0;0m"
bold  = "\033[;1m"
reverse = "\033[;7m"


class Console():
    def __init__(self, **kwargs):
        print("util/Console.py init", kwargs);

    @classmethod
    def log(cls, text):
        print(bold+"[LOG]: "+reset+text)

