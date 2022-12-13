# infra.osbuild.setup_server

This role automates the setup of a server capable of performing [osbuild](https://www.osbuild.org/)
[compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html)
using the osbuild backend [Weldr](https://weldr.io/) API.

## Requirements

None

## Role Variables

### setup_server_custom_repos

Type: complex
Required: false

Custom list of RPM repositories to make available to the 
[osbuild](https://www.osbuild.org/) [compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html).

Each list entry is a [YAML dictionary](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
type and has the following attributes:

| Variable Name | Type                              | Required  | Default Value |
|---------------|-----------------------------------|-----------|---------------|
| repo_name     | string                            | **Yes**   | n/a           |
| base_url      | string                            | **Yes**   | n/a           |
| type          | string                            | No        | "yum-baseurl" |
| check_ssl     | bool                              | No        | true          |
| check_gpg     | bool                              | No        | true          |
| gpgkey_urls   | list of strings                   | No        | omit          |
| rhsm          | bool                              | No        | false         |
| state         | string ("present" or "absent" )   | No  | "present"     | 

Example:

```yaml
setup_server_custom_repos:
  - name: EPEL Everything
    base_url: "https://dl.fedoraproject.org/pub/epel/{{ hostvars[inventory_hostname].ansible_distribution_major_version }}/Everything/x86_64/"
    type: yum-baseurl
    check_ssl: true
    check_gpg: true
    state: present
  - name: My company custom repo
    base_url: "https://repo.example.com/company_repo/x86_64/"
```

## Variables Exported by the Role

None.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Run osbuild_builder role to setup obuild compose build server
  become: true
  hosts: all
  vars:
    setup_server_custom_repos:
      - name: EPEL Everything
        base_url: "https://dl.fedoraproject.org/pub/epel/{{ hostvars[inventory_hostname].ansible_distribution_major_version }}/Everything/x86_64/"
        type: yum-baseurl
        check_ssl: true
        check_gpg: true
        state: present
      - name: My company custom repo
        base_url: "https://repo.example.com/company_repo/x86_64/"
        type: yum-baseurl
  tasks:
    - name: Run the role
      ansible.builtin.import_role:
        name: infra.osbuild.setup_server
```


## License

GPLv3


