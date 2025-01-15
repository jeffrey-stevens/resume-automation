# Syntax of Word DOCX XML files

## Structural elements

### Paragraphs and runs

- w:p: Paragraph
  - w:pPr: Paragraph properties
    - w:pStyle w:val="[style name]": Paragraph styling
  - w:r: Run
    - w:rPr: Run properties
      - w:rStyle w:val="[style name]": Run styling
    - w:t: Text

- w:t must be contained inside an w:r, which must be contained in a w:p
- w:pPr and w:r occur at the same level

### Tables

- w:tbl:  Table
  - w:tr:  Table row
    - w:tc:  Table column
      - Then w:p, etc.

#### Table units

- Percentages:  Given in 1/50 of 1%.
  - Thus 5000 = 100%
- w:gridCol
  - Units are in 1/20 of a pt ("twip")

### Referencing and tracking attributes

- w:rsidR, etc. attributes are for document tracking and aren't necessary
- w14:paraId and w14:textId are for paragraph and run identification, and aren't needed if the document doesn't use internal referencing


## Styles

- w:latentStyles:  Styles not shown to the user?

### Style syntax

- w:style w:type="[type]" w:styleId="[style ID]"
  - Attributes:
    - Style types: paragraph, character, table, numbering, linked
    - w:default="1":  Set as the default style
  - w:name w:val="[style name]"
  - w:basedOn w:val="[style id]"
  - w:pPr
    - w:align w:val="[e.g. center]":  Alignment
    - w:spacing w:before="..." w:after="...":  Spacing before and after paragraph
      - In units of 1/20 of a pt
      - Other attributes:
        - w:line="...":  Line spacing
  - w:rPr
    - w:b:  Bold
    - w:sz:  Size
    - w:color w:val="[hex color]"


### Fonts

- w:sz w:val="[size]": Font size, in half-points
- w:szCs:  Font size for complex scripts --- probably not important