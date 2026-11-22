"""Where the பதவுரை ends and the விளக்கம் begins.

The parsers take the first paragraph after a poem as its பதவுரை (word-by-word meaning: **word** - meaning; ...)
and the paragraphs after it as its விளக்கம். The printed page does not always break the paragraphs there:

  * the விளக்கம் is often printed straight after the last word's meaning, in the same paragraph
    ("... **பறை அடுத்தது போலும்** - (கடுமையான) பறையோசை வீழ்ந்ததைப் போன்றது. இசையில் மகிழ்ந்து ...");
  * the பதவுரை sometimes runs on over a page break, so its last words come out as a separate paragraph
    ("... அவன் கூறும் அந்த உறுதி" | "மொழிகளுக்கு; **ஒரு பொருள் இன்று ஆயிலும்** - ...").

rebalance() moves the text to the right side. It never drops or changes any words: the பதவுரை and the
விளக்கம் together read exactly as before, in the same order.
"""
import re

# "**word** - meaning" or "**word -** meaning"
GLOSS_RE = re.compile(r'\*\*[^*]{1,160}?\*\*\s*[-–]|\*\*[^*]{1,160}?[-–]\s*\*\*')
TAMIL = re.compile(r'[஀-௿]')
OPEN, CLOSE = '([{“‘', ')]}”’'


def has_gloss(text, at_start=False):
    m = GLOSS_RE.search(text or '')
    if not m:
        return False
    return m.start() < 3 if at_start else True


# பால காண்டம்'s PDF often prints a full stop where the book has a comma ("செய்யப் பெற்று. பச்சை மணிகள் ..."),
# so there a full stop only ends a meaning after a word that can end a sentence.
FINITE = re.compile(r'(?:ான்|ாள்|ார்|ாம்|ேன்|ோம்|ீர்|ாய்|ர்கள்|னர்|ின|ன|டது|ற்றது|ந்தது|ன்றது|த்தது|ட்டது|வது|யது|ளது|லது|'
                    r'ரது|னது|ணது|மது|கிறது|கின்றது|ண்டு|இல்லை|அன்று|என்க|என்பர்|போலும்|கும்|டும்|ஆயிற்று|ஆம்|உண்டு)$')
# a sentence after the last gloss that is a grammar note, so the விளக்கம் starts there even after a ';'
NOTE_END = re.compile(r'(?:முற்றெச்சங்கள்|முற்றெச்சம்|வினையெச்சம்|பெயரெச்சம்|எச்சங்கள்|அசைநிலை|ஈற்றசை|அசை|தேற்றம்|விகாரம்|'
                      r'ஆகுபெயர்|அணி|என்றார்|என்க|எனலாம்|என்பர்|கருத்து|என்றபடி|என்றவாறு|என்பதாம்)$')


def _scan(s, start, stops):
    """Positions of the characters in stops at bracket and quote depth 0, from start on."""
    depth, dq = 0, False
    for i in range(start, len(s)):
        ch = s[i]
        if ch in OPEN:
            depth += 1
        elif ch in CLOSE:
            depth = max(0, depth - 1)
        elif ch == '"':
            dq = not dq
        elif ch in stops and depth == 0 and not dq and (i + 1 == len(s) or s[i + 1].isspace() or s[i + 1] in '*‘“'):
            yield i


def _after(s, i):
    j = i + 1
    if s[j:j + 2] == '**':               # "...போன்றது.**" — keep the closing bold marker
        j += 2
    m = re.match(r'\s*\([^()]{1,30}\)', s[j:])
    if m:
        j += m.end()
    return j


def meaning_end(s, start, kandam=0):
    """Index just after the end of the meaning that begins at s[start], or None."""
    if re.search(r'[.]\s*\*\*$', s[:start]):   # "**காணாய் -.**": the bold word's meaning is empty
        return start
    semis = list(_scan(s, start, ';?!'))
    for i in _scan(s, start, '.'):
        word = re.sub(r'[*’”\'")\]]+$', '', s[:i].split()[-1]) if s[:i].split() else ''
        if kandam == 1 and not FINITE.search(word):
            continue
        # a grammar note straight after a ';' ("... கூறலானான்; இறைஞ்சினன், நின்றனன் இவை முற்றெச்சங்கள்.")
        before = [x for x in semis if x < i]
        if before and NOTE_END.search(word) and '**' not in s[before[-1]:i]:
            return _after(s, before[-1])
        return _after(s, i)
    return None


def rebalance(pad, notes, kandam=0):
    """(pad, notes) with the பதவுரை / விளக்கம் boundary put where the meaning of the last gloss ends."""
    pad = (pad or '').strip()
    notes = [dict(x) for x in (notes or [])]
    # 1. the பதவுரை continued in the next paragraph(s)
    while notes and 'p' in notes[0] and has_gloss(notes[0]['p']):
        first = notes[0]['p']
        if not pad or not pad.rstrip('* ').endswith(('.', '?', '!')) or has_gloss(first, at_start=True):
            pad = (pad + ' ' + notes.pop(0)['p']).strip()
        else:
            break
    # 2. the விளக்கம் printed in the same paragraph as the last gloss: it starts after the meaning of the last
    #    bold word (every word glossed in the பதவுரை is printed in bold)
    bolds = [m.end() for m in re.finditer(r'\*\*[^*]+\*\*', pad)]
    if bolds:
        j = meaning_end(pad, bolds[-1], kandam)
        if j is not None:
            tail = pad[j:].strip()
            head = pad[:j].rstrip()
            if TAMIL.search(tail) and not re.fullmatch(r'\([^()]{0,60}\)[.;]?', tail) and head.count('**') % 2 == 0:
                pad = head
                # a sentence cut by a page break goes on in the next paragraph
                if notes and 'p' in notes[0] and not tail.rstrip('* ').endswith(tuple('.?!:;)’”\'"')):
                    tail = tail + ' ' + notes.pop(0)['p']
                notes.insert(0, {'p': tail})
    return pad, notes
