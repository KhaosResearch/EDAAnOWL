# EDAAnOWL Pull Request

## Type of Change

- [ ] 🚀 **New Version** (Major/Minor/Patch release)
- [ ] 🐛 **Bug Fix** (Non-breaking change which fixes an issue)
- [ ] ✨ **New Feature** (Non-breaking change which adds functionality)
- [ ] 📝 **Documentation** (Update to README, comments, diagrams, etc.)
- [ ] 🧹 **Maintenance** (Refactoring, dependency updates, scripts)

## Description

Please include a summary of the changes and the problem that is fixed.

- What is the goal of this PR?
- Any specific design decisions?

## Checklist (for New Versions)

If this PR introduces a new release (e.g., v0.0.2), please verify the following based on `CONTRIBUTING.md`:

- [ ] **Directory**: A new folder `src/X.Y.Z/` exists with all assets.
- [ ] **Ontology Version**: `EDAAnOWL.ttl` has updated:
    - [ ] `owl:versionIRI`
    - [ ] `owl:versionInfo`
    - [ ] `owl:priorVersion`
- [ ] **Vocabulary Imports**: All `owl:imports` point to the new version path (`.../X.Y.Z/...`).
- [ ] **Vocabularies**: Each file in `vocabularies/` has updated `@base` and `owl:Ontology` URI.
- [ ] **Changelog**: `CHANGELOG.md` is updated with an `[Unreleased]` section detailing changes.
- [ ] **Validation**: Local validation (`scripts/local-validate.sh` / `validate_shacl.py`) passes.
- [ ] **Examples**: Included examples (e.g., `test-consistency.ttl`) are valid against the new ontology.

## Checklist (General)

- [ ] My code follows the style guidelines of this project.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding changes to the documentation.
- [ ] My changes generate no new warnings.

## Related Issues

Closes # (issue)
