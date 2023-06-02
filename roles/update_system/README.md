# infra.osbuild.update_system

This role updates a running rpm-ostree based system with the latest image.

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
- name: Update systems
  become: true
  hosts: all
  tasks:
    - name: Use role to update system
      ansible.builtin.import_role:
        name: infra.osbuild.update_system
```

## License

GPLv3
