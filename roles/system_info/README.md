# infra.osbuild.system_info

This role automates the gathering of information from a running rpm-ostree based system.

## Requirements

None

## Role Variables

## Variables Exported by the Role

None.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Get system info
  hosts: all
  tasks:
    - name: Use system role to get image version
      ansible.builtin.import_role:
        name: infra.osbuild.system_info

    - name: debug
      ansible.builtin.debug:
        msg: "{{ ansible_facts['rpm_ostree'] }}"
```


## License

GPLv3


