# PRC Website — propertyandrentconsult.com

Astro static site for Property and Rent Consult. Companion document: PRC_Website_Master_Brief.docx (ref PRC-WEB-BRF-2026-01).

## Run locally
    npm install
    npm run dev        # http://localhost:4321
    npm run build      # outputs to dist/

## Deploy to Netlify
1. Push this folder to a Git repository (GitHub).
2. In Netlify: Add new site → Import from Git → select the repo. netlify.toml already sets build command and publish dir.
3. Point www.propertyandrentconsult.com DNS at Netlify.
Forms (lead-magnet, consultation, contact) use Netlify Forms via data-netlify="true" — enable form notifications in the Netlify dashboard.

## Before launch (placeholders to replace)
- [price] on /products/ pages and Selar URLs (SELAR_URL constants)
- WhatsApp number: search for wa.me/233000000000
- Rent Control directory data: src/pages/resources/rent-control-offices.astro (load the 65-office dataset)
- Privacy and Terms final text
- Lead magnet PDF delivery (connect form to email provider)
- Review /services/ and /disclaimer/ boundaries text against Civil Service code-of-conduct rules

## Adding articles
Drop a .md file into src/content/knowledge/ with the frontmatter fields: title, description, topic (Advance Rent | Agreements | Rent Control | Eviction | Compliance), pubDate, lastReviewed. It publishes automatically.
