#! /usr/bin/env python3.1

suffixes = {
    2: ["को","मा", "का", "कि", "की"],
    3: [ "संग", "बाट"],
    4: [, "लागि", "माथि"],
    5: ["हरुको", "हरुका", "हरुकि", "हरुकी", "द्वारा", "निम्ति", "हरुमा", "हरुले"],
    6: ["अनुसार", "हरुलाई", "हरुसंग"],
    7: ["हरुद्वारा",],
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
