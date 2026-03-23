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

# tsftemplate Repository

The tsftemplate Repository is a hello-world style template illustrating how to build Trustable Software Framework [TSF](https://codethinklabs.gitlab.io/trustable/trustable/) CI pipelines that automate the collection of TSF statement evidence, the scoring of the resulting TSF tree and generation of a TSF report.

The heart of tsftemplate is a release workflow which serves to illustrate how tsffer and tsflink GitHub actions can be used in CI pipelines to automate the process of collecing TSF evidence, linking it into an existing TSF argument, and performing the scoring and report generation as part of a release flow. The result of this automation is a detailed TSF report published alongside the project documentation, including links to follow up on any evidence that is used to support project TSF statements.

## Trustable Software Framework context

todo

## tsftemplate Vision

This is a diagram representation of what the TSF method enables software development teams to do, and how the approach might be streamlined and automated as much as possible.

![tsftemplate helps to streamline the 3 stages of a TSF-driven software quality process.](docs/img/tsftemplate-vision.drawio.svg "tsftemplate Vision")

## Todos

- describe workflow idea
- describe actual release flow
- describe combination of tools
- document workspace layout
- how-to-extend example
- tsflink README
