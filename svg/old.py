from typing import Callable, Union
import logging
import json  # !Remove after debugging


DEFAULT_MODE = "w+"
FILE_FMT = "%(asctime)s - %(message)s"
DATE_FMT = "%d-%m-%Y %H:%M:%S"
LEVEL = logging.ERROR


_CONTEXT_ERR_MSG = \
    "Function self.{} must be called within a context manager"


coords = tuple[float, float]


logging.basicConfig(format=FILE_FMT, datefmt=DATE_FMT, level=LEVEL)


def context(strict: bool = False):
    def inner(func: Callable):
        def wrapper(self, *args, **kwargs):
            if not self.in_context:
                if strict:
                    raise NotInContext("")
                logging.warning()
            return func(self, *args, **kwargs)
        return wrapper
    return inner


class NotInContext(Exception):
    def __init__(self, *args, **kwargs):
        self.err = self.__class__.__name__
        self.msg = args[0]
        super().__init__(args, **kwargs)

    def __str__(self):
        return f"{self.err}({self.msg})"


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def coords(self): return (self.x, self.y)

    def __iter__(self):
        return iter(self.coords)


class SVGWriter:
    def __init__(self, filepath: str, *args, **kwargs):
        self.svg_file_path = filepath
        self.svg_data: dict[str, Union[list[str], str]] = {}

        self.in_context = False

        self.unclosed_tags = []
        self.indent = 0

        open(filepath, DEFAULT_MODE)  # Create file but don't store / read

    def __enter__(self):
        self.svg_file = open(self.svg_file_path, "r+")
        self.in_context = True

        return self

    def __exit__(self, type, value, traceback):
        print(f"exit: {type, value, traceback}")
        self.svg_file.close()
        self.in_context = False

    def check_context(self, func: Callable, ensure: bool = False):
        if not self.in_context:

            if ensure:
                raise NotInContext(_CONTEXT_ERR_MSG.format(func.__name__))
            logging.error(_CONTEXT_ERR_MSG.format(func.__name__))

    def ensure_context(self, func: Callable):
        self.check_context(func, ensure=True)

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def add_element(self, name: str, data: str):
        self.svg_data.setdefault(name, [])

        self.svg_data[name].append(data)

    def tag(self,
            name,
            attrs: dict[str, str] = {},
            closing: bool = False,
            closed: bool = True
            ):
        if closing:
            return f"</{name}>"

        if not attrs:
            attrs = "\b"
        else:
            attrs = " ".join([f'{k}={v}' for k, v in attrs.items()])

        return f"<{name} {attrs} {'/' if closed else ''}>"

    @context(strict=True)
    def write_line(self, line: str):
        self.svg_file.write(f"{line}\n")

    @context(strict=True)
    def compile_svg(self):
        print(json.dumps(self.svg_data, indent=4))

        # Open svg tag
        self.write_line(self.tag("svg", self.svg_data["svg"],
                        closing=False, closed=False))

        # Remove svg tag from data
        del self.svg_data["svg"]

        # Loop through all defined elements to beb added
        for tag, data in self.svg_data.items():
            if type(data) == str:
                self.write_line(self.tag(tag, data,
                                closing=False, closed=True))

            else:
                for i, _ in enumerate(data):
                    self.write_line(self.tag(tag, data[i],
                                    closing=False, closed=True))

        # Close svg tag
        self.write_line(self.tag("svg", closing=True))

    def init_svg(self, height, width):
        self.add_element("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:ev": "http://www.w3.org/2001/xml-events",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "baseProfile": "full",
            "version": "1.2",
            "height": str(height),
            "width": str(width),
        })

    def line(self, x1: int, x2: int,
             y1: int, y2: int,
             style: str = "stroke: black;"
             ):

        self.add_element("line", {
            "x1": str(x1),
            "x2": str(x2),
            "y1": str(y1),
            "y2": str(y2),
            "style": style,
        })


def main():
    svg = SVGWriter("new.svg")

    with svg:
        svg.init_svg(960, 540)
        svg.line(100, 100, 860, 440, "stroke: black; stroke-width: 6;")
        svg.compile_svg()


if __name__ == "__main__":
    svg = SVGWriter("new.svg")

    with svg:
        svg.init_svg(200, 200)
        svg.line(10, 10, 190, 190)
        svg.compile_svg()
