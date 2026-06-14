import { createRequire } from 'module';
import { writeFileSync } from 'fs';
import { join } from 'path';
const require = createRequire(import.meta.url);
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, WidthType, Header, Footer,
        ShadingType } = require('docx');

const BASE = String.raw`C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs`;

// Brand colours (hex without #)
const DEEP_BROWN = '36221C';
const STEEL_BLUE = '516984';
const WARM_GREY  = '63645A';
const LIGHT_BLUE = 'E8EEF3';
const OFF_WHITE  = 'F5EDE8';
const WHITE      = 'FFFFFF';

const shade = (color) => ({ type: ShadingType.SOLID, color, fill: color });

const h1 = (text) => new Paragraph({
  children: [new TextRun({ text, bold: true, size: 28, color: DEEP_BROWN, font: 'Calibri' })],
  spacing: { before: 240, after: 120 },
});

const h2 = (text) => new Paragraph({
  children: [new TextRun({ text, bold: true, size: 22, color: STEEL_BLUE, font: 'Calibri' })],
  spacing: { before: 180, after: 80 },
});

const body = (text, bold=false, color='2D2D2D') => new Paragraph({
  children: [new TextRun({ text, bold, size: 22, color, font: 'Calibri' })],
  spacing: { after: 60 },
});

const bullet = (text) => new Paragraph({
  children: [new TextRun({ text: `• ${text}`, size: 22, color: '2D2D2D', font: 'Calibri' })],
  spacing: { after: 40 },
});

const numbered = (n, text) => new Paragraph({
  children: [new TextRun({ text: `${n}. ${text}`, size: 22, color: '2D2D2D', font: 'Calibri' })],
  spacing: { after: 40 },
});

const spacer = () => new Paragraph({ children: [new TextRun('')], spacing: { after: 100 } });

const headerRow = (cells, widths) => new TableRow({
  children: cells.map((text, i) => new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, size: 18, color: WHITE, font: 'Calibri' })],
      alignment: AlignmentType.CENTER,
    })],
    shading: shade(DEEP_BROWN),
    width: { size: widths[i], type: WidthType.DXA },
  })),
  tableHeader: true,
});

const dataRow = (cells, widths, bg=WHITE) => new TableRow({
  children: cells.map((text, i) => new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, size: 18, color: '2D2D2D', font: 'Calibri' })],
    })],
    shading: shade(bg),
    width: { size: widths[i], type: WidthType.DXA },
  })),
});

function buildDoc(tier) {
  const sections = [
    // COVER
    h1('TENANT SCREENING CHECKLIST & SCORECARD'),
    h2('Ghana Edition — For Landlords, Agents & Property Managers'),
    body('Reduce tenancy risk with structured, evidence-based screening'),
    body('2026 Edition | Property and Rent Consult'),
    spacer(),

    // INSTRUCTIONS
    h1('HOW TO USE THIS SCORECARD'),
    ...[
      'Collect all required documents from the applicant BEFORE scoring.',
      'Complete Section 1 (Minimum Requirements). If ANY item fails — Reject immediately.',
      'Complete the Scoring Table in Section 2. Total the score out of 25.',
      'Match the score to the Risk Category in Section 3.',
      'Complete the Verification Checklist in Section 4 — ALL items must be checked.',
      'Record the final decision and sign Section 5.',
    ].map((s, i) => numbered(i+1, s)),
    spacer(),
    h2('Documents to Collect from Applicant'),
    ...[
      'Ghana Card or valid Passport (mandatory)',
      'Recent payslip or 3-month bank statement (self-employed: business registration + MoMo/bank record)',
      'Utility bill in applicant\'s name (ECG/NEDCO or Ghana Water Company, not older than 3 months)',
      'Guarantor\'s Ghana Card + proof of address + employment letter or business evidence',
      'Written consent for reference checks',
    ].map(bullet),
    spacer(),

    // SECTION 1
    h1('SECTION 1 — MINIMUM REQUIREMENTS (GATE CHECK)'),
    body('If ANY item below is not met, STOP. Do not proceed to scoring. Issue a polite rejection.', false, WARM_GREY),
    spacer(),
    new Table({
      width: { size: 9200, type: WidthType.DXA },
      rows: [
        headerRow(['Ref','Criterion','Pass / Fail'], [1000, 6700, 1500]),
        ...['MR-01|Valid Ghana Card or Passport presented and verified',
            'MR-02|Applicant aged 21 years or above',
            'MR-03|Monthly income verified at 3x the monthly rent',
            'MR-04|No prior eviction record (self-declared and cross-checked)',
            'MR-05|Employed (minimum 6 months) OR verifiable business income',
        ].map((row, i) => {
          const [ref, criterion] = row.split('|');
          return dataRow([ref, criterion, 'Pass / Fail'], [1000, 6700, 1500], i%2===0 ? OFF_WHITE : WHITE);
        }),
      ],
    }),
    spacer(),
    body('If ALL five criteria are met → proceed to Section 2.', true),
    spacer(),

    // SECTION 2
    h1('SECTION 2 — SCORING CRITERIA (Maximum Score: 25)'),
    new Table({
      width: { size: 9200, type: WidthType.DXA },
      rows: [
        headerRow(['Criteria','0 pts','1-2 pts','3-4 pts','5 pts','Score','Notes'], [1600,1200,1200,1400,1400,700,700]),
        ...([
          ['Employment Status','Unemployed','Casual/part-time <6 months','Permanent 6-24 months','Permanent >2 years','___',''],
          ['Income-to-Rent Ratio','Income <2x rent','Exactly 2x rent','Between 2x and 2.5x','Income 3x or above','___',''],
          ['Previous Landlord Reference','Declined/hostile/eviction','Mixed or neutral','Good; ended by relocation','Excellent long-term','___',''],
          ['Guarantor Quality','None offered','Unverified/insufficient','Verified stable employment','Professional/property owner','___',''],
          ['Utility Bill Payment','Frequent disconnections','Occasional late payments','Mostly on time','Consistent on-time','___',''],
        ].map((row, i) => dataRow(row, [1600,1200,1200,1400,1400,700,700], i%2===0 ? OFF_WHITE : WHITE))),
        dataRow(['TOTAL SCORE','','','','','___ / 25',''], [1600,1200,1200,1400,1400,700,700], LIGHT_BLUE),
      ],
    }),
    spacer(),

    // SECTION 3
    h1('SECTION 3 — RISK CATEGORY & RECOMMENDED ACTION'),
    new Table({
      width: { size: 9200, type: WidthType.DXA },
      rows: [
        headerRow(['Score Range','Risk Level','Recommended Action','Notes'], [1500,1800,3000,2900]),
        dataRow(['20 – 25','Low Risk','Approve on standard terms','Proceed with standard deposit'], [1500,1800,3000,2900], 'D4EDDA'),
        dataRow(['15 – 19','Medium Risk','Approve with conditions','Require larger deposit (2 months) or additional guarantor'], [1500,1800,3000,2900], 'FFF3CD'),
        dataRow(['10 – 14','High Risk','Consider with significant conditions only','Require 6 months rent paid in advance; guarantor mandatory'], [1500,1800,3000,2900], 'FFE0C0'),
        dataRow(['Below 10','Very High Risk','Reject','Politely decline; do not negotiate exceptions'], [1500,1800,3000,2900], 'F8D7DA'),
      ],
    }),
    spacer(),

    // SECTION 4
    h1('SECTION 4 — VERIFICATION CHECKLIST'),
    new Table({
      width: { size: 9200, type: WidthType.DXA },
      rows: [
        headerRow(['Ref','Item','Done?','Date','Notes'], [900,5200,1000,1100,1000]),
        ...([
          ['VC-01','Called employer; confirmed position, start date, and salary'],
          ['VC-02','Spoke directly to previous landlord (not just WhatsApp); no red flags'],
          ['VC-03','Verified guarantor Ghana Card, address, and income in person or video call'],
          ['VC-04','Reviewed utility bills — name matches applicant; 3 months minimum reviewed'],
          ['VC-05','Conducted eviction/court record check via Rent Control or local network'],
        ].map(([ref, item], i) => dataRow([ref, item, '___', '___', ''], [900,5200,1000,1100,1000], i%2===0 ? OFF_WHITE : WHITE))),
      ],
    }),
    spacer(),

    // SECTION 5
    h1('SECTION 5 — FINAL DECISION RECORD'),
    ...[
      'Property Address: _____________________________________________',
      'Unit / Apartment: _____________________________________________',
      'Applicant Full Name: _____________________________________________',
      'Ghana Card Number: _____________________________________________',
      'Application Date: _____________________________________________',
      'Total Score: ___ / 25',
      'Risk Category: _____________________________________________',
      'Deposit Required: GHS _______________________________________',
      'Additional Conditions: _____________________________________________',
    ].map(f => body(f)),
    spacer(),
    body('DECISION (tick one):', true),
    body('[ ]  APPROVED — Standard terms apply'),
    body('[ ]  CONDITIONALLY APPROVED — See conditions noted above'),
    body('[ ]  REJECTED — Applicant does not meet required threshold'),
    spacer(),
    h2('SIGNATURE BLOCK'),
    ...['Property Manager / Agent Name: ___________________________',
        'Signature: ___________________________',
        'Date: ___________________________',
        'Stamp / Company: ___________________________',
    ].map(f => body(f)),
    spacer(),

    // BONUS: Call Script
    h1('BONUS — PREVIOUS LANDLORD REFERENCE CALL SCRIPT'),
    body('Use this script when calling the previous landlord. WhatsApp messages alone are insufficient.', false, WARM_GREY),
    spacer(),
    ...[
      '"Good [morning/afternoon], please may I speak with [Landlord Name]?',
      '',
      'My name is [Your Name] and I am a property manager at [Company Name]. I am screening [Applicant Name] who has applied to rent one of my properties. They have listed you as a previous landlord.',
      '',
      '1. Did [Applicant Name] occupy a property managed or owned by you? From when to when?',
      '2. Did they pay rent on time, in full?',
      '3. Were there any complaints from neighbours or other tenants?',
      '4. Did they leave the property in good condition?',
      '5. Would you rent to them again?',
      '6. Is there anything else I should know before I make a decision?',
      '',
      'Thank you very much. I appreciate your time."',
    ].map(line => body(line)),
    spacer(),

    // BONUS: Guarantor Declaration
    h1('BONUS — GUARANTOR DECLARATION'),
    body('I, [Full Name] ______________________________, holder of Ghana Card / Passport No. _____________, residing at ______________________________, hereby declare that I am willing to act as guarantor for [Applicant Name] ______________________________ in respect of the tenancy of the premises at ______________________________.'),
    spacer(),
    body('I understand that as guarantor I am liable for:', true),
    bullet('Any unpaid rent if the tenant defaults on payment.'),
    bullet('Any damage to the property beyond fair wear and tear.'),
    bullet('Any lawful costs incurred by the landlord as a result of the tenant\'s breach.'),
    spacer(),
    ...['Signed: ___________________________', 'Date: ___________________________',
        'Witness Name: ___________________________', 'Witness Signature: ___________________________',
    ].map(f => body(f)),
    spacer(),

    // TERMS
    h1('TERMS OF USE'),
    body('© 2026 Property and Rent Consult. All rights reserved.', true),
    body('This template is licensed for personal and internal business use only. You may use it to screen tenants for properties you own or manage. You may duplicate it as many times as required for your internal business operations.'),
    spacer(),
    body('You may NOT:', true),
    bullet('Resell, redistribute, or republish this template in any form.'),
    bullet('Claim authorship or ownership of this template.'),
    bullet('Modify and sell it as your own product.'),
    body('Violation of these terms may constitute an infringement of Ghanaian copyright law.'),
    body('For licensing enquiries, contact Property and Rent Consult.'),
  ];

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            children: [new TextRun({
              text: 'Property and Rent Consult  |  Tenant Screening Scorecard — Ghana Edition',
              size: 16, color: WARM_GREY, font: 'Calibri',
            })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            children: [new TextRun({ text: '© 2026 Property and Rent Consult', size: 16, color: WARM_GREY, font: 'Calibri' })],
          })],
        }),
      },
      children: sections,
    }],
  });

  return doc;
}

// Build README
function buildReadme(tier, files) {
  const fileRows = files.map((f, i) => dataRow([f.name, f.desc, f.how], [2500, 3500, 3200], i%2===0 ? OFF_WHITE : WHITE));

  const doc = new Document({
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
      children: [
        h1('Thank You for Your Purchase'),
        h2('What\'s Inside This Package'),
        spacer(),
        body('Property and Rent Consult (PRC) is a Ghana-based property and tenancy advisory brand. This product — the Tenant Screening Checklist & Scorecard (Ghana Edition) — gives you a structured, evidence-based system for evaluating every rental applicant before you sign a tenancy agreement.'),
        spacer(),
        new Table({
          width: { size: 9200, type: WidthType.DXA },
          rows: [
            headerRow(['File Name', 'What It Is', 'How to Use It'], [2500, 3500, 3200]),
            ...fileRows,
          ],
        }),
        spacer(),
        h2('Terms of Use'),
        body('For personal and internal business use only. You may use these files to screen tenants for properties you own or manage. Redistribution or resale is not permitted. © 2026 Property and Rent Consult.'),
        spacer(),
        h2('Contact'),
        body('Questions? Email info@propertynrentconsult.com or WhatsApp +233208071633'),
      ],
    }],
  });
  return doc;
}

const basicFiles = [
  { name: 'PRC-Tenant-Scorecard-Printable.pdf', desc: 'Print-ready A4 PDF', how: 'Print one copy per applicant and file with their documents' },
  { name: 'PRC-Tenant-Scorecard-Fillable.pdf', desc: 'Interactive fillable PDF', how: 'Type directly into the form on any device. Save a digital copy per applicant.' },
];
const proFiles = [
  ...basicFiles,
  { name: 'PRC-Tenant-Scorecard-Excel.xlsx', desc: 'Auto-scoring Excel workbook', how: 'Open in Excel or Google Sheets (File > Make a Copy). Enter scores in the yellow cells.' },
  { name: 'PRC-Tenant-Scorecard-Editable.docx', desc: 'Editable Word document', how: 'Open in Word and customise with your company name, logo, or additional questions.' },
];
const agencyFiles = [
  ...proFiles,
  { name: 'PRC-WhatsApp-Card-1.png to Card-5.png', desc: '5 branded WhatsApp image cards', how: 'Share with your team on WhatsApp or post to Instagram Stories.' },
];

async function main() {
  // Scorecard DOCX — Pro and Agency tiers
  for (const [tier, label] of [['Pro_Tier','Pro'], ['Agency_Tier','Agency']]) {
    const doc = buildDoc(label);
    const buf = await Packer.toBuffer(doc);
    const out = join(BASE, tier, 'PRC-Tenant-Scorecard-Editable.docx');
    writeFileSync(out, buf);
    console.log('DOCX saved:', out);
  }

  // README — all three tiers
  const tiers = [
    ['Basic_Tier', basicFiles],
    ['Pro_Tier', proFiles],
    ['Agency_Tier', agencyFiles],
  ];
  for (const [tier, files] of tiers) {
    const doc = buildReadme(tier, files);
    const buf = await Packer.toBuffer(doc);
    const out = join(BASE, tier, 'PRC-READ-ME-FIRST.docx');
    writeFileSync(out, buf);
    console.log('README saved:', out);
  }
}

main().catch(console.error);
