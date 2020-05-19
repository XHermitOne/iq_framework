#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for converting paper size indices getInto real sizes in
hundredths of a millimeter.
"""

__version__ = (0, 0, 0, 1)

# Excel paper size constants

xlPaper11x17 = 17               # 11 in. x 17 in.
xlPaperA4 = 9                   # A4 (210 mm x 297 mm)
xlPaperA5 = 11                  # A5 (148 mm x 210 mm)
xlPaperB5 = 13                  # A5 (148 mm x 210 mm)
xlPaperDsheet = 25              # D size sheet
xlPaperEnvelope11 = 21          # Envelope= #11 (4-1/2 in. x 10-3/8 in.)
xlPaperEnvelope14 = 23          # Envelope= #14 (5 in. x 11-1/2 in.)
xlPaperEnvelopeB4 = 33          # Envelope B4 (250 mm x 353 mm)
xlPaperEnvelopeB6 = 35          # Envelope B6 (176 mm x 125 mm)
xlPaperEnvelopeC4 = 30          # Envelope C4 (229 mm x 324 mm)
xlPaperEnvelopeC6 = 31          # Envelope C6 (114 mm x 162 mm)
xlPaperEnvelopeDL = 27          # Envelope DL (110 mm x 220 mm)
xlPaperEnvelopeMonarch = 37     # Envelope Monarch (3-7/8 in. x 7-1/2 in.)
xlPaperEsheet = 26              # E size sheet
xlPaperFanfoldLegalGerman = 41  # German Legal Fanfold (8-1/2 in. x 13 in.)
xlPaperFanfoldUS = 39           # U.S. Standard Fanfold (14-7/8 in. x 11 in.)
xlPaperLedger = 4               # Ledger (17 in. x 11 in.)
xlPaperLetter = 1               # Letter (8-1/2 in. x 11 in.)
xlPaperNote = 18                # Note (8-1/2 in. x 11 in.)
xlPaperStatement = 6            # Statement (5-1/2 in. x 8-1/2 in.)
xlPaperUser = 256               # User-defined
xlPaper10x14 = 16               # 10 in. x 14 in.
xlPaperA3 = 8                   # A3 (297 mm x 420 mm)
xlPaperA4Small = 10             # A4 Small (210 mm x 297 mm)
xlPaperB4 = 12                  # B4 (250 mm x 354 mm)
xlPaperCsheet = 24              # C size sheet
xlPaperEnvelope10 = 20          # Envelope= #10 (4-1/8 in. x 9-1/2 in.)
xlPaperEnvelope12 = 22          # Envelope= #12 (4-1/2 in. x 11 in.)
xlPaperEnvelope9 = 19           # Envelope= #9 (3-7/8 in. x 8-7/8 in.)
xlPaperEnvelopeB5 = 34          # Envelope B5 (176 mm x 250 mm)
xlPaperEnvelopeC3 = 29          # Envelope C3 (324 mm x 458 mm)
xlPaperEnvelopeC5 = 28          # Envelope C5 (162 mm x 229 mm)
xlPaperEnvelopeC65 = 32         # Envelope C65 (114 mm x 229 mm)
xlPaperEnvelopeItaly = 36       # Envelope (110 mm x 230 mm)
xlPaperEnvelopePersonal = 38    # Envelope (3-5/8 in. x 6-1/2 in.)
xlPaperExecutive = 7            # Executive (7-1/2 in. x 10-1/2 in.)
xlPaperFanfoldStdGerman = 40    # German Legal Fanfold (8-1/2 in. x 13 in.)
xlPaperFolio = 14               # Folio (8-1/2 in. x 13 in.)
xlPaperLegal = 5                # Legal (8-1/2 in. x 14 in.)
xlPaperLetterSmall = 2          # Letter Small (8-1/2 in. x 11 in.)
xlPaperQuarto = 15              # Quarto (215 mm x 275 mm)
xlPaperTabloid = 3              # Tabloid (11 in. x 17 in.)

#
WIDTH_IDX = 0
HEIGHT_IDX = 1

# Excel constants to paper size conversion dictionary
XL_PAPER_SIZE = {
    xlPaper11x17: None,                     # 11 in. x 17 in.
    xlPaperA4: (21000, 29700),              # A4 (210 mm x 297 mm)
    xlPaperA5: (14800, 21000),              # A5 (148 mm x 210 mm)
    xlPaperB5: (14800, 21000),              # A5 (148 mm x 210 mm)
    xlPaperDsheet: None,                    # D size sheet
    xlPaperEnvelope11: None,                # Envelope= #11 (4-1/2 in. x 10-3/8 in.)
    xlPaperEnvelope14: None,                # Envelope= #14 (5 in. x 11-1/2 in.)
    xlPaperEnvelopeB4: (25000, 35300),      # Envelope B4 (250 mm x 353 mm)
    xlPaperEnvelopeB6: (17600, 12500),      # Envelope B6 (176 mm x 125 mm)
    xlPaperEnvelopeC4: (22900, 32400),      # Envelope C4 (229 mm x 324 mm)
    xlPaperEnvelopeC6: (11400, 16200),      # Envelope C6 (114 mm x 162 mm)
    xlPaperEnvelopeDL: (11000, 22000),      # Envelope DL (110 mm x 220 mm)
    xlPaperEnvelopeMonarch: None,           # Envelope Monarch (3-7/8 in. x 7-1/2 in.)
    xlPaperEsheet: None,                    # E size sheet
    xlPaperFanfoldLegalGerman: None,        # German Legal Fanfold (8-1/2 in. x 13 in.)
    xlPaperFanfoldUS: None,                 # U.S. Standard Fanfold (14-7/8 in. x 11 in.)
    xlPaperLedger: None,                    # Ledger (17 in. x 11 in.)
    xlPaperLetter: None,                    # Letter (8-1/2 in. x 11 in.)
    xlPaperNote: None,                      # Note (8-1/2 in. x 11 in.)
    xlPaperStatement: None,                 # Statement (5-1/2 in. x 8-1/2 in.)
    xlPaperUser: None,                      # User-defined
    xlPaper10x14: None,                     # 10 in. x 14 in.
    xlPaperA3: (29700, 42000),              # A3 (297 mm x 420 mm)
    xlPaperA4Small: (21000, 29700),         # A4 Small (210 mm x 297 mm)
    xlPaperB4: (25000, 35400),              # B4 (250 mm x 354 mm)
    xlPaperCsheet: None,                    # C size sheet
    xlPaperEnvelope10: None,                # Envelope= #10 (4-1/8 in. x 9-1/2 in.)
    xlPaperEnvelope12: None,                # Envelope= #12 (4-1/2 in. x 11 in.)
    xlPaperEnvelope9: None,                 # Envelope= #9 (3-7/8 in. x 8-7/8 in.)
    xlPaperEnvelopeB5: (17600, 25000),      # Envelope B5 (176 mm x 250 mm)
    xlPaperEnvelopeC3: (32400, 45800),      # Envelope C3 (324 mm x 458 mm)
    xlPaperEnvelopeC5: (16200, 22900),      # Envelope C5 (162 mm x 229 mm)
    xlPaperEnvelopeC65: (11400, 22900),     # Envelope C65 (114 mm x 229 mm)
    xlPaperEnvelopeItaly: (11000, 23000),   # Envelope (110 mm x 230 mm)
    xlPaperEnvelopePersonal: None,          # Envelope (3-5/8 in. x 6-1/2 in.)
    xlPaperExecutive: None,                 # Executive (7-1/2 in. x 10-1/2 in.)
    xlPaperFanfoldStdGerman: None,          # German Legal Fanfold (8-1/2 in. x 13 in.)
    xlPaperFolio: None,                     # Folio (8-1/2 in. x 13 in.)
    xlPaperLegal: None,                     # Legal (8-1/2 in. x 14 in.)
    xlPaperLetterSmall: None,               # Letter Small (8-1/2 in. x 11 in.)
    xlPaperQuarto: (21500, 27500),          # Quarto (215 mm x 275 mm)
    xlPaperTabloid: None,                   # Tabloid (11 in. x 17 in.)
}
