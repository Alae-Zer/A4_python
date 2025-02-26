def readIntoList(filename):
    """Reads a file into a list of strings, one line per string.

       Caller must handle IO exceptions.

    Args:
        filename (str): the name of the file to read

    Returns:
       list: a list of strings, one line per element
    """
    fin = open(filename)
    lines = []
    for line in fin:
        lines.append(line.strip("\n"))
    fin.close()
    return lines


def writeListToFile(lines, fileName):
    """Writes a list of strings to a file, one string per line.

       Specified file name is created if it doesn't exist,
       or over-written if it does.

       Caller must handle IO exceptions.

    Args:
        filename (str): the name of the file to read

    Returns:
       list: a list of strings, one line per element
    """
    fout = open(fileName, "w")
    for line in lines:
        fout.write(line + "\n")
    fout.close()
