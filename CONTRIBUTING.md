# Contributing guidelines

## Workflow

We are using the [GitHub workflow](https://docs.github.com/en/get-started/quickstart/github-flow).
Some notes about it:
- The main branch is *master* and there are feature branches.
- The feature branches are created from master and after the work is done, they are merged into master through a Merge Request.
- Feature branches must be considered as entities with a short life, like 1 sprint or less.

## Commit guidelines

The standard is [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

Types of commits:

| Type     | Use case                                                             | Version (major.minor.patch) |
|----------|----------------------------------------------------------------------|-----------------------------|
| feat     | new feature for the user, not a new feature for build script         | Minor                       |
| fix      | bug fix for the user, not a fix to build a script                    | Patch                       |
| docs     | changes the documentation                                            | No upper version            |
| refactor | refactoring production code, eg. renaming a variable                 | No upper version            |
| style    | formatting, missing semi colons, etc; no production code change      | No upper version            |
| test     | adding missing tests, refactoring tests; no production code change   | No upper version            |
| chore    | updating grunt tasks etc; no production code change                  | No upper version            |
| ci       | changes to our CI configuration files and scripts                    | No upper version            |


Additionally, if you introduce a breaking change in the code, it means you have the increase the major number, the commit syntax for that is:

```
type(<TICKET-REF>): <commit description>
BREAKING CHANGE: <new version>
<optional
commit
message
body>
```

Examples
```
fix(<TICKET-REF>): "Commit message" => version from 0.1.5 to 0.1.6

feat(<TICKET-REF>): "Commit message" => version from 0.1.6 to 0.2.0

feat(<TICKET-REF>): "Commit message"+ BREAKING CHANGE: 1.0.0  => version from 0.2.0 to 1.0.0
```

## Branch names

The branches follow the pattern
```
type/<TICKET-REF>-<short_description>
