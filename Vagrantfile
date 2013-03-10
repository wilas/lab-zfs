# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.define :zetta do |node_config|
    vm_name= "zetta"
    node_config.vm.box = "SL6"
    node_config.vm.host_name = "#{vm_name}.farm"
    node_config.vm.customize ["modifyvm", :id, "--memory", "2048", "--name", "#{vm_name}"]

    node_config.vm.network :hostonly, "77.77.77.99"
    node_config.vm.share_folder "v-root", "/vagrant", "."

    node_config.vm.provision :puppet do |puppet|
        puppet.options = "--hiera_config hiera.yaml"
        puppet.manifests_path = "manifests"
        puppet.manifest_file  = "zetta.pp"
        puppet.module_path = "modules"
    end
  end

  config.vm.define :zepto do |node_config|
    vm_name= "zepto"
    node_config.vm.box = "SL6"
    node_config.vm.host_name = "#{vm_name}.farm"
    node_config.vm.customize ["modifyvm", :id, "--memory", "2048", "--name", "#{vm_name}"]

    node_config.vm.network :hostonly, "77.77.77.98"
    node_config.vm.share_folder "v-root", "/vagrant", "."

    node_config.vm.provision :puppet do |puppet|
        puppet.options = "--hiera_config hiera.yaml"
        puppet.manifests_path = "manifests"
        puppet.manifest_file  = "zetta.pp"
        puppet.module_path = "modules"
    end
  end
end
