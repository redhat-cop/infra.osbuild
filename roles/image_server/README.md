Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Run osbuild_image_server role
      hosts: all
      become: true
      tasks:
        - name: Get list of all created images
          osbuild.composer.get_all_finished_images:
          register: all_images

        - name: Create directory to hold all rhel version directories
          ansible.builtin.file:
            path: /var/www/html/rhel{{ ansible_distribution_major_version }}/
            state: directory
            mode: '0755'

        - name: Create directory to hold all image directories
          ansible.builtin.file:
            path: /var/www/html/rhel{{ ansible_distribution_major_version }}/images/
            state: directory
            mode: '0755'

        - name: run the role for each finished image
          with_items: "{{ all_images['result']['finished'] }}"
          ansible.builtin.include_role:
            name: osbuild.composer.image_server
          vars:
            image_uuid: "{{ item  }}"


License
-------

GNU General Public License v3.0

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
