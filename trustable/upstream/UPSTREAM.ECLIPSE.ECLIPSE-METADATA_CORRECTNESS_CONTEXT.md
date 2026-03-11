---
normative: false
---

The [Eclipse Foundation Project Handbook (section Project Resources and Services)](https://www.eclipse.org/projects/handbook/#project-resources-and-services) states that (please refer to the official Eclipse document for definitive and canonical definitions):

---

Eclipse open source projects must keep their project metadata accurate and up-to-date and ensure that project information is consistent and vendor-neutral. This metadata is critical for software build, distribution, governance and legal compliance.

The Eclipse Foundation supports projects with infrastructure (e.g., Git hosting, CI/CD, artifact signing, mailing lists), security services (e.g., vulnerability reporting, security audits), intellectual property (IP) due diligence, governance support, and promotion resources. Correct project metadata ensures these services are applied properly, supports IP compliance, and enables downstream consumers to rely on accurate legal and technical information.

Failure to maintain correct project metadata can lead to IP compliance risks, governance delays (e.g., during reviews), misapplied infrastructure services, and reduced transparency for the community and adopters. Proper metadata management is therefore a core responsibility for all project teams.

---

Evidence for compliance might include (but is not limited to):

* Project repository, including e.g. Cargo.toml, jar index files, etc
* Project CI in some form checking/using/validating metadata
