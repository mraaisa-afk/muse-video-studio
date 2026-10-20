## What this changes

<!-- one paragraph, plain language -->

## Evidence

<!-- the part that matters. A timestamp, a metric, a before/after, a failing fixture.
     "It feels better" is not evidence. -->

## Type

- [ ] New preset
- [ ] New or changed lint rule
- [ ] New platform profile
- [ ] New language calibration
- [ ] Case card
- [ ] Documentation
- [ ] Bug fix

## Checklist

- [ ] `python3 scripts/validate_skill.py` passes
- [ ] `python3 tests/run_tests.py` passes (14/14 or more)
- [ ] Every shipped example still lints clean
- [ ] If a rule changed: a fixture fails before this PR and passes after
- [ ] If a threshold changed: the reason is written in the PR, not just the number
- [ ] No media files, no keys, no personal data committed

## Related

Closes #
