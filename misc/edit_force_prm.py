import os


def str2unix(input_str: str) -> str:
    r"""\
    Converts the string from \r\n line endings to \n

    Parameters
    ----------
    input_str
        The string whose line endings will be converted

    Returns
    -------
        The converted string
    """
    r_str = input_str.replace('\r\n', '\n')
    return r_str

def dos2unix(source_file: str, dest_file: str):
    """\
    Coverts a file that contains Dos like line endings into Unix like

    Parameters
    ----------
    source_file
        The path to the source file to be converted
    dest_file
        The path to the converted file for output
    """
    # NOTE: Could add file existence checking and file overwriting
    # protection
    with open(source_file, 'r') as reader:
        dos_content = reader.read()

    unix_content = str2unix(dos_content)

    with open(dest_file, 'w') as writer:
        writer.write(unix_content)


os.chdir(r'Y:\germany-drought\00_parameter_files')

for year in range(2018, 2020):

    in_file = open('tsa_observations.prm','r')
    string = 'tsa_monthly_NDVI_' + str(year) + '.prm'
    out_file = open(string, 'w', newline='')
    print(str)
    for i, line in enumerate(in_file):
        if i == 52:
            out_file.write('YEAR_MIN = ' + str(year) + '\n')
        elif i == 53:
            out_file.write('YEAR_MAX = ' + str(year) + '\n')
        else:
            out_file.write(line)

    print("Close files.")
    in_file.close()
    out_file.close()

# for i in range(2000, 2018):
#     dos2unix('tsa_monthly_NDVI_' + str(i) + '.prm','force-tsa ' +  'tsa_monthly_NDVI_' + str(i) + '2.prm' )

batch_file = open('batch_tsa.sh','w', newline='')
for i in range(2018, 2020):
    print(i)
    batch_file.write('force-tsa ' +  'tsa_monthly_NDVI_' + str(i) + '.prm\n')
batch_file.close()

