# infra.osbuild.builder

This role automates [osbuild](https://www.osbuild.org/) [compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html)
using the osbuild backend [Weldr](https://weldr.io/) API.

## Requirements

The role requires a system to be running the `osbuild-composer` service which
the `infra.osbuild.builder` role will automate the deployment of.

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

#### NOTES:

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

### builder_custom_repos_persist

Type: bool
Required: false

This variable will cause custom repositories provided in the `builder_custom_repos`
variable to persist for all osbuild stages.

### builder_blueprint_name

Type: string
Required: false

This is the name of the [osbuild blueprint](https://www.osbuild.org/guides/blueprint-reference/blueprint-reference.html?highlight=distro#distribution-selection-with-blueprints)
to use. The blueprint will be auto generated based on the contents of the 
`builder_compose_customizations` role variable. In the event an of an [rpm-ostree](https://rpm-ostree.readthedocs.io/en/stable/)
based compose type specified by the `builder_compose_type` role variable, the
blueprint name defined in this variable will use used to define the resulting [ostree](https://ostreedev.github.io/ostree/)
repository.

### builder_blueprint_src_path

Type: string
Required: false

This is the path to a location on the osbuild server that the generated
blueprint should be stored at and used as the source content for the osbuild
compose build.

### builder_ostree_url

Type: string
Required: false

This variable is used to pass the ostree repo url of a perviously built commit to build an installer from. When this variable is not defined a new commit will be built for the installer.

Example:
```yaml
builder_ostree_url: "http://0.0.0.0/test_blueprint_aap/repo/"
```

### builder_blueprint_ref

Type: string
Required: false

This variable need not be set and is only used when an [rpm-ostree]() based
image is defined in the `builder_compose_type` variable. The `builder_blueprint_ref`
variable defines the [ostree](https://ostreedev.github.io/ostree/) ref (branch)
to commit the ostree payload to in the resulting ostree repository on the
osbuild server.


### builder_compose_type

Type: string
Required: false

This variable defines the type of compose desired, valid inputs will vary based
on operating system (RHEL, CentOS Stream, or Fedora) and release version therin.

For RHEL, the Red Hat Enterprise Linux Documentation Team publishes these and they can be found [here](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/composing_a_customized_rhel_system_image/index#composer-output-formats_composer-description).

For CentOS Stream and Fedora, you will need to reference the output of the 
`composer-cli compose types` command on the osbuild server (this can also be 
done on RHEL if preferred).

### builder_wait_compose_timeout

Type: int
Required: false

The amount of time in seconds that the wait_compose module will wait for a build to complete before failing. By default wait_compose waits for 1800 seconds unless this variable is set.

Example:
```yaml
builder_wait_compose_timeout: 2400
```

### builder_password

Type: string
Required: false

Password for the user that is created by the kickstart file

builder_password or builder_pub_key needs to be defined when using the kickstart file

### builder_pub_key

Type: string
Required: false

Path to location of ssh public key to inject into the resulting image to allow
key-based ssh functionality without extra configuration for systems installed
with the resulting build media.

builder_password or builder_pub_key needs to be defined when using the kickstart file


Example:
```yaml
builder_pub_key: ~/.ssh/id_rsa.pub
```

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

### builder_compose_customizations:

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

### builder_image_storage_threshold
Type: int
Required: false

The minimum amount of space left for the image storage expressed as a percentage.
For example defining 3 (default) means there needs to be at least 3% left of storage for images to be built successfully.

Example:
```yaml
builder_image_storage_threshold: 3
```

### builder_image_storage_cleared
Type: bool
Required: false

This variable will cause all images to be removed

Example:
```yaml
builder_image_storage_cleared: true
```

## Kickstart Variables

Varibles used to create a kickstart file

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
  - user --name={{ builder_compose_customizations['user']['name'] }} {{ "--password" if builder_password is defined  }} {{ builder_password if builder_password is defined }} --group=wheel,user
  - ostreesetup --nogpg --osname=rhel --remote=edge --url=http://{{ ansible_host }}/{{ builder_blueprint_name }}/repo/ --ref={{ builder_blueprint_ref }}
```

### builder_kickstart_post

Type: list
Required: false

List of kickstart post options to add to the kickstart file. Use default(None) when conditionally setting a variable in the builder_kickstart_post list.

Example:
```yaml
builder_kickstart_post: 
  - "{{ lookup('ansible.builtin.template', '../templates/auto_register_aap.j2') }}"
  - "{{ microshift_image_ovn_options_template | default(None) }}"
```

## Kickstart AAP Variables

Define these variables to auto register the system with AAP

Example: 
```yaml
builder_aap_url: 'https://<IP_ADDRESS>/api/v2/inventories/<INVENTORY_NUMBER>/hosts/'
builder_set_hostname: "{% raw %}{{ ansible_default_ipv4.macaddress | replace(':','') }}{% endraw %}"
builder_aap_ks_user: 'user1'
builder_aap_ks_password: 'pass1'
builder_set_variables: "{% raw %}{ipaddress: {{ ansible_all_ipv4_addresses }}, macaddress: '{{ ansible_default_ipv4.macaddress }}' }{% endraw %}"
```

### builder_aap_url

Type: string
Required: false

Optionally perform automatic enrollment of systems installed via the resulting
image build using a companion [kickstart](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/installation_guide/chap-kickstart-installations)
with [Ansible Automation Platform](https://www.ansible.com/products/automation-platform),
then set this variable to point to the URL where the Ansible Automation Platform
can be reached.

### builder_set_hostname

Type: string
Required: false

Example:
```yaml
builder_set_hostname: "{% raw %}{{ ansible_default_ipv4.macaddress | replace(':','') }}{% endraw %}"
```

### builder_aap_user

Type: string
Required: false

### builder_aap_ks_user

Type: string
Required: false

### builder_aap_ks_password

Type: string
Required: false

Example:
```yaml
builder_set_variables: "{% raw %}{ipaddress: {{ ansible_all_ipv4_addresses }}, macaddress: '{{ ansible_default_ipv4.macaddress }}' }{% endraw %}"
```

## Variables Exported by the Role

None.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Run osbuild_builder role
  become: true
  hosts: all
  vars:
    builder_compose_type: edge-commit
    builder_blueprint_name: mybuild
    builder_pub_key: ~/.ssh/id_rsa.pub
    builder_compose_pkgs:
      - vim-enhanced
      - httpd
      - ansible-core
      - tmux
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
        enabled: ["httpd", "sshd", "firewalld"]
      firewalld.services:
        enabled: ["ssh", "https"]
  tasks:
    - name: Run the role
      ansible.builtin.import_role:
        name: infra.osbuild.builder
```


## License

GPLv3

