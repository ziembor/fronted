# Email, CK, Mailbox, Mailing List, IP, Hostname and GUID Extractor

A simple single-page web application that extracts email addresses, CK identifiers, LSA codes, shared mailbox names, mailing list names, IPv4 addresses, hostnames, and GUIDs from text input.

## Overview

This tool provides a straightforward interface for parsing text and automatically identifying:
- Email addresses
- CK codes (custom identifier format)
- LSA codes (CK with specific suffixes)
- Shared mailbox names (short `mbx` names or `MBX-WP` followed by digits)
- Mailing list names (`ML-` followed by a name)
- IPv4 addresses
- Hostnames with four dot-separated segments or a recognized prefix
- Standard GUIDs

The extraction happens in real-time as you type or paste content into the input field.

## Features

- **Real-time extraction**: Results update automatically as you type
- **Dual-panel layout**: Input on the left, results on the right
- **Duplicate removal**: Each unique value is listed only once in its section
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
3. View extracted emails, CKs, LSAs, shared mailboxes, mailing lists, IPv4 addresses, hostnames, and GUIDs in the right panel

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

### Shared Mailboxes
Matches whole names case-insensitively using either format:
- `mbx` followed by letters, digits, or underscores, with fewer than 9 characters
  total (3-8 characters).
- `MBX-WP` followed by one or more digits, with no length limit.

Examples: `mbxteam`, `MBX12345`, `MBX-WP123456`.
Longer short-format names such as `mbx123456`, and malformed names such as
`MBX-WP123abc`, are not partially extracted.

### Mailing Lists
Matches whole names starting with `ML-` (case-insensitive), followed by one or
more letters, digits, or underscores, with internal or trailing hyphens allowed.
An empty suffix is not accepted.

Examples: `ML-Team`, `ml-project_123`, `ML-Project-Team`.

### IPv4 Addresses
Matches four numeric octets separated by dots, each containing one to three digits with a value from 0 to 255.

Examples: `192.168.1.10`, `10.0.0.1`, `255.255.255.255`.
Invalid addresses such as `999.168.1.10` are not extracted or listed as hostnames.

### Hostnames
Matches names with exactly four dot-separated segments, or names starting with
`su800`, `sx9`, or `CLRV0` (case-insensitive). Prefixed names may have a single
segment or multiple segments.

Segments contain letters, digits, or internal hyphens, are 1-63 characters long,
and cannot start or end with a hyphen. Names must contain at least one letter
and be at most 253 characters long. IPv4 addresses appear only in their own section.

Examples: `server.site.example.com`, `su800123`, `sx9node`, `CLRV01`,
`SU800123.example.com`.

### GUIDs
Matches hexadecimal GUIDs in the standard `8-4-4-4-12` format, with uppercase
or lowercase letters. Surrounding braces are accepted but not included in results.
No particular UUID version or variant is required.

Examples: `550e8400-e29b-41d4-a716-446655440000`,
`{6F9619FF-8B86-D011-B42D-00C04FC964FF}`.

## Browser Compatibility

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## License

Free to use and modify.
