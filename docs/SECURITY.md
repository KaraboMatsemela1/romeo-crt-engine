# Security and Secrets

- Never commit broker tokens, API keys, passwords, certificates, account IDs, or personal trading credentials.
- Use environment variables / local secret stores for development and a managed secret system for deployments.
- `.env` is ignored; `.env.example` contains names only.
- Logs must not print secrets or authentication headers.
- Separate paper and live credentials/accounts.
- Live authorization must require an explicit deployment configuration and should default to disabled.
- Restrict broker API permissions where possible; withdrawal permissions should not be required for trading execution.
