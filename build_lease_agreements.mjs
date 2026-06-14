import { createRequire } from 'module';
import { writeFileSync } from 'fs';
import { join } from 'path';
const require = createRequire(import.meta.url);
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, WidthType, Header, Footer, ShadingType, BorderStyle,
  PageNumber, NumberFormat,
} = require('docx');

const BASE = String.raw`C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Ghana_Lease_Pack`;

const DEEP_BROWN = '36221C';
const STEEL_BLUE = '516984';
const WARM_GREY  = '63645A';
const LIGHT_BLUE = 'E8EEF3';
const OFF_WHITE  = 'F5EDE8';
const WHITE      = 'FFFFFF';

const shade = c => ({ type: ShadingType.SOLID, color: c, fill: c });

const p = (text, opts = {}) => new Paragraph({
  children: [new TextRun({ text, font: 'Calibri', size: 20, color: '2D2D2D', ...opts })],
  spacing: { after: 60 },
});
const pb = (text, color = DEEP_BROWN) => new Paragraph({
  children: [new TextRun({ text, bold: true, font: 'Calibri', size: 20, color })],
  spacing: { after: 60 },
});
const h1 = text => new Paragraph({
  children: [new TextRun({ text, bold: true, font: 'Calibri', size: 26, color: DEEP_BROWN })],
  spacing: { before: 200, after: 100 },
});
const h2 = text => new Paragraph({
  children: [new TextRun({ text, bold: true, font: 'Calibri', size: 22, color: STEEL_BLUE })],
  spacing: { before: 160, after: 80 },
});
const sp = () => new Paragraph({ children: [new TextRun('')], spacing: { after: 80 } });
const field = label => new Paragraph({
  children: [
    new TextRun({ text: `${label}: `, bold: true, font: 'Calibri', size: 20, color: '2D2D2D' }),
    new TextRun({ text: '_'.repeat(50), font: 'Calibri', size: 20, color: '2D2D2D' }),
  ],
  spacing: { after: 60 },
});
const check = label => new Paragraph({
  children: [new TextRun({ text: `[ ] ${label}`, font: 'Calibri', size: 20, color: '2D2D2D' })],
  spacing: { after: 40 },
});

const coverBar = (title, sub, legal) => [
  new Paragraph({
    children: [new TextRun({ text: 'PROPERTY AND RENT CONSULT', bold: true, font: 'Calibri', size: 28, color: WHITE })],
    alignment: AlignmentType.CENTER,
    shading: shade(DEEP_BROWN),
    spacing: { before: 80, after: 40 },
  }),
  new Paragraph({
    children: [new TextRun({ text: title, bold: true, font: 'Calibri', size: 32, color: WHITE })],
    alignment: AlignmentType.CENTER,
    shading: shade(DEEP_BROWN),
    spacing: { after: 40 },
  }),
  new Paragraph({
    children: [new TextRun({ text: sub, font: 'Calibri', size: 22, color: WHITE })],
    alignment: AlignmentType.CENTER,
    shading: shade(STEEL_BLUE),
    spacing: { after: 40 },
  }),
  new Paragraph({
    children: [new TextRun({ text: legal, font: 'Calibri', size: 18, color: WHITE })],
    alignment: AlignmentType.CENTER,
    shading: shade(STEEL_BLUE),
    spacing: { after: 120 },
  }),
];

const sectionBar = text => new Paragraph({
  children: [new TextRun({ text, bold: true, font: 'Calibri', size: 22, color: WHITE })],
  shading: shade(STEEL_BLUE),
  spacing: { before: 120, after: 60 },
});

const tblHeader = (cells, widths) => new TableRow({
  children: cells.map((t, i) => new TableCell({
    children: [new Paragraph({ children: [new TextRun({ text: t, bold: true, font: 'Calibri', size: 18, color: WHITE })], alignment: AlignmentType.CENTER })],
    shading: shade(DEEP_BROWN),
    width: { size: widths[i], type: WidthType.DXA },
  })),
  tableHeader: true,
});
const tblRow = (cells, widths, bg = WHITE) => new TableRow({
  children: cells.map((t, i) => new TableCell({
    children: [new Paragraph({ children: [new TextRun({ text: t, font: 'Calibri', size: 18, color: '2D2D2D' })] })],
    shading: shade(bg),
    width: { size: widths[i], type: WidthType.DXA },
  })),
});

const execBlock = () => [
  sectionBar('EXECUTION'),
  sp(),
  pb('SIGNED by the LANDLORD:'),
  field('Full Name'), field('Signature'), field('Date'),
  field('Witness Name'), field('Witness Signature'),
  sp(),
  pb('SIGNED by the TENANT:'),
  field('Full Name'), field('Signature'), field('Date'),
  field('Witness Name'), field('Witness Signature'),
];

const standardSchedules = (extras = []) => [
  sp(),
  sectionBar('SCHEDULE 1 — FIXTURES AND FITTINGS INVENTORY'),
  p('(Attach completed move-in inspection checklist)'),
  new Table({
    width: { size: 9200, type: WidthType.DXA },
    rows: [
      tblHeader(['Item', 'Condition at Commencement', 'Condition at Vacation', 'Notes'], [2300, 2300, 2300, 2300]),
      ...[1,2,3,4,5].map((_, i) => tblRow(['', '', '', ''], [2300, 2300, 2300, 2300], i%2===0 ? LIGHT_BLUE : WHITE)),
    ],
  }),
  sp(),
  sectionBar('SCHEDULE 2 — SPECIAL CONDITIONS'),
  p('1. ' + '_'.repeat(80)),
  p('2. ' + '_'.repeat(80)),
  p('3. ' + '_'.repeat(80)),
  ...extras,
];

const makeDoc = (headerTitle, children) => new Document({
  sections: [{
    properties: {
      page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } },
    },
    headers: {
      default: new Header({ children: [new Paragraph({ children: [new TextRun({ text: `Property and Rent Consult | ${headerTitle}`, font: 'Calibri', size: 16, color: WARM_GREY })] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ children: [new TextRun({ text: '© 2026 Property and Rent Consult — For personal/internal business use only. Not for resale.', font: 'Calibri', size: 16, color: WARM_GREY })] })] }),
    },
    children,
  }],
});

// ── PARTIES BLOCK (residential) ─────────────────────────────────────────────
const residentialParties = () => [
  sectionBar('PARTIES'),
  p('TENANCY AGREEMENT made this ______ day of ________________, ________'),
  sp(),
  pb('LANDLORD'),
  field('Full Name'), field('Ghana Card / Passport No.'), field('Contact Address'), field('Phone'), field('Email'),
  p('(hereinafter referred to as "the Landlord")'),
  sp(),
  pb('AND'),
  sp(),
  pb('TENANT'),
  field('Full Name'), field('Ghana Card / Passport No.'), field('Employer / Business'), field('Contact Address'), field('Phone'), field('Email'),
  p('(hereinafter referred to as "the Tenant")'),
  sp(),
  pb('PREMISES'),
  field('Property Address'), field('Unit / Apt No.'), field('Nearest Landmark'), field('Ghana Post GPS'),
  p('Property Type:'), check('Apartment'), check('House'), check('Flat'), check('Other: _______________'),
];

// ── RECITALS ────────────────────────────────────────────────────────────────
const recitals = () => [
  sectionBar('RECITALS'),
  p('WHEREAS the Landlord is the owner or authorised agent of the Premises and is desirous of letting the same to the Tenant on the terms herein;'),
  p('AND WHEREAS the Tenant is desirous of taking the Premises on those terms;'),
  pb('NOW THEREFORE the parties agree as follows:'),
];

// ── STANDARD CLAUSES 4–11 ────────────────────────────────────────────────────
const standardClauses4to11 = () => [
  h1('CLAUSE 4 — SECURITY DEPOSIT'),
  p('4.1  The Tenant shall pay a security deposit of GHS _________________ on signing, held by the Landlord as security against:'),
  p('     (a) unpaid rent;'), p('     (b) damage beyond fair wear and tear;'), p('     (c) any other breach of this Agreement.'),
  p('4.2  The deposit shall not be applied as rent.'),
  p('4.3  Within fourteen (14) days of the Tenant vacating, the Landlord shall either return the deposit in full or provide a written itemised statement of deductions with supporting evidence and return the balance.'),
  p('4.4  Deposit disputes may be referred to the Rent Control Department.'),

  h1('CLAUSE 5 — UTILITIES AND SERVICE CHARGES'),
  p("5.1  The following are the Tenant's direct responsibility:"),
  check('Electricity (ECG / NEDCo)'), check('Water (Ghana Water Company / Local Supply)'), check('Internet / Cable Television'), check('Refuse Collection'),
  p("5.2  The following are included in rent or are the Landlord's responsibility: _______________________________________________"),
  p('5.3  Service charges of GHS _____________ per month are payable by the Tenant for: _______________________________________________'),
  p('5.4  The Tenant shall not tamper with or interfere with any utility meter or connection.'),

  h1('CLAUSE 6 — LANDLORD OBLIGATIONS'),
  p('6.1  The Landlord shall:'),
  p('     (a) put and keep the Premises in a reasonable state of repair at the commencement of the tenancy;'),
  p('     (b) ensure the Premises are structurally sound and fit for habitation;'),
  p('     (c) carry out structural repairs and external maintenance within a reasonable time of written notification by the Tenant;'),
  p("     (d) not interfere with the Tenant's quiet enjoyment of the Premises;"),
  p('     (e) give at least twenty-four (24) hours\' written notice before entering the Premises for inspection or repair, except in emergency;'),
  p('     (f) issue a written receipt for every payment of rent or deposit.'),

  h1('CLAUSE 7 — TENANT OBLIGATIONS'),
  p('7.1  The Tenant shall:'),
  p('     (a) pay rent on the dates and in the manner agreed herein;'),
  p('     (b) keep the Premises clean, tidy, and in good condition;'),
  p('     (c) not carry out any structural alteration without prior written consent of the Landlord;'),
  p('     (d) not sublet, assign, or transfer the Premises without prior written consent of the Landlord;'),
  p('     (e) not use the Premises for any unlawful purpose or in a manner constituting a nuisance to neighbours;'),
  p('     (f) permit the Landlord or their authorised agent to enter and inspect at reasonable times with twenty-four (24) hours\' notice;'),
  p('     (g) report any defect, damage, or required repair promptly in writing;'),
  p('     (h) not keep any pet without prior written consent of the Landlord;'),
  p('     (i) comply with all applicable laws, by-laws, and regulations;'),
  p('     (j) return all keys, access cards, and remote controls on vacation.'),

  h1('CLAUSE 8 — CONDITION ON VACATION'),
  p('8.1  The Tenant shall return the Premises in the same condition as at commencement, subject to fair wear and tear.'),
  p('8.2  A joint inspection shall be conducted within forty-eight (48) hours of vacation. Defects shall be recorded in writing and signed by both parties.'),
  p('8.3  All keys, access cards, and remote controls shall be returned on the day of vacation.'),

  h1('CLAUSE 9 — TERMINATION AND NOTICES'),
  p('9.1  Either party may terminate at the end of the fixed term by giving _______ [30/60] days\' written notice.'),
  p('9.2  The Landlord may terminate before term expiry only on grounds permitted by Act 220, including:'),
  p('     (a) non-payment of rent exceeding one (1) month;'),
  p('     (b) material breach unremedied after fourteen (14) days\' written notice;'),
  p('     (c) use of the Premises for an illegal purpose;'),
  p('     (d) serious damage caused by the Tenant.'),
  p('9.3  All notices shall be in writing and delivered personally, by registered post, or by email to the address stated herein.'),
  p('9.4  The Tenant shall not be removed except by lawful order of a competent court or Rent Tribunal following the procedure under Act 220.'),

  h1('CLAUSE 10 — DISPUTE RESOLUTION'),
  p('10.1 Disputes not resolved directly shall be referred first to the Rent Control Department of the relevant district.'),
  p('10.2 Unresolved matters may then be referred to the District Magistrate Court having jurisdiction.'),
  p('10.3 Nothing herein prevents either party seeking urgent injunctive relief from a court of competent jurisdiction.'),

  h1('CLAUSE 11 — GENERAL'),
  p('11.1 This Agreement is the entire agreement between the parties in respect of the Premises and supersedes all prior negotiations and representations.'),
  p('11.2 Any variation shall be in writing and signed by both parties.'),
  p('11.3 If any provision is unenforceable, the remaining provisions continue in full force.'),
  p('11.4 This Agreement is governed by the laws of the Republic of Ghana.'),
];

// ══════════════════════════════════════════════════════════════
// AGREEMENT 1 — FIXED-TERM RESIDENTIAL
// ══════════════════════════════════════════════════════════════
async function buildFixedTerm(outPath) {
  const children = [
    ...coverBar('RESIDENTIAL TENANCY AGREEMENT (FIXED-TERM)', 'Property and Rent Consult — Ghana Edition', 'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369'),
    ...residentialParties(),
    ...recitals(),
    h1('CLAUSE 1 — TERM'),
    p('1.1  The Landlord lets and the Tenant takes the Premises for a fixed term of _______ [months / years] commencing on _______________ and ending on _______________, unless sooner determined under this Agreement.'),
    p('1.2  This Agreement shall not renew automatically on expiry. Renewal requires a fresh written agreement. Either party must give at least _______ [90] days\' written notice of intention to renew before the term expires.'),
    p('1.3  On expiry without renewal the Tenant shall immediately vacate and return possession of the Premises to the Landlord.'),
    h1('CLAUSE 2 — RENT'),
    p('2.1  The Tenant shall pay rent at GHS _____________ per [month / year], payable in advance as set out in Clause 3.'),
    p('2.2  Rent shall be paid without deduction, set-off, or counterclaim except as permitted by the Rent Act, 1963 (Act 220).'),
    p('2.3  The rent shall not be increased during the fixed term without the mutual written consent of both parties, subject to Act 220 and L.I. 369.'),
    p('2.4  Should a permitted increase arise after the fixed term, the Landlord shall give not less than three (3) months\' written notice before the increase takes effect, in compliance with L.I. 369.'),
    h1('CLAUSE 3 — ADVANCE PAYMENT'),
    p('3.1  The Tenant shall pay _______ [months / years] rent in advance on signing this Agreement, totalling GHS _________________.'),
    p('3.2  The Landlord shall issue a written receipt upon receiving the advance, as required by section 25 of Act 220.'),
    p('3.3  The advance rent shall be applied against successive monthly rent obligations as they fall due during the advance period.'),
    p('3.4  Where the advance period expires before the end of the fixed term, further advance rent is payable on written terms agreed between the parties.'),
    ...standardClauses4to11(),
    ...execBlock(),
    ...standardSchedules(),
  ];
  const buf = await Packer.toBuffer(makeDoc('Fixed-Term Residential Tenancy Agreement', children));
  writeFileSync(outPath, buf);
  console.log('Saved:', outPath);
}

// ══════════════════════════════════════════════════════════════
// AGREEMENT 2 — MONTH-TO-MONTH RESIDENTIAL
// ══════════════════════════════════════════════════════════════
async function buildMonthToMonth(outPath) {
  const children = [
    ...coverBar('RESIDENTIAL TENANCY AGREEMENT (MONTH-TO-MONTH)', 'Property and Rent Consult — Ghana Edition', 'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369'),
    ...residentialParties(),
    ...recitals(),
    h1('CLAUSE 1 — TERM'),
    p('1.1  The Landlord lets and the Tenant takes the Premises on a month-to-month basis commencing on _______________, continuing on a rolling monthly basis until terminated in accordance with this Agreement.'),
    p('1.2  There is no fixed end date. The tenancy continues each month until a valid written termination notice is served.'),
    p('1.3  Either party may terminate by giving not less than ONE (1) full calendar month\'s written notice, expiring at the end of a rental month.'),
    p('1.4  The Landlord may terminate on the grounds set out in Clause 9.2 by giving the appropriate notice under Act 220.'),
    h1('CLAUSE 2 — RENT'),
    p('2.1  The Tenant shall pay rent at GHS _____________ per month, payable in advance as set out in Clause 3.'),
    p('2.2  Rent shall be paid without deduction, set-off, or counterclaim except as permitted by the Rent Act, 1963 (Act 220).'),
    p('2.3  Rent may be reviewed by the Landlord on a [monthly / quarterly / annual] basis. Any proposed increase requires not less than three (3) months\' written notice to the Tenant, as required by L.I. 369.'),
    p('2.4  Should a permitted increase arise, the Landlord shall give not less than three (3) months\' written notice before the increase takes effect, in compliance with L.I. 369.'),
    p('2.5  In the event of a rent review, both parties may negotiate the revised amount. If agreement cannot be reached, either party may refer the matter to the Rent Control Department.'),
    h1('CLAUSE 3 — ADVANCE PAYMENT'),
    p('3.1  The Tenant shall pay _______ [1 / 2 / 3] months\' rent in advance on signing, totalling GHS _________________. Advance periods exceeding three (3) months require express written agreement in this clause.'),
    p('3.2  The Landlord shall issue a written receipt upon receiving the advance, as required by section 25 of Act 220.'),
    p('3.3  The advance rent shall be applied against successive monthly rent obligations as they fall due during the advance period.'),
    p('3.4  Where the advance period expires, further advance rent is payable on written terms agreed between the parties.'),
    ...standardClauses4to11(),
    ...execBlock(),
    ...standardSchedules(),
  ];
  const buf = await Packer.toBuffer(makeDoc('Month-to-Month Residential Tenancy Agreement', children));
  writeFileSync(outPath, buf);
  console.log('Saved:', outPath);
}

// ══════════════════════════════════════════════════════════════
// AGREEMENT 3 — ROOM RENTAL
// ══════════════════════════════════════════════════════════════
async function buildRoomRental(outPath) {
  const houseRulesSchedule = [
    sp(),
    sectionBar('SCHEDULE 3 — HOUSE RULES'),
    p('1.  Quiet Hours: (____)PM to (____)AM daily'),
    p('2.  No cooking in the room unless a dedicated cooking space is provided'),
    p('3.  Visitors must leave the premises by 10:00 PM unless otherwise agreed in writing with the Landlord'),
    p('4.  All refuse must be deposited in designated bins only'),
    p('5.  No loud music or noise likely to disturb other occupants at any time'),
    p('6.  No modifications, nails, or fixtures to be attached to walls or fittings without consent'),
    p('7.  Shared bathrooms and kitchens must be cleaned after each use'),
    p('8.  Additional House Rules: _______________________________________________'),
  ];
  const children = [
    ...coverBar('ROOM RENTAL AGREEMENT', 'For Single-Room Tenancies in Shared Compound Houses and Multi-Occupancy Buildings', 'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369'),
    ...residentialParties(),
    sectionBar('ROOM DETAILS'),
    field('Room Description'), field('Floor / Location within Building'),
    pb('Shared Facilities Available to Tenant:'),
    check('Kitchen'), check('Bathroom'), check('Toilet'), check('Compound / Yard'), check('Other: _______________'),
    field('Current Occupants in Building / Compound'),
    ...recitals(),
    h1('CLAUSE 1 — TERM'),
    p('Circle the applicable term type:'),
    sp(),
    pb('Option A — Fixed-Term:', STEEL_BLUE),
    p('The Landlord lets and the Tenant takes the Room for a fixed term of _______ [months / years] commencing on _______________ and ending on _______________.'),
    sp(),
    pb('Option B — Month-to-Month:', STEEL_BLUE),
    p("The Landlord lets and the Tenant takes the Room on a month-to-month basis commencing on _______________, terminable by one (1) month's written notice by either party expiring at the end of a rental month."),
    h1('CLAUSE 2 — RENT'),
    p('2.1  The Tenant shall pay rent at GHS _____________ per [month / year], payable in advance as set out in Clause 3.'),
    p('2.2  Rent shall be paid without deduction, set-off, or counterclaim except as permitted by the Rent Act, 1963 (Act 220).'),
    p('2.3  The rent shall not be increased without the mutual written consent of both parties, subject to Act 220 and L.I. 369.'),
    p('2.4  Should a permitted increase arise, the Landlord shall give not less than three (3) months\' written notice before the increase takes effect.'),
    h1('CLAUSE 3 — ADVANCE PAYMENT'),
    p('3.1  The Tenant shall pay _______ months\' rent in advance on signing this Agreement, totalling GHS _________________.'),
    p('3.2  The Landlord shall issue a written receipt upon receiving the advance, as required by section 25 of Act 220.'),
    p('3.3  The advance rent shall be applied against successive monthly rent obligations as they fall due.'),
    p('3.4  Where the advance period expires, further advance rent is payable on written terms agreed between the parties.'),
    h1('CLAUSE 4 — SECURITY DEPOSIT'),
    p('4.1  The Tenant shall pay a security deposit of GHS _________________ on signing, held by the Landlord as security against unpaid rent, damage beyond fair wear and tear, and any other breach of this Agreement.'),
    p('4.2  The deposit shall not be applied as rent.'),
    p('4.3  Within fourteen (14) days of the Tenant vacating, the Landlord shall either return the deposit in full or provide a written itemised statement of deductions with supporting evidence and return the balance.'),
    p('4.4  Deposit disputes may be referred to the Rent Control Department.'),
    h1('CLAUSE 5 — UTILITIES'),
    p('5.1  Utility responsibility (circle applicable for each):'),
    p('     Electricity:   Tenant pays directly  /  Included in rent  /  Shared cost'),
    p('     Water:         Tenant pays directly  /  Included in rent  /  Shared cost'),
    p("5.2  Where electricity and/or water are shared with other occupants, the Tenant's proportionate share is GHS _____________ per month, subject to revision if actual usage changes materially."),
    p('5.3  The Tenant shall not install any independent electrical connection or tap into any utility supply without prior written consent.'),
    h1('CLAUSE 6 — LANDLORD OBLIGATIONS'),
    p("6.1  The Landlord shall: (a) put and keep the Room and shared areas in reasonable repair; (b) ensure the premises are fit for habitation; (c) carry out structural repairs within a reasonable time of written notification; (d) not interfere with the Tenant's quiet enjoyment; (e) give at least twenty-four (24) hours' written notice before entering; (f) issue a written receipt for every payment."),
    h1('CLAUSE 7 — TENANT OBLIGATIONS'),
    p('7.1  The Tenant shall:'),
    p('     (a) pay rent on the dates and in the manner agreed herein;'),
    p('     (b) keep the Room clean, tidy, and in good condition;'),
    p('     (c) not carry out any structural alteration without prior written consent of the Landlord;'),
    p('     (d) not sublet the Room or any part of the Premises without prior written consent of the Landlord;'),
    p('     (e) not use the Room for any unlawful purpose or in a manner constituting a nuisance to other occupants;'),
    p('     (f) permit the Landlord or their authorised agent to enter and inspect at reasonable times with twenty-four (24) hours\' notice;'),
    p('     (g) report any defect, damage, or required repair promptly in writing;'),
    p('     (h) not keep any pet without prior written consent of the Landlord;'),
    p('     (i) comply with all applicable laws, by-laws, and regulations;'),
    p('     (j) return all keys, access cards, and remote controls on vacation;'),
    p('     (k) not bring additional permanent occupants to share the room without prior written consent of the Landlord;'),
    p('     (l) comply with the House Rules set out in Schedule 3;'),
    p('     (m) not store any flammable, hazardous, or illegal materials in the room or in any shared area.'),
    h1('CLAUSE 8 — CONDITION ON VACATION'),
    p('8.1  The Tenant shall return the Room in the same condition as at commencement, subject to fair wear and tear.'),
    p('8.2  A joint inspection shall be conducted within forty-eight (48) hours of vacation. Defects shall be recorded in writing and signed by both parties.'),
    p('8.3  All keys, access cards, and remote controls shall be returned on the day of vacation.'),
    h1('CLAUSE 9 — TERMINATION AND NOTICES'),
    p("9.1  Either party may terminate this Agreement by giving the applicable notice period set out in Clause 1."),
    p('9.2  The Landlord may terminate before the end of term only on grounds permitted by Act 220, including: (a) non-payment of rent exceeding one (1) month; (b) material breach unremedied after fourteen (14) days\' written notice; (c) use of the Room for an illegal purpose; (d) serious damage caused by the Tenant.'),
    p('9.3  All notices shall be in writing and delivered personally, by registered post, or by email to the address stated herein.'),
    p('9.4  The Tenant shall not be removed except by lawful order of a competent court or Rent Tribunal following the procedure under Act 220.'),
    h1('CLAUSE 10 — DISPUTE RESOLUTION'),
    p('10.1 Disputes not resolved directly shall be referred first to the Rent Control Department of the relevant district.'),
    p('10.2 Unresolved matters may then be referred to the District Magistrate Court having jurisdiction.'),
    p('10.3 Nothing herein prevents either party seeking urgent injunctive relief from a court of competent jurisdiction.'),
    h1('CLAUSE 11 — GENERAL'),
    p('11.1 This Agreement is the entire agreement between the parties in respect of the Room and supersedes all prior negotiations and representations.'),
    p('11.2 Any variation shall be in writing and signed by both parties.'),
    p('11.3 If any provision is unenforceable, the remaining provisions continue in full force.'),
    p('11.4 This Agreement is governed by the laws of the Republic of Ghana.'),
    ...execBlock(),
    ...standardSchedules(houseRulesSchedule),
  ];
  const buf = await Packer.toBuffer(makeDoc('Room Rental Agreement', children));
  writeFileSync(outPath, buf);
  console.log('Saved:', outPath);
}

// ══════════════════════════════════════════════════════════════
// AGREEMENT 4 — COMMERCIAL LEASE
// ══════════════════════════════════════════════════════════════
async function buildCommercial(outPath) {
  const children = [
    ...coverBar('COMMERCIAL LEASE AGREEMENT', 'Property and Rent Consult — Ghana Edition', 'Subject to the Rent Act, 1963 (Act 220) and the Contracts Act, 1960 (Act 25)'),
    sectionBar('PARTIES'),
    p('COMMERCIAL LEASE AGREEMENT made this ______ day of _______________, ________'),
    sp(),
    pb('LANDLORD / LESSOR'),
    field('Full Name / Company Name'), field('Ghana Card / RC Number'), field('Registered Address'), field('Phone'), field('Email'),
    p('(hereinafter referred to as "the Landlord")'),
    sp(), pb('AND'), sp(),
    pb('TENANT / LESSEE'),
    field('Full Name / Company Name'), field('Ghana Card / RC Number / TIN'), field('Nature of Business'), field('Registered / Trading Address'), field('Phone'), field('Email'),
    p('(hereinafter referred to as "the Tenant")'),
    sp(),
    pb('PREMISES'),
    field('Property Address'), field('Total Floor Area (sqm)'), field('Floor / Level'), field('Ghana Post GPS Address'), field('Shared Areas Included'),
    p('Premises Type:'), check('Office'), check('Shop / Retail'), check('Warehouse'), check('Salon'), check('Clinic / Consulting Room'), check('Restaurant'), check('Other: _______________'),
    sectionBar('RECITALS'),
    p('WHEREAS the Landlord is the owner or authorised agent of the Premises and is willing to let the same for commercial use on the terms herein;'),
    p('AND WHEREAS the Tenant wishes to take the Premises for the purpose of conducting lawful commercial operations;'),
    pb('NOW THEREFORE the parties agree as follows:'),
    h1('CLAUSE 1 — TERM'),
    p('1.1  The Landlord lets and the Tenant takes the Premises for a fixed term of _______ years commencing on _______________ and ending on _______________.'),
    p('1.2  The Tenant shall notify the Landlord in writing not less than _______ [60/90] days before expiry if they wish to renew. Renewal is not automatic and requires a fresh written agreement.'),
    p('1.3  On expiry without renewal, the Tenant shall immediately vacate and deliver up vacant possession of the Premises.'),
    h1('CLAUSE 2 — PERMITTED USE'),
    p('2.1  The Tenant shall use the Premises solely for the purpose of: _______________________________________________ and for no other purpose without the prior written consent of the Landlord.'),
    p('2.2  The Tenant shall conduct their business in compliance with all applicable laws, including the requirements of any relevant regulatory or licensing authority in Ghana.'),
    p('2.3  The Tenant shall not use the Premises for any residential purpose.'),
    p('2.4  The Tenant shall obtain and maintain all licences, permits, and approvals required for the conduct of their business at the Premises, at their own cost.'),
    h1('CLAUSE 3 — RENT'),
    p('3.1  The Tenant shall pay rent at GHS _____________ per [month / year / quarter], payable in advance as set out in Clause 4.'),
    p('3.2  Rent shall be paid without deduction, counterclaim, or set-off.'),
    p('3.3  Any rent review shall be subject to _______ [90/180] days\' prior written notice by the Landlord.'),
    p('3.4  In the event of a dispute over a proposed rent increase, either party may refer the matter to arbitration or the Rent Control Department.'),
    h1('CLAUSE 4 — ADVANCE PAYMENT AND DEPOSIT'),
    p('4.1  The Tenant shall pay rent in advance for _______ [months / years] totalling GHS _________________ at signing.'),
    p('4.2  The Tenant shall pay a security deposit of GHS _________________ at signing, to be held against unpaid rent, damage, and breach.'),
    p('4.3  The Landlord shall issue written receipts for all payments.'),
    p('4.4  The deposit shall be returned within twenty-one (21) days of vacation, subject to verified deductions with itemised written justification.'),
    h1('CLAUSE 5 — UTILITIES AND OUTGOINGS'),
    p("5.1  The following are the Tenant's direct responsibility:"),
    check('Electricity'), check('Water'), check('Internet / Telephone'), check('Security'), check('Refuse / Waste Disposal'), check('Air Conditioning maintenance'),
    p('5.2  The Tenant shall pay all rates, levies, and statutory charges relating to the business conducted at the Premises, including any applicable business operating permit fees.'),
    p('5.3  Service charges of GHS _____________ per month are payable for shared facilities including: _______________________________________________'),
    p('5.4  The Tenant shall not install additional electrical fittings or air conditioning units without prior written consent and shall ensure any installation complies with applicable electrical codes.'),
    h1('CLAUSE 6 — LANDLORD OBLIGATIONS'),
    p('6.1  The Landlord shall: (a) deliver the Premises in a state reasonably fit for the permitted use at commencement; (b) maintain the structural fabric of the building, including the roof, external walls, and foundations; (c) maintain shared areas, access routes, and common facilities in reasonable condition; (d) not interfere with the Tenant\'s peaceful enjoyment of the Premises for the permitted use; (e) give not less than forty-eight (48) hours\' written notice before entering the Premises, except in emergency.'),
    h1('CLAUSE 7 — TENANT OBLIGATIONS'),
    p('7.1  The Tenant shall: (a) pay rent and all other sums due on time; (b) keep the interior clean and in good repair, subject to fair wear and tear; (c) not carry out structural alterations, signage installation, or fit-out works without prior written consent; (d) not assign, sublet, or share possession without prior written consent; (e) not store hazardous, flammable, or illegal goods on the Premises; (f) comply with all applicable laws, by-laws, planning conditions, and health and safety requirements; (g) permit the Landlord to enter with forty-eight (48) hours\' notice; (h) not obstruct access to shared areas or emergency exits; (i) on termination, remove all fixtures, fittings, and trade equipment and make good any damage caused.'),
    h1('CLAUSE 8 — ALTERATIONS AND FIT-OUT'),
    p('8.1  The Tenant may, with the prior written consent of the Landlord, carry out internal alterations and fit-out works for the permitted use.'),
    p("8.2  All approved works shall be carried out by qualified contractors, at the Tenant's expense, and to a standard reasonably acceptable to the Landlord."),
    p('8.3  On termination, the Tenant shall either: (a) remove all alterations and restore the Premises to their original condition; or (b) leave approved permanent alterations in place if the Landlord consents in writing.'),
    h1('CLAUSE 9 — SIGNAGE'),
    p('9.1  The Tenant may install business signage at or on the Premises with the prior written consent of the Landlord.'),
    p('9.2  All signage must comply with applicable by-laws of the relevant Municipal Assembly (e.g., AMA, KMA, KEEA).'),
    p('9.3  On termination, all signage shall be removed and any damage to the building fabric made good.'),
    h1('CLAUSE 10 — INSURANCE'),
    p('10.1 The Landlord shall maintain insurance covering the structural fabric of the building.'),
    p("10.2 The Tenant shall maintain insurance covering: (a) their business contents, stock, and equipment; (b) public liability in respect of the Premises at a minimum of GHS _________________ per occurrence."),
    p('10.3 Each party shall, on request, provide evidence of their insurance cover to the other party.'),
    h1('CLAUSE 11 — CONDITION ON VACATION'),
    p('11.1 On expiry or termination, the Tenant shall: (a) vacate the Premises and remove all personal property and trade equipment by the vacation date; (b) return the Premises in a clean and tidy condition; (c) return all keys, access cards, and security codes; (d) make good any damage caused during the tenancy beyond fair wear and tear.'),
    p('11.2 A joint exit inspection shall be conducted within forty-eight (48) hours of the vacation date. Findings shall be recorded in writing and signed.'),
    h1('CLAUSE 12 — TERMINATION'),
    p("12.1 Either party may terminate at the end of the fixed term by giving _______ [6] months' written notice."),
    p('12.2 The Landlord may terminate early on the following grounds: (a) non-payment of rent or other sums due for more than _______ days; (b) material breach of any term, unremedied after twenty-one (21) days\' written notice; (c) insolvency, winding-up, or cessation of business by the Tenant; (d) use of the Premises for an illegal or unauthorised purpose.'),
    p("12.3 The Tenant may terminate early only with the written agreement of the Landlord, subject to payment of any agreed break fee."),
    h1('CLAUSE 13 — DISPUTE RESOLUTION'),
    p('13.1 Disputes shall first be referred to direct negotiation between the parties.'),
    p('13.2 If unresolved within twenty-one (21) days, either party may refer the dispute to arbitration under the Alternative Dispute Resolution Act, 2010 (Act 798), or to the court of competent jurisdiction in Ghana.'),
    p('13.3 For matters falling within the jurisdiction of the Rent Control Department under Act 220, either party may refer the matter there.'),
    h1('CLAUSE 14 — GENERAL'),
    p('14.1 This Agreement constitutes the entire agreement between the parties.'),
    p('14.2 Any variation shall be in writing and signed by both parties.'),
    p('14.3 This Agreement is governed by the laws of the Republic of Ghana.'),
    p('14.4 The invalidity of any provision shall not affect the remaining provisions.'),
    ...execBlock(),
    sp(), sectionBar('SCHEDULE 1 — DESCRIPTION AND CONDITION OF PREMISES AT COMMENCEMENT'),
    p('(Record current condition of floors, walls, ceilings, fittings, electrical points, plumbing, and any landlord-installed equipment)'),
    sp(), sectionBar('SCHEDULE 2 — APPROVED FIT-OUT WORKS (IF ANY)'),
    p('(Description of any works pre-approved at the time of signing)'),
    sp(), sectionBar('SCHEDULE 3 — SPECIAL CONDITIONS'),
    p('1. ' + '_'.repeat(80)), p('2. ' + '_'.repeat(80)), p('3. ' + '_'.repeat(80)),
  ];
  const buf = await Packer.toBuffer(makeDoc('Commercial Lease Agreement', children));
  writeFileSync(outPath, buf);
  console.log('Saved:', outPath);
}

// ══════════════════════════════════════════════════════════════
// AGREEMENT 5 — KIOSK / CONTAINER
// ══════════════════════════════════════════════════════════════
async function buildKiosk(outPath) {
  const children = [
    ...coverBar('TEMPORARY STRUCTURE RENT AGREEMENT', 'For Kiosk, Container, and Temporary Commercial Structure Rentals', 'Subject to the Contracts Act, 1960 (Act 25) and applicable Municipal Assembly Permit Requirements'),
    sectionBar('IMPORTANT NOTE TO BUYER'),
    p('This Agreement covers the rental of a space or plot of land for the placement of a kiosk, shipping container, wooden booth, or similar temporary structure for commercial purposes. It is used extensively for micro-businesses in Ghana including provision sellers, mobile money agents, phone charging stations, food vendors, phone accessories sellers, and similar traders. The agreement addresses both the land/space rental and, where applicable, the ownership and installation of the physical structure itself.'),
    sectionBar('PARTIES'),
    p('TEMPORARY STRUCTURE RENT AGREEMENT made this ______ day of _______________, ________'),
    sp(), pb('SPACE OWNER / LANDLORD'),
    field('Full Name'), field('Ghana Card / Passport No.'), field('Address'), field('Phone'), field('Email'),
    p('(hereinafter referred to as "the Space Owner")'),
    sp(), pb('AND'), sp(),
    pb('OCCUPANT / TRADER'),
    field('Full Name'), field('Ghana Card / Passport No.'), field('Nature of Business'), field('Phone'), field('Email'),
    p('(hereinafter referred to as "the Occupant")'),
    sp(), pb('SPACE AND STRUCTURE DETAILS'),
    field('Location of Space (Street address, neighbourhood, landmark)'), field('Ghana Post GPS'), field('Space Dimensions (metres × metres, approximate)'),
    p('Structure Type:'), check('Metal Kiosk'), check('Wooden Booth'), check('Shipping Container'), check('Converted Container'), check('Canvas / Semi-Permanent'), check('Other: _______________'),
    p('Structure Ownership:'), check('Structure belongs to the Space Owner (rented with the space)'), check('Structure belongs to the Occupant (placed on the space)'), check('Structure to be provided by _______________ (specify)'),
    sectionBar('RECITALS'),
    p('WHEREAS the Space Owner holds the right to let or licence the above-described space for commercial use and is willing to permit the Occupant to use it on the terms herein; AND WHEREAS the Occupant wishes to use the space for the conduct of lawful commercial activities; NOW THEREFORE the parties agree as follows:'),
    h1('CLAUSE 1 — TERM'),
    p('1.1  The Space Owner permits and the Occupant takes occupation of the Space described above for a period of _______________ commencing on _______________ [and ending on _______________ / on a month-to-month basis until terminated].'),
    p('1.2  Either party may terminate this Agreement by giving _______ [7/14/30] days\' written notice to the other party.'),
    p('1.3  The Space Owner may terminate immediately, without notice, only where: (a) the Occupant conducts an illegal business or activity at the Space; (b) the Occupant causes serious damage to the Space, neighbouring property, or persons.'),
    h1('CLAUSE 2 — RENT'),
    p('2.1  The Occupant shall pay to the Space Owner rent at GHS _____________ per [week / month], payable [in advance / on the _____ day of each month].'),
    p('2.2  Rent shall be paid by [cash / mobile money / bank transfer] to: [Mobile Money Number / Bank Account: ___________________________]'),
    p('2.3  The Space Owner shall issue a written receipt for every payment made, as required by Act 220 where applicable.'),
    p('2.4  Rent shall not be increased without at least _______ [30/60] days\' written notice from the Space Owner.'),
    h1('CLAUSE 3 — STRUCTURE OWNERSHIP AND INSTALLATION'),
    p('3.1  Where the structure belongs to the SPACE OWNER: (a) the structure is let to the Occupant as part of this Agreement in its current condition; (b) the Occupant shall keep the structure clean and in reasonable condition; (c) the Occupant shall report any structural defect to the Space Owner promptly in writing; (d) the Space Owner shall carry out structural repairs within a reasonable time of written notification.'),
    p('3.2  Where the structure belongs to the OCCUPANT: (a) the Occupant shall have the right to place and use their structure on the Space for the duration of this Agreement; (b) the Occupant shall install the structure at their own cost and maintain it in safe condition; (c) on termination, the Occupant shall remove the structure from the Space within _______ [7/14] days and restore the space to its previous condition; (d) failure to remove the structure within the stated period shall entitle the Space Owner to arrange removal at the Occupant\'s cost.'),
    p('3.3  Neither party shall permit the structure to be used as a permanent residential dwelling.'),
    h1('CLAUSE 4 — PERMITTED USE'),
    p('4.1  The Occupant shall use the Space and structure solely for the purpose of: _______________________________________________'),
    p('4.2  The Occupant shall not expand, enlarge, or add to the structure without prior written consent of the Space Owner.'),
    p('4.3  The Occupant shall conduct their business in compliance with all applicable laws, including requirements of the relevant Municipal Assembly (e.g., AMA, KMA, GCMA) regarding trading permits and temporary structures.'),
    p('4.4  The Occupant shall obtain and maintain any permit, licence, or approval required by the Municipal Assembly or any regulatory authority for the operation of their business at the Space, at their own cost.'),
    p('4.5  The Occupant shall not use the Space for any residential purpose, for storage of hazardous materials, or for any illegal activity.'),
    h1('CLAUSE 5 — UTILITIES'),
    p('5.1  Electricity and water arrangements (circle applicable):'), check('No utility connection available at this Space'), check('The Occupant may connect to the Space Owner\'s supply subject to a monthly utility contribution of GHS _________________ per month'), check('The Occupant shall arrange their own independent utility supply through the appropriate authority'),
    p('5.2  The Occupant shall not tap into any utility supply (ECG, Ghana Water, or otherwise) without express written consent of the Space Owner and proper authorisation from the relevant utility provider.'),
    p('5.3  All costs of independent utility supply, connection, and metering shall be borne solely by the Occupant.'),
    h1('CLAUSE 6 — MAINTENANCE AND CLEANLINESS'),
    p('6.1  The Occupant shall: (a) keep the Space and structure clean and free of rubbish at all times; (b) not deposit waste, refuse, or used packaging in the area surrounding the Space in a manner that creates a nuisance; (c) not block pedestrian access or public walkways with goods, equipment, or signage; (d) carry out minor maintenance of the structure at their own cost; (e) maintain the area immediately around the Space in a clean and tidy condition.'),
    h1('CLAUSE 7 — MUNICIPAL PERMITS AND COMPLIANCE'),
    p('7.1  The Occupant is solely responsible for obtaining and renewing any permit or approval required by the relevant Municipal Assembly for the operation of a temporary commercial structure at the Space.'),
    p('7.2  The Space Owner makes no representation that the Space is permitted for commercial use by the Municipal Assembly. It is the Occupant\'s responsibility to verify and secure all necessary approvals.'),
    p('7.3  If a Municipal Assembly order, notice, or enforcement action requires the removal or demolition of the structure, the Occupant shall comply immediately and at their own cost. This Agreement shall terminate automatically upon such enforcement action.'),
    p('7.4  Neither party shall be liable to the other for loss arising from a Municipal Assembly enforcement action requiring removal of the structure.'),
    h1('CLAUSE 8 — SPACE OWNER OBLIGATIONS'),
    p('8.1  The Space Owner shall: (a) permit the Occupant quiet use of the Space for the permitted purpose during the agreement; (b) not interfere with the Occupant\'s business operations without cause; (c) give _______ [7/14] days\' notice before requiring the Occupant to temporarily vacate for any legitimate purpose.'),
    h1('CLAUSE 9 — DAMAGE AND LIABILITY'),
    p("9.1  The Occupant shall be responsible for any damage caused to the Space or surrounding property by the structure, the Occupant's activities, or the Occupant's employees, agents, or customers."),
    p("9.2  The Space Owner shall not be liable for loss or damage to the Occupant's goods, stock, equipment, or business resulting from theft, weather, fire, or any event beyond the Space Owner's reasonable control."),
    p("9.3  The Occupant shall not hold the Space Owner liable for any loss of business, income, or profit arising from any cause."),
    h1('CLAUSE 10 — TERMINATION AND VACATION'),
    p('10.1 On expiry or termination of this Agreement: (a) the Occupant shall immediately cease commercial operations at the Space; (b) if the structure belongs to the Occupant, it shall be removed within the period specified in Clause 3.2(c); (c) the Space shall be left clean and in its original condition.'),
    p('10.2 The Space Owner may recover the Space through self-help where the Occupant has abandoned the Space or has clearly vacated, without requiring a court order, provided no force is used against any person.'),
    p('10.3 For contested evictions, the Space Owner shall follow the applicable procedure under Act 220 or seek relief from a court of competent jurisdiction.'),
    h1('CLAUSE 11 — DISPUTE RESOLUTION'),
    p('11.1 Disputes shall be resolved by direct discussion between the parties in the first instance.'),
    p('11.2 Unresolved disputes may be referred to the Rent Control Department (where Act 220 applies) or to the District Magistrate Court.'),
    h1('CLAUSE 12 — GENERAL'),
    p('12.1 This Agreement is the entire agreement between the parties regarding the Space.'),
    p('12.2 Any variation shall be in writing and signed by both parties.'),
    p('12.3 This Agreement is governed by the laws of the Republic of Ghana.'),
    p('12.4 If any provision is invalid, the remaining provisions continue in force.'),
    ...execBlock(),
    sp(), sectionBar('SCHEDULE 1 — DESCRIPTION OF SPACE AND STRUCTURE AT COMMENCEMENT'),
    p('(Record current condition, approximate dimensions, utility connections, any existing damage or defects)'),
    sp(), sectionBar('SCHEDULE 2 — PERMIT / APPROVAL DETAILS'),
    field('Municipal Assembly'), field('Permit Number (if any)'), field('Permit Expiry Date'), field('Conditions attached to permit'),
    sp(), sectionBar('SCHEDULE 3 — SPECIAL CONDITIONS'),
    p('1. ' + '_'.repeat(80)), p('2. ' + '_'.repeat(80)), p('3. ' + '_'.repeat(80)),
  ];
  const buf = await Packer.toBuffer(makeDoc('Temporary Structure Rent Agreement', children));
  writeFileSync(outPath, buf);
  console.log('Saved:', outPath);
}

async function main() {
  const LP = BASE;
  // Agreement 1 — all tiers
  const ft = 'PRC-Fixed-Term-Residential-Tenancy-Agreement.docx';
  await buildFixedTerm(join(LP, 'Basic_Tier', ft));
  await buildFixedTerm(join(LP, 'Pro_Tier', ft));
  await buildFixedTerm(join(LP, 'Agency_Tier', ft));
  // Agreement 2 — Pro + Agency
  const m2m = 'PRC-Month-to-Month-Residential-Tenancy-Agreement.docx';
  await buildMonthToMonth(join(LP, 'Pro_Tier', m2m));
  await buildMonthToMonth(join(LP, 'Agency_Tier', m2m));
  // Agreement 3 — Pro + Agency
  const room = 'PRC-Room-Rental-Agreement.docx';
  await buildRoomRental(join(LP, 'Pro_Tier', room));
  await buildRoomRental(join(LP, 'Agency_Tier', room));
  // Agreement 4 — Agency only
  await buildCommercial(join(LP, 'Agency_Tier', 'PRC-Commercial-Lease-Agreement.docx'));
  // Agreement 5 — Agency only
  await buildKiosk(join(LP, 'Agency_Tier', 'PRC-Temporary-Structure-Rent-Agreement.docx'));
  console.log('All agreement DOCX files done.');
}
main().catch(console.error);
