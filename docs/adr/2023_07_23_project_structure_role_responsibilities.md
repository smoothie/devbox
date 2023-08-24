# Project Structure: Role Responsibilities

* Status: accepted
* Date: 2023-07-23

## Context and Problem Statement

The main focus of this discussion is to determine the responsibilities of Ansible roles in the 
project.

## Decision Drivers

* Organized and maintainable playbooks and roles
* Fine-grained local development environments
* Ease of adding and removing technologies
* An easy-to-learn and understandable way of configuring local development environments

## Considered Options

### One Role per Technology

**Project Structure:**

```markdown
site.yaml                   # master playbook
development.ini             # inventory for development environment
staging.ini                 # inventory for staging environment

roles/
    common/                 # role for default things like installing gcc, vim 
    apache2/                # role for the Apache2 HTTP server
    php/                    # role for PHP
```

* Good, because fine-grained by design.
* Good, because technologies can be independent of another, resulting in loose coupling.
* Good, because smaller chunks lead to better maintainability. 
* Bad, because more directories lead to more files, which might make it harder to find specific items.

### Group Technologies into Usable Chunks 

**Project Structure:**

```markdown
site.yaml                   # master playbook
development.ini             # inventory for development environment
staging.ini                 # inventory for staging environment

roles/
    common/                 # role for default things like installing gcc, vim 
    webserver/              # role for everything what is HTTP related (apache2, php-fpm, ...)
        tasks/
            main.yaml       # setting up the running tasks
            apache2.yaml    # tasks for the Apache2 HTTP server         
            php.yaml        # tasks for PHP
            ...
```

* Good, because it is obvious what a role's use case is.
* Bad, because in real-world examples, it is challenging to draw a clear boundary for grouping 
  technologies. For some projects, web servers and databases may be related, while for others, 
  they may not.
* Bad, because the roles may become quite large and complex.
* Bad, because roles would still need to organize tasks into smaller chunks. 
  * At that point, the question arises as to why introduce a separate layer when Ansible's role 
    functionalities can be used directly.

## Decision Outcome

Chosen option: "[One Role per Technology](#one-role-per-technology)".

Both options support a fine-grained approach for configuring environments.

However, it seems that one role per technology is more manageable, easier to learn, easier to 
understand, and significantly easier to maintain.

## References

* none
