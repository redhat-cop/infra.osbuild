# infra.osbuild.builder

This role automates [osbuild](https://www.osbuild.org/) [compose builds](https://www.osbuild.org/guides/user-guide/user-guide.html)
using the osbuild backend [Weldr](https://weldr.io/) API.

## Requirements

The role requires a system to be running the `osbuild-composer` service which
the `infra.osbuild.setup_server` role will automate the deployment of.

## Role Variables

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

### builder_pub_key

Type: string
Required: false

Path to location of ssh public key to inject into the resulting image to allow
key-based ssh functionality without extra configuration for systems installed
with the resulting build media.

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

