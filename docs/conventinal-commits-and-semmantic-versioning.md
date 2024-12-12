conventional commits
semantic versioning
automated changelog generation


Conventional Commits is a lightweight specification for standardizing commit messages in version control systems. The commit message structure follows this format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Main Types

**Primary Types**:
- `feat`: introduces a new feature[2]
- `fix`: patches a bug in the codebase[2]
- `docs`: changes to documentation[3]
- `test`: adding or modifying tests[3]
- `perf`: performance improvements[3]
- `chore`: maintenance tasks[3]

## Benefits

Conventional Commits provides several advantages for development teams:
- Automatic CHANGELOG generation[2]
- Semantic version determination based on commit types[2]
- Improved communication between team members[1]
- Easier project contribution through structured commit history[2]

## Breaking Changes

Breaking changes can be indicated in two ways:
- Adding `BREAKING CHANGE:` at the start of the commit body
- Appending a `!` after the type/scope[2][3]

Example of a breaking change:
```
fix(api)!: remove deprecated endpoint

BREAKING CHANGE: The /v1/users endpoint has been removed
```



Here are the primary conventional commit types:

## Core Types
- `feat`: Introduces new features to the codebase[1][2]
- `fix`: Patches a bug in the codebase[1][2]
- `docs`: Changes to documentation only[2][4]
- `style`: Changes that don't affect code meaning (formatting, spacing)[4]
- `refactor`: Code changes that neither fix bugs nor add features[4]
- `perf`: Performance improvements[2][4]
- `test`: Adding or modifying tests[2][4]

## Additional Types
- `build`: Changes affecting build system or dependencies[4]
- `ci`: Changes to CI configuration files and scripts[4]
- `chore`: Maintenance tasks and other changes that don't modify source or test files[2][4]
- `revert`: Reverts a previous commit[4]

## Special Annotations
Breaking changes can be indicated by either:
- Adding `BREAKING CHANGE:` in the commit body
- Appending a `!` after the type/scope[2]


Conventional Commits directly map to Semantic Versioning (SemVer) through their commit types, enabling automated version management:

## Version Mapping

**Major Version (X)**
- Triggered by commits containing `BREAKING CHANGE` in the footer
- Can be indicated by appending `!` after the type/scope
- Represents incompatible API changes[1][3]

**Minor Version (Y)**
- Triggered by `feat` type commits
- Represents new features that maintain backward compatibility[2][3]

**Patch Version (Z)**
- Triggered by `fix` type commits
- Represents backward-compatible bug fixes[2][3]

## Benefits of Integration

The integration of Conventional Commits with SemVer enables:
- Automatic version number determination based on commit types
- Automated CHANGELOG generation
- Clear communication of change impact to stakeholders
- Structured approach to version management[1][3]

## Version Format

The resulting version follows the format:
```
MAJOR.MINOR.PATCH
```

For example, in version `2.0.3`:
- 2 represents major version (breaking changes)
- 0 represents minor version (new features)
- 3 represents patch version (bug fixes)[2]


Conventional Commits enable automated and structured CHANGELOG generation by providing a standardized commit message format that tools can parse and organize effectively.

## Automation Benefits

The structured format allows automated tools to:
- Generate comprehensive and readable changelogs from commit history[1][2]
- Categorize changes based on commit types
- Split changes into appropriate versions with dates[3]
- Track features and bug fixes systematically

## CHANGELOG Structure

The generated changelogs typically organize commits into sections:
- Breaking changes (from commits with `BREAKING CHANGE` or `!`)
- New features (from `feat` commits)
- Bug fixes (from `fix` commits)
- Other changes (documentation, performance, etc.)

## Implementation Tools

Several tools facilitate automated changelog generation:
- **conventional-changelog**: Generates changelogs from git metadata[5]
- **standard-version**: Combines versioning and changelog generation[4]
- **release-please**: Provides both changelog generation and versioning automation[3]

## Team Benefits

Automated changelog generation through conventional commits:
- Reduces manual documentation effort
- Ensures consistent documentation of changes
- Improves project maintainability
- Makes it easier for new contributors to understand project history[1]
