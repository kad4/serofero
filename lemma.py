suffixes = {
    1: ["को", "का", "कि", "की"],
    2: ["लाई", "लागि", "द्वारा", "निम्ति", "बाट"],
    3: ["मा", "संग", "माथि"],
    4: ["हरुको", "हरुका", "हरुकि", "हरुकी", "हरुमा", "हरुलाई", "हरुद्वारा", "हरुसंग", "हरुले"],
}

def nep_stemmer(word):
    for L in 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
    return word

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 1:
        sys.exit('{} takes no arguments'.format(sys.argv[0]))
    for line in sys.stdin:
        print(*[nep_stemmer(word) for word in line.split()])
