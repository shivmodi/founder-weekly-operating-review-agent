# How to fork and use Founder Weekly Operating Review Agent

This guide is for a founder or operator who wants to adapt the repo without turning it into a generic portfolio project.

## First pass

1. Fork the repo.
2. Rename it for your company or operating workflow.
3. Read the README Quick Start section.
4. Replace sample inputs, templates, or context files with your own company context.
5. Run the workflow if executable, or copy the first template if it is a playbook.
6. Open the main output listed in the README before changing deeper logic.

## Company fork path

1. Click Fork.
2. Rename the repo if needed.
3. Replace `examples/weekly_metrics.csv` with your weekly metrics.
4. Replace `examples/company_context.md` with company context.
5. Run the weekly review command.
6. Move decisions into Linear, Asana, ClickUp, Notion, or your internal ops tracker.

## Non-technical path

- Replace one CSV: `examples/weekly_metrics.csv`.
- Edit one context file: `examples/company_context.md`.
- Run one command.
- Read one output first: `outputs/demo/weekly_operating_review.md`.

## Data safety

The included sample data is synthetic, anonymized, or template-only unless a public source is explicitly documented. Do not commit private customer, prospect, employee, investor, borrower, merchant, payment, or company data to a public fork.

## Tools to connect later

Start with files first. After the workflow is useful, connect outputs to Google Sheets, Notion, Airtable, HubSpot, Pipedrive, Attio, Linear, Asana, ClickUp, Slack, or your internal ops tracker where relevant.
