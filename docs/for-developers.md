# For developers

You have work to do and an agent to do it with. These are the questions you probably have, in the order they come up.

**Where do I start?** [Install the skills](tutorial/01-install.md), then ask your agent to set up spec-driven development. Fifteen minutes later you have a project with a constitution, an index and a first change. The [tutorial](tutorial/index.md) walks every step with real transcripts.

**How much do I have to write?** For a standard change, one page that says why it matters and what should be done. The agent asks at most five clarifying questions and writes it with you. Requirements, design and tasks come after approval, and the agent drafts them from your page.

**What if the change is tiny?** Use the quick tier: three files, no requirements. The one rule is that a quick change may not change behaviour. If it does, it is standard, however small.

**Who approves?** The owner of each capability your change touches. Often that is your own team. Approval is a review of the one page, not of a design.

**How do I know when I am done?** Ask the agent to verify. It walks the Gate 2 checklist with evidence and tells you exactly what blocks done. Nothing is marked done by hand.

**What goes in a commit message?** Whatever your team already does for the subject line, plus two trailers: `Change: 014` on every commit that belongs to the change, and `Requirements: REQ-014-01, REQ-014-03` on the ones that cover requirements. Tests name the requirement ids too.

**Where did my spec go after it shipped?** To `specs/archive/`, and its requirements now live in the capability specs under `specs/capabilities/`. That is the living description of the system. Look there, not in the archive.

**What if a task turns out to be wrong?** The agent stops and tells you, instead of quietly building something else. You edit the requirement in a reviewed change. That is a feature.

## Read next

- [Tutorial: your first change](tutorial/index.md)
- [The six skills](skills/index.md)
- [The method, in full](method.md)
