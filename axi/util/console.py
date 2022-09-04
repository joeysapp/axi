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

import sys

red   = "\033[1;31m"  
blue  = "\033[1;34m"
cyan  = "\033[1;36m"
green = "\033[0;32m"
reset = "\033[0;0m"
bold  = "\033[;1m"
reverse = "\033[;7m"
class Console():
    # def __init__(self, **kwargs):
    #     print("util/Console.py init", kwargs);

    @classmethod
    def cat(cls, msg, extra_args) -> str:
        s = "{}".format(msg)
        for obj in extra_args:
            s = "{}\n\t{}".format(s, obj)
        return s

    @classmethod
    def log(cls, msg, *args):
        s = cls.cat(msg, args)
        sys.stdout.write(bold+"[log] "+reset+s)

    @classmethod
    def info(cls, msg, *args):
        s = cls.cat(msg, args)
        sys.stdout.write(bold+blue+"[info] "+reset+s)

    @classmethod
    def error(cls, msg, *args):
        s = cls.cat(msg, args)
        sys.stdout.write(bold+red+"\n[err] "+reset+s)
