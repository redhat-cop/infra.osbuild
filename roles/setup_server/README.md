# infra.osbuild.setup_server

This role automates the setup of a server capable of performing [osbuild](https://www.osbuild.org/)
[compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html)
using the osbuild backend [Weldr](https://weldr.io/) API.

## Requirements

None

## Role Variables

### setup_server_rhsatellite

Type: boolean
Required: false

This variable is used to check when Satellite setup should run. When set to true Satellite setup will run.

Example:

```yaml
setup_server_rhsatellite: true
```

### setup_server_rhsatellite_host

Type: string
Required: false

This variable is used to connect to the Satellite host in order to setup the repositories for baseos and appstream.

Example:

```yaml
setup_server_rhsatellite_host: "test.dev"
```

### setup_server_rhsatellite_organization

Type: string
Required: false

This variable is used to build the url order to setup the repositories for baseos and appstream using Satellite.

Example:

```yaml
setup_server_rhsatellite_organization: "Default"
```

### setup_server_rhsatellite_environment

Type: string
Required: false

This variable is used to build the url order to setup the repositories for baseos and appstream using Satellite.

Example:

```yaml
setup_server_rhsatellite_environment: "Library"
```

### setup_server_rhsatellite_contentview

Type: string
Required: false

This variable is used to build the url order to setup the repositories for baseos and appstream using Satellite.

Example:

```yaml
setup_server_rhsatellite_contentview: "RHEL_8"
```

### setup_server_beta_repos

Type: boolean
Required: true

This variable is used to setup beta repositories for appstream and baseos, set true to setup beta repositories and false to setup non-beta repositories.

Example:

```yaml
setup_server_beta_repos: true
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
  tasks:
    - name: Run the role
      ansible.builtin.import_role:
        name: infra.osbuild.setup_server
```

## License

GPLv3
