import sys
import re
from sys import argv
from urllib.parse import unquote


def identify_key(input_key):
    key = ''
    for i in input_key[1:]:
        if i != ":":
            key += i
        elif not i.isdigit() and not i.isalpha:
            error.write("ERROR -- invalid key. key must only contain digits and letters")
        else:
            return key
    return


def identify_type(input_key):
    if validate_integer(input_key) != nothing:
        return "int"
    elif validate_empty(input_key) != nothing:
        return "empty"
    elif validate_simple_string(input_key) != nothing:
        return "simple_string"
    elif validate_complex_string(input_key) != nothing:
        return "complex_string"
    elif validate_map(input_key) != nothing:
        return "map"
    else:
        error.write("ERROR -- invalid type. only acceptable types are integer, string, or map.")
        exit(66)
    return


def validate_brackets(input_key):
    open_num = 0
    close_num = 0
    if input_key[0] != '<':
        error.write("ERROR -- invalid input. first non-blank character must be '<'.")
        exit(66)
    if input_key[-1] != '>':
        error.write("ERROR -- invalid input. last non-blank character must be '>'.")
        exit(66)
    for i in input_key:
        if i == '<':
            open_num += 1
        elif i == '>':
            close_num += 1
    if open_num != close_num:
        error.write("ERROR -- invalid input. must be an equal amount of < and >.")
        exit(66)

    return


def validate_integer(input_key):
    regex = r"\s*<[a-zA-Z0-9]+:i-*[0-9]+>\s*"
    result = re.fullmatch(regex, input_key)
    return result


def validate_empty(input_key):
    regex = r"\s*<>\s*"
    result = re.fullmatch(regex, input_key)
    return result

def validate_simple_string(input_key):
    regex = r"\s*<[a-zA-Z0-9]+:[a-zA-Z0-9\t\ ]+s>\s*"
    result = re.fullmatch(regex, input_key)
    return result


def validate_complex_string(input_key):
    regex = r"\s*<[a-zA-Z0-9]+:([a-zA-Z0-9]*(%[a-fA-F0-9]{2})+)+[a-zA-Z0-9]*>\s*"
    result = re.fullmatch(regex, input_key)
    return result


def validate_map(input_key):
    regex = r"\s*<[a-zA-Z0-9]+:<.*>>\s*"
    result = re.fullmatch(regex, input_key)
    return result


def validate_unique_keys(key_set):
    identifiers = []
    for k in key_set:
        identifier = k.split(":", 1)[0]
        if identifier in identifiers:
            error.write("ERROR -- All identifiers must be unique within their level.")
            exit(66)
        else:
            identifiers.append(identifier)
    return


def separate_map(input_key):
    level = -1
    key = ""
    keys = []
    for i in input_key:
        if i == "<":
            level += 1
            if level != 0:
                key += i
        elif i == ">":
            if level != 0:
                key += i
            else:
                keys.append(key)
                key = ''
            level -= 1
        elif i == ",":
            if level == 0:
                keys.append(key)
                key = ''
            else:
                key += i
        else:
            key += i
    return keys


def handle_value(input_key, key_type):
    if key_type == "int":
        key_parts = input_key[1:-1].split(":")
        key = key_parts[0]
        value = key_parts[1]
        value = value[1:]
        output.write(key + " -- integer -- " + value + "\n")
        return
    elif key_type == "empty":
        return
    elif key_type == "simple_string":
        key_parts = input_key[1:-1].split(":")
        key = key_parts[0]
        value = key_parts[1]
        value = value[:-1]
        output.write(key + " -- string -- " + value + "\n")
        return
    elif key_type == "complex_string":
        key_parts = input_key[1:-1].split(":")
        key = key_parts[0]
        value = key_parts[1]
        print(value)
        value = unquote(value)
        print(value)
        output.write(key + " -- string -- " + value + "\n")
        return
    elif key_type == "map":
        key_parts = input_key[1:-1].split(":", 1)
        key = key_parts[0]
        output.write(key + " -- map -- \n")
        output.write("begin-map\n")
        _main(key_parts[1])
        output.write("end-map\n")
        return
    return


def unpack_nosj(input_nosj):
    value_type = identify_type(input_nosj)
    handle_value(input_nosj, value_type)
    return


def _main(nosj_set):
    keys = separate_map(nosj_set)
    validate_unique_keys(keys)
    validate_brackets(nosj_set.strip())
    for nosj in keys:
        nosj = "<" + nosj + ">"
        unpack_nosj(nosj)
    return


if __name__ == '__main__':
    nothing = None
    output = sys.stdout
    error = sys.stderr
    fileName = argv[1]
    if not fileName.endswith(".txt"):
        error.write("ERROR -- invalid file input type. please use a .txt file.")
        exit(66)
    file = open(fileName, "r", encoding = 'utf-8')
    fileData = file.read()
    _main(fileData)
