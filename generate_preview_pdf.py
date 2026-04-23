"""
Preview of the one-page PDF that matches the updated jsPDF browser download.
Sample results: Seen 70%, Booked 30%, Paid 10% (primary gap: Booked)
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from datetime import datetime
import os

OUTPUT = os.path.join(os.path.dirname(__file__), 'SBP-Diagnostic-Results-PREVIEW.pdf')

# Colors
accent = Color(107/255, 102/255, 233/255)
text_dark = Color(44/255, 42/255, 39/255)
text_muted = Color(112/255, 110/255, 104/255)
seen = Color(107/255, 102/255, 233/255)
booked = Color(29/255, 158/255, 117/255)
paid = Color(200/255, 85/255, 42/255)
lime = Color(222/255, 255/255, 85/255)
border = Color(232/255, 226/255, 217/255)
ivory = Color(249/255, 246/255, 240/255)
body_gray = Color(61/255, 59/255, 55/255)
bg_muted = Color(240/255, 236/255, 229/255)

# Sample data
ss, bs, ps = 70, 30, 10
gap_title = 'Your primary gap is in the Booked stage'
gap_body = ('People are raising their hand and opting in. The top of the system is working. But there is nothing '
            'waiting to take them from interested to booked automatically - and so they disappear into silence. '
            'This is the most common gap for service providers running Meta ads. You are getting leads. You are just '
            'not getting calls. The reason is that the pathway between the opt-in and the calendar is broken, '
            'incomplete, or missing entirely. Every lead who disappears after opting in was interested enough to '
            'give you their email address. They did not change their mind. Nothing followed up fast enough, clearly '
            'enough, or specifically enough to move them from "I just opted in" to "I just booked a call." '
            'The fix first recommendation below shows you exactly where to start closing that gap.')
fix_title = 'Build an automated follow-up sequence that starts within 30 minutes of opt-in'
fix_action = ('This is the most important piece in the entire Booked stage. The probability of a lead booking drops '
              'dramatically within 30 minutes of silence after opt-in. Build a sequence of at least 3 automated emails '
              'that runs within the first 24-48 hours. Email 1: deliver the lead magnet and reframe the real problem. '
              'Email 2: your proof story - the before and the after. Email 3: a direct, specific invitation to book a '
              'call with your calendar link clearly visible.')

score_notes = {
    'seen': 'Your Seen stage has meaningful gaps that may be attracting the wrong leads or producing unqualified opt-ins.',
    'booked': 'Your Booked stage needs significant work. This is almost certainly where your leads are disappearing.',
    'paid': 'Your Paid stage is mostly missing. Every lead who did not book in the first 48 hours is currently receiving nothing from you.'
}

c = canvas.Canvas(OUTPUT, pagesize=letter)
W, H = letter
margin = 40
content_w = W - (margin * 2)
y = H - margin


def wrapped_lines(text, font, size, max_w):
    words = text.split(' ')
    lines = []
    line = ''
    for w in words:
        test = (line + ' ' + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


# Top gradient bar
c.setFillColor(accent)
c.rect(0, H - 6, W / 2, 6, fill=1, stroke=0)
c.setFillColor(lime)
c.rect(W / 2, H - 6, W / 2, 6, fill=1, stroke=0)

y = H - margin - 14

# Brand
c.setFont('Helvetica-Bold', 8.5)
c.setFillColor(accent)
c.drawString(margin, y, 'PERFECTLY MADE MARKETING')
y -= 22

# Title (two lines)
c.setFont('Times-Roman', 22)
c.setFillColor(text_dark)
c.drawString(margin, y, 'The Seen Booked Paid Diagnostic')
y -= 22
c.drawString(margin, y, 'Your Results')
y -= 20

# Date
c.setFont('Helvetica', 9.5)
c.setFillColor(text_muted)
c.drawString(margin, y, datetime.now().strftime('%B %d, %Y'))
y -= 18

# Divider
c.setStrokeColor(border)
c.setLineWidth(0.5)
c.line(margin, y, W - margin, y)
y -= 22

# YOUR SCORES
c.setFont('Helvetica-Bold', 9.5)
c.setFillColor(text_muted)
c.drawString(margin, y, 'YOUR SCORES')
y -= 18


def draw_score(label, score, color, note):
    global y
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(color)
    c.drawString(margin, y, label)
    c.setFont('Times-Roman', 14)
    c.setFillColor(text_dark)
    c.drawRightString(W - margin, y, f'{score}%')
    y -= 8
    c.setFillColor(bg_muted)
    c.roundRect(margin, y - 6, content_w, 6, 3, fill=1, stroke=0)
    fill_w = (content_w * score) / 100
    if fill_w > 0:
        c.setFillColor(color)
        c.roundRect(margin, y - 6, fill_w, 6, 3, fill=1, stroke=0)
    y -= 16
    c.setFont('Helvetica', 9)
    c.setFillColor(text_muted)
    lines = wrapped_lines(note, 'Helvetica', 9, content_w)
    for ln in lines:
        c.drawString(margin, y, ln)
        y -= 12
    y -= 14


draw_score('01 - SEEN', ss, seen, score_notes['seen'])
draw_score('02 - BOOKED', bs, booked, score_notes['booked'])
draw_score('03 - PAID', ps, paid, score_notes['paid'])

y -= 6

# PRIMARY GAP
c.setFont('Helvetica-Bold', 8.5)
c.setFillColor(booked)
c.drawString(margin, y, 'PRIMARY GAP IDENTIFIED - BOOKED STAGE')
y -= 16

c.setFont('Times-Roman', 14)
c.setFillColor(text_dark)
title_lines = wrapped_lines(gap_title, 'Times-Roman', 14, content_w)
for ln in title_lines:
    c.drawString(margin, y, ln)
    y -= 17
y -= 10

# Gap body
c.setFont('Helvetica', 9.5)
c.setFillColor(body_gray)
lines = wrapped_lines(gap_body, 'Helvetica', 9.5, content_w)
for ln in lines:
    c.drawString(margin, y, ln)
    y -= 13
y -= 20

# FIX THIS FIRST
c.setFillColor(lime)
c.circle(margin + 4, y - 3, 4.5, fill=1, stroke=0)
c.setFont('Helvetica-Bold', 8.5)
c.setFillColor(text_muted)
c.drawString(margin + 14, y, 'FIX THIS FIRST')
y -= 16

c.setFont('Times-Roman', 13)
c.setFillColor(text_dark)
ftl = wrapped_lines(fix_title, 'Times-Roman', 13, content_w)
for ln in ftl:
    c.drawString(margin, y, ln)
    y -= 16
y -= 8

c.setFont('Helvetica', 9.5)
c.setFillColor(body_gray)
fl = wrapped_lines(fix_action, 'Helvetica', 9.5, content_w)
for ln in fl:
    c.drawString(margin, y, ln)
    y -= 13
y -= 20

# NEXT STEP card
card_h = 62
c.setFillColor(ivory)
c.roundRect(margin, y - card_h, content_w, card_h, 8, fill=1, stroke=0)
cy = y - 18
c.setFont('Helvetica-Bold', 8.5)
c.setFillColor(booked)
c.drawString(margin + 16, cy, 'NEXT STEP')
cy -= 14
c.setFont('Times-Roman', 11.5)
c.setFillColor(text_dark)
c.drawString(margin + 16, cy, 'Install what you just learned')
cy -= 14
c.setFont('Helvetica', 9)
c.setFillColor(accent)
c.drawString(margin + 16, cy, 'https://offer.perfectlymademarketing.com/')

# Footer
c.setFont('Helvetica', 8)
c.setFillColor(text_muted)
c.drawCentredString(W / 2, 24, '(c) Perfectly Made Marketing  |  perfectlymademarketing.com')

c.save()
print(f'Preview PDF saved: {OUTPUT}')
print(f'Pages: {c.getPageNumber()}')
