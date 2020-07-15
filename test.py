def guild_read_page():
    file = open('guild_board.txt', 'r')
    lines = file.readlines()
    new = []
    for line in lines:
        new.append(line.rsplit('\n')[0])
    lines = new
    output = []
    for i in range(0, len(lines), 2):
        output.append([lines[i], lines[i+1]])
    print(output)

def guild_write_page(arr):
    file = open('guild_board.txt', 'w')
    for notice in arr:
        file.write(notice[0])
        file.write('\n')
        file.write(str(notice[1]))
        file.write('\n')

guild_write_page([['a', 500], ['hello', 100]])
