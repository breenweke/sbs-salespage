/**
 * CUSTOM META ADS + FUNNEL AUDIT — Google Form Builder
 *
 * HOW TO RUN THIS:
 *   1. Go to https://script.google.com → click "New project"
 *   2. Delete the placeholder code and paste this entire file in
 *   3. Click the Save (disk) icon
 *   4. In the function dropdown at the top, select: createAuditIntakeForm
 *   5. Click "Run" → approve permissions the first time (Google will ask)
 *   6. When it finishes, open "Execution log" (View menu → Logs) to see your
 *      form's URLs. The form will also be in your Google Drive.
 *
 * The form lives in YOUR Drive under your account. You can edit, share,
 * or move it anywhere afterward.
 */

function createAuditIntakeForm() {
  var form = FormApp.create('Custom Meta Ads + Funnel Audit — Intake Form');

  // ============ INTRO ============
  var intro =
    "Welcome! I'm excited to dig into your Meta ads and funnel.\n\n" +
    "Before you get started, a few quick notes:\n\n" +
    "💻  PLEASE FILL THIS OUT ON A LAPTOP OR DESKTOP IF POSSIBLE.\n" +
    "Several questions ask for links and longer answers, and it's much easier on a bigger screen.\n\n" +
    "✍️  THE MORE DETAIL YOU GIVE ME, THE SHARPER YOUR AUDIT WILL BE.\n" +
    "I'd rather you over-share than under-share. Even small context about your business, your audience, or what hasn't worked before helps me see the whole picture.\n\n" +
    "🚫  PLEASE ANSWER IN YOUR OWN WORDS.\n" +
    "Do not use ChatGPT or any AI tool to generate your responses. I'm going to walk into your ad account and funnel based on what you tell me here — and the more honest and personal your answers are, the more accurate and useful the audit will be for you.\n\n" +
    "Once you submit, I'll follow up with secure instructions for granting me access to your ad account and funnel.\n\n" +
    "Talk soon,\n— Bree";

  form.setTitle('Custom Meta Ads + Funnel Audit — Intake Form');
  form.setDescription(intro);
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(
    "Thanks for filling this out!\n\n" +
    "I'll be in touch within the next business day with secure instructions for granting me access to your ad account and funnel. Once I have everything, I'll have your audit ready within 3 business days, then we'll schedule your 45-minute Zoom call.\n\n" +
    "— Bree"
  );

  // ============ SECTION 1: BASIC INFO ============
  form.addSectionHeaderItem()
    .setTitle('1. Basic Info')
    .setHelpText("Let's start with the basics so I know who I'm working with.");

  form.addTextItem()
    .setTitle('Name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Business Name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Website')
    .setHelpText('Please include the full URL (https://...)')
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

  form.addParagraphTextItem()
    .setTitle('Instagram and Facebook social media links')
    .setHelpText('Please include both if applicable.')
    .setRequired(false);

  // ============ SECTION 2: BUSINESS + OFFER ============
  form.addPageBreakItem()
    .setTitle('2. Your Business + Offer')
    .setHelpText('A little context about your business and what your ads are promoting.');

  form.addParagraphTextItem()
    .setTitle('What do you do, and who do you serve?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What offer are your ads currently promoting?')
    .setHelpText('Please include the offer name, price, and a short description.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What is the main goal of this offer?')
    .setHelpText('Example: grow your email list, book calls, prepare for a launch, get applications, sell a paid offer, webinar sign-ups, workshop registrations, etc.')
    .setRequired(true);

  // ============ SECTION 3: CURRENT ADS ============
  form.addPageBreakItem()
    .setTitle('3. Your Current Ads')
    .setHelpText("Let's talk about what your ads are doing right now.");

  form.addMultipleChoiceItem()
    .setTitle('Are your Meta ads currently running?')
    .setChoiceValues([
      'Yes, they are currently running',
      'No, but I recently ran ads',
      'No, I do not have recent ad data'
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle('What is your current or recent daily ad budget?')
    .setHelpText('Example: $10/day, $25/day, $50/day, etc.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("What is the #1 issue you're currently experiencing with your ads?")
    .setHelpText('Example: high cost per lead, clicks but no conversions, leads not buying, low-quality leads, no sales, tracking issues, etc.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What specific campaigns, ad sets, or ads do you want me to review?')
    .setHelpText('You can list names here or say "all recent campaigns connected to this offer."')
    .setRequired(true);

  // ============ SECTION 4: FUNNEL ============
  form.addPageBreakItem()
    .setTitle('4. Your Funnel')
    .setHelpText("Now let's look at where your ads are sending people.");

  form.addParagraphTextItem()
    .setTitle('Where are your ads sending people?')
    .setHelpText(
      'Please include links to any pages connected to your ads:\n' +
      '• Opt-in page\n' +
      '• Sales page\n' +
      '• Booking page\n' +
      '• Application page\n' +
      '• Webinar/workshop page\n' +
      '• Thank-you page\n' +
      '• Checkout page (if applicable)'
    )
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('What happens after someone opts in, books, applies, or purchases?')
    .setHelpText('Briefly describe the next step they receive and the next step you want them to take.')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Do you have an email sequence connected to this funnel?')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('If yes, please share the emails below or share your login details for me to access.')
    .setHelpText('Please do NOT submit passwords in this form. I will send secure instructions separately if needed.')
    .setRequired(false);

  // ============ SECTION 5: WHAT SUCCESS LOOKS LIKE ============
  form.addPageBreakItem()
    .setTitle('5. What Success Looks Like')
    .setHelpText("Help me understand what you want to walk away with.");

  form.addParagraphTextItem()
    .setTitle('What would make this audit feel successful for you?')
    .setHelpText('Example: knowing what to fix first, understanding your numbers, improving lead quality, knowing whether to keep running ads, etc.')
    .setRequired(true);

  // ============ SECTION 6: QUESTIONS FOR BREE ============
  form.addPageBreakItem()
    .setTitle('6. Questions for Bree')
    .setHelpText("Anything specific you want us to cover, or anything I should know going in.");

  form.addParagraphTextItem()
    .setTitle('What questions do you want to make sure we cover during your audit or Zoom call?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Is there anything else you want me to know that was not mentioned inside this form?')
    .setRequired(false);

  // ============ SECTION 7: ACCESS ============
  form.addPageBreakItem()
    .setTitle('7. Access')
    .setHelpText("Almost done. Just one more question about access.");

  form.addMultipleChoiceItem()
    .setTitle('Do you need to provide login details for any funnel, landing page, or email platform for me to review?')
    .setHelpText('Please do NOT submit passwords in this form. If you answer Yes, I will send secure instructions separately.')
    .setChoiceValues(['Yes', 'No', 'Not sure'])
    .setRequired(true);

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
