Conventions: Commits
---

## Introduction

In this project, we follow the Conventional Commits specification [v1.0.0][conventional_commits_v1_0_0] to structure our commit 
messages.

Conventional Commits provide a consistent and standardized way to format commit messages, making it
easier to understand the nature of changes in the codebase.

## Commit Message Structure

The general format is as follows:

```markdown
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

The type describes the kind of change made in the commit. We use the following types in our project:

- **feat:** A new feature or enhancement added to the codebase.
- **chore:** Miscellaneous changes that do not modify the source code (e.g., updating build scripts,
  configuration etc.).
- **ci:** Changes related to continuous integration (CI) configurations or pipeline scripts.
- **fix:** A bug fix or correction made to the code.
- **docs:** Changes related to documentation, such as updating the README or user guides.
- **style:** Code changes that do not affect the meaning (e.g., formatting, indentation, etc.).
- **refactor:** Code changes that neither fix a bug nor add a feature but improve the code structure.
- **test:** Changes related to adding or modifying test cases.
- **perf:** Performance-related improvements or optimizations.


## Scopes

Scopes are optional and are used to provide additional context about the commit. They help specify
the part of the codebase that the change affects. The following are some common scopes used in our
project:

- **{technology}:** Changes on a specific technology (e.g. php, apache2, etc.).
- **config:** Changes related to configuration files or settings.
- **security:** Changes addressing security concerns.
  affect the code's functionality.

## Example Commit Messages

Here are a few examples of conventional commit messages used in our project:

- **\`feat(php): Add user authentication feature using PHP.\`**
- **\`chore(config): Update build script for improved performance.\`**
- **\`ci(continuous-integration): Configure CI pipeline for automated testing.\`**
- **\`fix(security): Patch security vulnerability in login module.\`**
- **\`docs(readme): Update README with installation instructions.\`**
- **\`style(php): Format code according to coding standards.\`**
- **\`refactor(apache2): Refactor Apache2 configuration for better performance.\`**
- **\`test(apache2): Add test cases for apache2 automation.\`**
- **\`perf(database): Optimize database queries for faster response times.\`**

By following this convention, our commit messages are more structured and informative, making it
easier for developers and contributors to understand the nature of changes made to the codebase.

## Resources
- [Conventional Commits v1.0.0][conventional_commits_v1_0_0]
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)


[conventional_commits_v1_0_0]: https://www.conventionalcommits.org/en/v1.0.0/
