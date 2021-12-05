import sys
import re
import types
import logging

logging.basicConfig(
    #filename='example.log',
    level=logging.DEBUG if len(sys.argv) > 1 and sys.argv[1] == 'debug' else logging.INFO)

def method(self):
    def to_method(f):
        def mf(self, input):
            logging.debug(f"{f.__qualname__}({input!r})...")
            return f(self, input)
        return mf
    return lambda f: types.MethodType(to_method(f), self)

class Rule:
    """parse Rule"""

    rules = dict()

    def __init__(self, pat, *, name = None):
        logging.debug(f"build {pat!r} Rule, name = {name!r}")
        if isinstance(pat, str):
            @method(self)
            def match(self, input):
                if input.startswith(pat):
                    return [len(pat)]
                else:
                    return []
            self.match = match
        elif isinstance(pat, tuple): # alt
            @method(self)
            def match(self, input):
                res = []
                for p in pat:
                    if (r := p.match(input)):
                        res += r
                logging.debug(res)
                return res
            self.match = match
        elif isinstance(pat, list): # seq
            @method(self)
            def match(self, input):
                res = []
                if len(pat) > 0:
                    if (r := Rule.rules[pat[0]].match(input)):
                        res += r
                for rn in pat[1:]:
                    new_res = []
                    for resn in res:
                        if (r := Rule.rules[rn].match(input[resn:])):
                            new_res += (resn + x for x in r)
                    res = new_res
                    if not res:
                        break
                logging.debug(res)
                return res
            self.match = match

        if name != None:
            Rule.rules[name] = self

    def matchfull(self, input):
        l = self.match(input)
        logging.debug(f"match({input!r}) = {l}")
        return max(l, default=0) == len(input)

    rule_spec = [
        ('SEQ',   r'(?P<name1>\d+):(?P<gs>( \d+)+)'),
        ('ALT',   r'(?P<name2>\d+):(?P<gs1>( \d+)+) \|(?P<gs2>( \d+)+)'),
        ('LIT',   r'(?P<name3>\d+): \"(?P<lit>.*)\"'),
    ]

    rule_re = re.compile('|'.join('(?P<%s>%s)' % p for p in rule_spec) + '')

    @staticmethod
    def parse_rule(input):
        if (m := Rule.rule_re.fullmatch(input)):
            if m["SEQ"]:
                return Rule(list(m['gs'].split()), name = m['name1'])
            elif m["ALT"]:
                r1 = Rule(list(m['gs1'].split()))
                r2 = Rule(list(m['gs2'].split()))
                return Rule((r1, r2), name = m['name2'])
            elif m["LIT"]:
                return Rule(m['lit'], name = m['name3'])

        raise RuntimeError(f"Unknown rule {input!r}")
        
def parse_input(fin):
    for line in fin:
        line = line.strip()
        if len(line) == 0:
            break
        Rule.parse_rule(line)

    strs = []
    for line in fin:
        line = line.strip()
        if len(line) == 0:
            break
        strs.append(line)

    return strs

def main():
    strs = parse_input(sys.stdin)
    cnt = sum(1 for s in strs if Rule.rules["0"].matchfull(s))
    print(f"{cnt=}")

if __name__ == '__main__':
    main()
