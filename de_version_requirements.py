"""
Removes the version number from the requirements file
so render can download available versions for its use
"""
with open('requirements.txt') as source_file,\
    open('render-requirements.txt', 'w+') as destination_file:
    for line in source_file:
        line = line.split('==')[0] + '\n'
        destination_file.write(line)
