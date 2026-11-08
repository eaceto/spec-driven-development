# For team leads

You are deciding whether to adopt this, or how to run it across several teams. These are the parts that are yours.

**The constitution.** One page per project: purpose, up to ten principles, definitions, an amendment log. Agents load it on every run, so every line costs tokens on every task. An organisation constitution can sit above it; a project may add rules to the one it extends and may never relax one. You own this document, and it decays without an owner.

**Ownership.** Every capability has an owning team, declared in its frontmatter. A change lists the capabilities it touches, and Gate 1 needs a review from each owner. With GitHub or GitLab, mapping `specs/capabilities/<name>/` to the team in `CODEOWNERS` enforces the archive step for free. The approval itself is a review of a one-page spec, which is the lightest review your team will do.

**The index.** `specs/INDEX.md` is the view of intent: every active change with its status, tier, owner and capabilities, and every capability with its requirement count. Your tracker stays the view of schedule. The spec holds intent, the tracker holds who is working on it this sprint, the wiki holds background. Nothing is synchronised, and nothing has to be.

**Many repositories.** Specs live in the repository whose code they govern. A thin central repository holds the organisation constitution, the pinned version of templates and skills, and an aggregated index. Cross-team initiatives are a tracker epic with one change per affected repository. Across repositories a change is `payments-api:014`.

**Adopting in an existing codebase.** Do not spec the whole system. Write the constitution from what exists, add a capability map with purpose only, then spec the next change you were going to make anyway. Capabilities grow from the edges.

**What you can enforce.** The validator checks the mechanical rules and runs in continuous integration. The skills refuse to act in the wrong state. What remains for people is judgement: is the purpose real, is the scenario meaningful, is the design sound.

**What it costs.** One page before each piece of work, and a review of that page. In return, every requirement is traceable to the commits and tests that delivered it, and the specs still describe the system a year later.

## Read next

- [See one change go through, in fifteen minutes](tutorial/index.md)
- [The method: ownership and approval](method.md#ownership-and-approval)
- [The method: many repositories](method.md#many-repositories)
- [Agents your teams can use](agents.md)
