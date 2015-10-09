import goslate
roman_gs = goslate.Goslate(writing=goslate.WRITING_ROMAN)
in_sent = raw_input()
print(roman_gs.translate(in_sent, 'hi'))