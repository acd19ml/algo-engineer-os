# Lecture 01 - Introduction to Artificial Intelligence

**Course**: CS5491: Artificial Intelligence
**Instructors**: Jianyuan Guo, Zhichao Lu
**Content Credits**: Prof. Wei's CS4486 Course & Prof. Boddeti's AI Course

---

## 1. What Can AI Do?

### 1.1 Current AI Capabilities (Perception)
- **Object & Face Recognition**
- **Scene Segmentation**
- **Image Classification**
- **Image Captioning**

### 1.2 Natural Language Processing
- **Question Answering**
- **Machine Translation**
- **Sentiment Analysis**
- **Web Search**

### 1.3 Speech
- **Automatic Speech Recognition (ASR)**
- **Text-to-Speech Synthesis (TTS)**
- **Speaker Verification**
- **Chatbots**

### 1.4 Robotics
- Self-driving cars
- Warehouse robots (e.g., Amazon)
- Rescue robots
- Soccer robots

### 1.5 Game Playing
- AI systems capable of superhuman performance in games

### 1.6 What AI Cannot Do (Yet) — "Threshold Test"
| Task | AI Capable? |
|------|------------|
| Play table tennis (decent level) | ? |
| Play Jeopardy | ✓ (Watson) |
| Drive on a curving mountain road | ? |
| Drive safely on Grand River Ave | ? |
| Buy groceries online | ? |
| Buy groceries from physical store | ✗ |
| Discover/prove math theorems | Partially |
| Converse for an hour | Partially |
| Fold laundry | ✗ |
| Write funny stories | Partially |

---

## 2. What Is AI?

### 2.1 Four Classical Definitions (2×2 Matrix)

|  | **Like Humans** | **Rationally** |
|--|-----------------|----------------|
| **Think** | Cognitive Science / Neuroscience | Logic & Automated Reasoning |
| **Act** | Turing Test | Intelligent Agents |

> The course focuses on **Acting Rationally** — the "Intelligent Agents" quadrant.

---

## 3. Acting Humanly — The Turing Test

### 3.1 Background
- Proposed by **Alan Turing in 1950**
- Original question: *"Can machines think?"* → reframed as *"Can machines behave intelligently?"*
- Provides an **operational definition** of intelligence

### 3.2 How It Works
- A human interrogator communicates (in writing) with both a human and an AI
- If the interrogator cannot reliably distinguish AI from human → AI "passes"

### 3.3 Attempts to Pass the Turing Test
| Era | System | Notes |
|-----|--------|-------|
| 1960s | **ELIZA** (Joseph Weizenbaum) | Pattern-matching chatbot |
| 1990s | **ALICE** | Natural language AI |
| Ongoing | **Loebner Prize** | Annual competition |

> **Key fact**: No machine has fully passed the Turing test yet.

### 3.4 Application: CAPTCHA
- **C**ompletely **A**utomatic **P**ublic **T**uring test to tell **C**omputers and **H**umans **A**part
- Inverted Turing test — humans prove they are NOT machines

### 3.5 Critical Question
> *Why would we want to replicate human behavior, including imperfections?*

This motivates moving from "Acting Humanly" to "Acting Rationally."

---

## 4. Acting Rationally

### 4.1 Definition of Rationality
- **Do the right thing** — not merely "whatever humans think or act"
- Two notions of "right":
  - **Logic**: Conclusions are provable from inputs
  - **Economics**: Utility of outcomes is maximized

### 4.2 Important Distinctions
| Misconception | Reality |
|---------------|---------|
| Irrational = insane | Irrational just means sub-optimal |
| Rational = successful | Rational action may still fail (incomplete knowledge, uncontrollable circumstances) |

> **Key insight**: Rationality concerns *what decisions are made*, NOT the thought process behind them.

### 4.3 AI as Rational Machines
- **Rational**: maximally achieving pre-defined goals
- Goals expressed via **utility of outcomes**
- Being rational = **maximizing expected utility**

### Core Theme of Course
> **MAXIMIZE YOUR EXPECTED UTILITY**

---

## 5. Designing Rational Agents

### 5.1 Key Definitions
- **Agent**: an entity that **perceives** and **acts**
- **Rational agent**: selects actions that **maximize its (expected) utility**

### 5.2 What Determines the Right Technique?
The characteristics of:
1. **Percepts** (what the agent senses)
2. **Environment** (where the agent operates)
3. **Action space** (what the agent can do)

→ These dictate which AI technique to use.

### 5.3 Example: Pac-Man as an Agent
- **Percepts**: current game state (ghost positions, food locations)
- **Actions**: move up/down/left/right
- **Goal**: maximize score (eat food, avoid ghosts)

---

## 6. Course Goals

- Have fun learning AI
- Understand core ideas beyond the hype
- Learn **key techniques and algorithms**
- Apply AI to **real-world problems**
- Inspire research thinking

> **Scope**: This course is NOT primarily about vision, NLP, or machine learning — it focuses on **classical AI** (search, planning, optimization, reasoning).

---

## 7. A Short History of AI

### 7.1 Pre-History (400 B.C. – )
| Field | Contribution |
|-------|-------------|
| Philosophy | Mind/body, dualism, materialism |
| Mathematics | Logic, probability, decision theory, game theory |
| Cognitive psychology | Understanding of mind |
| Computer engineering | Hardware foundations |

### 7.2 Birth of AI (1943–1956)
| Year | Event |
|------|-------|
| 1943 | McCulloch & Pitts: simple neural network model |
| 1950 | Turing test proposed |
| 1955–56 | Newell & Simon: Logic Theorist |
| **1956** | **Dartmouth Conference** — term "Artificial Intelligence" officially adopted (McCarthy, Minsky, Rochester, Shannon) |

### 7.3 Early Success (1950–1960)
| Year | Achievement |
|------|-------------|
| 1952 | Arthur Samuel: checkers program with self-play learning |
| 1958 | McCarthy: LISP language, advice taker, time sharing |
| 1958 | Rosenblatt: Perceptron learns to recognize letters |
| 1968–72 | Shakey the robot (uses **A\* algorithm**) |
| 1971–74 | Blocksworld planning and reasoning |

### 7.4 First AI Winter (Late 1970s)
- **1969**: Minsky & Pappert's *"Perceptrons"* — proved single-layer networks cannot represent XOR
- **1973**: Lighthill Report ends AI funding in UK
- **1970**: DARPA cuts funding for AI projects

> **Lesson**: Over-promising leads to funding collapse.

### 7.5 Expert Systems Era (1970–1980)
- Approach: encode domain expert knowledge as **logical rules**
- Notable systems:
  - **DENDRAL** (molecular structure prediction)
  - **MYCIN** (medical diagnosis)
- 1981: Japan's "fifth generation" computer project (Prolog-based)
- 1982: **R1** — expert system for configuring DEC computer orders

### 7.6 Focus on Applications (1990–2010)
| Year | Milestone |
|------|-----------|
| 1997 | **Deep Blue** defeats Garry Kasparov (chess) |
| 2001–10 | $60B in combinatorial sourcing auctions |
| 2005/07 | Stanford & CMU win DARPA Grand Challenge (autonomous driving) |
| 2011 | **IBM Watson** defeats humans on Jeopardy |

### 7.7 Reemergence of AI (2010–Present)
| Year | Milestone |
|------|-----------|
| 2012 | **AlexNet** wins ImageNet — deep learning revolution begins |
| 2013 | DeepMind: computer learns Atari games from pixels |
| 2015–17 | Superhuman speech recognition |
| 2015+ | Generating realistic fake images & video (GANs) |

> Big tech (Google, Facebook, Microsoft, Amazon) all established major AI labs.

---

## 8. Where Does AI Fit?

```
AI
├── Machine Learning
│   ├── Deep Learning
│   └── Statistical Learning
├── Search & Planning
├── Knowledge Representation
├── Natural Language Processing
├── Computer Vision
└── Robotics
```

---

## 9. Reading Assignments

| Lecture | Reading |
|---------|---------|
| Today (Lecture 1) | RN Chapter 1 and 2 |
| Next (Lecture 2) | RN Chapter 3.1–3.4 |

> **RN** = *Artificial Intelligence: A Modern Approach* by Russell & Norvig

---

## 10. Key Concepts Summary

| Concept | Definition |
|---------|-----------|
| AI | Science of making machines that think/act like humans or rationally |
| Turing Test | Test of intelligent behavior via indistinguishability from humans |
| CAPTCHA | Inverted Turing test |
| Rational Agent | Entity that perceives, acts, and maximizes expected utility |
| Expected Utility | Weighted average of outcomes, used as optimization objective |
| AI Winter | Period of reduced funding/interest due to unmet expectations |

---

## 11. Personal Notes & Reflections

- The **4-quadrant framework** (think/act × humanly/rationally) is a clean mental model for positioning different AI approaches.
- The shift from "acting humanly" to "acting rationally" is fundamental — it allows rigorous mathematical formulation (utility maximization).
- **History lesson**: AI winters warn against hype. The current AI boom (post-2012 deep learning) needs to deliver practical value.
- The **Pac-Man agent** analogy is a useful pedagogical tool: simple enough to reason about, rich enough to illustrate key agent concepts.
- Course emphasis on **classical AI** techniques (search, CSP, optimization) provides the foundation that makes modern ML interpretable.
