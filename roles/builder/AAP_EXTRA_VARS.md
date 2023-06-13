# AAP extra vars
These are optional extra variables that can be added to the section `other prompts` in AAP template launcher to provide further customization to osbuild.

To get started remove everything from the variables text box and provide any of the variables below in either yaml or json format.

## Role Variables

### builder_custom_repos

Type: complex
Required: false

Custom list of RPM repositories to make available to the
[osbuild](https://www.osbuild.org/) [compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html).

Each list entry is a [YAML dictionary](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)
type and has the following attributes:

| Variable Name | Type                              | Required  | Default Value |
|---------------|-----------------------------------|-----------|---------------|
| name          | string                            | **Yes**   | n/a           |
| base_url      | string                            | **Yes**   | n/a           |
| type          | string                            | No        | "yum-baseurl" |
| check_ssl     | bool                              | No        | true          |
| check_gpg     | bool                              | No        | true          |
| gpgkey_urls   | list of strings                   | No        | omit          |
| rhsm          | bool                              | No        | false         |
| state         | string ("present" or "absent" )   | No  | "present"     |

Example:

```yaml
builder_custom_repos:
  - name: EPEL Everything
    base_url: "https://dl.fedoraproject.org/pub/epel/{{ hostvars[inventory_hostname].ansible_distribution_major_version }}/Everything/x86_64/"
    type: yum-baseurl
    check_ssl: true
    check_gpg: true
    state: present
  - name: My company custom repo
    base_url: "https://repo.example.com/company_repo/x86_64/"
```

### builder_rhsm_repos

Type: list
Required: false

List of RHSM repositories to make available to the
[osbuild](https://www.osbuild.org/) [compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html).

Example:

```yaml
builder_rhsm_repos:
  - "rhocp-4.12-for-rhel-{{ ansible_distribution_major_version }}-{{ ansible_architecture }}-rpms"
  - "fast-datapath-for-rhel-{{ ansible_distribution_major_version }}-{{ ansible_architecture }}-rpms"
```

#### NOTES

osbuild performs builds in [multiple stages](https://www.osbuild.org/guides/developer-guide/osbuild.html?highlight=stage#osbuild)
and if an `*-installer` compose type is defined for `builder_compose_type`, as
defined below, then the build pipeline will include a stage that will create an
ISO Image that can be installed from. The ISO Installer stage has a different
set of package requirements and can sometimes cause package conflicts with the
contents of custom repositories. Therefore, **the repositories defined in this
variable are enabled only for the installable payload the installer will put on
disk, not the bootable ISO itself** and these repositories will be disabled
after the payload build is completed or has failed. In the event content from the
custom repos is required for an `*-installer` compose type (such as customer
drivers are needed), please set the `builder_custom_repos_persist` value to `true`.

### builder_compose_pkgs

Type: list
Required: false

List of RPMs to include in the image.

Example:

```yaml
builder_compose_pkgs:
  - "vim-enhanced"
  - "git"
  - "tmux"
```

### builder_compose_customizations

Type: dict
Required: false

This variable is the YAML dict expression of
[osbuild blueprint](https://www.osbuild.org/guides/blueprint-reference/blueprint-reference.html) customizations.

Example:

```yaml
builder_compose_customizations:
  user:
    name: "testuser"
    description: "test user"
    password: "testpassword"
    key: "{{ builder_pub_key }}"
    groups: '["users", "wheel"]'
  kernel:
    append: "nomst=force"
  services:
    enabled: ["firewalld"]
  firewalld.services:
    enabled: ["ssh", "https"]

```

### builder_kickstart_options

Type: list
Required: false

List of kickstart options to add to the kickstart file

Example:

```yaml
builder_kickstart_options:
  - lang en_US.UTF-8
  - keyboard us
  - timezone Etc/UTC --isUtc
  - text
  - zerombr
  - clearpart --all --initlabel
  - autopart
  - reboot
  - ostreesetup --nogpg --osname=rhel --remote=edge --url=http://{{ ansible_host }}/{{ builder_blueprint_name }}/repo/ --ref={{ builder_blueprint_ref }}
```

### additional_kickstart_post

Type: list
Required: false

List of kickstart post options to add to the kickstart file. Use default(None)
when conditionally setting a variable in the builder_kickstart_post list.

Example:

```yaml
additional_kickstart_post:
  - "{{ microshift_image_ovn_options_template | default(None) }}"
```

## License

GPLv3
