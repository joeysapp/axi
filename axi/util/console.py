import sys, time

attribute_code_escape_sequence = "\033["
attribute_code_return_sequence = "m"
attribute_codes = {
    "gray": "90",
    "red": "91",
    "green": "92",
    "yellow": "93",
    "blue": "94",
    "magenta": "95",
    "cyan": "96",
    "white": "97",
    "bg-gray": "100",
    "bg-red": "101",
    "bg-green": "102",
    "bg-yellow": "103",
    "bg-blue": "104",
    "bg-magenta": "105",
    "bg-cyan": "106",
    "bg-white": "106",
    
    # text effects
    "none": "0",
    "reset": "0",
    "bold": "1",
    "faint": "2",
    "italic": "3",
    "underline": "4",
    "blink": "5",
    "fast-blink": "6",
    "reverse": "7",
    "conceal": "8",
    "strikethrough": "9",
    "gothic": "20",
    "double-underline": "21",
    "normal": "22",
    "no-italic": "23",
    "no-underline": "24",
    "no-blink": "25",
    "proportional": "26",
    "no-reverse": "27",
    "no-conceal": "28",
    "no-strikethrough": "29",
}

class Console():
    timestamp = False

    # list formatting
    @classmethod
    def list(cls, list) -> str:
        s = ""
        for obj in list:
            s = "{}\n\t{}".format(s, obj)
        return s
    
    # timestamp
    @classmethod
    def ts(cls, t) -> str:
        return "" if not cls.timestamp else "[{:.7f}]".format(t)

    # colors
    @classmethod
    def ansi(cls, type, fg=True):
        a = attribute_code_escape_sequence
        b = attribute_codes[type] if type in attribute_codes else "0"
        c = attribute_code_return_sequence
        s = "{}{}{}".format(a, b, c)
        return s

    @classmethod
    def cat(cls, msg, extra_args) -> str:
        s = "{}".format(msg)
        for obj in extra_args:
            s = "{}\n\t{}".format(s, obj)
        return s


    @classmethod
    def cls(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("blue")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{} {}".format("\t"*indent,style, cls.ts(t), "[clas]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def serial(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("cyan")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{}{}{} {}{}".format("\t"*indent,style, cls.ts(t), "[SERI]", cls.ansi("reset"), cls.ansi("italic"), cls.ansi("bg-gray"), s, cls.ansi("reset"))
        sys.stdout.write(output)

    @classmethod
    def init(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("cyan")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{} {}".format("\t"*indent,style, cls.ts(t), "[init]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("yellow")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{} {}".format("\t"*indent,style, cls.ts(t), "[dbug]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def method(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("yellow")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{} {}".format("\t"*indent,style, cls.ts(t), "[mthd]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def time(cls, msg, *args, **kwargs):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("yellow")
        t = time.process_time()
        indent = kwargs.get("level") or 0
        output = "{}{}{}{}{} {}".format("\t"*indent,style, cls.ts(t), "[time]", cls.ansi("reset"), s)
        sys.stdout.write(output)


    @classmethod
    def log(cls, msg, *args):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("gray")
        t = time.process_time()    
        output = "{}{}{}{} {}".format(style, cls.ts(t), "[logg]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def info(cls, msg, *args):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("green")
        output = "{}{}{} {}".format(style, "[info]", cls.ansi("reset"), s)
        sys.stdout.write(output)

    @classmethod
    def error(cls, msg, *args):
        s = cls.cat(msg, args)
        style = cls.ansi("bold") + cls.ansi("red")
        output = "{}{}{} {}".format(style, "[erro]", cls.ansi("reset"), s)
        sys.stdout.write(output)
