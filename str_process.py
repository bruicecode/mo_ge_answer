import sys


def replace_repeated_chars(s, k):
    output = []
    for i, char in enumerate(s):
        if char in s[max(0, i-k):i]:
            output.append('-')
        else:
            output.append(char)
    return ''.join(output)


if __name__ == '__main__':
    input_str = sys.argv[1]
    input_len = int(sys.argv[2])
    print(replace_repeated_chars(input_str, input_len))