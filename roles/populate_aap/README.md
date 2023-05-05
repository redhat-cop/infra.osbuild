# infra.osbuild.populate_aap

This role automates the process of populating AAP with infra.osbuild content

This role uses the [controller_configuration](https://github.com/redhat-cop/controller_configuration) roles to populate AAP

## Requirements

None

## Role Variables
### populate_aap_controller_hostname
Type: string
Required: true

Hostname for the AAP controller instance to connect to

Example:
```yaml
populate_aap_controller_hostname: http://0.0.0.0:443
```

### populate_aap_controller_username
Type: string
Required: true

Username for the AAP controller instance to connect to

Example:
```yaml
populate_aap_controller_username: admin
```

### populate_aap_controller_password
Type: string
Required: true

Password for the AAP controller instance to connect to

Example:
```yaml
populate_aap_controller_password: test
```

### populate_aap_admin_password
Type: string
Required: true

Admin password for the AAP controller instance to connect to

Example:
```yaml
populate_aap_admin_password: test
```

### populate_aap_controller_validate_certs
Type: bool
Required: true

Set in order to validate or not validate certs

Example:
```yaml
populate_aap_controller_validate_certs: false
```

### populate_aap_controller_configuration_async_retries
Type: int
Required: false

Set the amount of time to retry a task

Example:
```yaml
populate_aap_controller_configuration_async_retries: 20
```

### populate_aap_execution_environments
Type: list
Required: false

Use to populate AAP with execution environments
More information can be found in [Configuration Collection execution environments role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/execution_environments)

Example:
```yaml
populate_aap_execution_environments:
  - name: osbuild_ee
    image: quay.io/repository/org/image
    pull: always
```

### populate_aap_organizations
Type: list
Required: false

Use to populate AAP with organizations
More information can be found in [Configuration Collection organizations role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/organizations)

Example:
```yaml
populate_aap_organizations: 
  - name: Osbuild_test
```

### populate_aap_inventories
Type: list
Required: false

Use to populate AAP with inventories
More information can be found in [Configuration Collection inventories role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/inventories)

Example:
```yaml
populate_aap_inventories:
  - name: osbuild_inventory
    organization: Osbuild_test
```

### populate_aap_hosts
Type: list
Required: false

Use to populate AAP with hosts
More information can be found in [Configuration Collection hosts role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/hosts)

Example:
```yaml
populate_aap_hosts:
  - name: osbuild_remote_system
    inventory: osbuild_inventory
    variables:
      ansible_host: 0.0.0.0
      ansible_user: user
```

### populate_aap_projects
Type: list
Required: false

Use to populate AAP with projects
More information can be found in [Configuration Collection projects role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/projects)

Example:
```yaml
populate_aap_projects:
  - name: osbuild_project
    organization: Osbuild_test
    default_environment: osbuild_ee
    scm_type: git
    scm_url: https://github.com/redhat-cop/infra.osbuild
```

### populate_aap_credentials
Type: list
Required: false

Use to populate AAP with credentials
More information can be found in [Configuration Collection credentials role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/credentials)

Example:
```yaml
populate_aap_credentials:
  - name: osbuild_credential
    organization: Osbuild_test
    credentail_type: Machine
    inputs:
      username: user
      ssh_key_data: "{{ lookup('file', '~/.ssh/id_rsa_aap', errors='warn') }}"
```

### populate_aap_job_templates
Type: list
Required: false

Use to populate AAP with job templates
More information can be found in [Configuration Collection job templates role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/job_templates)

Example:
```yaml
populate_aap_job_templates:
  - name: osbuild_setup_server
    job_type: run
    inventory: osbuild_inventory
    project: osbuild_project
    playbook: playbooks/osbuild_setup_server.yml
    credentials:
      - osbuild_credential
```


## Variables Exported by the Role

None.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Run populate_aap role to populate AAP with infra.osbuild content
  become: true
  hosts: all
  tasks:
    - name: Run the role
      ansible.builtin.import_role:
        name: infra.osbuild.populate_aap
```


## License

GPLv3

