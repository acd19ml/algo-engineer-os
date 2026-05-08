# CityU CS5491 Tutorial on MDP and RL

Source PDF: `INBOX/CS5491 Artificial Intelligence/tutorial/week10_mdp_rl_tutorial_solution.pdf`

> **【新增中文总注释：本讲学习目标】**
>
> 这份 tutorial 实际上有两条主线：
>
> 1. **MDP / Value Iteration**：当环境模型已知，也就是你知道状态、动作、转移概率、奖励和折扣因子时，怎样用 Bellman equation 一步步算出每个 state 的 value。
> 2. **Reinforcement Learning / Approximate Q-learning**：当环境模型不一定完整已知，但你不断观察到 transition sample $(s,a,r,s')$ 时，怎样用样本更新 $Q(s,a)$，再由 $Q$ 选择动作。
>
> 学习时要特别区分三个量：**reward 是“这一步拿到的即时分数”**，**value 是“从这个状态出发未来总共能拿多少的期望”**，**q-value 是“在这个状态先做某个动作以后未来总共能拿多少的期望”**。很多题目的第一笔都不是直接写答案，而是先写清楚：当前在算 $V$ 还是 $Q$，当前用的是旧值还是新值，当前状态是不是 terminal state。

## Markov Decision Processes Recap

- A Markov Decision Process (MDP) is similar to a state transition system. It has states, actions, a transition function $T(s,a,s')$ specifying the probability an agent ends up in state $s'$ when he takes action $a$ from state $s$, a distribution over start states, and possibly a set of terminal states. It also has a reward function $R(s,a,s')$, which represents the reward that an agent receives for performing action $a$ in state $s$ and ending up in state $s'$.
- A q-state is a `(state, action)` pair. From a state $s$, the agent chooses an action $a$, and then from that q-state $(s,a)$, the transition function chooses the resulting state $s'$.
- The utility of a state is not just the reward associated with that state; it also depends on what is going to happen in the future. We can define the utility of a sequence of rewards $[r_0,r_1,r_2,\ldots]$ as

$$
U([r_0,r_1,r_2,\ldots])=\gamma^0r_0+\gamma^1r_1+\gamma^2r_2+\cdots
$$

for some $0 \le \gamma \le 1$. If $\gamma \ne 1$, the sum will converge, so the utilities will be finite; this is called temporal discounting.

- The value of a state $s$ is the total expected future utility given that the agent is currently in state $s$. Similarly, the q-value of a q-state $(s,a)$ is the total expected future utility given that the agent is currently in state $s$ and has just taken action $a$. Under an optimal policy, the value and q-value are denoted $V^*(s)$ and $Q^*(s,a)$.
- The Bellman equations specify the relationship between $V^*(s)$ and $Q^*(s,a)$:

$$
V^*(s)=\max_a Q^*(s,a)
$$

$$
Q^*(s,a)=\sum_{s'}T(s,a,s')\left(R(s,a,s')+\gamma V^*(s')\right)
$$

- Plugging the second Bellman equation into the first gives a recursive definition of $V^*(s)$. We can approximate $V^*(s)$ by $V^*_k(s)$, the optimal value considering only the next $k$ time steps. As $k \to \infty$, $V^*_k \to V^*(s)$. To compute $V^*$, use value iteration: initialize $V^*_0(s)=0$ for all $s$, then given $V^*_i$, plug it into the Bellman equations to compute $V^*_{i+1}$, and repeat until convergence. Policy iteration is a similar process but updates the policy instead of the values. Often, the policy will converge before the values do.

> **【新增中文注释：MDP 与 Bellman update 的核心】**
>
> 看到 MDP 题，先从题干找五件事：状态 $S$、动作 $A$、转移概率 $T$、奖励 $R$、折扣因子 $\gamma$。本题问的是 value iteration，没有给定固定 policy，所以默认求 **optimal value**。
>
> 对普通状态，第一笔写 Bellman optimal update：
>
> $$
> V_{k+1}(s)=R(s)+\gamma\max_a\sum_{s'}T(s,a,s')V_k(s')
> $$
>
> 这句话的意思是：**先对每个 action 算“下一状态 value 的概率加权平均”，再选平均值最大的 action**。不是直接挑一个最好的 next state，因为动作有随机性，你只能选择 action，不能选择环境实际把你送到哪里。
>
> 三个概念要分清：
>
> - reward：这一步立刻拿到的分数。
> - value：从当前 state 出发，未来总回报的估计。
> - q-value：在当前 state 先做某个 action 后，未来总回报的估计。
>
> 易错点：terminal state 没有未来项；普通 state 要加当前 reward；未来 value 要乘 $\gamma$；动作随机时要先按概率求期望。

## Reinforcement Learning

- In reinforcement learning (RL) an agent gets feedback in the form of rewards, and he wants to learn a policy to maximize his expected utility. In passive RL, the policy is given, and the agent needs to learn the states' values from observation. In active RL, the agent has to choose actions and create a policy.
- In temporal difference (TD) learning, the agent estimates $V$ directly from samples, without estimating $T$ and $R$. It uses an exponentially-weighted moving average:

$$
V_{\text{new}}=\alpha V_{\text{sampled}}+(1-\alpha)V_{\text{old}}
$$

for some weight $\alpha$, known as the learning rate.

- For constructing a policy, it is more useful to know $Q$ than to know $V$. $Q$-learning is sample-based q-value iteration: each time the agent takes an action, he updates his $Q$ values based on the Bellman equations.
- An agent must trade off between exploration and exploitation. In the $\epsilon$-greedy method, with probability $\epsilon$ the agent chooses a random action; otherwise he acts according to his current policy. A better alternative is to have an "optimistic" utility function, which adds more utility to states that the agent knows less about.
- Approximate $Q$-Learning is useful when there are too many states to explore and store separately. One solution is to encode states or q-states as feature vectors and estimate value as a linear function of features:

$$
V(s)=w_1f_1(s)+w_2f_2(s)+\cdots+w_nf_n(s)
$$

$$
Q(s,a)=w_1f_1(s,a)+w_2f_2(s,a)+\cdots+w_nf_n(s,a)
$$

Approximate $Q$-learning with linear $Q$-functions:

$$
\text{transition}=(s,a,r,s')
$$

$$
\Delta=\left(r+\gamma\max_{a'}Q(s',a')\right)-Q(s,a)
$$

$$
w_i \leftarrow w_i+\alpha[\Delta]f_i(s,a)
$$

> **【新增中文注释：RL 与 Approximate Q-learning 知识点】**
>
> **1. RL 和 MDP 的关系**
>
> MDP 更像“题目把世界规则都告诉你”，你可以直接算最优 value。RL 更像“你在环境里试错”，每次只看到一个样本：
>
> $$
> (s,a,r,s')
> $$
>
> 其中 $s$ 是原状态，$a$ 是采取的动作，$r$ 是这一步拿到的 reward，$s'$ 是到达的新状态。
>
> **2. passive RL 与 active RL**
>
> - passive RL：策略已经给定，你只需要评估这个策略好不好。
> - active RL：你还要自己选动作，所以要在“探索未知动作”和“利用当前看起来最好的动作”之间权衡。
>
> **3. TD learning 的核心**
>
> TD learning 不等整条 episode 结束，而是看一步 sample 后立刻修正估计。它的思想是：
>
> $$
> \text{新估计}=\text{旧估计}+\alpha(\text{样本目标}-\text{旧估计})
> $$
>
> $\alpha$ 越大，越相信最新样本；$\alpha$ 越小，更新越保守。
>
> **4. 为什么要学 $Q$ 而不只学 $V$**
>
> 如果只有 $V(s)$，你知道“这个状态好不好”，但不一定知道“下一步该选哪个动作”。如果有 $Q(s,a)$，你可以直接比较：
>
> $$
> \pi(s)=\arg\max_a Q(s,a)
> $$
>
> 也就是说，$Q$ 自带动作选择信息。
>
> **5. Approximate Q-learning 的用途**
>
> 普通 Q-learning 需要为每个 $(s,a)$ 单独存一个 $Q$ 值。但现实中状态可能很多，例如自动驾驶的距离、速度、车道、障碍物组合起来无限接近连续空间。Approximate Q-learning 不再记住每个状态，而是提取 features：
>
> $$
> Q(s,a)=\sum_i w_if_i(s,a)
> $$
>
> 这里 $f_i(s,a)$ 是你观察到的特征，$w_i$ 是模型学出来的权重。解题时第一笔通常写：
>
> $$
> \Delta=\left(r+\gamma\max_{a'}Q(s',a')\right)-Q(s,a)
> $$
>
> 然后只更新当前 sample 中与 $(s,a)$ 有关的 feature 权重：
>
> $$
> w_i\leftarrow w_i+\alpha\Delta f_i(s,a)
> $$
>
> 注意：更新权重时使用的是 **当前状态 $s$ 和当前动作 $a$ 的 feature**，不是下一状态 $s'$ 的 feature。下一状态只用于算 target 里的 $\max_{a'}Q(s',a')$。

## 1. MDP Exercise: Value Iteration

> **【新增中文注释：本题审题重点】**
>
> 这道题是 grid world 的 value iteration。关键信息是：普通格子 reward 为 `-2`，green `[2,3]` 是 terminal 且 value 为 `+1`，red `[1,3]` 是 terminal 且 value 为 `-1`，折扣因子 $\gamma=0.8$。动作不是确定的：计划方向概率 `0.8`，两个垂直方向各 `0.1`。
>
> 手算时先画出当前 state 做某个 action 后可能到达的三个位置，再代入 Bellman update。

For today's class the environment we're exploring is a grid world.

| Row / Col | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 2 | `[2,0]` | `[2,1]` | `[2,2]` | `green` terminal, reward `+1` |
| 1 | `[1,0]` | wall | `[1,2]` | `red` terminal, reward `-1` |
| 0 | `[0,0]` | `[0,1]` | `[0,2]` | `[0,3]` |

With this grid world, we define the following Markov decision process $\langle S,A,T,R,\gamma\rangle$:

| Component | Definition |
|---|---|
| $S$ | States are represented as grid cells; each grid cell is one state in the world. |
| $A$ | The robot can move `UP`, `DOWN`, `LEFT`, and `RIGHT`; there are 4 total actions. |
| $T$ | The robot moves as expected with action $a$ from state $s$ to state $s'$ with probability `0.8`. With probability `0.1`, the robot moves either left or right perpendicular to action $a$. |
| $R$ | The reward function only depends on the state: $R(green)=+1$, $R(red)=-1$, and $R(everywhere\ else)=-2$. |
| $\gamma$ | The fixed discounting factor is `0.8`. |

> **【新增中文注释：两个 `0.8` 不要混淆】**
>
> 表中有两个含义不同的 `0.8`：一个是 transition probability，表示动作按计划方向发生的概率；另一个是 discount factor $\gamma=0.8$，表示未来 value 要打折。算式里常常两个都会出现。

Transition examples:

- If $a$ specifies that the robot should move to the `RIGHT`, with probability `0.8` the robot will move right, with probability `0.1` it will move up, and with probability `0.1` it will move down.
- If $a$ specifies that the robot should move `DOWN`, with probability `0.8` the robot will move down, with probability `0.1` it will move right, and with probability `0.1` it will move left.

Task today: compute the value for each state in the grid world using the Bellman equation and value iteration. Before value iteration starts, assume that the value for each state is `0`.

> **【新增中文注释：本题计算模板】**
>
> 普通格子的 reward 都是 `-2`，所以：
>
> $$
> V_{\text{new}}(s)=-2+0.8\cdot\max_a E_a
> $$
>
> 其中每个动作的下一状态期望是：
>
> $$
> E_a=0.8V(s'_{\text{intended}})+0.1V(s'_{\text{perp1}})+0.1V(s'_{\text{perp2}})
> $$
>
> 先算每个 action 的 $E_a$，再取最大的那个。边界或 wall 通常按“撞上后留在原地”处理；如果题目另有说明，以题目为准。

### Shared Trajectories

To keep everyone on the same page, all trajectories below use row-column notation where the bottom left is the origin `[0,0]`. For example, the green state at time $k$ is represented as $s_k=[2,3]$.

> **【新增中文注释：Shared Trajectories 怎么读】**
>
> 这张表主要是用几条路径展示 value 如何变化，不是说 value 一定要沿着表中动作逐步累加。真正计算每个 $V(s)$ 时，仍然要用 Bellman optimal update。
>
> 坐标是 `[row,col]`：`UP` 让 row 加 1，`RIGHT` 让 col 加 1。`[2,3]` 是 green terminal，value 为 `+1`；`[1,3]` 是 red terminal，value 为 `-1`，terminal 不再展开未来项。

| Step | Trajectory 1 | Trajectory 2 | Trajectory 3 | Trajectory 4 | Trajectory 5 | Trajectory 6 |
|---|---|---|---|---|---|---|
| $s_0$ | `[0,0]` | `[0,0]` | `[0,0]` | `[0,0]` | `[0,0]` | `[0,0]` |
| $V$ | $V([0,0])=-2$ | $V([0,0])=-2.32$ | $V([0,0])=-2.47$ | $V([0,0])=-3.77$ | $V([0,0])=-4.89$ | $V([0,0])=-5.09$ |
| $a_0$ | `UP` | `UP` | `RIGHT` | `RIGHT` | `UP` | `RIGHT` |
| $s_1$ | `[1,0]` | `[1,0]` | `[0,1]` | `[0,1]` | `[1,0]` | `[0,1]` |
| $V$ | $V([1,0])=-2$ | $V([1,0])=-3.6$ | $V([0,1])=-2$ | $V([0,1])=-3.6$ | $V([1,0])=-4.88$ | $V([0,1])=-4.07$ |
| $a_1$ | `UP` | `UP` | `RIGHT` | `RIGHT` | `UP` | `RIGHT` |
| $s_2$ | `[2,0]` | `[2,0]` | `[0,2]` | `[0,2]` | `[2,0]` | `[0,2]` |
| $V$ | $V([2,0])=-2$ | $V([2,0])=-3.6$ | $V([0,2])=-2$ | $V([0,2])=-2.34$ | $V([2,0])=-4.88$ | $V([0,2])=-3.70$ |
| $a_2$ | `RIGHT` | `RIGHT` | `UP` | `RIGHT` | `RIGHT` | `UP` |
| $s_3$ | `[2,1]` | `[2,1]` | `[1,2]` | `[0,3]` | `[2,1]` | `[1,2]` |
| $V$ | $V([2,1])=-2$ | $V([2,1])=-3.6$ | $V([1,2])=-2.28$ | $V([0,3])=-2.08$ | $V([2,1])=-3.54$ | $V([1,2])=-3.06$ |
| $a_3$ | `RIGHT` | `RIGHT` | `RIGHT` | `UP` | `RIGHT` | `UP` |
| $s_4$ | `[2,2]` | `[2,2]` | `[1,3]` | `[1,3]` | `[2,2]` | `[2,2]` |
| $V$ | $V([2,2])=-2$ | $V([2,2])=-1.52$ | $V([1,3])=-1$ | $V([1,3])=-1$ | $V([2,2])=-1.66$ | $V([2,2])=-1.74$ |
| $a_4$ | `RIGHT` | `RIGHT` |  |  | `RIGHT` | `RIGHT` |
| $s_5$ | `[2,3]` | `[2,3]` |  |  | `[2,3]` | `[2,3]` |
| $V$ | $V([2,3])=1$ | $V([2,3])=1$ |  |  | $V([2,3])=1$ | $V([2,3])=1$ |

> **【新增中文注释：追溯表中数字的办法】**
>
> 对表中任意一个普通格子，都按同一套流程：先写 `-2 + 0.8(...)`；括号里只放下一状态 value 的概率加权平均；对所有 action 都算一遍；选择期望最大的 action。靠近 green 的 state 会因为下一步可能到达 `+1` 而变好，远离 terminal 或容易停留在负 value 区域的 state 会更负。
>
> 注意：表格中的 path action 和 value 公式有一处明显不一致，后面 Trajectory 2 会专门说明。因此做题时以 Bellman optimal update 和具体公式为准。

### Trajectory Notes

- Trajectory 1:
  - $V([2,3])=1$
    - We can determine this value because $R(s_t,a_t)=+1$ for being in the green state and once we get into the state, the world ends. We cannot transition into any further states, meaning that for all $a_t$:

$$
\gamma\sum_{s'\in S}T(s,a,s')V(s')=0
$$

  - $V(\text{all other states})=-2$
    - We can determine this value because $R(s_t,a_t)=-2$ and all states initially start with value `0` until after the first iteration.

> **【新增中文注释：Trajectory 1 为什么普通格子都是 `-2`】**
>
> Trajectory 1 对应第一次 value update。题目说开始前所有 state value 都是 `0`，所以任意普通格子的未来期望都是 0：
>
> $$
> V_1(s)=-2+0.8\cdot0=-2
> $$
>
> 这不是说未来真的没有收益，而是第一次更新时未来信息还没有传播回来。因此此时 `UP`、`RIGHT`、甚至撞墙后留在原地，通常都会得到同样的普通格子 value。terminal 例外：green 直接是 `+1`，red 直接是 `-1`。

- Trajectory 2:

$$
V([0,0])=-2+\gamma(0.8\cdot0+0.1\cdot(-2)+0.1\cdot(-2))
$$

$$
=-2+\gamma(-0.4)=-2+0.8\cdot(-0.4)=-2.32
$$

  - The optimal action in this case would be a move to the `RIGHT` since the value of state `[0,1]` is currently `0` and the value of state `[1,0]` is currently `-2`.

$$
V([1,0])=-2+\gamma(0.8\cdot(-2)+0.1\cdot(-2)+0.1\cdot(-2))
$$

$$
=-2+\gamma(-2)=-2+0.8\cdot(-2)=-3.6
$$

  - The optimal action in this case would be `UP` since the value of state `[2,0]` is currently `-2` and the value of state `[0,0]` is now `-2.32`.

> **【新增中文注释：Trajectory 2 的关键与表格不一致处】**
>
> 这里已经不是第一次更新了，所以一些旧 value 已经不是 0。算 $V([0,0])$ 时，应该比较 action 的期望值，然后选最大的 action。
>
> 公式中的
>
> $$
> 0.8\cdot0+0.1\cdot(-2)+0.1\cdot(-2)
> $$
>
> 对应从 `[0,0]` 选择 `RIGHT`：80% 到 `[0,1]`，10% 偏上到 `[1,0]`，10% 偏下撞边界后留在 `[0,0]`。代入当时的 value：
>
> $$
> 0.8V([0,1])+0.1V([1,0])+0.1V([0,0])
> =0.8\cdot0+0.1(-2)+0.1(-2)=-0.4
> $$
>
> 所以：
>
> $$
> V([0,0])=-2+0.8(-0.4)=-2.32
> $$
>
> 如果真的按表格里的 `a_0=UP` 算，会得到：
>
> $$
> -2+0.8(0.8(-2)+0.1(0)+0.1(-2))=-3.44
> $$
>
> 这和答案的 `-2.32` 不一致。因此这里应理解为：**表格中 Trajectory 2 的 `a_0=UP` 与公式/文字说明不一致；求 value 时以 Bellman optimal update 为准，`[0,0]` 这一格应按 `RIGHT` 的期望来算。**
>
> 后面 `[1,0]` 的计算则可以按 `UP` 理解：
>
> $$
> V([1,0])=-2+0.8(0.8(-2)+0.1(-2)+0.1(-2))=-3.6
> $$
>
> 总结：遇到新题时，不要机械跟 trajectory 表的路径动作走；只要题目说 value iteration / optimal value，就对每个 action 算期望，取最大值。

## RL Exercise: Approximate Q-learning

> **【新增中文注释：本题类型识别】**
>
> 这一题不是让你枚举完整 MDP，也不是普通 tabular Q-learning；它是 Approximate Q-learning。识别信号是题目给了 features 和 weights：
>
> $$
> Q(s,a)=w_{AD}f_{AD}(s,a)+w_{AS}f_{AS}(s,a)+w_{BD}f_{BD}(s,a)+w_{BS}f_{BS}(s,a)
> $$
>
> 所以解题第一笔应该写“当前权重是多少”，第二笔写“当前 sample 的 feature 值是多少”，第三笔写 TD error $\Delta$，最后更新权重。

A self-driving car needs to decide whether to Accelerate (`A`) or Brake (`B`) so as to drive to a location without hitting other cars. It receives a reward of `+1` if the car moves and does not hit another car, `0` if it does not move, and `-2` if it hits another car. The discount factor is $\gamma=1$.

We want to use Approximate $Q$-learning to learn a good driving policy for the car. The car has sensors that allow it to observe the distance (`D`) to the nearest object and the current speed (`S`). We create four features:

| Action | Distance feature | Speed feature |
|---|---|---|
| `A` | $f_{AD}$ | $f_{AS}$ |
| `B` | $f_{BD}$ | $f_{BS}$ |

$Q$ values are approximated by a linear combination of four features, with weights $w_{AD},w_{AS},w_{BD},w_{BS}$. Suppose some learning has already happened so that $w_{AD}=1$, while all other weights are `0`. The learning rate is $\alpha=0.5$.

> **【新增中文注释：题干变量翻译】**
>
> - `A` = Accelerate，加速。
> - `B` = Brake，刹车。
> - `D` = Distance to nearest object，离最近障碍物的距离。
> - `S` = Speed，当前速度。
> - $f_{AD}$：当动作是 `A` 时使用的 distance feature。
> - $f_{AS}$：当动作是 `A` 时使用的 speed feature。
> - $f_{BD}$：当动作是 `B` 时使用的 distance feature。
> - $f_{BS}$：当动作是 `B` 时使用的 speed feature。
>
> 这四个 feature 是“按动作分组”的。若当前动作是 `A`，通常只有 $f_{AD},f_{AS}$ 非零，刹车相关的 $f_{BD},f_{BS}$ 为 0；若当前动作是 `B`，则反过来。
>
> 初始权重是：
>
> $$
> w_{AD}=1,\quad w_{AS}=0,\quad w_{BD}=0,\quad w_{BS}=0
> $$
>
> 这表示模型一开始只认为“加速时的距离 feature”有正贡献，其他 feature 暂时没有贡献。

> **【新增中文注释：Approximate Q-learning 解题模板】**
>
> 对每一条 observed data，都按下面顺序写：
>
> 1. 用当前 $s,a$ 的 features 计算旧的 $Q(s,a)$。
> 2. 用当前权重分别计算 $Q(s',A)$ 和 $Q(s',B)$。
> 3. 取 $\max(Q(s',A),Q(s',B))$ 得到下一状态的最佳估计。
> 4. 计算 TD error：
>
> $$
> \Delta=(r+\gamma\max_{a'}Q(s',a'))-Q(s,a)
> $$
>
> 5. 更新每个权重：
>
> $$
> w_i\leftarrow w_i+\alpha\Delta f_i(s,a)
> $$
>
> 最关键的细节：第 5 步的 $f_i(s,a)$ 来自“当前状态和刚才实际采取的动作”，不是来自 $s'$。

> **【新增中文注释：完全不会时的手算草稿纸格式】**
>
> 先把四个权重固定成一个顺序：
>
> $$
> w=(w_{AD},w_{AS},w_{BD},w_{BS})
> $$
>
> 对任意传感器读数 $(D,S)$，如果假设动作是 `A`，feature vector 写成：
>
> $$
> f(s,A)=(D,S,0,0)
> $$
>
> 如果假设动作是 `B`，feature vector 写成：
>
> $$
> f(s,B)=(0,0,D,S)
> $$
>
> 然后 $Q$ 值就是点积：
>
> $$
> Q(s,a)=w\cdot f(s,a)
> $$
>
> 每看到一条样本 $(s,a,r,s')$，草稿纸按这个顺序写：
>
> 1. 写当前权重 $w$。
> 2. 写当前 feature $f(s,a)$，算旧估计 $Q(s,a)$。
> 3. 在下一状态 $s'$ 分别假设动作 `A` 和 `B`，算 $Q(s',A)$、$Q(s',B)$。
> 4. 算 target：
>
> $$
> \text{target}=r+\gamma\max(Q(s',A),Q(s',B))
> $$
>
> 5. 算误差：
>
> $$
> \Delta=\text{target}-Q(s,a)
> $$
>
> 6. 更新整组权重：
>
> $$
> w_{\text{new}}=w_{\text{old}}+\alpha\Delta f(s,a)
> $$
>
> 这题里 $\gamma=1$，所以未来项不打折；$\alpha=0.5$，所以每次更新只走误差的一半。注意：下一状态 $s'$ 只用来算 target，不用 $f(s',a')$ 去更新权重。

| Observed Data | Weights after seeing data |
|---|---|
| Initial weights | $w_{AD}=1,\ w_{AS}=w_{BD}=w_{BS}=0$ |
| Initial Sensors: $D=0,S=2$<br>Action: `A`<br>Reward: `-2`<br>Final Sensors: $D=1,S=0$ | $s[D=0,S=2]$, taken action `A`: $f_{AD}=0,\ f_{AS}=2,\ f_{BD}=f_{BS}=0$<br><br>$Q(s,A)=w_{AD}f_{AD}+w_{AS}f_{AS}+w_{BD}f_{BD}+w_{BS}f_{BS}$<br>$=1\cdot0+0\cdot2+0\cdot0+0\cdot0=0$<br><br>$s'[D=1,S=0]$, taken action `A`: $f_{AD}=1,\ f_{AS}=0,\ f_{BD}=f_{BS}=0$<br>$Q(s',A)=1\cdot1+0\cdot0+0\cdot0+0\cdot0=1$<br><br>$s'[D=1,S=0]$, taken action `B`: $f_{AD}=f_{AS}=0,\ f_{BD}=1,\ f_{BS}=0$<br>$Q(s',B)=1\cdot0+0\cdot0+0\cdot1+0\cdot0=0$<br><br>$\Delta=(-2+1.0\cdot\max(Q(s',A),Q(s',B)))-0=-2+1.0(1)-0=-1$<br><br>$w_{AD}\leftarrow w_{AD}+0.5\cdot\Delta\cdot f_{AD}(s,A)=1+0.5\cdot(-1)\cdot0=1$<br>$w_{AS}\leftarrow w_{AS}+0.5\cdot\Delta\cdot f_{AS}(s,A)=0+0.5\cdot(-1)\cdot2=-1$<br>$w_{BD}=0,\ w_{BS}=0$ |
| Initial Sensors: $D=1,S=0$<br>Action: `B`<br>Reward: `0`<br>Final Sensors: $D=1,S=0$ | $s[D=1,S=0]$, taken action `B`: $f_{AD}=f_{AS}=0,\ f_{BD}=1,\ f_{BS}=0$<br><br>$Q(s,B)=w_{AD}f_{AD}+w_{AS}f_{AS}+w_{BD}f_{BD}+w_{BS}f_{BS}$<br>$=1\cdot0+(-1)\cdot0+0\cdot0+0\cdot0=0$<br><br>$s'[D=1,S=0]$, taken action `A`: $f_{AD}=1,\ f_{AS}=0,\ f_{BD}=f_{BS}=0$<br>$Q(s',A)=1\cdot1+(-1)\cdot0+0\cdot0+0\cdot0=1$<br><br>$s'[D=1,S=0]$, taken action `B`: $f_{AD}=f_{AS}=0,\ f_{BD}=1,\ f_{BS}=0$<br>$Q(s',B)=1\cdot0+(-1)\cdot0+0\cdot1+0\cdot0=0$<br><br>$\Delta=(0+1.0\cdot\max(Q(s',A),Q(s',B)))-0=0+1.0(1)-0=1$<br><br>$w_{AD}=1,\ w_{AS}=-1$<br>$w_{BD}\leftarrow w_{BD}+0.5\cdot\Delta\cdot f_{BD}(s,B)=0+0.5\cdot1\cdot1=0.5$<br>$w_{BS}\leftarrow w_{BS}+0.5\cdot\Delta\cdot f_{BS}(s,B)=0+0.5\cdot1\cdot0=0$ |

> **【新增中文注释：第一条 observed data 手算全过程】**
>
> 样本是：
>
> $$
> s=(D=0,S=2),\quad a=A,\quad r=-2,\quad s'=(D=1,S=0)
> $$
>
> 当前权重：
>
> $$
> w=(1,0,0,0)
> $$
>
> 因为当前动作是 `A`，所以当前 feature vector 是：
>
> $$
> f(s,A)=(D,S,0,0)=(0,2,0,0)
> $$
>
> 先算旧估计：
>
> $$
> Q(s,A)=w\cdot f(s,A)=(1,0,0,0)\cdot(0,2,0,0)=0
> $$
>
> 接着看下一状态 $s'=(D=1,S=0)$。为了算 target，要在 $s'$ 分别假设下一步动作是 `A` 和 `B`：
>
> $$
> f(s',A)=(1,0,0,0),\quad Q(s',A)=(1,0,0,0)\cdot(1,0,0,0)=1
> $$
>
> $$
> f(s',B)=(0,0,1,0),\quad Q(s',B)=(1,0,0,0)\cdot(0,0,1,0)=0
> $$
>
> 所以下一状态最好的估计是：
>
> $$
> \max(Q(s',A),Q(s',B))=\max(1,0)=1
> $$
>
> target 是：
>
> $$
> \text{target}=r+\gamma\max Q(s',a')=-2+1\cdot1=-1
> $$
>
> TD error 是：
>
> $$
> \Delta=\text{target}-Q(s,A)=-1-0=-1
> $$
>
> 最后更新权重。用向量一次写完：
>
> $$
> w_{\text{new}}=w_{\text{old}}+\alpha\Delta f(s,A)
> $$
>
> $$
> =(1,0,0,0)+0.5(-1)(0,2,0,0)
> $$
>
> $$
> =(1,0,0,0)+(0,-1,0,0)=(1,-1,0,0)
> $$
>
> 所以更新后：
>
> $$
> w_{AD}=1,\quad w_{AS}=-1,\quad w_{BD}=0,\quad w_{BS}=0
> $$
>
> 直觉解释：这条经验说“距离为 0、速度为 2 时还加速会撞车”，所以 `A` 动作下的 speed 权重 $w_{AS}$ 被调低。

> **【新增中文注释：第二条 observed data 手算全过程】**
>
> 第二条样本是：
>
> $$
> s=(D=1,S=0),\quad a=B,\quad r=0,\quad s'=(D=1,S=0)
> $$
>
> 注意：现在要用第一条样本更新后的权重：
>
> $$
> w=(1,-1,0,0)
> $$
>
> 当前动作是 `B`，所以当前 feature vector 是：
>
> $$
> f(s,B)=(0,0,D,S)=(0,0,1,0)
> $$
>
> 旧估计：
>
> $$
> Q(s,B)=w\cdot f(s,B)=(1,-1,0,0)\cdot(0,0,1,0)=0
> $$
>
> 下一状态仍然是 $s'=(D=1,S=0)$。分别假设下一步动作是 `A` 和 `B`：
>
> $$
> f(s',A)=(1,0,0,0),\quad Q(s',A)=(1,-1,0,0)\cdot(1,0,0,0)=1
> $$
>
> $$
> f(s',B)=(0,0,1,0),\quad Q(s',B)=(1,-1,0,0)\cdot(0,0,1,0)=0
> $$
>
> target：
>
> $$
> \text{target}=0+1\cdot\max(1,0)=1
> $$
>
> TD error：
>
> $$
> \Delta=1-Q(s,B)=1-0=1
> $$
>
> 向量式更新：
>
> $$
> w_{\text{new}}=(1,-1,0,0)+0.5(1)(0,0,1,0)
> $$
>
> $$
> =(1,-1,0,0)+(0,0,0.5,0)=(1,-1,0.5,0)
> $$
>
> 所以更新后：
>
> $$
> w_{AD}=1,\quad w_{AS}=-1,\quad w_{BD}=0.5,\quad w_{BS}=0
> $$
>
> 直觉解释：当前动作是 `B`，所以只可能更新刹车相关的权重 $w_{BD},w_{BS}$。由于 $S=0$，$f_{BS}=0$，所以 $w_{BS}$ 不变；由于 $D=1$ 且 $\Delta>0$，所以 $w_{BD}$ 增加。

Given the learned weights, suppose that the sensors read $D=1,S=1$. Which action would be preferred?

- At state $s[D=1,S=1]$, if taking action `A`:

$$
Q(s,A)=1\cdot1+(-1)\cdot1+0.5\cdot0+0\cdot0=0
$$

- At state $s[D=1,S=1]$, if taking action `B`:

$$
Q(s,B)=1\cdot0+(-1)\cdot0+0.5\cdot1+0\cdot1=0.5
$$

Hence, action `B` will be preferred as the corresponding $Q$-value, $Q(s,B)$, is greater.

> **【新增中文注释：最终选择动作的完整思路】**
>
> 学完两条样本后，最终权重是：
>
> $$
> w_{AD}=1,\quad w_{AS}=-1,\quad w_{BD}=0.5,\quad w_{BS}=0
> $$
>
> 现在传感器读数是 $D=1,S=1$，要做的是“用同一个状态分别假设动作为 `A` 和 `B`”，然后比较两个 $Q$ 值。
>
> 若动作是 `A`：
>
> $$
> f_{AD}=1,\quad f_{AS}=1,\quad f_{BD}=0,\quad f_{BS}=0
> $$
>
> $$
> Q(s,A)=1\cdot1+(-1)\cdot1+0.5\cdot0+0\cdot0=0
> $$
>
> 若动作是 `B`：
>
> $$
> f_{AD}=0,\quad f_{AS}=0,\quad f_{BD}=1,\quad f_{BS}=1
> $$
>
> $$
> Q(s,B)=1\cdot0+(-1)\cdot0+0.5\cdot1+0\cdot1=0.5
> $$
>
> 因为 $0.5>0$，所以选择 `B`。从直觉上看，模型已经学到“速度对加速有负面影响”，而“刹车时距离 feature 有正贡献”，所以在 $D=1,S=1$ 这个状态下，刹车更稳。
>
> **【新增中文注释：举一反三检查清单】**
>
> 遇到同类 Approximate Q-learning 题，按下面检查：
>
> 1. 如果题目给的是 observed transition，就要更新权重；如果只是问“哪个 action preferred”，只算 $Q$ 值，不更新。
> 2. 当前动作是 `A`，feature 写 $(D,S,0,0)$；当前动作是 `B`，feature 写 $(0,0,D,S)$。
> 3. 算 target 时要看下一状态 $s'$ 的所有候选动作，即 $Q(s',A)$ 和 $Q(s',B)$。
> 4. 更新权重时只用当前的 $f(s,a)$，不是下一状态的 feature。
> 5. $\Delta>0$ 表示旧估计偏低，相关权重要沿 feature 方向增加；$\Delta<0$ 表示旧估计偏高，相关权重要降低。
>
> 最后选动作时，永远是对每个候选动作分别构造 feature vector，再代入当前 weights 算 $Q(s,a)$。不要用 reward 直接选动作，因为 reward 是单步反馈，而策略选择依赖的是估计的长期价值 $Q$。
