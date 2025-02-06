"""
MIT licence
Author: Jacek Ankowski
E-mail: jacek12260@op.pl
"""

from enum import Enum


class CurrentMapPart(Enum):
    START = None
    ARCHIVE_MEMBER = "Archive member included to satisfy reference by file (symbol)"
    DISCARDED_INPUT = "Discarded input sections"
    MEMORY_CONFIGURATIONS = "Memory Configuration"
    LINKER_SCRIPT_AND_MEMORY_MAP = "Linker script and memory map"
    DISCARD = "/DISCARD/"
    OUTPUT = "OUTPUT"


mapPartList = [mapPart.value for mapPart in CurrentMapPart][1:]  # without starting value
disable_mapping_sections_list = ["data1", "exception_ranges"]
MAP_FILENAME = 'tmp.map'
sections_dict = {}


def save_values(_section_name: str, _section_fullname: str, _section_starting_byte: int,
                _section_length: int, _section_path: str):
    if _section_name not in sections_dict.keys():
        sections_dict[_section_name] = []
    sections_dict[_section_name].append(
        {
            "section_fullname": _section_fullname,
            "section_starting_byte": _section_starting_byte,
            "section_length": _section_length,
            "section_path": _section_path
        })


if __name__ == '__main__':
    currentPart = CurrentMapPart.START
    lineCounter = 0
    with open(MAP_FILENAME, 'r') as file:
        section_name = "None"
        section_fullname = "None"
        section_starting_byte = 0
        section_length = 0
        section_path = "None"
        got_section_size = True
        for line in file:
            line = line.strip()
            lineCounter += 1
            if line:
                if not line.startswith(("0x", ".", "*", "LOAD", "CMakeFiles", "[!provide]")):
                    # print(line)
                    if line in mapPartList:
                        # print(CurrentMapPart._value2member_map_)
                        # print(line in CurrentMapPart._value2member_map_)
                        currentPart = CurrentMapPart(line)
                        print(f"CurrentPart: {currentPart.name}, provious line counter { lineCounter}")
                        lineCounter = 0
                        continue

                if currentPart is CurrentMapPart.LINKER_SCRIPT_AND_MEMORY_MAP:
                    # print(line)
                    # print(line)
                    parameters = line.split()
                    # section name are in the line
                    if parameters and parameters[0].startswith("."):
                        # print(line)
                        section_fullname = parameters[0]
                        section_name = parameters[0].split(".")[1]
                        # print(section_name)
                        # print(parameters)
                        if len(parameters) > 1:
                            # starting size is in this line as well as size
                            if parameters[1].startswith("0x"):
                                section_starting_byte = int(parameters[1], 16)
                                section_length        = int(parameters[2], 16)
                                # print(f"0x{section_starting_byte:X}")
                                # print(f"0x{section_length:X}")
                            if len(parameters) >= 4:
                                section_path = parameters[3]
                                # print(section_path)
                            # only one size per section is printed
                            got_section_size = True
                            save_values(section_name, section_fullname, section_starting_byte, section_length, section_path)
                            section_name = "None"
                            section_fullname = "None"
                            section_starting_byte = 0
                            section_length = 0
                            section_path = "None"
                            # print("got section size")
                        else:
                            got_section_size = False
                            # print(section_name)
                            # print("did not got section size")

                        # print(parameters[0])
                    #
                    # # section size gets here
                    # print(line)
                    if section_name not in disable_mapping_sections_list and   \
                                                not got_section_size and       \
                                                parameters and                 \
                                                parameters[0].startswith("0x") \
                        :
                        # print(line)
                        print(section_name)
                        got_section_size = True
                        section_starting_byte = int(parameters[0], 16)
                        if parameters[1].startswith("0x"):
                            section_length        = int(parameters[1], 16)
                            print(f"0x{section_starting_byte:X}")
                            print(f"0x{section_length:X}")
                            if len(parameters) >= 3:
                                section_path = parameters[2]
                                print(section_path)
                        else:
                            raise ValueError(f"Error while parsing section {section_name}! Unknown argument!")

                        save_values(section_name, section_fullname, section_starting_byte, section_length, section_path)
                        section_name = "None"
                        section_fullname = "None"
                        section_starting_byte = 0
                        section_length = 0
                        section_path = "None"
        print(sections_dict)
