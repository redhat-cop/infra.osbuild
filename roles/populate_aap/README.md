# infra.osbuild.populate_aap

This role automates the process of populating AAP with infra.osbuild content

This role uses the [controller_configuration](https://github.com/redhat-cop/controller_configuration) roles to populate AAP

## Requirements

None

## Role Variables

|Variable Name|Default Value|Required|Type|Description|Example|
|:---:|:---:|:---:|:---:|:---:|:---|
|`controller_hostname`|""|yes|str|URL to the Ansible Controller Server.|<pre>controller_hostname: http://0.0.0.0:443</pre>|
|`controller_username`|""|yes|str|Admin User on the Ansible Controller Server. Either username / password or oauthtoken need to be specified.|<pre>controller_username: admin</pre>|
|`controller_password`|""|yes|str|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.|<pre>controller_password: test</pre>|
|`controller_validate_certs`|True|yes|bool|Whether or not to validate the Ansible Controller Server's SSL certificate.|<pre>controller_validate_certs: false</pre>|
|`controller_configuration_async_retries`|30|yes|int|This variable sets the number of retries to attempt for the role globally.|<pre>controller_configuration_async_retries: 20</pre>|
|`populate_aap_execution_environments`|None|no|list|Use to populate AAP with execution environments More information can be found in [Configuration Collection execution environments role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/execution_environments)|<pre>populate_aap_execution_environments:<br>  - name: osbuild_ee<br>    image: quay.io/repository/org/image<br>    pull: always</pre>|
|`populate_aap_organizations`|None|no|list|Use to populate AAP with organizations. More information can be found in [Configuration Collection organizations role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/organizations)|<pre>populate_aap_organizations:<br>  - name: Osbuild_test</pre>|
|`populate_aap_inventories`|None|no|list|Use to populate AAP with inventories. More information can be found in [Configuration Collection inventories role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/inventories)|<pre>populate_aap_inventories:<br>  - name: osbuild_inventory<br>    organization: Osbuild_test</pre>|
|`populate_aap_hosts`|None|no|list|Use to populate AAP with hosts. More information can be found in [Configuration Collection hosts role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/hosts)|<pre>populate_aap_hosts:<br>  - name: osbuild_remote_system<br>    inventory: osbuild_inventory<br>    variables:<br>      ansible_host: 0.0.0.0<br>      ansible_user: user</pre>|
|`populate_aap_projects`|None|no|list|Use to populate AAP with projects. More information can be found in [Configuration Collection projects role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/projects)|<pre>populate_aap_projects:<br>  - name: osbuild_project<br>    organization: Osbuild_test<br>    default_environment: osbuild_ee<br>    scm_type: git<br>    scm_url: https://github.com/redhat-cop/infra.osbuild</pre>|
|`populate_aap_credentials`|None|no|list|Use to populate AAP with credentials. More information can be found in [Configuration Collection credentials role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/credentials)|<pre>populate_aap_credentials:<br>  - name: osbuild_credential<br>    organization: Osbuild_test<br>    credentail_type: Machine<br>    inputs:<br>      username: user<br>      ssh_key_data: "{{ lookup('file', '~/.ssh/id_rsa_aap', errors='warn') }}" </pre>|
|`populate_aap_job_templates`|None|no|list|Use to populate AAP with job templates. More information can be found in [Configuration Collection job templates role README](https://github.com/redhat-cop/controller_configuration/tree/devel/roles/job_templates)|<pre>populate_aap_job_templates:<br>  - name: osbuild_setup_server<br>      job_type: run<br>      inventory: osbuild_inventory<br>      project: osbuild_project<br>      playbook: playbooks/<br>      osbuild_setup_server.yml<br>      credentials:<br>        - osbuild_credential</pre>|

### populate_aap_default_host_user

Type: string
Required: false

Default host user for the remote system.

### populate_aap_default_host_ip

Type: string
Required: false

Default ip for the remote system.

### populate_aap_ssh_key_path

Type: string
Required: false

Path to the private ssh key that will be used for communication remote systems.

## Variables Exported by the Role

None.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Run populate_aap role to populate AAP with infra.osbuild content
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Run the role
      ansible.builtin.import_role:
        name: infra.osbuild.populate_aap
      vars:
        controller_hostname: https://0.0.0.0  # noqa var-naming[no-role-prefix]
        controller_username: admin  # noqa var-naming[no-role-prefix]
        controller_password: test  # noqa var-naming[no-role-prefix]
        populate_aap_default_host_user: user
        populate_aap_default_host_ip: 0.0.0.0
        populate_aap_organizations:
          - name: "{{ populate_aap_organization_name }}"
        populate_aap_execution_environments:
          - name: "{{ populate_aap_execution_environment_name }}"
            image: quay.io/repository/osbuildee/osbuildee
            pull: always
            organization: "{{ populate_aap_organization_name }}"
        populate_aap_inventories:
          - name: "{{ populate_aap_inventory_name }}"
            organization: "{{ populate_aap_organization_name }}"
        populate_aap_hosts:
          - name: osbuild_remote_system
            inventory: "{{ populate_aap_inventory_name }}"
            variables:
              ansible_host: "{{ populate_aap_default_host_ip }}"
              ansible_user: "{{ populate_aap_default_host_user }}"
        populate_aap_projects:
          - name: "{{ populate_aap_project_name }}"
            organization: "{{ populate_aap_organization_name }}"
            default_environment: "{{ populate_aap_execution_environment_name }}"
            scm_type: git
            scm_url: https://github.com/redhat-cop/infra.osbuild
        populate_aap_credentials:
          - name: "{{ populate_aap_credential_name }}"
            organization: "{{ populate_aap_organization_name }}"
            credential_type: Machine
            inputs:
              username: "{{ populate_aap_default_host_user }}"
              ssh_key_data: "{{ lookup('file', populate_aap_ssh_key_path) if populate_aap_ssh_key_path is defined else '' }}"
        populate_aap_job_templates:
          - name: osbuild_setup_server
            job_type: run
            inventory: "{{ populate_aap_inventory_name }}"
            project: "{{ populate_aap_project_name }}"
            playbook: playbooks/osbuild_setup_server.yml
            credentials:
              - "{{ populate_aap_credential_name }}"

          - name: osbuild_builder
            job_type: run
            inventory: "{{ populate_aap_inventory_name }}"
            project: "{{ populate_aap_project_name }}"
            playbook: playbooks/osbuild_builder.yml
            survey_enabled: true
            survey: "{{ lookup('template', 'template_surveys/builder_survey.yml') | from_yaml }}"
            ask_variables_on_launch: true
            extra_vars:
              _docs: 'REPLACE WITH VARS FROM DOCS: https://github.com/redhat-cop/infra.osbuild/blob/main/roles/builder/APP_EXTRA_VARS.md'  # yamllint disable-line rule:line-length
            credentials:
              - "{{ populate_aap_credential_name }}"

          - name: osbuild_system_info
            job_type: run
            inventory: "{{ populate_aap_inventory_name }}"
            project: "{{ populate_aap_project_name }}"
            playbook: playbooks/osbuild_system_info.yml
            credentials:
              - "{{ populate_aap_credential_name }}"

          - name: osbuild_update_system
            job_type: run
            inventory: "{{ populate_aap_inventory_name }}"
            project: "{{ populate_aap_project_name }}"
            playbook: playbooks/osbuild_update_system.yml
            credentials:
              - "{{ populate_aap_credential_name }}"
```

## License

GPLv3
