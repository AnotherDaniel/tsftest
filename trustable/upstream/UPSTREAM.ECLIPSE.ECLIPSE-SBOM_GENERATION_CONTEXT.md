---
normative: false
---

[Eclipse Foundation Project Handbook (section Software Bill of Materials)](https://www.eclipse.org/projects/handbook/#sbom) states that (please refer to the official Eclipse document for definitive and canonical definitions):

---

All Eclipse open source projects are encouraged to generate Software Bills of Materials (SBOMs) for their software. SBOMs provide a comprehensive inventory of all software components and dependencies, enabling improved supply chain security, effective vulnerability management, regulatory compliance, efficient development, and faster incident response. Additional guidance and best practices are available in the [Eclipse Foundation Security Handbook](https://eclipse-csi.github.io/security-handbook/index.html).

Projects should follow these core practices when generating SBOMs:

* Use standard formats: Create SBOMs in recognized formats such as SPDX or CycloneDX.
* Provide resolvable coordinates: Identify components unambiguously using formats such as Package URL (pURL) to specify namespace, name, and version.
* Identify licenses accurately: Include correct license information for project files and third-party dependencies.
* Distribute SBOMs with artifacts: Publish SBOMs alongside the corresponding build artifacts (e.g., with Maven artifacts).
* Support SBOM generation by others: Ensure clear copyright headers, SPDX-License-Identifiers, and accurate metadata to make it easy for adopters to generate their own SBOMs.

By following these practices, projects help ensure the security, compliance, and quality of their software while supporting the broader open-source ecosystem.

---

Evidence for compliance might include (but is not limited to):

* SBOM information e.g. as part of releases
