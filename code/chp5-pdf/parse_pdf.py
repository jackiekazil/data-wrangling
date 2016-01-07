import slate

pdf = 'EN-FINAL Table 9.pdf'

with open(pdf) as f:
    doc = slate.PDF(f)

for page in doc[:2]:
    print type(page)
