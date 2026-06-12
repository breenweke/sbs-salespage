/**
 * APPLY TO WORK WITH US — Google Form Builder
 *
 * HOW TO RUN THIS:
 *   1. Go to https://script.google.com -> click "New project"
 *   2. Delete the placeholder code and paste this entire file in
 *   3. Click the Save (disk) icon
 *   4. In the function dropdown at the top, select: createApplyToWorkWithUsForm
 *   5. Click "Run" -> approve permissions the first time (Google will ask)
 *   6. When it finishes, open "Execution log" (View menu -> Logs) to see your
 *      form's URLs. The form will also be in your Google Drive.
 *
 * AFTER CREATING THE FORM:
 *   - In the form editor, open the SETTINGS gear and turn on the option
 *     "Show link to submit another response" if you want it; off by default.
 *   - To make the "Book Your Strategy Call" link clickable in the confirmation
 *     message, EDIT the BOOKING_URL constant below BEFORE running. Or you can
 *     edit the confirmation message directly in the form editor after creation.
 */

// ====================================================================
//  CONFIGURE THIS BEFORE RUNNING (paste your Calendly / Acuity / etc.)
// ====================================================================
var BOOKING_URL = 'PASTE_YOUR_BOOKING_URL_HERE';
// ====================================================================

function createApplyToWorkWithUsForm() {
  var form = FormApp.create('Apply to Work With Us — Perfectly Made Marketing');

  // ============ INTRO ============
  var intro =
    "We're so excited you're here!\n\n" +
    "We'd love to learn a little more about you, your business, your offer, and your goals for Meta ads.\n\n" +
    "This application helps us make sure we're a good fit before we hop on a call.\n\n" +
    "After you submit your answers, you'll be directed to book a strategy call with us.\n\n" +
    "🔒  This call is for business owners who are seriously interested in one of our done-for-you services. It is not a free audit, general marketing advice session, or \"pick my brain\" call.\n\n" +
    "We can't wait to learn more about you!";

  form.setTitle('Apply to Work With Us');
  form.setDescription(intro);
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);

  // ============ CONFIRMATION MESSAGE ============
  var confirmation =
    "Thank you for applying to work with Perfectly Made Marketing!\n\n" +
    "Your application has been received.\n\n" +
    "Next, please book your strategy call so we can speak to you about your business, your goals, and which service may be the best fit for you.\n\n" +
    "This call is for serious done-for-you service inquiries only. We'll use our time to determine whether we're a good fit, answer questions about our services, and talk through the best next step.\n\n" +
    "➜  Book Your Strategy Call: " + BOOKING_URL;
  form.setConfirmationMessage(confirmation);

  // ============ SECTION 1: BASICS ============
  form.addSectionHeaderItem()
    .setTitle('1. The Basics')
    .setHelpText("Let's start with how to reach you.");

  // Q1
  form.addTextItem()
    .setTitle("What's your first & last name?")
    .setRequired(true);

  // Q2 — email with validation
  var emailItem = form.addTextItem()
    .setTitle("What's your email?")
    .setRequired(true);
  emailItem.setValidation(
    FormApp.createTextValidation()
      .requireTextIsEmail()
      .setHelpText('Please enter a valid email address.')
      .build()
  );

  // Q3
  form.addTextItem()
    .setTitle('Link to your website?')
    .setHelpText('Please include the full URL (https://...)')
    .setRequired(true);

  // Q4
  form.addTextItem()
    .setTitle('Link to your main social media profile or business page?')
    .setHelpText('This can be your Instagram, Facebook page, LinkedIn, or another platform where we can learn more about your business.')
    .setRequired(true);

  // ============ SECTION 2: SERVICE INTEREST + OFFER ============
  form.addPageBreakItem()
    .setTitle('2. Your Service Interest + Offer')
    .setHelpText("Tell us what you're hoping we can help with.");

  // Q5
  form.addMultipleChoiceItem()
    .setTitle('Which service are you most interested in?')
    .setChoiceValues([
      'Leads on Demand in 30 Days',
      'Meta Ads Management',
      'Meta Ads Management + Funnel Build',
      "I'm not sure which one is the best fit yet"
    ])
    .setRequired(true);

  // Q6 — checkboxes
  form.addCheckboxItem()
    .setTitle('I want to run Meta ads for…')
    .setHelpText('Check all that apply.')
    .setChoiceValues([
      'Growing my email list',
      'Booking more qualified sales calls',
      'Filling a challenge',
      'Filling a webinar or free training',
      'Selling a course or digital offer',
      'Promoting a tripwire or low-ticket offer',
      'Retargeting warm audiences',
      'Supporting a launch',
      'Supporting an evergreen funnel',
      'Something else'
    ])
    .setRequired(true);

  // Q6 follow-up
  form.addParagraphTextItem()
    .setTitle('If something else, please explain.')
    .setRequired(false);

  // Q7
  form.addParagraphTextItem()
    .setTitle('What type of product or service do you provide?')
    .setHelpText('Please share what you sell, who you help, and any helpful links.')
    .setRequired(true);

  // Q8
  form.addMultipleChoiceItem()
    .setTitle('Is this a proven offer?')
    .setChoiceValues([
      "Yes, I know this offer sells and I'm ready to scale.",
      'Yes, but the offer, funnel, or messaging may need a few tweaks.',
      'Somewhat. I have sold it, but not consistently.',
      'No, this is a brand-new offer.'
    ])
    .setRequired(true);

  // Q9
  form.addMultipleChoiceItem()
    .setTitle('Do you have testimonials, reviews, or client results for this offer?')
    .setChoiceValues([
      'Yes',
      'A few',
      'Not yet'
    ])
    .setRequired(true);

  // ============ SECTION 3: YOUR BUSINESS CONTEXT ============
  form.addPageBreakItem()
    .setTitle('3. Your Business Context + Goals')
    .setHelpText("Help us understand where your business is right now and where you're headed.");

  // Q10
  form.addMultipleChoiceItem()
    .setTitle("What's your current ad budget or what are you planning to spend each month on ads?")
    .setChoiceValues([
      'Less than $1,500/month',
      '$1,500–$3,000/month',
      '$3,000–$5,000/month',
      '$5,000–$10,000/month',
      '$10,000+/month',
      "I'm not sure yet"
    ])
    .setRequired(true);

  // Q11
  form.addMultipleChoiceItem()
    .setTitle('Have you run Meta ads before?')
    .setChoiceValues([
      "Yes, I'm currently running ads.",
      "Yes, I've run ads in the past.",
      'No, this would be my first time.'
    ])
    .setRequired(true);

  // Q12
  form.addParagraphTextItem()
    .setTitle('How are you currently generating leads or sales?')
    .setHelpText('For example: referrals, organic content, launches, evergreen funnels, paid ads, email list, networking, DMs, etc.')
    .setRequired(true);

  // Q13
  form.addParagraphTextItem()
    .setTitle('What is your current monthly revenue and what is your monthly goal?')
    .setRequired(true);

  // Q14
  form.addParagraphTextItem()
    .setTitle('What do you feel is currently holding you back from reaching that goal?')
    .setRequired(true);

  // Q15
  form.addParagraphTextItem()
    .setTitle('What would a successful campaign look like for you and your business?')
    .setHelpText('For example: more leads, better lead quality, booked calls, sales, applications, challenge registrations, webinar sign-ups, etc.')
    .setRequired(true);

  // ============ SECTION 4: INVESTMENT + TIMING ============
  form.addPageBreakItem()
    .setTitle('4. Investment + Timing')
    .setHelpText("A few last questions before you book your call.");

  // Q16
  form.addMultipleChoiceItem()
    .setTitle('Our done-for-you services begin at:')
    .setHelpText(
      'Leads on Demand in 30 Days: $1,350, plus ad spend\n' +
      'Meta Ads Management: $2,500/month, 3-month minimum, plus ad spend\n' +
      'Meta Ads Management + Funnel Build: $3,500 first month, then $2,500/month, 4-month minimum, plus ad spend\n\n' +
      'Which best describes you?'
    )
    .setChoiceValues([
      "I'm ready to invest if we're a good fit.",
      "I'm seriously considering it and understand the investment range.",
      'I need more information, but I understand this is a paid done-for-you service.',
      "I'm not financially ready for done-for-you support yet."
    ])
    .setRequired(true);

  // Q17
  form.addMultipleChoiceItem()
    .setTitle('If we both decide this is a fit, when would you like to get started?')
    .setChoiceValues([
      'Immediately',
      'Within the next 2 weeks',
      'Within the next 30 days',
      'In 1–3 months',
      "I'm just exploring right now"
    ])
    .setRequired(true);

  // Q18
  form.addMultipleChoiceItem()
    .setTitle('Please confirm you understand this is a strategy call for serious done-for-you service inquiries only.')
    .setChoiceValues([
      "Yes, I understand and I'm seriously interested in one of your done-for-you services.",
      "I'm not sure I'm ready yet, but I understand this is not a free audit or general advice session."
    ])
    .setRequired(true);

  // ============ DONE — LOG URLs ============
  Logger.log('====================================================');
  Logger.log('YOUR APPLICATION FORM IS READY!');
  Logger.log('====================================================');
  Logger.log('Shareable link (use this on your buttons):');
  Logger.log(form.getPublishedUrl());
  Logger.log('');
  Logger.log('Edit link (for you to edit the form later):');
  Logger.log(form.getEditUrl());
  Logger.log('====================================================');
  if (BOOKING_URL === 'PASTE_YOUR_BOOKING_URL_HERE') {
    Logger.log('');
    Logger.log('⚠️  REMINDER: You did not paste a real BOOKING_URL.');
    Logger.log('   Open the form in the editor, click the Settings gear -> Presentation,');
    Logger.log('   and replace the placeholder in the confirmation message with your real');
    Logger.log('   Calendly / Acuity / TidyCal booking link.');
  }
}
