# Security policy

Do not report credentials, private repository contents, proprietary Unreal project assets, or customer data in public issues.

This repository contains guidance and local validation tools rather than a hosted service. Security-sensitive changes should still be reviewed for:

- unsafe path handling or source overwrite;
- command injection in shell and PowerShell templates;
- accidental collection or publication of secrets;
- untrusted repository or web content being treated as instructions;
- examples that expand Unreal editor, file-system, network, or packaging permissions without an explicit need.

Use GitHub private vulnerability reporting when available. Otherwise contact the repository owner privately and provide the affected path, reproduction, impact, and a minimal remediation proposal.
