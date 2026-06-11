/**
 * LEADS ON DEMAND — Onboarding Form Builder
 *
 * HOW TO RUN THIS:
 *   1. Go to https://script.google.com -> click "New project"
 *   2. Delete the placeholder code and paste this entire file in
 *   3. Click the Save (disk) icon
 *   4. In the function dropdown at the top, select: createLeadsOnDemandForm
 *   5. Click "Run" -> approve permissions the first time (Google will ask)
 *   6. When it finishes, open "Execution log" (View menu -> Logs) to see your
 *      form's URLs. The form will also be in your Google Drive.
 *
 * The form lives in YOUR Drive under your account. You can edit, share,
 * or move it anywhere afterward.
 */

function createLeadsOnDemandForm() {
  var form = FormApp.create('Leads on Demand — Onboarding Form');

  // ============ INTRO ============
  var intro =
    "Welcome! I'm so glad you're inside Leads on Demand.\n\n" +
    "Please complete this form as thoroughly as possible so we can prepare your list-building campaign, review your funnel, and create ads that speak to the right people. If you're unsure about anything, write \"not sure\" and we'll review it together.\n\n" +
    "A few quick notes before you start:\n\n" +
    "💻  PLEASE FILL THIS OUT ON A LAPTOP OR DESKTOP IF POSSIBLE.\n" +
    "Several questions ask for links, longer answers, and brand details. It's much easier on a bigger screen.\n\n" +
    "✍️  THE MORE DETAIL YOU GIVE ME, THE SHARPER YOUR CAMPAIGN WILL BE.\n" +
    "I'd rather you over-share than under-share. Even small context about your business, audience, or past results helps me build the right campaign for you.\n\n" +
    "🚫  PLEASE ANSWER IN YOUR OWN WORDS.\n" +
    "Do not use ChatGPT or any AI tool to generate your responses. I'm going to write ad copy and creative direction based on what you tell me here — and the more honest and personal your answers are, the better the campaign will perform.\n\n" +
    "🔒  PLEASE DO NOT SUBMIT PASSWORDS IN THIS FORM.\n" +
    "If login access is needed, I'll send secure instructions separately.\n\n" +
    "Once you submit, I'll follow up within one business day with next steps and our kickoff call.\n\n" +
    "Talk soon,\n— Bree";

  form.setTitle('Leads on Demand — Onboarding Form');
  form.setDescription(intro);
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(
    "Thanks for filling this out!\n\n" +
    "I'll review everything and reach out within one business day to schedule your kickoff call and share next steps for access to your ad account and funnel.\n\n" +
    "— Bree"
  );

  // ============ SECTION 1: BASICS ============
  form.addSectionHeaderItem()
    .setTitle('1. Basics')
    .setHelpText("Let's start with the basics so I know who I'm working with.");

  form.addTextItem()
    .setTitle('First + Last Name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Business Name')
    .setRequired(true);

  var emailItem = form.addTextItem()
    .setTitle('Email Address')
    .setRequired(true);
  emailItem.setValidation(
    FormApp.createTextValidation()
      .requireTextIsEmail()
      .setHelpText('Please enter a valid email address.')
      .build()
  );

  form.addTextItem()
    .setTitle('Website')
    .setHelpText('Please include the full URL (https://...)')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Instagram / main social media link')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Best phone number')
    .setRequired(true);

  // ============ SECTION 2: BUSINESS, OFFER + CUSTOMER JOURNEY ============
  form.addPageBreakItem()
    .setTitle('2. Your Business, Offer + Customer Journey')
    .setHelpText('Context on your business and what we are building toward.');

  form.addParagraphTextItem()
    .setTitle('Briefly describe what you do and who you help.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What paid offer are you ultimately wanting these leads to move toward?')
    .setHelpText('Include the offer name, price, short description, and sales page or booking page link if available.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Tell us a little bit about your current customer journey. How do people currently buy from you?')
    .setHelpText('Example: evergreen funnel, sales calls, applications, DM conversations, webinar, live launch, workshop, sales page, etc.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What is the main goal of this campaign?')
    .setHelpText('Example: grow my email list, test my lead magnet, get more qualified leads, build a warm audience before a launch, etc.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Are there any important dates, launches, workshops, or promotions coming up that we should know about?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('What would make this 30-day sprint feel successful to you?')
    .setRequired(true);

  // ============ SECTION 3: LEAD MAGNET + FUNNEL ============
  form.addPageBreakItem()
    .setTitle('3. Your Lead Magnet + Funnel')
    .setHelpText('Tell me about the lead magnet and the path connected to it.');

  form.addMultipleChoiceItem()
    .setTitle('Do you already have a lead magnet ready to promote?')
    .setChoiceValues([
      'Yes',
      'No, I purchased the Funnel Add-On',
      'I have an idea, but it still needs to be created'
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle('What is the name / title of your lead magnet?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('What does your lead magnet help people do or understand?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Please upload or link your lead magnet.')
    .setHelpText('If you have two lead magnets you want to test, share both here.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Why do you believe this lead magnet is connected to your paid offer?')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Please share your opt-in page link.')
    .setRequired(false);

  form.addTextItem()
    .setTitle('Please share your thank-you page link.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('What happens after someone opts in?')
    .setHelpText('Example: they receive a welcome email, nurture sequence, invite to book a call, webinar invitation, sales page, etc.')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Do you have a welcome or nurture email sequence connected to this lead magnet?')
    .setChoiceValues([
      'Yes',
      'No',
      'Not yet',
      "I'd like recommendations",
      'I purchased the Funnel Add-On'
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('If yes, please paste or link the emails.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Are there any existing issues with your current funnel that you want us to know about?')
    .setHelpText('Example: low opt-in rate, tech issues, email delivery issues, people opting in but not booking, etc.')
    .setRequired(false);

  // ============ SECTION 4: FUNNEL ADD-ON CLIENTS ONLY ============
  form.addPageBreakItem()
    .setTitle('4. Funnel Add-On Clients Only')
    .setHelpText('Skip this section if you did not purchase the Funnel Add-On. If you did, please answer the questions below.');

  form.addCheckboxItem()
    .setTitle('What do you need us to create?')
    .setChoiceValues([
      'Lead magnet',
      'Opt-in page',
      'Thank-you page',
      'Email platform / CRM setup',
      'All of the above'
    ])
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('What is your lead magnet idea?')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('What type of lead magnet would you prefer?')
    .setChoiceValues([
      'Checklist',
      'PDF guide',
      'Workbook',
      'Template',
      'Swipe file',
      'Quiz',
      'Free training',
      "Not sure — I'd like your recommendation"
    ])
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Where would you like the funnel built?')
    .setChoiceValues([
      "Perfectly Made Marketing's custom CRM",
      'GHL',
      'Systeme.io',
      'Other compatible platform',
      'Not sure'
    ])
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('If using your own platform, please provide the platform name and add hello@perfectlymademarketing.com as an admin/team member.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Please upload or link any brand colors, fonts, logo, photos, or images you want used.')
    .setHelpText('You can also share the link of your brand guide or a Google Drive folder that houses all of these items in one place.')
    .setRequired(false);

  // ============ SECTION 5: AUDIENCE + MESSAGING ============
  form.addPageBreakItem()
    .setTitle('5. Your Audience + Messaging')
    .setHelpText('Help me understand who your ideal client is and how to speak to them.');

  form.addParagraphTextItem()
    .setTitle('Who is your ideal client for this campaign?')
    .setHelpText('Include niche, industry, stage of business/life, pain points, desires, and what makes them a good fit.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What makes someone a qualified lead for your business?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Who is not a good fit for your business or offer?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What are 3–5 Facebook pages, Instagram accounts, podcasts, speakers, authors, brands, or businesses your ideal client follows or pays attention to?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('How would you describe your brand voice?')
    .setHelpText('Example: warm, bold, faith-led, funny, polished, direct, nurturing, luxury, simple, etc.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Are there any words, phrases, claims, or messaging angles you do not want us to use?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Are there any words, phrases, topics, or messaging angles you love and want us to include?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Do you have any existing content, testimonials, posts, or ads we can reference for messaging?')
    .setHelpText('Please link them here.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Have you seen any ads recently that made you stop scrolling?')
    .setHelpText('Links or descriptions are both fine.')
    .setRequired(false);

  // ============ SECTION 6: META ADS, BUDGET + ACCESS ============
  form.addPageBreakItem()
    .setTitle('6. Meta Ads, Budget + Access')
    .setHelpText('Tell me about your Meta Ads setup and budget.');

  form.addMultipleChoiceItem()
    .setTitle('Do you currently have a Meta Business Manager?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Do you currently have a Meta ad account?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Is your Meta ad account active and in good standing?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Have you run Meta ads before?')
    .setChoiceValues(['Yes', 'No'])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('If yes, what has your experience been like?')
    .setHelpText('Example: what worked, what didn\'t, average cost per lead, lead quality, issues you ran into, etc.')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Do you have a Meta Pixel installed on your website or landing page?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Do you have Conversions API set up?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('What daily ad budget do you want to start with?')
    .setChoiceValues([
      '$15/day for one lead magnet',
      '$30/day for two lead magnets',
      'More than $30/day',
      "I'd like your recommendation"
    ])
    .setRequired(true);

  // ============ SECTION 7: FINAL QUESTIONS ============
  form.addPageBreakItem()
    .setTitle('7. Final Questions')
    .setHelpText("Almost done. A few last things so I know what matters most to you.");

  form.addParagraphTextItem()
    .setTitle('What questions do you want to make sure we cover on your kickoff call?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Is there anything else you want me to know before we get started?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('What would make working with us a memorable experience for you?')
    .setRequired(false);

  // ============ DONE — LOG URLs ============
  Logger.log('====================================================');
  Logger.log('YOUR FORM IS READY!');
  Logger.log('====================================================');
  Logger.log('Shareable link (send this to clients):');
  Logger.log(form.getPublishedUrl());
  Logger.log('');
  Logger.log('Edit link (for you to edit the form):');
  Logger.log(form.getEditUrl());
  Logger.log('====================================================');
}
