# Project Structure: Where to place host_vars and group_vars

* Status: accepted
* Date: 2023-07-23

## Context and Problem Statement

The question is, where should `host_vars/` and `group_vars/` be placed? 

Ansible [recommends](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout) 
two project structures:
- Keeping them in the root directory
- Moving them into a separate `inventories/` directory

## Decision Drivers

* Flexibility in local development environment structures
* Low to no maintenance effort
* Consideration of scalability for different environments (testing/staging/production)

## Considered Options

### Keeping them in the root directory

```markdown
production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1.yml             # here we assign variables to particular groups
   group2.yml
host_vars/
   hostname1.yml          # here we assign variables to particular systems
   hostname2.yml
```

* Good, because having one group for all inventories is simple to manage.
* Bad, because a host/group_var configuration for one specific inventory is not possible. 

### Moving them into a separate `inventories/` directory

```markdown
inventories/
   production/
      hosts               # inventory file for production servers
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         hostname1.yml    # here we assign variables to particular systems
         hostname2.yml

   staging/
      hosts               # inventory file for staging environment
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         stagehost1.yml   # here we assign variables to particular systems
         stagehost2.yml

```

* Good, because fine-granular inventory host/group variable configuration is possible.
* Bad, because it results in more files.
* Bad, because it may become harder to manage as some inventories might work while others may not.

## Decision Outcome

Chosen option: "[Keeping them in root](#keeping-them-in-the-root-directory)".

It's easy to manage, and while using the `connection:local` mode, we will probably be able to scale.

## References

* [Ansible's Best Practices: Directory Layout](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout)
