# Email and CK Extractor

A simple single-page web application that extracts email addresses, CK identifiers, and LSA codes from text input.

## Overview

This tool provides a straightforward interface for parsing text and automatically identifying:
- Email addresses
- CK codes (custom identifier format)
- LSA codes (CK with specific suffixes)

The extraction happens in real-time as you type or paste content into the input field.

## Features

- **Real-time extraction**: Results update automatically as you type
- **Dual-panel layout**: Input on the left, results on the right
- **Duplicate removal**: Each unique email/CK is listed only once
- **Count display**: Shows the total number of found items
- **No dependencies**: Pure HTML, CSS, and vanilla JavaScript
- **Single file**: Everything in one HTML file for easy deployment

## What is a CK?

A CK is a specific identifier format consisting of:
- 2 letters + 2 numbers + 2 letters (e.g., `AB12CD`)
- Optionally prefixed with `AD\` or `ADACC\` (e.g., `AD\AB12CD`, `ADACC\AB12CD`)

## What is an LSA?

An LSA is a CK identifier with a specific suffix:
- A CK followed by one of: `LSA`, `LSAA`, `T`, `A`, or `D`
- Examples: `AB12CDLSA`, `AD\XY34ZWLSAA`, `PQ56RST`, `ADACC\MN78GHA`

Note: LSAs are extracted separately from CKs. If a code matches the LSA pattern, it will only appear in the LSA section.

## Usage

1. Open `index.html` in any modern web browser
2. Paste or type your text into the left panel
3. View extracted emails, CKs, and LSAs in the right panel

No installation or server required.

## Detection Patterns

### Email Addresses
Matches standard email format: `name@domain.extension`

Regex: `/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g`

### CK Identifiers
Matches the pattern: `[AD\|ADACC\]LetterLetterNumberNumberLetterLetter`

Regex: `/(?:AD\\|ADACC\\)?[A-Za-z]{2}\d{2}[A-Za-z]{2}\b/g`

Examples:
- `AB12CD`
- `AD\XY34ZW`
- `ADACC\PQ56RS`

### LSA Identifiers
Matches the pattern: `[AD\|ADACC\]LetterLetterNumberNumberLetterLetter[LSA|LSAA|T|A|D]`

Regex: `/(?:AD\\|ADACC\\)?[A-Za-z]{2}\d{2}[A-Za-z]{2}(?:LSAA|LSA|[TAD])\b/g`

Examples:
- `AB12CDLSA`
- `XY34ZWLSAA`
- `AD\PQ56RST`
- `ADACC\MN78GHA`
- `KL90JKD`

## Browser Compatibility

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## License

Free to use and modify.
