# Security Policy

## Supported Versions
We provide security fixes for the following versions:

| Version  | Supported |
|---------:|:---------:|
| 0.4.x    | ✅        |
| 0.3.x    | ✅        |
| 0.2.x    | ✅        |
| 0.1.x    | ⚠️ Critical fixes only (if feasible) |
| < 0.1.0  | ❌        |

## Reporting a Vulnerability
Please **do not** open a public issue for security matters.

- Use **GitHub → Security → “Report a vulnerability”** (private advisory), or  
- Email: <martinjs@uma.es>

Provide a minimal, reproducible example if possible, affected version(s), and any CVE references.

## Response Timeline
- **Acknowledgement:** within **5 business days**  
- **Initial assessment:** within **7 days**  
- **Fix & coordinated disclosure:** target **30 days** (severity-dependent)

We will credit reporters (unless you request anonymity) and coordinate disclosure once a patch/release is available.

## Scope
Vulnerabilities affecting:
- Ontology artifacts distributed in this repo (TTL/OWL), SHACL shapes, docs site and build scripts.
- Supply chain of this repository (GitHub Actions workflows, published releases).

Out of scope: issues in *downstream* forks, third-party libraries, or unrelated infrastructure.

## PGP (optional)
If you prefer encrypted email, publish your key and add the fingerprint here.
