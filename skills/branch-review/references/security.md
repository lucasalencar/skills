# Security

- Injection (SQL, command, template), unsafe deserialization, path traversal.
- AuthN/authZ gaps: missing checks, privilege confusion, insecure direct object references.
- Secrets or credentials in code, logs, or error messages.
- SSRF, unsafe use of `eval`/`exec`/dynamic code loading.
- Missing input validation/sanitization at trust boundaries (external input, file uploads, deserialized payloads).
- Weak or misused cryptography/randomness (e.g. non-CSPRNG for tokens).
