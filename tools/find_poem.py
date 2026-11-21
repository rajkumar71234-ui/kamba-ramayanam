import json, re, sys
L = [json.loads(l) for l in open('work/lines.jsonl')]
for n in sys.argv[1:]:
    for d in L:
        t = ''.join(x for x, b in d['runs'])
        if re.search(r'(^|\s)' + n + r'\s*\.', t) and (d['size'] >= 15 or d['bold'] > 0.7) and d['page'] <= 840:
            print(n, '->', d['page'], d['x0'], d['y'], d['size'], d['bold'], repr(t[:80]))
