# Questions people ask

**The change is tiny. Do I really need five files?**
No. Use the quick tier: `spec.md`, `tasks.md`, `checklist.md`. The one rule is that a quick change may not add, modify or remove a requirement. If behaviour changes, it is standard, however small. [Tiers](method.md#five-files).

**Who approves a change?**
The owner of each capability it touches, by reviewing the one page. Often that is your own team. The approver sets three fields in the frontmatter and that is Gate 1. [Ownership](method.md#ownership-and-approval).

**What counts as "tested" for Gate 2?**
The validator counts a requirement as tested when its id appears in a test file outside comment lines. That is the floor a machine can check. Whether the test proves the scenario is the reviewer's judgement. [Gates](method.md#five-states-three-gates).

**We squash merges. Do the trailers survive?**
Keep the `Change:` trailer in the squashed message and list every `Requirements:` id the squashed commits delivered. [Commits](method.md#commits-and-pull-requests).

**We number work by tracker ticket, not sequentially.**
Set `numbering: ticket` in the constitution. The directory becomes `ABC-123-name_of_change`, the id is `ABC-123`, and requirement ids are `REQ-ABC-123-01` onward. The validator accepts it. [Numbering](method.md#numbering-and-claiming).

**What goes in a commit message?**
Whatever your team already does for the subject line, plus `Change: 014` on every commit that belongs to the change, and `Requirements: REQ-014-01, REQ-014-03` on the ones that cover requirements.

**Where did my spec go after it shipped?**
To `specs/archive/`, and its requirements now live in the capability specs under `specs/capabilities/`. That is the living description of the system. Read there, not in the archive. [Two folders](method.md#two-folders).

**A task turned out to be wrong. What now?**
The agent stops and names the gap instead of building something else. You edit `requirements.md` in a reviewed change. That stop is the feature. [sdd-implement](skills/sdd-implement.md).

**Can I use this without an agent?**
Yes. Every skill is a procedure a person can follow by hand, and the validator checks the result either way. [Skills](skills/index.md).

**How long should the constitution be?**
One page, at most eighty lines, up to ten principles. Agents load it on every run, so every line costs on every task. [The constitution](method.md#the-constitution).

**We have an existing codebase. Do we spec everything first?**
No. Constitution from what exists, a capability map with purpose only, then the next change. [Adopting an existing project](adopting.md).

**Which agents work?**
Claude Code and Devin CLI are tested. Any agent that reads the open skills standard from `.agents/skills/` should work and is listed as untested until someone reports a run. [Agents](agents.md).
