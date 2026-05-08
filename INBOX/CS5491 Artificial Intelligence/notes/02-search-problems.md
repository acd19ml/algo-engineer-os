# Lecture 02 - Search Problems

**Course**: CS5491: Artificial Intelligence
**Reading**: RN Chapter 3.1–3.4

---

## 1. Reminder: Rational Agents

- **Agent**: an entity that perceives and acts
- **Rational agent**: selects actions that maximize its (expected) utility
- Characteristics of percepts, environment, and action space dictate which techniques to use

### Key Questions About Rational Agents

| Question | Answer |
|----------|--------|
| Are rational agents omniscient? | **No** — limited by what they can perceive |
| Are rational agents clairvoyant? | **No** — lack knowledge of environment dynamics |
| Do rational agents explore and learn? | **Yes** — essential in unknown environments |

> **Conclusion**: Rational agents are not necessarily *successful*, but they are **autonomous**.

---

## 2. PEAS Framework

PEAS = **P**erformance Measure · **E**nvironment · **A**ctuators · **S**ensors

### Example 1: Pac-Man Agent

| PEAS Component | Detail |
|----------------|--------|
| **Performance Measure** | -1 per time step; +10 food; +500 win; -500 die; +200 hit scared ghost |
| **Environment** | Pac-Man dynamics + ghost behavior |
| **Actuators** | North, West, East, South, Stop (idle) |
| **Sensors** | Entire state is visible |

### Example 2: RoboTaxi Agent

| PEAS Component | Detail |
|----------------|--------|
| **Performance Measure** | Income, happy customers, vehicle costs, fines, insurance |
| **Environment** | Streets, other drivers, customers |
| **Actuators** | Steering, brake, gas, display/speaker |
| **Sensors** | Cameras, LiDAR, radar, ultrasonic, accelerometer, microphone |

---

## 3. Environment Categorization

| Property | Pac-Man | RoboTaxi |
|----------|---------|----------|
| Observable | **Fully** | **Partially** |
| Agent Type | **Multi** | **Multi** |
| Determinism | **Deterministic** | **Stochastic** |
| Dynamics | **Static** | **Dynamic** |
| Space | **Discrete** | **Continuous** |

### Definitions

- **Fully Observable**: agent can see complete state at all times
- **Partially Observable**: agent has limited/noisy sensor data
- **Deterministic**: action outcomes are predictable
- **Stochastic**: actions have uncertain outcomes
- **Static**: environment doesn't change while agent deliberates
- **Dynamic**: environment changes even when agent isn't acting
- **Discrete**: finite number of states and actions
- **Continuous**: states/actions are real-valued

---

## 4. Types of Agents

### 4.1 Reflex Agents
- Choose actions based on **current observation** (and maybe memory)
- May maintain a model of the world's current state
- **Do NOT consider future consequences** of actions
- Consider how the world **IS**
- Question: *Can a reflex agent be rational?*
  - Only if the environment is fully observable and deterministic

### 4.2 Planning Agents
- Decisions based on **predicted consequences** of actions
- Must have a **transition model**: how the world evolves in response to actions
- Must formulate a **goal**
- Consider how the world **WOULD BE**

#### Spectrum of Deliberativeness
| Approach | Description |
|----------|-------------|
| **Offline Planning** | Generate complete, optimal plan first, then execute |
| **Online Planning** | Generate simple/greedy plan, start executing, **replan** if necessary |

---

## 5. Search Problems

### 5.1 Formal Definition

A search problem consists of:

| Component | Description |
|-----------|-------------|
| **State Space** | Set of all possible states |
| **Successor Function** | Given a state → returns (action, next_state, cost) pairs |
| **Start State** | Initial state of the agent |
| **Goal Test** | Function that checks if a state is the goal |

> **Solution**: A sequence of actions (a **plan**) that transforms the start state into a goal state.

### 5.2 Key Insight: Search Problems Are Models
- They are **abstractions** of real-world problems
- We discard irrelevant details and keep only what matters for planning

---

## 6. Example: Traveling in Romania

**Goal**: Travel from Arad to Bucharest

| Component | Value |
|-----------|-------|
| **State Space** | Cities in Romania |
| **Successor Function** | Roads between cities (cost = distance) |
| **Start State** | Arad |
| **Goal Test** | Is current state == Bucharest? |

- The solution is the **sequence of cities** forming the shortest/optimal path.

---

## 7. World State vs. Search State

| Concept | Description |
|---------|-------------|
| **World State** | Includes **every** last detail of the environment |
| **Search State** | Keeps **only** details necessary for planning |

### Example: Pac-Man State Spaces

#### Problem 1: Pathing (just reach a location)
| Component | Value |
|-----------|-------|
| States | `(x, y)` position |
| Actions | N, E, W, S |
| Successor | Update location |
| Goal Test | `(x, y) == END` |

#### Problem 2: Eat-All-Dots
| Component | Value |
|-----------|-------|
| States | `(x, y)` + boolean for each dot |
| Actions | N, E, W, S |
| Successor | Update location + update dot booleans |
| Goal Test | All dot booleans are `False` |

---

## 8. Search Space Size

**World State Variables** (Pac-Man example):

| Variable | Count |
|----------|-------|
| Agent positions | 120 |
| Food count | 30 dots |
| Ghost positions | 12 |
| Agent orientation | 4 (NEWS) |

**State Space Sizes**:

| Problem | Formula | Meaning |
|---------|---------|---------|
| Total world states | `120 × 2^30 × 12 × 4` | Astronomically large |
| Pathing only | `120` | Just position |
| Eat-all-dots | `120 × 2^30` | Position + which dots remain |

> **Key Insight**: Proper state abstraction dramatically reduces the search space. Only include variables that affect future decisions.

---

## 9. Summary

| Concept | Key Point |
|---------|-----------|
| Rational Agent | Maximizes expected utility; autonomous but not omniscient |
| PEAS | Framework for specifying agent design |
| Reflex Agent | Reacts to current state; no future planning |
| Planning Agent | Uses transition model to predict consequences |
| Search Problem | (State Space, Successor Function, Start State, Goal Test) |
| Solution | Sequence of actions from start → goal |
| State Abstraction | Keep only planning-relevant details to reduce state space |

---

## 10. Reading

- **This lecture**: RN Chapter 3.1–3.4
- **Next lecture**: RN Chapter 3.1–3.4 (continued — uninformed search algorithms)
