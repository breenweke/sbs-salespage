"""
Generate The Self-Booking System Checklist PDF
Branded for Perfectly Made Marketing
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
import os

# ── BRAND COLORS ──
ACCENT = HexColor("#6b66e9")
ACCENT_LIGHT = HexColor("#eeecfc")
LIME = HexColor("#deff55")
LIME_SOFT = HexColor("#f2ffb8")
CREAM = HexColor("#f9f6f0")
IVORY = HexColor("#fdfbf7")
TEXT_DARK = HexColor("#1a1a1a")
TEXT_BODY = HexColor("#7a7067")
TEXT_MUTED = HexColor("#a69e94")
TAUPE_100 = HexColor("#f0ece6")
TAUPE_200 = HexColor("#e4dfd7")
SOFT_RED = HexColor("#d4715a")
SOFT_RED_BG = HexColor("#fef6f4")
SOFT_GREEN = HexColor("#5a9e6b")
SOFT_GREEN_BG = HexColor("#f4faf4")
WARM_WHITE = HexColor("#fefefe")

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "The-Self-Booking-System-Checklist.pdf")

# ── CUSTOM FLOWABLES ──

class GradientBar(Flowable):
    """Top gradient bar accent -> lime"""
    def __init__(self, width, height=5):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        steps = 100
        for i in range(steps):
            t = i / steps
            r = ACCENT.red + (LIME.red - ACCENT.red) * t
            g = ACCENT.green + (LIME.green - ACCENT.green) * t
            b = ACCENT.blue + (LIME.blue - ACCENT.blue) * t
            c.setFillColorRGB(r, g, b)
            x = (self.width / steps) * i
            c.rect(x, 0, self.width / steps + 1, self.height, fill=1, stroke=0)


class StageBadge(Flowable):
    """Lime-colored stage badge/pill"""
    def __init__(self, text):
        super().__init__()
        self.text = text
        self._text_width = 0

    def wrap(self, availWidth, availHeight):
        self._text_width = len(self.text) * 6.5 + 28
        return (self._text_width, 24)

    def draw(self):
        c = self.canv
        w = self._text_width
        h = 20
        r = 10
        c.setFillColor(LIME)
        c.roundRect(0, 0, w, h, r, fill=1, stroke=0)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(14, 6, self.text)


class SubSectionHeader(Flowable):
    """Accent-colored sub-section header"""
    def __init__(self, text, width):
        super().__init__()
        self.text = text
        self.full_width = width

    def wrap(self, availWidth, availHeight):
        return (self.full_width, 30)

    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT)
        c.rect(0, 0, 3, 22, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(12, 6, self.text)


class CheckboxItem(Flowable):
    """Checkbox square with text"""
    def __init__(self, text, width):
        super().__init__()
        self.text = text
        self.full_width = width
        self._height = 0

    def wrap(self, availWidth, availHeight):
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.text, "Helvetica-Bold", 10, self.full_width - 30)
        self._height = max(len(lines) * 14 + 4, 18)
        return (self.full_width, self._height)

    def draw(self):
        c = self.canv
        y = self._height - 14
        # Checkbox
        c.setStrokeColor(TAUPE_200)
        c.setFillColor(WARM_WHITE)
        c.roundRect(0, y - 2, 14, 14, 2, fill=1, stroke=1)
        # Text
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica-Bold", 10)
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.text, "Helvetica-Bold", 10, self.full_width - 30)
        for i, line in enumerate(lines):
            c.drawString(22, y - i * 14, line)


class YesNoLine(Flowable):
    """Yes / No circles"""
    def __init__(self):
        super().__init__()

    def wrap(self, availWidth, availHeight):
        return (200, 22)

    def draw(self):
        c = self.canv
        # Yes
        c.setStrokeColor(SOFT_GREEN)
        c.setFillColor(SOFT_GREEN_BG)
        c.circle(30, 8, 7, fill=1, stroke=1)
        c.setFillColor(TEXT_BODY)
        c.setFont("Helvetica", 9)
        c.drawString(42, 4, "Yes")
        # No
        c.setStrokeColor(SOFT_RED)
        c.setFillColor(SOFT_RED_BG)
        c.circle(90, 8, 7, fill=1, stroke=1)
        c.setFillColor(TEXT_BODY)
        c.drawString(102, 4, "No")


class ScoreBlock(Flowable):
    """Colored score block"""
    def __init__(self, range_text, description, color, width):
        super().__init__()
        self.range_text = range_text
        self.description = description
        self.color = color
        self.full_width = width
        self._height = 0

    def wrap(self, availWidth, availHeight):
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.description, "Helvetica", 9.5, self.full_width - 40)
        self._height = len(lines) * 13 + 36
        return (self.full_width, self._height)

    def draw(self):
        c = self.canv
        # Background
        bg = HexColor("#f4faf4") if self.color == SOFT_GREEN else (SOFT_RED_BG if self.color == SOFT_RED else ACCENT_LIGHT)
        c.setFillColor(bg)
        c.roundRect(0, 0, self.full_width, self._height, 8, fill=1, stroke=0)
        # Left accent bar
        c.setFillColor(self.color)
        c.roundRect(0, 0, 4, self._height, 2, fill=1, stroke=0)
        # Range text
        c.setFillColor(self.color)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(16, self._height - 22, self.range_text)
        # Description
        c.setFillColor(TEXT_BODY)
        c.setFont("Helvetica", 9.5)
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.description, "Helvetica", 9.5, self.full_width - 40)
        y = self._height - 38
        for line in lines:
            c.drawString(16, y, line)
            y -= 13


# ── STYLES ──

def get_styles():
    return {
        'title': ParagraphStyle(
            'Title', fontName='Times-Bold', fontSize=28, leading=34,
            textColor=TEXT_DARK, alignment=TA_CENTER, spaceAfter=12
        ),
        'subtitle': ParagraphStyle(
            'Subtitle', fontName='Times-Italic', fontSize=13, leading=18,
            textColor=TEXT_BODY, alignment=TA_CENTER, spaceAfter=8
        ),
        'h2': ParagraphStyle(
            'H2', fontName='Times-Bold', fontSize=20, leading=26,
            textColor=TEXT_DARK, spaceBefore=20, spaceAfter=10
        ),
        'h2_center': ParagraphStyle(
            'H2Center', fontName='Times-Bold', fontSize=20, leading=26,
            textColor=TEXT_DARK, spaceBefore=20, spaceAfter=10, alignment=TA_CENTER
        ),
        'h3': ParagraphStyle(
            'H3', fontName='Times-Bold', fontSize=14, leading=19,
            textColor=TEXT_DARK, spaceBefore=14, spaceAfter=6
        ),
        'body': ParagraphStyle(
            'Body', fontName='Helvetica', fontSize=10, leading=16,
            textColor=TEXT_BODY, spaceAfter=8
        ),
        'body_bold': ParagraphStyle(
            'BodyBold', fontName='Helvetica-Bold', fontSize=10, leading=16,
            textColor=TEXT_DARK, spaceAfter=8
        ),
        'body_italic': ParagraphStyle(
            'BodyItalic', fontName='Helvetica-Oblique', fontSize=10, leading=16,
            textColor=TEXT_BODY, spaceAfter=8
        ),
        'insight': ParagraphStyle(
            'Insight', fontName='Helvetica', fontSize=9.5, leading=15,
            textColor=TEXT_DARK, leftIndent=16, rightIndent=8, spaceAfter=8,
            backColor=ACCENT_LIGHT, borderPadding=(10, 10, 10, 10)
        ),
        'practice': ParagraphStyle(
            'Practice', fontName='Helvetica', fontSize=9.5, leading=15,
            textColor=TEXT_BODY, leftIndent=16, spaceAfter=8
        ),
        'practice_label': ParagraphStyle(
            'PracticeLabel', fontName='Helvetica-BoldOblique', fontSize=9.5, leading=15,
            textColor=TEXT_DARK, leftIndent=16, spaceBefore=6, spaceAfter=2
        ),
        'cta_heading': ParagraphStyle(
            'CTAHeading', fontName='Times-Bold', fontSize=16, leading=22,
            textColor=ACCENT, spaceBefore=16, spaceAfter=8
        ),
        'cta_body': ParagraphStyle(
            'CTABody', fontName='Helvetica', fontSize=10, leading=16,
            textColor=TEXT_BODY, spaceAfter=8
        ),
        'cta_link': ParagraphStyle(
            'CTALink', fontName='Helvetica-Bold', fontSize=10, leading=16,
            textColor=ACCENT, spaceAfter=16
        ),
        'footer_text': ParagraphStyle(
            'FooterText', fontName='Helvetica', fontSize=7, leading=10,
            textColor=TEXT_MUTED, alignment=TA_CENTER
        ),
        'copyright': ParagraphStyle(
            'Copyright', fontName='Helvetica', fontSize=8, leading=12,
            textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=20
        ),
    }


# ── PAGE TEMPLATE ──

def footer_handler(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(TEXT_MUTED)
    w, h = letter
    canvas.drawCentredString(w / 2, 30, "Perfectly Made Marketing  |  The Self-Booking System Checklist")
    canvas.drawRightString(w - 50, 30, f"{doc.page}")
    canvas.restoreState()


def cover_footer(canvas, doc):
    pass  # No footer on cover


# ── BUILD PDF ──

def build_pdf():
    w, h = letter
    content_width = w - 2 * 60  # 60pt margins

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=60, rightMargin=60,
        topMargin=50, bottomMargin=50
    )

    s = get_styles()
    story = []

    # ════════════════════ COVER PAGE ════════════════════
    story.append(GradientBar(content_width, 5))
    story.append(Spacer(1, 120))
    story.append(Paragraph("THE SELF-BOOKING<br/>SYSTEM CHECKLIST", s['title']))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width=80, thickness=2, color=ACCENT, spaceAfter=16, spaceBefore=8, hAlign='CENTER'))
    story.append(Paragraph(
        "The exact pieces I have in place for myself and every client<br/>"
        "who gets booked calls every week — without posting daily,<br/>"
        "chasing leads, or manually following up.",
        s['subtitle']
    ))
    story.append(Spacer(1, 40))

    # Framework pills on cover
    framework_data = [["SEEN", "BOOKED", "PAID"]]
    framework_styles = [
        ("BACKGROUND", (0, 0), (0, 0), LIME),
        ("BACKGROUND", (1, 0), (1, 0), LIME),
        ("BACKGROUND", (2, 0), (2, 0), LIME),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT_DARK),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]
    ft = Table(framework_data, colWidths=[100, 100, 100], hAlign='CENTER')
    ft.setStyle(TableStyle(framework_styles))
    story.append(ft)

    story.append(Spacer(1, 60))
    story.append(Paragraph("Perfectly Made Marketing", ParagraphStyle(
        'BrandName', fontName='Times-Italic', fontSize=12, textColor=TEXT_MUTED, alignment=TA_CENTER
    )))

    story.append(PageBreak())

    # ════════════════════ INTRODUCTION ════════════════════
    story.append(GradientBar(content_width, 4))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Before you go through this, here's what you need to understand.", s['h3']))
    story.append(Spacer(1, 4))

    intro_paras = [
        "Most service providers think getting booked calls from Meta ads is about running a good ad. So they focus all their energy on the creative, the targeting, the budget — and wonder why leads keep coming in but calls aren't happening.",
        "The ad is only one piece. And it's not even the most important one.",
        "Getting booked calls consistently requires a complete system — three stages working together in sequence. I call it the <b>Seen → Booked → Paid</b> framework. Each stage has a specific job. Skip a piece in any stage and the whole thing leaks.",
        "<b>SEEN</b> is how your ideal client finds you. It's your ad, your lead magnet, your creative, and your copy — all working together to put you in front of the right person at the right time and give them a reason to raise their hand.",
        "<b>BOOKED</b> is what happens after they raise their hand. It's the system that takes someone from \"I'm interested\" to \"I just booked a call\" — automatically, without you involved.",
        "<b>PAID</b> is what happens after they're in your world. It's the follow-up system that nurtures the leads who didn't book immediately, keeps your existing list warm, and makes sure the people who do book actually show up ready to work with you.",
        "When all three stages are fully built and connected, the system runs without you. Leads come in. Calls get booked. You show up and close. That's what this checklist reveals — exactly which pieces you have in place and which ones are creating the leaks you've been trying to fix.",
        "<b>Go through each section. Check yes or no. By the end you'll know exactly what to fix first.</b>"
    ]
    for p in intro_paras:
        story.append(Paragraph(p, s['body']))

    story.append(PageBreak())

    # ════════════════════ HELPER FUNCTIONS ════════════════════

    def add_stage(stage_label, stage_title, stage_intro):
        story.append(GradientBar(content_width, 4))
        story.append(Spacer(1, 12))
        story.append(StageBadge(stage_label))
        story.append(Spacer(1, 8))
        story.append(Paragraph(stage_title, s['h2']))
        if stage_intro:
            story.append(Paragraph(stage_intro, s['body']))
        story.append(Spacer(1, 8))

    def add_subsection(title):
        story.append(Spacer(1, 10))
        story.append(SubSectionHeader(title, content_width))
        story.append(Spacer(1, 10))

    def add_checkbox(text):
        story.append(CheckboxItem(text, content_width))
        story.append(Spacer(1, 4))
        story.append(YesNoLine())
        story.append(Spacer(1, 8))

    def add_body(text):
        story.append(Paragraph(text, s['body']))

    def add_practice_block(label, text):
        story.append(Paragraph(label, s['practice_label']))
        story.append(Paragraph(text, s['practice']))

    def add_insight_block(text):
        # Accent-bordered insight block
        t = Table(
            [[Paragraph(text, ParagraphStyle(
                'InsightInner', fontName='Helvetica', fontSize=9.5, leading=15,
                textColor=TEXT_DARK
            ))]],
            colWidths=[content_width - 20],
            hAlign='LEFT'
        )
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ACCENT_LIGHT),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEBEFOREPURE', (0, 0), (0, -1), 3, ACCENT),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

    # ════════════════════ STAGE 1: SEEN ════════════════════

    add_stage(
        "STAGE 1: SEEN",
        "Getting in front of the right person and giving them a reason to raise their hand",
        "Most service providers running Meta ads are either attracting the wrong people or not attracting enough of the right ones. The reason is almost never the budget. It's that the lead magnet, the creative, and the copy aren't all speaking to the same person about the same problem at the same time. When those three things are aligned, the right person stops scrolling, clicks, and opts in. When they're not, you get leads who never book — or worse, leads who were never going to buy in the first place."
    )

    # YOUR LEAD MAGNET
    add_subsection("YOUR LEAD MAGNET")

    add_checkbox("Your lead magnet solves a problem your ideal client is actively trying to fix right now — not a problem you think they should care about.")
    add_body("This is the most important piece of the entire system and the one most people get wrong. A lead magnet that solves an active, urgent problem attracts people who are already in motion — already looking for a solution, already willing to act. A lead magnet that solves a passive problem — one that's nice to know but not burning — attracts curious people who download things and disappear.")
    add_body("Ask yourself honestly: is the person who downloads this freebie someone who woke up this morning thinking about this problem? Or is it someone you have to convince that the problem matters? The first person books calls. The second person collects free PDFs.")
    add_practice_block("The difference in practice:", "A health coach who creates \"10 Healthy Habits for a Balanced Life\" is solving a passive problem. Everyone wants balance. Nobody is urgently Googling \"how do I get more balanced\" at 11pm. But a health coach who creates \"Why You Keep Losing Weight and Gaining It Back — And What to Do Differently\" is solving an active, burning problem. That person is lying awake frustrated about the exact thing the lead magnet addresses. That's who downloads it. That's who books calls.")

    add_checkbox("Your lead magnet delivers a specific insight or shift — not just information.")
    add_body("Your ideal client has already consumed a lot of free content. They don't need more information — they need a new way of seeing their problem. The best lead magnets don't just teach. They reframe. They show the reader something about their situation they hadn't seen before, and they make the reader think \"oh — that's what's actually happening.\" That moment of clarity is what builds trust fast. And trust is what makes someone book a call with a stranger.")
    add_practice_block("The difference in practice:", "A lead magnet that says \"here are 5 tips to get more clients\" gives information. A lead magnet that says \"here's why your marketing isn't working even though you're doing everything right — and the one shift that changes it\" delivers a reframe. The first one teaches. The second one changes how they see their problem. Reframes build trust. Information just adds to the pile.")

    add_checkbox("Your lead magnet naturally leads to a conversation with you — not just a download.")
    add_body("The job of your lead magnet is not to educate. It's to start a relationship that ends in a booked call. Every piece of your freebie should be moving the reader toward the conclusion that they need your help to implement what they just learned. If someone can read your lead magnet, feel fully satisfied, and never think about you again — it's not doing its job. It should leave them clearer on the problem and more aware that solving it requires more than a PDF.")
    add_body("Ask yourself: After reading your lead magnet, does your ideal client think \"I understand this now, I've got it\" — or do they think \"I understand this now, but I need help actually doing it\"? The first reaction means your lead magnet gave away too much. The second reaction means it did its job.")

    # YOUR AD CREATIVE
    add_subsection("YOUR AD CREATIVE")

    add_checkbox("Your ad creative stops the scroll for the right person — and actively filters out the wrong person.")
    add_body("A good ad creative is not designed to get as many clicks as possible. It's designed to get clicks from the specific person you want on your calendar — and to be invisible to everyone else. That means your image or video should immediately signal who it's for through the visual itself, not just the copy.")
    add_practice_block("The difference in practice:", "An ad with a stock photo of a laptop and coffee on a desk could be for anyone selling anything online. It stops no one specifically because it speaks to everyone generally. An ad that shows a screenshot of a Meta Ads Manager dashboard with a high lead count and zero booked calls — that image speaks directly to the service provider who is living that exact experience. They stop because they recognize their own screen. That recognition is worth more than any amount of polish.")

    add_checkbox("Your creative looks like your brand — not like an ad.")
    add_body("The ads that perform best in 2025 don't look like ads. They look like content from someone your ideal client already follows and trusts. That doesn't mean unpolished — it means intentional. Your colors, your fonts, your aesthetic should be consistent enough across your content and your ads that when your ideal client sees your ad, it feels familiar even if they've never seen you before.")
    add_practice_block("The difference in practice:", "A bright red \"FREE GUIDE\" banner ad with a stock photo signals \"this is an ad, ignore me.\" A clean, warm-toned graphic with your brand colors, a specific headline in your brand font, and no \"FREE\" badge anywhere signals \"this is from someone who takes their work seriously.\" Your ideal client is a professional. They make a split-second judgment about your brand before they read a single word. Make sure that judgment works in your favor.")

    # YOUR AD COPY
    add_subsection("YOUR AD COPY")

    add_checkbox("Your hook names your ideal client's exact situation — not a vague pain point.")
    add_body("The first line of your ad copy has one job: make the right person stop and think \"how did she know?\" That only happens when you name something specific — not a feeling, not a goal, not a category of problem. A specific situation they are in right now today.")
    add_practice_block("The difference in practice:", "\"Struggling to get more clients?\" — This is so broad it applies to every business owner on the platform. Nobody stops for it because nobody feels specifically seen by it.\n\"You're spending money on Meta ads. Leads are coming in. But booked calls? Still barely any.\" — This only resonates with someone who is currently running Meta ads, currently getting leads, and currently frustrated that those leads aren't booking. Everyone else scrolls past. The right person stops cold. That specificity is the filter.")

    add_checkbox("Your copy speaks to where your ideal client already is — not where you want them to be.")
    add_body("One of the most common mistakes in ad copy is writing to the version of your ideal client who already understands why they need your solution. Your actual ideal client is still in the problem. They're frustrated, confused, and slightly skeptical. Your copy needs to meet them exactly where they are — name what they're experiencing, validate that it makes sense given what they've been trying, and then introduce a new way of seeing the problem.")
    add_practice_block("The difference in practice:", "\"Ready to finally build a system that books clients on autopilot?\" speaks to someone who already believes a system is the answer. But most of your ideal clients haven't gotten there yet. They're still wondering if it's their offer, their pricing, or their niche. Copy that says \"You've tweaked your audience. Tested new creatives. Adjusted the budget. And your calendar looks exactly the same\" speaks to where they actually are. Meet them there first. Then show them a different way of looking at it.")

    add_checkbox("Your copy includes specific proof — not vague claims.")
    add_body("\"I help service providers get more clients\" means nothing to someone who has heard that sentence from a hundred different people. Specific numbers — especially a before and after story with real context — are credible in a way that general statements never are.")
    add_practice_block("The difference in practice:", "\"I help coaches build systems that get them booked consistently\" is a claim. \"I spent $544 on lead ads, got 244 leads, and booked zero calls. Then I fixed 4 things in my system. My next campaign: 86 leads, 16 booked calls, $2 per lead, 2 weeks\" is proof. The claim asks your ideal client to trust you. The proof gives them a reason to. One requires faith. The other requires nothing — the numbers speak for themselves.")

    # YOUR CTA
    add_subsection("YOUR CTA")

    add_checkbox("Your call to action tells them exactly what to do and exactly what they'll get.")
    add_body("\"Learn more\" is not a CTA. It tells someone what to do but not what they'll get. \"Download now\" tells them what to do but not why it's worth doing. A CTA that converts tells them both — the action and the specific outcome of taking it.")
    add_practice_block("The difference in practice:", "\"Download\" tells them the action, not the value. \"Download the free guide that shows you the 4 reasons your Meta ads aren't booking calls\" tells them the action AND exactly what they're getting AND who it's for. The more specific you are about what happens when they click, the more the right person feels compelled to click it. Vague CTAs create hesitation. Specific CTAs create momentum.")

    add_checkbox("Your CTA matches the temperature of a cold audience.")
    add_body("Cold traffic — people who have never heard of you — will not book a call directly from an ad. The commitment is too large and the trust isn't there yet. Every CTA needs to match the level of trust that exists at that moment in the relationship.")
    add_practice_block("The temperature scale in practice:", "Cold traffic: Download a free resource, watch a short video. Warm traffic (they've been in your world for a few days): Book a free call, join a challenge. Hot traffic (they've read your content, consumed your emails, feel like they know you): Buy, apply, enroll.")
    add_body("If your ad is going to cold traffic and your CTA is asking them to book a call or buy something, you are skipping two stages of trust-building and your conversion rate will reflect that. Your CTA should ask for the smallest possible commitment that still moves them into your world — because once they're in your world, you have the ability to build the trust that leads to a call.")

    story.append(PageBreak())

    # ════════════════════ STAGE 2: BOOKED ════════════════════

    add_stage(
        "STAGE 2: BOOKED",
        "Turning a lead into a booked call — automatically, without you involved",
        "This is the stage where most service providers leak the most leads. They have an ad that works, they're getting opt-ins, and they assume the next step is to follow up manually — send a DM, shoot an email, reach out personally. And sometimes that works. But it doesn't scale, it doesn't run while you're with clients, and it makes your booking rate entirely dependent on how much energy you have that day.\n\nThe Booked stage is about building a pathway so intentional and so specific that the right lead moves from \"I just downloaded this\" to \"I just booked a call\" without you touching anything."
    )

    # YOUR OPT-IN PAGE
    add_subsection("YOUR OPT-IN PAGE")

    add_checkbox("Your opt-in page has one headline, one offer, and one form — nothing else.")
    add_body("Every element on your opt-in page that isn't the headline, the offer, or the form is a distraction that reduces your conversion rate. No navigation menu. No links to other pages. No multiple offers. One page, one decision, one action.")
    add_practice_block("What this looks like in practice:", "If someone can do anything on your opt-in page other than submit their name and email — click a link, navigate to another page, read your blog — your opt-in page has too much on it. The moment you give someone more than one thing to click, you've introduced a fork in the road. And forks reduce conversions because some people will always take the other path. Remove every fork. One road, one destination.")

    add_checkbox("Your opt-in page headline matches your ad copy exactly.")
    add_body("When someone clicks your ad and lands on your opt-in page, the first thing they see should be a direct continuation of what made them click in the first place. If the language shifts — even slightly — there's a moment of confusion where the reader wonders if they're in the right place. That moment of confusion is enough for some people to leave.")
    add_practice_block("What this looks like in practice:", "Your ad says \"4 fixes to book more calls from your Meta ads.\" Your opt-in page headline says \"Download My Free Marketing Guide.\" That disconnect — from specific to generic — breaks the momentum the ad created. The reader was primed for something specific and landed somewhere vague. Your headline should feel like the next sentence of your ad, not the beginning of a new conversation.")

    add_checkbox("Your opt-in page is mobile-optimized and loads in under 3 seconds.")
    add_body("More than half of your ad traffic will land on your opt-in page from a mobile device. If your page isn't built for mobile first — small text, hard-to-tap form fields, slow load time — you are losing leads you already paid for before they even see your offer. Check your page on your own phone right now. If you have to pinch to zoom, something is wrong.")

    # YOUR BOOKING PAGE
    add_subsection("YOUR BOOKING PAGE")

    add_checkbox("Your booking page speaks to the real reason they downloaded your lead magnet — not the surface-level reason.")
    add_body("This is the piece that separates a booking page that occasionally gets clicks from a booking page that consistently converts — and it's the one almost nobody gets right.")
    add_body("Here's the principle: your ideal client didn't download your lead magnet because they wanted a PDF. They downloaded it because they're experiencing a specific, painful problem and they're hoping this is the thing that finally helps them understand it. Your booking page's job is to name that real reason out loud — to go one layer deeper than the surface-level topic of the freebie and speak to what's actually driving the frustration.")
    add_practice_block("What this looks like in practice:", "A booking page that says \"Book a Free Strategy Call\" with a Calendly embed is asking someone to trust you with their time before you've given them any reason to. A booking page that says \"I know you didn't download this guide just because you wanted tips on Meta ads. The real reason you downloaded it is because you're tired of spending money on ads that aren't turning into calls — and you're starting to wonder if this is ever going to work for you. That's exactly why I want to get on a call with you\" — that page makes the reader feel like you've been reading their mind. And when someone feels understood, booking a call with you feels like relief, not a risk.")

    add_checkbox("Your booking page pre-qualifies who should book — and makes clear who shouldn't.")
    add_body("Your booking page should be honest about who the call is for and who it isn't. Not everyone who downloads your lead magnet is the right person for your offer — and taking calls with the wrong people wastes your time, lowers your close rate, and drains your energy.")
    add_practice_block("What this looks like in practice:", "\"This call is for service providers who already have a proven offer and are ready to invest in building a system — not for those still figuring out what they sell.\" That one sentence filters out the people who are curious and keeps the people who are ready. You'll get fewer bookings — and dramatically better ones. Your show rate goes up. Your close rate goes up. Your energy after calls goes up. Pre-qualification isn't gatekeeping. It's protecting your calendar so that every call you take has a real chance of becoming a client.")

    add_checkbox("Your booking page removes all friction from the actual booking process.")
    add_body("Once someone decides they want to book, getting on your calendar should take no more than 2-3 clicks. No creating an account. No logging into a third-party platform. No filling out a long intake form before they can even see your availability.")
    add_practice_block("What to audit right now:", "Click through your own booking process as if you're a new lead. Count every step between \"I want to book\" and \"I am booked.\" If there are more than three steps, identify which ones can be removed or simplified. Every extra step is a place where a qualified, interested person can change their mind, get distracted, or decide it's too much work. Make it as frictionless as possible — because you already did the hard work of getting them to this page.")

    # YOUR BOOKING CONFIRMATION PAGE
    add_subsection("YOUR BOOKING CONFIRMATION PAGE")

    add_checkbox("Your confirmation page affirms that booking the call was the right decision.")
    add_body("The moment someone books a call with a stranger, a small voice in their head says \"wait — did I just make a mistake?\" This is normal. It happens to everyone. Your confirmation page's job is to immediately and specifically silence that voice — not with hype, but with warmth and clarity.")
    add_practice_block("What this looks like in practice:", "\"Your call is confirmed. You'll receive a calendar invite shortly.\" does nothing to address the doubt. It just confirms the logistics. \"You just did something most people keep putting off. That decision matters — and I'm going to make sure this call is worth your time\" does something completely different. It validates the decision they just made and sets a tone of mutual investment.")

    add_checkbox("Your confirmation page builds anticipation for the call — not just logistics.")
    add_body("Your show rate is determined largely by how excited someone is about the call between the moment they book and the moment it happens. A confirmation page that only gives them a Zoom link gives them nothing to look forward to. A confirmation page that tells them what the call will reveal, what to think about beforehand, and what's possible on the other side of the conversation gives them a reason to show up with their full attention.")
    add_practice_block("What to include on your confirmation page:", "Tell them specifically what you're going to cover on the call. Tell them one thing to think about or prepare so they arrive having already engaged with the topic. Tell them what people typically walk away with. Each of these things does one thing: it makes the call feel real and valuable before it happens. And when a call feels real and valuable, people show up for it.")

    story.append(PageBreak())

    # ════════════════════ STAGE 3: PAID ════════════════════

    add_stage(
        "STAGE 3: PAID",
        "Nurturing your list, recovering the leads who didn't book, and making sure every call converts",
        "Most service providers think their job is done once someone opts in or books a call. It isn't. The Paid stage is the system that runs in the background — quietly warming your list, recovering the leads who weren't ready to book on day one, and making sure the calls that do happen end in a clear next step. Without this stage, you're leaving the majority of your ad spend on the table every single month."
    )

    # YOUR WELCOME EMAIL SEQUENCE
    add_subsection("YOUR WELCOME EMAIL SEQUENCE")
    add_body("The welcome sequence is the most important emails you will ever send to a lead — because they are the emails that arrive when that lead is the most interested they will ever be in you. The window between \"I just opted in\" and \"I've moved on with my life\" is small. Your welcome sequence is what keeps you in the conversation during that window.")

    add_checkbox("Email 1 delivers the lead magnet immediately and opens a two-way conversation.")
    add_body("This email goes out the moment someone opts in — not an hour later, not the next morning. The moment they submit their information, your lead magnet should be in their inbox. Immediacy signals professionalism and respects the micro-commitment they just made.")
    add_body("But delivery is only half the job. The other half is opening a dialogue. This email should invite a reply — ask them what they're most hoping the resource helps them with, or what specific challenge they're dealing with right now. The leads who reply to this email are telling you they're engaged. They're warm. They're the ones most likely to book a call. Make it easy and natural for them to talk to you from the very first interaction.")

    add_checkbox("Email 2 reframes the problem — and makes it clear it's not a \"you\" problem.")
    add_body("By day two your lead has had time to sit with their situation. And in that space, doubt often moves in. They start wondering if their niche is too crowded, if their offer isn't good enough, if they're just not the type of person who's good at marketing. This story — \"maybe the problem is me\" — is the story that keeps them stuck.")
    add_body("Email 2 interrupts that story directly. It validates that what they're experiencing is real and common, and it makes clear that the problem has nothing to do with their ability or their effort. It's a systems problem. They've been running pieces without a complete system. That reframe — from personal failure to structural gap — is what shifts a lead from feeling defeated to feeling solvable. And feeling solvable is what makes them ready to take the next step.")

    add_checkbox("Email 3 describes their daily experience so accurately they feel like you've been watching them.")
    add_body("Email 3 is not a pitch. It's a mirror. It names the cycle — the inconsistency, the unpredictability, the exhaustion of having results that depend entirely on how present they were that week. It describes what it feels like to check their calendar on a Monday and not know whether this week will be full or empty. It names the mental load of trying to stay visible while also serving existing clients.")
    add_body("The more precisely you can describe their daily experience — not the big-picture problem but the small, specific, lived moments — the more trust you build. Because precision signals understanding. And understanding is what makes a stranger feel like the right person to work with.")

    add_checkbox("Email 4 asks the question that makes the cost of inaction personal — then invites them to book.")
    add_body("This is where the invitation happens. But it doesn't lead with \"book a call.\" It leads with a question that makes the reader sit with the cost of staying where they are. Something like: \"If this problem were no longer an issue — if your calendar was consistently full without you having to chase or post or guess — what would that change for you?\"")
    add_body("That question does the emotional work before the CTA does the logical work. By the time they see your booking link, they've already answered the question in their own head. They know what changes. They know what it costs to keep waiting. The booking link becomes the obvious next step — not a pitch they have to be convinced by.")

    # YOUR ONGOING EMAIL STRATEGY
    add_subsection("YOUR ONGOING EMAIL STRATEGY")
    add_body("Once your welcome sequence ends, your leads don't disappear — but your relationship with them can if you go silent. The leads who didn't book during the welcome sequence aren't gone. They're waiting. They're watching. They're deciding whether you're consistent enough, credible enough, and relevant enough to trust with a real conversation. Your ongoing emails are what answer that question week after week.")

    add_checkbox("Your ongoing emails teach a piece of your methodology — not just share thoughts or updates.")
    add_body("There's a difference between an email that keeps you top of mind and an email that builds authority. An email that says \"here's what I've been thinking about this week\" keeps you present. An email that says \"here's why most service providers never fix their booking problem — and what the ones who do have in common\" builds the belief that you specifically understand this problem better than anyone else.")
    add_body("Your ongoing emails should each teach one specific piece of how you think about the Self-Booking System. Not the full system — just one insight, one reframe, one piece of your methodology that your ideal client hasn't heard put that way before. Each email should leave them thinking \"I need to save this\" or \"I need to share this with someone.\" That's the email that builds the kind of trust that eventually becomes a booked call.")

    add_checkbox("Every email you send ties back to the one problem your system solves — from a different angle.")
    add_body("Consistency of topic builds authority faster than variety of topic. If every email you send — regardless of the specific subject — comes back to the same core problem (inconsistent bookings, unpredictable income, a calendar that doesn't reflect the quality of their work), your list will begin to associate you with that problem specifically. You become the person who understands that problem better than anyone.")
    add_practice_block("What this looks like in practice:", "An email about a client result — ties back to the problem. An email about a mindset shift — ties back to the problem. An email about a tactical tip — ties back to the problem. An email about something you learned this week — ties back to the problem. Every entry point is different. Every email lands in the same place. That consistency is what makes you the obvious choice when someone on your list is finally ready to act.")

    add_checkbox("You have a consistent sending cadence — and your list knows when to expect to hear from you.")
    add_body("Inconsistent email sending is one of the fastest ways to make a warm list go cold. When you disappear for two or three weeks and then send a promotional email, your list treats you like a stranger. Consistency — even if it's just once a week — keeps the relationship active. It tells your list that you show up reliably. And a service provider who shows up reliably in someone's inbox is the same kind of service provider they imagine working with.")

    # YOUR BOOKED CALL CONFIRMATION SEQUENCE
    add_subsection("YOUR BOOKED CALL CONFIRMATION SEQUENCE")
    add_body("Booking a call and showing up to that call are two different commitments separated by time, life, and second thoughts. Your confirmation sequence is what bridges the gap — keeping the call real, keeping the person excited, and making sure that when your calendar notification fires, they're already thinking about you.")

    add_checkbox("You have an automated reminder sequence that goes out before every booked call.")
    add_body("At minimum: one reminder 24 hours before and one reminder 1 hour before. These are not optional. People are busy. Life happens between the moment they book and the moment the call is supposed to start. A reminder sequence doesn't just prevent no-shows — it re-enrolls the person in the decision they made when they booked. Each reminder is another opportunity to remind them why they said yes.")

    add_checkbox("Your reminders re-sell the call — they don't just confirm the logistics.")
    add_body("\"This is a reminder that your call is tomorrow at 2pm. Here is the Zoom link.\" is a logistics email. It confirms the appointment. It does nothing to increase the likelihood that someone shows up engaged and ready to make a decision.")
    add_practice_block("What a re-enrollment reminder looks like:", "\"Tomorrow we're going to look at exactly what's keeping your calendar inconsistent and map out what actually needs to change. Come ready to be honest about where things are right now — the more open you are, the more useful this call will be for you.\" That reminder makes them think about the call. It makes them prepare. It makes them show up with their guard down and their mind already engaged with the topic. That's the version of the call that converts.")

    # YOUR CALL FRAMEWORK
    add_subsection("YOUR CALL FRAMEWORK")

    add_checkbox("You have a clear structure for how your calls run — from open to close.")
    add_body("A call framework is not a script. You're not reading lines. It's a sequence of four conversations designed to move naturally from understanding someone's situation to presenting your offer in a way that feels like a conclusion rather than a pitch.")
    add_body("<b>A strong call framework moves through four phases — in this order:</b>")
    add_body("<b>Phase 1 — Understand their situation.</b> Where are they right now? What have they tried? What's not working and for how long?")
    add_body("<b>Phase 2 — Quantify the cost of the problem.</b> What is staying here actually costing them — in revenue, in time, in the mental weight of inconsistency? This is where the questions that make the cost personal live. Not \"what are your goals\" but \"what has this cost you over the last 6 months?\"")
    add_body("<b>Phase 3 — Present the solution.</b> Now that they've articulated the problem and felt its weight, you show them what a different outcome looks like and how your offer creates it. At this point in the call, your offer doesn't feel like a pitch. It feels like an answer.")
    add_body("<b>Phase 4 — Handle what comes up.</b> Objections, questions, hesitation. This phase isn't about overcoming — it's about understanding. What's missing? What didn't land? What concern is underneath the \"I need to think about it\"? Curiosity here is more powerful than any closing technique.")
    add_body("Without this structure, calls meander. You cover what comes up instead of what matters. Objections catch you off guard. The close feels like a pivot rather than a conclusion. With it, every call ends in one of two places: a clear yes, or a clear no. Both are good outcomes. The one you're trying to avoid is \"I'll think about it\" — which almost never turns into a yes.")

    add_checkbox("Your framework includes questions that reveal the real cost of the problem — not just the surface symptoms.")
    add_body("Most discovery calls stay at the surface. \"What are your goals?\" \"What have you tried?\" \"What's your budget?\" These are fine questions but they don't move anyone toward a decision. The questions that actually shift the energy of a call are the ones that make the cost of the problem personal, specific, and time-sensitive.")
    add_practice_block("Questions that do this work:", "\"What has this inconsistency cost you over the last 6 months — in revenue, in time, in the mental energy of not knowing what next month looks like?\" \"If nothing changes in the next 90 days, where does that leave you?\" \"How long have you been trying to solve this on your own?\"")
    add_body("These questions aren't manipulative. They're honest. They help the person on the other side of the call articulate something they've been feeling but haven't said out loud. And when someone says it out loud, they own it in a way they didn't before. That ownership is what makes a decision possible.")

    add_checkbox("You know how to handle the most common objections before they come up.")
    add_body("\"I need to think about it.\" \"I need to talk to my partner.\" \"I don't have the budget right now.\" These aren't surprises — they're patterns. Every service provider hears the same three or four objections on almost every single call. If you don't have a thoughtful, honest response prepared for each one, you'll either push too hard or fold too quickly. Both responses cost you clients.")
    add_body("The goal is not to overcome objections. It's to understand them. \"I need to think about it\" almost always means \"I'm not convinced this is the right solution for my specific situation.\" The right response isn't \"what specifically do you need to think about?\" in a salesy way — it's genuine curiosity about what's missing. What question didn't get answered? What concern didn't get addressed? When you approach objections with curiosity instead of pressure, qualified conversations stay alive long enough to become a yes.")

    story.append(PageBreak())

    # ════════════════════ RESULTS SECTION ════════════════════

    story.append(GradientBar(content_width, 4))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Now Look At Your Results", s['h2_center']))
    story.append(Spacer(1, 4))

    add_body("Go back through the checklist. Count every item you marked NO.")
    add_body("But before you look at that number, I want you to sit with something first.")
    add_body("Every NO on this checklist is a place where a real person — someone who clicked your ad, felt something, and raised their hand — fell through the cracks. Not because they weren't the right person. Not because your offer wasn't right for them. But because the system wasn't there to catch them.")
    add_body("<b>Every NO is a lead you paid for that didn't become a conversation.</b>")
    add_body("<b>Every NO is a conversation that didn't become a booked call.</b>")
    add_body("<b>Every NO is a booked call that didn't happen — and a client you didn't get to serve.</b>")
    add_body("That's what's been accumulating quietly in the background while you've been tweaking your ad creative and wondering why the calendar isn't filling up.")

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Now look at your number.</b>", s['body_bold']))
    story.append(Spacer(1, 8))

    # Score blocks
    story.append(ScoreBlock(
        "0-5 NO answers",
        "Your system is mostly built. The gaps are in the details — specificity of copy, depth of connection, consistency of follow-up. The Self-Booking System Course will show you how to tighten every piece until the whole system converts at the level it's capable of.",
        SOFT_GREEN, content_width
    ))
    story.append(Spacer(1, 10))
    story.append(ScoreBlock(
        "6-12 NO answers",
        "You have a foundation but significant gaps across multiple stages. You're getting some results but they're inconsistent and unpredictable — because a system with that many gaps runs inconsistently by design. The course walks you through building every missing piece in the right order so the whole thing starts working together.",
        ACCENT, content_width
    ))
    story.append(Spacer(1, 10))
    story.append(ScoreBlock(
        "13+ NO answers",
        "Your system isn't built yet. I know that number might feel overwhelming. But here's what it actually means: you haven't been failing. You've been running ads into an incomplete system and wondering why they weren't converting. Now you know exactly why. And now you know exactly what to build. That clarity is worth more than anything you could have learned from another ad tweak.",
        SOFT_RED, content_width
    ))

    story.append(Spacer(1, 16))

    # Corrected closing
    story.append(Paragraph("<b>Whatever your number — you now know what to fix first.</b>", s['body_bold']))
    add_body("If you have pieces already in place across multiple stages, don't start at the top and work down. <b>Start in Stage 2.</b> That's where most leads are lost — not because the ad failed, but because the pathway from \"I just opted in\" to \"I just booked a call\" wasn't built to catch them. Fix Stage 2 first. Then go back and tighten Stage 1. Then build out Stage 3.")
    add_body("If you're starting from scratch, find the first NO in Stage 1 and work forward from there — in order, one piece at a time, until all three stages are connected and running together.")
    add_body("That's how the Self-Booking System gets built. And now you know exactly what every piece of it is.")
    add_body("<b>The system exists. You just saw every piece of it. Now it's time to build it.</b>")

    story.append(PageBreak())

    # ════════════════════ CTAs ════════════════════

    story.append(GradientBar(content_width, 4))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Ready to build every piece?", s['cta_heading']))
    story.append(Paragraph(
        "The Self-Booking System Course walks you through setting up everything in this checklist — step by step, in the right order, with every template and walkthrough you need to go from where you are right now to a fully working booking system that pulls in qualified calls every week.",
        s['cta_body']
    ))
    story.append(Paragraph("Yes, I'm ready to build my Self-Booking System", s['cta_link']))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width=content_width, thickness=0.5, color=TAUPE_200, spaceAfter=8))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Already know you'd rather have it done for you?", s['cta_heading']))
    story.append(Paragraph(
        "If you went through this checklist and thought \"I know I need all of this but I'm not going to build it myself\" — you're not alone. Most people who finish this checklist don't lack the desire to build the system. They lack the time, the tech comfort, or the bandwidth to build it correctly while also running their business.",
        s['cta_body']
    ))
    story.append(Paragraph(
        "That's exactly what the Done-For-You Self-Booking System Install is for. My team builds every piece — your lead magnet positioning, your opt-in page, your booking page written to speak to the real reason they opted in, your confirmation page, your welcome email sequence, your reminder emails, your ads. All of it. Built, connected, and running in 30 days.",
        s['cta_body']
    ))
    story.append(Paragraph(
        "<b>You show up to the calls. We handle everything else.</b>",
        s['cta_body']
    ))
    story.append(Paragraph("Tell me more about the Done-For-You Install", s['cta_link']))

    story.append(Spacer(1, 40))
    story.append(HRFlowable(width=80, thickness=1, color=TAUPE_200, spaceAfter=12, hAlign='CENTER'))
    story.append(Paragraph("Perfectly Made Marketing | All Rights Reserved", s['copyright']))

    # ── BUILD ──
    doc.build(story, onFirstPage=cover_footer, onLaterPages=footer_handler)
    print(f"PDF created: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
