# InvoiceFlow

> A workspace for understanding, validating, and testing UAE e-invoices — with a built-in AI assistant.

![HTML](https://img.shields.io/badge/Frontend-HTML5-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
![Python](https://img.shields.io/badge/Backend-Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)

InvoiceFlow takes a UAE **PINT-AE XML e-invoice**, converts it into a human-readable invoice, validates it against common UAE compliance rules, lets you intentionally generate broken invoices for testing, and answers questions about the invoice in plain English.

If you have no idea what any of that means yet—that's perfectly fine. This README starts from the basics.

---

# Table of Contents

- [What Problem Does This Solve?](#what-problem-does-this-solve)
- [The 60-Second Background](#the-60-second-background)
- [Features](#features)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [Deploy on Vercel](#deploy-on-vercel)
- [Run Locally](#run-locally)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Limitations](#limitations)
- [Glossary](#glossary)

---

# What Problem Does This Solve?

Traditional invoices are designed for humans.

UAE e-invoices are designed for **computers**.

Instead of receiving a PDF or printed invoice, businesses exchange invoices as **structured XML documents** following the **PINT-AE** standard.

Unfortunately:

- XML invoices are difficult for humans to read.
- Tiny mistakes cause invoices to be rejected.
- Debugging validation failures is frustrating.
- Practicing with intentionally broken invoices is difficult.

**InvoiceFlow** solves these problems.

Simply upload a PINT-AE invoice and the application will:

- 📄 Render it into a clean invoice
- ✅ Validate compliance
- ⚠ Explain errors in plain English
- 🧪 Simulate broken invoices
- 🤖 Answer questions about the invoice

---

# The 60-Second Background

Here are a few terms you'll encounter.

| Term | Meaning |
|-------|---------|
| **PINT-AE** | UAE's official e-invoice XML format |
| **Schematron** | Rulebook used to validate invoices |
| **ASP** | Accredited Service Provider that validates and routes invoices |
| **Peppol** | International secure e-invoicing network |
| **TRN** | UAE Tax Registration Number |

---

# Features

InvoiceFlow consists of a **Pre-flight Upload Stage**, four workspace tabs, and an AI assistant.

---

## 🚀 Pre-flight Upload

Before an invoice enters the workspace, InvoiceFlow performs a preliminary inspection.

### Left Panel

- Extracts key Business Terms (BT-1 → BT-115)
- Parses seller & buyer details
- Displays totals
- Checks basic compliance
- Detects fatal validation issues

### Right Panel

Displays:

- Raw XML
- Syntax highlighting
- Scrollable viewer
- Easy cross-referencing

---

## 📄 View

Transforms unreadable XML into a familiar invoice.

Includes:

- Seller information
- Buyer information
- Invoice lines
- VAT summary
- Total payable

Also supports:

- Print
- Save as PDF

---

## 📑 Details

Shows decoded invoice metadata.

Examples include:

- BT-1
- BT-31
- BT-110

Along with:

- Tax categories
- VAT subtotals
- Currency
- Local UAE guidelines

---

## ✅ Validation

Runs a heuristic UAE compliance engine.

Checks include:

- Missing mandatory fields
- Invalid TRNs
- VAT calculations
- Structural consistency
- Mathematical tolerances (±0.1 AED)

Every issue includes:

- Severity
- Rule ID
- Explanation
- Suggested fix

---

## 🧪 Test Lab

Generate intentionally broken invoices.

Examples:

- Missing Seller TRN
- Invalid VAT
- Incorrect totals
- Missing invoice number

Useful for learning how validation behaves before production deployment.

---

## 🤖 AI Assistant

The assistant understands the currently loaded invoice.

Ask questions like:

- Is my invoice valid?
- Explain this VAT calculation.
- What is a Peppol Access Point?
- Why did validation fail?
- Explain UAE e-invoicing.

When connected to the backend:

- Uses a live LLM.

When offline:

- Falls back to built-in knowledge.

---

# How It Works

```
Browser
┌────────────────────────────┐
│ Upload XML                 │
│ Pre-flight Parser          │
│ Invoice Renderer           │
│ Validation Engine          │
│ Test Lab                   │
│ Chat Interface             │
└──────────────┬─────────────┘
               │ POST /api/chat
               ▼
Server (Optional)
┌────────────────────────────┐
│ chat.py                    │
│ Stores API key             │
│ Calls LLM                  │
│ Returns response           │
└────────────────────────────┘
```

Everything except live AI chat runs **entirely inside your browser**.

No invoice data is uploaded during:

- Preview
- Parsing
- Validation
- Rendering

---

# Quick Start

## Option 1

Open:

```
index.html
```

Then:

1. Load sample invoice
2. Load non-compliant sample
3. Upload your own PINT-AE XML
4. Explore validation results

---

# Deploy on Vercel

Push the repository to GitHub.

Create a new Vercel project.

Add an environment variable:

```
ANTHROPIC_API_KEY
```

Redeploy.

Your AI assistant is now live.

---

# Run Locally

Open directly:

```
index.html
```

Everything works except live AI.

To enable AI locally:

```bash
npm i -g vercel

cd invoiceflow

vercel env add ANTHROPIC_API_KEY

vercel dev
```

---

# Project Structure

```
.
├── index.html
├── api
│   └── chat.py
├── requirements.txt
├── vercel.json
└── README.md
```

---

# Tech Stack

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript (ES6)
- DOMParser API

## Backend

- Python
- Vercel Serverless Functions
- Anthropic API

---

# Limitations

### Validation Engine

InvoiceFlow implements heuristic UAE validation rules.

It is **not** the official government Schematron validator.

Always verify invoices using the official UAE sandbox before production.

---

### No Data Storage

InvoiceFlow stores nothing permanently.

Everything lives inside the browser session.

Refreshing the page clears:

- invoices
- validation results
- AI conversations

---

# Glossary

| Term | Meaning |
|------|---------|
| **e-Invoice** | Structured invoice readable by computers |
| **PINT-AE** | UAE's official XML invoice format |
| **XML** | Structured markup language |
| **Schematron** | Validation rules |
| **Validation** | Checking compliance against rules |
| **ASP** | Accredited Service Provider |
| **TRN** | Tax Registration Number |
| **Tax Category** | VAT classification codes |
| **Business Term (BT)** | Standardized invoice field IDs |

---

# Disclaimer

InvoiceFlow is an **independent educational and validation workspace**.

It is **not affiliated with the UAE Federal Tax Authority (FTA)** and does **not constitute legal, tax, or accounting advice**.
