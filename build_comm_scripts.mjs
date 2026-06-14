import { createRequire } from 'module';
import { writeFileSync } from 'fs';
import { join } from 'path';
const require = createRequire(import.meta.url);
const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, ShadingType, WidthType } = require('docx');

const LP = String.raw`C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Communication_Scripts`;

const DEEP_BROWN = '36221C'; const STEEL_BLUE = '516984'; const WARM_GREY = '63645A'; const WHITE = 'FFFFFF';
const shade = c => ({ type: ShadingType.SOLID, color: c, fill: c });

const p = (text, bold = false, color = '2D2D2D') => new Paragraph({
  children: [new TextRun({ text, bold, font: 'Calibri', size: 20, color })],
  spacing: { after: 60 },
});
const sp = () => new Paragraph({ children: [new TextRun('')], spacing: { after: 80 } });
const divider = () => new Paragraph({
  children: [new TextRun({ text: '─'.repeat(80), font: 'Calibri', size: 18, color: WARM_GREY })],
  spacing: { before: 120, after: 120 },
});
const scriptBar = (n, title) => new Paragraph({
  children: [new TextRun({ text: `SCRIPT ${n} — ${title}`, bold: true, font: 'Calibri', size: 26, color: WHITE })],
  shading: shade(DEEP_BROWN),
  spacing: { before: 160, after: 80 },
});
const label = text => new Paragraph({
  children: [new TextRun({ text, bold: true, font: 'Calibri', size: 20, color: WHITE })],
  shading: shade(STEEL_BLUE),
  spacing: { before: 100, after: 60 },
});

const makeDoc = children => new Document({
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
    headers: { default: new Header({ children: [new Paragraph({ children: [new TextRun({ text: 'Property and Rent Consult | Landlord-Tenant Communication Scripts', font: 'Calibri', size: 16, color: WARM_GREY })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ children: [new TextRun({ text: '© 2026 Property and Rent Consult — For personal/internal business use only. Not for resale.', font: 'Calibri', size: 16, color: WARM_GREY })] })] }) },
    children,
  }],
});

const scripts12 = () => [
  // Cover
  new Paragraph({ children: [new TextRun({ text: 'PROPERTY AND RENT CONSULT', bold: true, font: 'Calibri', size: 32, color: WHITE })], shading: shade(DEEP_BROWN), alignment: AlignmentType.CENTER, spacing: { before: 80, after: 40 } }),
  new Paragraph({ children: [new TextRun({ text: 'LANDLORD-TENANT COMMUNICATION SCRIPTS', bold: true, font: 'Calibri', size: 26, color: WHITE })], shading: shade(DEEP_BROWN), alignment: AlignmentType.CENTER, spacing: { after: 40 } }),
  new Paragraph({ children: [new TextRun({ text: 'Core Pack — 4 Essential Scripts', font: 'Calibri', size: 22, color: WHITE })], shading: shade(STEEL_BLUE), alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  sp(),

  // SCRIPT 1
  scriptBar(1, 'RENT REMINDER NOTICE'),
  sp(),
  label('USAGE NOTES'),
  p('Send when rent is 1–7 days overdue. Use the Formal Version for written or postal delivery. Use the Short Version for WhatsApp or SMS. This is a reminder, not a legal notice — tone must remain polite. If rent remains unpaid after 14 days, escalate to a Formal Demand Letter (Script 3). Reference: Rent Act, 1963 (Act 220).'),
  sp(),
  label('FORMAL VERSION'),
  sp(),
  p('[DATE]'), sp(),
  p('Dear [TENANT NAME],'), sp(),
  p('RE: REMINDER — RENT PAYMENT DUE', true),
  sp(),
  p('We write to draw your attention to the fact that your rent for the period [PERIOD — e.g., 1st June 2026 to 30th June 2026] in the amount of GHS [AMOUNT] was due on [DUE DATE] and remains outstanding as at the date of this notice.'),
  p('We kindly request that you arrange payment of the outstanding amount within SEVEN (7) days of the date of this notice.'),
  p('If you have already made payment, please disregard this notice and forward proof of payment to us at your earliest convenience.'),
  p('Should you experience any difficulty in meeting this payment, we encourage you to contact us promptly so that we may discuss the matter. Please be aware that continued non-payment may result in further action in accordance with the Rent Act, 1963 (Act 220).'),
  sp(),
  p('Yours sincerely,'), sp(),
  p('_______________________________'),
  p('[LANDLORD / AGENT NAME]'),
  p('[PROPERTY ADDRESS]'),
  p('[PHONE] | [EMAIL]'),
  p('Date: _______________'),
  sp(),
  label('SHORT VERSION (WhatsApp / SMS)'),
  p('"Dear [Name], this is a friendly reminder that your rent of GHS [Amount] for [Period] was due on [Date]. Kindly make payment within 7 days or contact us if you need to discuss. Thank you — [Landlord/Agent Name]."'),
  divider(),

  // SCRIPT 2
  scriptBar(2, 'ROUTINE INSPECTION NOTICE'),
  sp(),
  label('USAGE NOTES'),
  p("Send at least 24–48 hours before any inspection. Under Act 220, a landlord may not enter the premises without reasonable notice except in an emergency. This notice satisfies that legal requirement. Tone must be professional and non-threatening — inspections are routine, not punitive."),
  sp(),
  label('FORMAL VERSION'),
  sp(),
  p('[DATE]'), sp(),
  p('Dear [TENANT NAME],'), sp(),
  p('RE: NOTICE OF ROUTINE PROPERTY INSPECTION — [PROPERTY ADDRESS]', true),
  sp(),
  p('We write to inform you that a routine inspection of the above-referenced premises will be conducted on [DATE] at [TIME].'),
  p('The purpose of this inspection is to assess the general condition of the property, identify any maintenance requirements, and ensure that all fixtures and fittings remain in good order. This is a scheduled routine inspection and does not imply any concern regarding your tenancy.'),
  p('We kindly request that you or a responsible adult be present during the inspection. If this date and time are not convenient, please contact us within 48 hours of this notice so that we may arrange an alternative time.'),
  p('The inspection is expected to take approximately [30–60] minutes.'),
  sp(),
  p('Yours sincerely,'), sp(),
  p('_______________________________'),
  p('[LANDLORD / AGENT NAME]'),
  p('[PROPERTY ADDRESS]'),
  p('[PHONE] | [EMAIL]'),
  p('Date: _______________'),
  sp(),
  label('SHORT VERSION (WhatsApp / SMS)'),
  p('"Dear [Name], please be informed that a routine inspection of your premises at [Address] is scheduled for [Date] at [Time]. Kindly ensure access is available. Contact us within 48 hours if this is not convenient. — [Landlord/Agent Name]."'),
];

const scripts34 = () => [
  divider(),
  // SCRIPT 3
  scriptBar(3, 'EVICTION WARNING NOTICE (FIRST FORMAL WARNING)'),
  sp(),
  label('USAGE NOTES'),
  p('This is a FIRST FORMAL WARNING — not a Quit Notice and not a court action. Use when rent is 14 or more days overdue OR when a breach of the tenancy agreement has been identified. This notice triggers a 14-day remedy period. It must be delivered in writing (physically, by email, or by registered post). DO NOT use this as a substitute for a formal Quit Notice — that is a separate document under Act 220. This script creates the paper trail required before a Quit Notice can be issued. The document contains BOTH the non-payment version and the breach version — delete the inapplicable paragraph before sending.'),
  sp(),
  label('FORMAL VERSION'),
  sp(),
  p('[DATE]'), sp(),
  p('Dear [TENANT NAME],'), sp(),
  p('RE: FORMAL WARNING — [NON-PAYMENT OF RENT / BREACH OF TENANCY AGREEMENT]', true),
  sp(),
  p('We write to you in connection with the tenancy of the premises at [PROPERTY ADDRESS], held by you under the Tenancy Agreement dated [DATE OF AGREEMENT].'),
  sp(),
  p('[SELECT AND DELETE THE INAPPLICABLE PARAGRAPH BELOW]', true, STEEL_BLUE),
  sp(),
  p('[NON-PAYMENT VERSION:]', true),
  p('As at the date of this notice, the following rent remains outstanding and unpaid:'),
  sp(),
  p('  Period:                [PERIOD]'),
  p('  Amount Due:            GHS [AMOUNT]'),
  p('  Original Due Date:     [DATE]'),
  p('  Total Outstanding:     GHS [TOTAL]'),
  sp(),
  p('[BREACH VERSION:]', true),
  p('It has come to our attention that you are in breach of Clause [CLAUSE NUMBER] of your Tenancy Agreement, specifically in that you have [DESCRIBE BREACH IN FULL].'),
  sp(),
  p('This constitutes a breach of your obligations under the Tenancy Agreement and the Rent Act, 1963 (Act 220).'),
  sp(),
  p('YOU ARE HEREBY FORMALLY WARNED that if the above [outstanding rent is not paid in full / breach is not remedied] within FOURTEEN (14) DAYS of the date of this notice, we shall be compelled to take further action, which may include the service of a formal Quit Notice and referral to the Rent Control Department in accordance with the provisions of Act 220 and L.I. 369.', true),
  sp(),
  p('We strongly urge you to address this matter immediately to avoid the inconvenience and cost of further proceedings.'),
  sp(),
  p('Yours faithfully,'), sp(),
  p('_______________________________'),
  p('[LANDLORD / AGENT NAME]'),
  p('[PROPERTY ADDRESS]'),
  p('[PHONE] | [EMAIL]'),
  p('Date: _______________'),
  sp(),
  label('SHORT VERSION (WhatsApp / SMS)'),
  p('"Dear [Name], this is a formal written warning regarding [unpaid rent of GHS [Amount] / breach of your tenancy agreement at [Address]]. You have 14 days to resolve this or further action will be taken under Act 220. Contact us urgently. — [Landlord/Agent]."'),
  divider(),

  // SCRIPT 4
  scriptBar(4, 'TENANCY RENEWAL OFFER'),
  sp(),
  label('USAGE NOTES'),
  p('Send 60–90 days before the end of the fixed term. A renewal offer is not a legal obligation — it is a courtesy and a business decision. Use this script only when the landlord WISHES to renew. If the landlord does not intend to renew, a Non-Renewal Notice is the appropriate document instead. This script includes a Tenant Acceptance section so the offer can double as a written renewal record once signed. Reference: L.I. 369 (3-month rent increase notice requirement applies if the new rent is higher).'),
  sp(),
  label('FORMAL VERSION'),
  sp(),
  p('[DATE]'), sp(),
  p('Dear [TENANT NAME],'), sp(),
  p('RE: OFFER OF TENANCY RENEWAL — [PROPERTY ADDRESS]', true),
  sp(),
  p("We write with pleasure to advise you that your tenancy of the above-referenced premises, held under the Agreement dated [ORIGINAL AGREEMENT DATE], is due to expire on [EXPIRY DATE]."),
  p('We would like to offer you the opportunity to renew your tenancy on the following terms:'),
  sp(),
  p('  New Term:              [NUMBER] [months / years] commencing [NEW START DATE]'),
  p('  New Rent:              GHS [AMOUNT] per [month / year]'),
  p('  Advance Period:        [NUMBER] [months / years]'),
  p('  Total Advance Payment: GHS [TOTAL ADVANCE AMOUNT]'),
  p('  Security Deposit:      [Existing deposit carried forward / New deposit of GHS [AMOUNT]]'),
  p('  Special Conditions:    _______________________________________________'),
  sp(),
  p('[INCLUDE THIS PARAGRAPH ONLY IF THE RENT HAS INCREASED:]', true, STEEL_BLUE),
  p('Please note that the revised rent reflects current market conditions and the cost of maintenance and upkeep of the property. In accordance with the Rent Regulations, 1964 (L.I. 369), this offer is being provided to you more than three (3) months before the proposed effective date.'),
  sp(),
  p('To accept this offer, kindly sign and return the enclosed copy of this letter by [RESPONSE DEADLINE DATE]. Failure to respond by this date may result in the property being offered to other prospective tenants.'),
  p('We value your tenancy and look forward to your continued occupation.'),
  sp(),
  p('Yours sincerely,'), sp(),
  p('_______________________________'),
  p('[LANDLORD / AGENT NAME]'),
  p('[PROPERTY ADDRESS]'),
  p('[PHONE] | [EMAIL]'),
  p('Date: _______________'),
  sp(),
  label('TENANT ACCEPTANCE'),
  p('I, [TENANT NAME], accept the renewal terms set out in this letter.'),
  sp(),
  p('Signature: _______________________________________________'),
  p('Date: _______________________________________________'),
  sp(),
  label('SHORT VERSION (WhatsApp / SMS)'),
  p('"Dear [Name], your tenancy at [Address] expires on [Date]. We would like to offer a renewal for [Term] at GHS [Rent]/month. Please respond by [Deadline]. Contact us to discuss or confirm. — [Landlord/Agent Name]."'),
];

async function main() {
  // Basic tier — scripts 1 & 2 only
  const basicDoc = makeDoc([...scripts12()]);
  writeFileSync(join(LP, 'Basic_Tier', 'PRC-Communication-Scripts-Basic.docx'), await Packer.toBuffer(basicDoc));
  console.log('Saved: Basic scripts');

  // Pro tier — all 4 scripts
  const proDoc = makeDoc([...scripts12(), ...scripts34()]);
  writeFileSync(join(LP, 'Pro_Tier', 'PRC-Communication-Scripts-Pro.docx'), await Packer.toBuffer(proDoc));
  console.log('Saved: Pro scripts');
}
main().catch(console.error);
