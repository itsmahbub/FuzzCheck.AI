# FuzzCheck.AI: On the Limitations of DNN Fuzzing to Discover Security Failures


## Overview

Deep neural networks (DNNs) are widely deployed in safety- and security-critical applications and remain vulnerable to adversarial manipulation. DNN fuzzing has emerged as a systematic approach to testing AI model reliability and security. However, DNN fuzzing research remains fragmented across goals, design choices, and evaluation practices, making it unclear how different fuzzing designs enable or limit different security testing objectives. To address this gap, we present **FuzzCheck.AI**, a structured evaluation framework that defines six metrics capturing key security testing objectives and enables systematic, qualitative assessment of DNN fuzzing papers. These metrics capture failure severity, targeted attack discovery, input plausibility, failure reproducibility, root-cause analysis, and attack transferability. We apply **FuzzCheck.AI** to 32 representative DNN fuzzing papers spanning vision, speech, and language models, and find that 72% (23/32) show low compliance with three or more metrics, while none demonstrate high compliance across all six metrics. These findings reveal systematic blind spots and trade-offs in current fuzzing designs, which often prioritize robustness failures and untargeted attack while neglecting attack realism, reproducibility, and cross-model transferability. Based on these findings, we distill actionable recommendations to guide the design of DNN fuzzers for security failure discovery that is realistic, reproducible, and transferable.


This repository contains:

- 📘 Evaluation codebook
- 🤖 LLM-generated and human-corrected assessments
- 📊 Scripts for analysis

---

## Repository Structure

<pre>
AI-FLARE/
├── codebook.json            # Evaluation criteria definitions
├── assessments.json         # LLM outputs + expert-corrected labels with rationale
├── analysis/                # Analysis scripts
│   ├── eval_stats.ipynb
│   └── plots/
└── README.md
</pre>

---

## Framework Overview

![AI-FLARE Framework Overview](./framework-overview.png)

*Figure 1: The AI-FLARE pipeline combining LLM assessments with expert validation.*


## Key Findings

- Oracle design limits vulnerability scope, with no fuzzers detecting privacy leakage or misalignment.
- Goal-directed fuzzing is rare (22.2%) and often reduces input plausibility.
- Cross-architecture generalization is common (55.6%), but cross-domain fuzzing remains rare (13.9%).
- Most fuzzers (80.6%) do not ensure discovered failures persist after saving and reloading inputs.
- Fuzzers exposing invariance violations dominate (86.1%), leaving many safety- and security-critical vulnerabilities underexplored.


## Design Choices of the Selected Fuzzers

| Paper | Access Level | Mutation Strategy | Exploration Strategy | Oracle |
| --- | --- | --- | --- | --- |
| PAIR | Blackbox | Model-driven | Oracle-guided | Property-based |
| PAPILLON | Blackbox | Model-driven | Oracle-guided | Property-based |
| LLM-Fuzzer | Blackbox | Model-driven | Oracle-guided | Property-based |
| Yuan et al. | Greybox | Metamorphic | Coverage-guided | Metamorphic |
| DRFuzz | Blackbox | Noise Injection, Metamorphic | Prediction-guided | Differential |
| DistXplore | Greybox | Rule-guided, Prediction-guided | Coverage-guided | Property-based |
| ASDF | Blackbox | Model-driven, Metamorphic, Rule-guided | Oracle-guided | Differential |
| CARROT | Whitebox | Gradient-guided, Metamorphic | Prediction-guided | Metamorphic |
| MDPFuzz | Blackbox | Noise Injection | Coverage-guided, Oracle-guided | Property-based |
| BET | Blackbox | Noise Injection | Prediction-guided | Differential, Property-based |
| QATest | Blackbox | Metamorphic | Statistical analysis-guided | Metamorphic |
| semSensFuzz | Blackbox | Metamorphic | Unguided | Metamorphic |
| Dola et al. | Whitebox | Gradient-guided | Coverage-guided, Prediction-guided, Statistical analysis-guided | Differential |
| TESTRNN | Greybox | Noise Injection, Metamorphic | Coverage-guided, Oracle-guided | Metamorphic |
| TACTIC | Greybox | Model-driven | Coverage-guided, Prediction-guided | Metamorphic |
| HDTest | Greybox | Noise Injection, Rule-guided | Prediction-guided | Metamorphic |
| CrossASR++ | Blackbox | Model-driven | Oracle-guided | Differential |
| Asyrofi et al. | Blackbox | Model-driven | Oracle-guided | Differential |
| Devil's Whisper | Blackbox | Gradient-guided | Prediction-guided | Property-based |
| Sensei | Blackbox | Metamorphic | Prediction-guided | Metamorphic, Property-based |
| KuK | Blackbox | Noise Injection, Prediction-guided | Prediction-guided | Metamorphic |
| MetaOD | Blackbox | Metamorphic | Oracle-guided | Metamorphic |
| ADAPT | Whitebox | Gradient-guided | Coverage-guided | Metamorphic |
| DeepSearch | Blackbox | Prediction-guided | Prediction-guided | Metamorphic |
| BMI-FGSM | Blackbox | Gradient-guided | Prediction-guided | Property-based |
| CrossASR | Blackbox | Model-driven | Oracle-guided | Differential |
| DeepHunter | Greybox | Metamorphic | Coverage-guided | Metamorphic, Differential |
| TensorFuzz | Greybox | Noise Injection | Coverage-guided | Property-based, Differential |
| DeepStellar | Greybox | Noise Injection, Metamorphic | Coverage-guided | Metamorphic, Property-based |
| Sun et al. | Whitebox | Gradient-guided, Constraint-guided | Coverage-guided | Metamorphic |
| LipFuzzer | Blackbox | Model-driven | Statistical analysis-guided | Metamorphic |
| DeepEvolution | Greybox | Metamorphic | Coverage-guided | Metamorphic, Differential |
| DeepTest | Greybox | Metamorphic | Coverage-guided | Metamorphic |
| DLFuzz | Whitebox | Gradient-guided | Coverage-guided, Prediction-guided | Metamorphic |
| DeepCruiser | Greybox | Metamorphic | Coverage-guided | Metamorphic |
| DeepXplore | Whitebox | Gradient-guided, Metamorphic | Coverage-guided, Oracle-guided | Differential |


## Prevalence of Design Choices in AI Model Fuzzing Papers

![Prevalence of Design Choices](./taxonomy_prevalence.png)


## Per Paper Assessments

| Paper | Year | Exposed Vulnerability Types | Support for Targeted Output Manipulation | Plausibility of Generated Test Inputs | Cross-Architecture Compatibility | Cross-Domain Input Compatibility | Empirical Justification of Feedback Signals | Fuzz-Guided Model Correction | Error Robustness to IO | Reproducibility of Evaluation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAIR | 2025 | Jailbreaks | Yes | Yes | Yes | No | Yes | No | No | No |
| PAPILLON | 2025 | Jailbreaks | Yes | Yes | Yes | No | Yes | No | Yes | Yes |
| LLM-Fuzzer | 2024 | Jailbreaks | Yes | Yes | Yes | No | No | No | No | Yes |
| Yuan et al. | 2023 | Invariance Violation | No | Yes | No | No | Yes | No | No | Yes |
| DRFuzz | 2023 | Invariance Violation | No | Yes | Yes | No | Yes | Yes | No | Yes |
| DistXplore | 2023 | OOD Failure | Yes | Yes | Yes | Yes | Yes | Yes | No | Yes |
| ASDF | 2023 | Invariance Violation | No | Yes | Yes | No | Yes | Yes | Yes | Yes |
| CARROT | 2022 | Invariance Violation | No | Yes | Yes | No | Yes | Yes | No | Yes |
| MDPFuzz | 2022 | Crash/Exception | No | Yes | Yes | Yes | Yes | Yes | No | Yes |
| BET | 2022 | Invariance Violation | Yes | Yes | No | No | No | Yes | Yes | No |
| QATest | 2022 | Invariance Violation | No | Yes | Yes | No | Yes | No | No | Yes |
| semSensFuzz | 2022 | Invariance Violation | No | Yes | Yes | No | - | No | No | Yes |
| Dola et al. | 2021 | Invariance Violation | No | Yes | No | No | No | No | No | Yes |
| TESTRNN | 2021 | Invariance Violation, Backdoor/Trigger | No | Yes | No | Yes | Yes | No | No | Yes |
| TACTIC | 2021 | Invariance Violation | No | Yes | No | No | Yes | No | No | Yes |
| HDTest | 2021 | Invariance Violation | No | Yes | No | No | Yes | Yes | No | No |
| CrossASR++ | 2021 | Invariance Violation | No | Yes | Yes | No | Yes | No | Yes | Yes |
| Asyrofi et al. | 2021 | Invariance Violation | No | Yes | Yes | No | No | Yes | No | Yes |
| Devil's Whisper | 2020 | Invariance Violation | Yes | No | Yes | No | No | No | Yes | Yes |
| Sensei | 2020 | Invariance Violation | No | Yes | No | No | Yes | Yes | No | Yes |
| KuK | 2020 | Invariance Violation | No | Yes | No | No | Yes | No | No | No |
| MetaOD | 2020 | Invariance Violation | No | Yes | Yes | No | Yes | Yes | Yes | Yes |
| ADAPT | 2020 | Invariance Violation | No | Yes | No | No | Yes | No | No | Yes |
| DeepSearch | 2020 | Invariance Violation | No | Yes | Yes | No | No | No | No | Yes |
| BMI-FGSM | 2020 | Invariance Violation | Yes | Yes | Yes | No | No | No | No | No |
| CrossASR | 2020 | Invariance Violation | No | Yes | Yes | No | Yes | No | No | Yes |
| DeepHunter | 2019 | Invariance Violation | No | Yes | No | No | Yes | No | No | No |
| TensorFuzz | 2019 | Invariance Violation, Crash/Exception | No | No | Yes | No | Yes | Yes | No | Yes |
| DeepStellar | 2019 | Invariance Violation | No | Yes | No | Yes | Yes | No | No | No |
| Sun et al. | 2019 | Invariance Violation | No | Yes | No | No | Yes | No | No | Yes |
| LipFuzzer | 2019 | Invariance Violation | Yes | Yes | Yes | No | Yes | No | Yes | No |
| DeepEvolution | 2019 | Invariance Violation | No | Yes | No | No | No | No | No | No |
| DeepTest | 2018 | Invariance Violation | No | Yes | Yes | No | No | Yes | No | No |
| DLFuzz | 2018 | Invariance Violation | No | Yes | No | No | No | Yes | No | Yes |
| DeepCruiser | 2018 | Invariance Violation | No | Yes | No | No | Yes | No | No | No |
| DeepXplore | 2017 | Invariance Violation | No | Yes | No | Yes | Yes | Yes | No | No |

