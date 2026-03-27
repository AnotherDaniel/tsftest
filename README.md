<!--
 * Copyright (C) 2026 Eclipse Foundation and others. 
 * 
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 * 
 * SPDX-FileType: DOCUMENTATION
 * SPDX-FileCopyrightText: 2026 Eclipse Foundation
 * SPDX-License-Identifier: EPL-2.0
-->

[![TSF Score](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanotherdaniel.github.io%2Ftsftemplate%2Ftrustable%2Fscore.json&query=%24.scores%5B0%5D.score&label=TSF%20Score&color=blue)](https://anotherdaniel.github.io/tsftemplate/trustable/dashboard.html)
[![TSF Report](https://img.shields.io/github/v/release/AnotherDaniel/tsftemplate?label=TSF%20Report&color=green)](https://anotherdaniel.github.io/tsftemplate/trustable/trustable_report_for_tsftemplate.html)

---

<!--
`impl~project-readme~1`
Covers:
- req~project-readme~1
-->

# tsftemplate - a getting-started template for applying the Trustable Software Framework

The `tsftemplate` repository is a hello-world style template illustrating how to build CI pipelines that automate the linking and collection of [Trustable Software Framework (TSF)](https://gitlab.eclipse.org/eclipse/tsf/tsf) statement evidence, the scoring of the resulting TSF graph, and generation of a TSF report.

The heart of `tsftemplate` is a release workflow which serves to illustrate how [`tsffer` ("TSF transfer")](https://github.com/AnotherDaniel/tsffer) and [`tsflink`](https://github.com/AnotherDaniel/tsflink) GitHub actions can be used in CI pipelines to automate the process of collecing TSF evidence, linking it into an existing TSF argument, and performing the scoring and report generation as part of a release flow. The result of this automation is a detailed TSF report published alongside the project release artifacts, including links to follow up on any evidence that is used to support project TSF statements.

## tsftemplate motivation

All Open Source projects typically share one challenge: [they are severly understaffed](https://xkcd.com/2347/ "xkcd 2347"). All idiosyncrasies and best practices pursued by Open Source projects result from this:

- any repetitive tasks must be automated
- developers hate to repeat themselves; all information relevant to the project must be easily accessible, within or very close to the source code repository
- work done for the project must have tangible and plausible benefits; there is no time for make-work and write-only documentation purely for the sake of process

The TSF method aims to be a viable software quality framework for such contexts, by being file-centric, openly available, conceptually simply, and automatable (to a degree). However, applying the method from scratch still comes with a non-trivial learning curve, especially for people who are new to the world of formalized software quality processes.

At the same time, open development models offer unique opportunities for crossing such hurdles, by community-sourcing method-tailoring for frequent scenarios, central touchpoints for related questions and advice, and providing best-practice getting-started templates that showcase how the method could be applied. `tsftemplate` aims to be such a template.

### Trustable Software Framework context

The [Eclipse Trustable Software Framework (TSF)](https://pages.eclipse.dev/eclipse/tsf/tsf/) approach is designed for consideration of software where factors such as safety, security, performance, availability and reliability are considered critical. TSF method asserts that any consideration of trust must be based on evidence.

TSF considers that delivery of software for critical systems must involve identification and management of the risks associated with the development, integration, release and maintenance of the software. In such contexts, software delivery is not complete without appropriate documentation and systems in place to review and mitigate these risks. The Eclipse Trustable Software Framework provides a method and tool consider supply chain and tooling risks as well as the risks inherent in pre-existing or newly developed software, and to apply statistical methods to measure confidence of the whole solution.

The TSF method places an emphasis on integrating well into a typical Open Source development process, by being built around versionable and bite-sized textual statements that get organized in a [DOT graph](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) - thus immediately benefitting from the associated tooling ecosystem. It comes with cli tool for manipulating the TSF dot-graph (`trudag`), immediately suggesting application in CI/automation workflows.

### tsftemplate goals

As a template for applying the TSF method, `tsftemplate` pursues three goals:

1. Be a hello-world style illustration of the overall approach - how is TSF supposed to be applied conceptually, what is the underlying idea?
2. Show how TSF can be integrated into a CI workflow - along with other related tools - to implement an automated pipeline around quality process artifacts.
3. Serve as a copy-paste template for setting up your own TSF-enabled quality process infrastructure.

## The 3 stages of quality process application

For the purposes of structuring TSF application in `tsftemplate`, we posit three activity stages:

1. Tailoring: the scope and extent of quality method application needs to be chosen, and a starting point found.
2. Engineering/application: the tailored method scope needs to be applied in the project, and related statements, evidences and artifacts created and identified.
3. Measuring and reporting: pulling together quality statements, code and documentation evidence and build artifacts, quality assessment and reporting can be done.

![tsftemplate helps to streamline the 3 stages of a TSF-driven software quality process.](docs/img/tsftemplate-vision.drawio.svg "tsftemplate Vision")

Each stage comprises a set of activities and related tools, that `tsftemplate` aims to provide a reference for, and that are described in greater detail below. By providing this starting point, `tsftemplate` wants to provide inspiration about how the approach might be streamlined and automated as much as possible.

### Stage I

Stage I is about defining how a quality method should be applied to an actual project/codebase, and getting set up to integrate the method into regular development workflows as quickly as possible. TSF is designed to grow in scope over time, following the focus areas identified by the project team. Therefore in an Open Source context it is a prime goal to lower the bar to entry, even at the expense of coverage or specificity - that can always be evolved going forward.

Combined with the capability for tool-based manipulation of the TSF statement graph, this offers a unique opportunity: community-driven TSF statement libraries, that build on top of the core TSF tenets (and each other), and provide technology- or context-specific tailoring blocks. For example:

- The Rust programming language comes with extensive language- and compiler-level security features, as well as a very rich tooling ecosystem that extends to managing licensing declarations or built-in CVE tracking and notification across the entire dependency tree: this is an ideal foundation for a Rust-TSF-library, that any Rust project can pull in to get started with applying TSF.
- The Eclipse Foundation defines a comprehensive set of [process](https://www.eclipse.org/projects/dev_process/ "Eclipse Foundation Development Process") and [behavioral guidance](https://www.eclipse.org/projects/handbook/ "Eclipse Foundation Project Handbook") that every Eclipse Foundation Open Source project must adhere to. Again an ideal starting point for EF projects, which can get ahead on TSF application by simply pulling in a Eclipse-TSF-library that codifies the Eclipse-related processes and best practices.

The creation and refinement of such statement libraries would make an ideal TSF community effort, where statement sets could be maintained in a contribution-centric model, allowing the open sharing of best practices for each relevant technology stack or process context.

The TSF library scenario, as illustrated in `tsftemplate`, is shown in the following diagram:

![Lower the bar to entry via community-driven TSF statement libraries](docs/img/tsftemplate-Stage%20I.drawio.svg "tsftemplate Stage I")

***Note***: At the moment, the TSF `trudag` tool does not yet fully support this vision, and there isn't yet a community-contrib model for TSF statement libraries. Therefore, `tsftemplate` operates from a starting point where TSF core tenets plus an Eclipse Process library have been pre-imported into the project TSF graph as starting points.

#### Workflow

1. at project start/when introducing TSF to the project, all relevant TSF context libraries are identified from the TSF contrib repository
2. the project TSF graph is initialized by importing TSF core tenets, plus any contrib statement libraries and their potential dependencies
3. if at any point in the project lifecycle there is a major change to used technology or applied process where a TSF contrib library exists, that could be added into the project graph as necessary

#### Associated tools, related `tsftemplate` file paths

The main tool for manipulating the TSF graph is the [TSF `trudag` tool](https://pages.eclipse.dev/eclipse/tsf/tsf/tools/install.html). `tsftemplate` might provide a devcontainer in the future that comes with `trudag` preinstalled; the main use of the tool happens inside the `tsflink` GitHub action used by `tsftemplate` CI.

`.dotstop.dot`: this is the DOT graph metadata file containing TSF graph nodes, links and freshness hash data.
`trustable/upstream`: this is the upstream TSF statements imported into `tsftemplate`, comprising the core TSF tenets and an Eclipse Process TSF statement library.
`trustable/tsftemplate`: this folder contains all `tsftemplate` project specific TSF statements - refer to the [next section](#stage-ii) for more information.

### Stage II

Once a quality method is selected and initially tailored, the main part of method application begins: the project needs to make specific statements about how it supports demands and guidelines expected by the tailored method (next section](#stage-ii)). For instance: where the quality method requires test automation, the specific project will explain (via a dedicated statement in its TSDF graph, linking to the more generic parent statement) that it uses GitHub action pipelines for any PR merge and release build. Once this conceptual linking is done, the final step is to provide proof of one's assertions - in the example, this might be done by pointing to the CI configuration ruleset that is also part of the repository.

This work is by far the largest part of quality method application, and it is a continual effort that accompanies the development work similar to the writing of test cases or the updating of documentation.
Any and every part of the development work can become the object of TSF statements and supporting evidence, depending on context and desired outcome - code, documentation, specification, configuration, collected performance data, release artifacts like test reports or coverage metrics, and so on.

![Help devs tie together code, docs, specs, CI and TSF monitoring - once](docs/img/tsftemplate-Stage%20II.drawio.svg "tsftemplate Stage II")

The first activity - the detailling of the TSF graph with project-specific statements - is supported by the `trudag` tool, and the fact that all content created that way is expressed as markdown snippets that are managed alongside the project code and all other files.

`tsftemplate` aims to showcase how the second activity - the linking of statement-supporting evidence - can be done in a 'don't repeat yourself' way, such that developers only need to formally declare the relationship between some project artifact and the statement it supports as part of the project CI, to then have both static (eg. code files) and dynamic (eg. release test reports) artifacts pulled into TSF evaluation, scoring and reporting as part of project automation.

### Workflow

1. For TSF areas that the project wants to improve its scoring in, developers consider how they support the TSF goals (compare [Stage I](#stage-ii)); from these considerations, project-specific TSF statements are added (via `trudag`) describing attributes, activities or measures performed by the project to support the stated goal.
2. Each project TSF statement requires supporting evidence to positively contribute to the overall TSF score; therefore developers now implement whatever mechanisms are necessary to provide such evidence, and create links between evidence and supported statement in the project CI using the `tsffer` GitHub action.

### Associated tools, related `tsftemplate` file paths

The main tool for manipulating the TSF graph is the [TSF `trudag` tool](https://pages.eclipse.dev/eclipse/tsf/tsf/tools/install.html). For automating the linking of evidence to project TSF statements, `tsftemplate` uses the [`tsffer` ("TSF transfer")](https://github.com/AnotherDaniel/tsffer) GitHub action. Tsffer action steps simply are provided with the evidence-information and targeted TSF statement IDs, and will during a workflow run record these relationships in little metadata files, which in [Stage III](#stage-iii) get pulled into TSF scoring and report generation.

`trustable/tsftemplate`: this folder contains all `tsftemplate` project specific TSF statements - building on and linking back to the more generic intial TSF graph as composed in [Stage I](#stage-i).
`.github/workflows/release.yml`: this is the `tsftemplate` release workflow, providing some examples of how `tsffer` is used for recording evidence-statement links during a release run.

### Stage III

Enable CI workflows that continually score and deliver TSF quality reporting

![Enable CI workflows that continually score and deliver TSF quality reporting](docs/img/tsftemplate-Stage%20III.drawio.svg "tsftemplate Stage III")

## Todos

- describe workflow idea
- describe actual release flow
- describe combination of tools
- document workspace layout
- how-to-extend example
- tsflink README
