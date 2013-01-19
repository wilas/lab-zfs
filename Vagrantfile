# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.define :zetta do |config|
    vm_name= "zetta"
    config.vm.box = "SL64_box"
    config.vm.host_name = "#{vm_name}.farm"
    config.vm.customize ["modifyvm", :id, "--memory", "2048", "--name", "#{vm_name}"]

    config.vm.network :hostonly, "77.77.77.99"
    config.vm.share_folder "v-root", "/vagrant", "."

    config.vm.provision :puppet do |puppet|
        puppet.manifests_path = "manifests"
        puppet.manifest_file  = "zetta.pp"
        puppet.module_path = "modules"
    end
  end

  config.vm.define :zepto do |config|
    vm_name= "zepto"
    config.vm.box = "SL64_box"
    config.vm.host_name = "#{vm_name}.farm"
    config.vm.customize ["modifyvm", :id, "--memory", "2048", "--name", "#{vm_name}"]

    config.vm.network :hostonly, "77.77.77.98"
    config.vm.share_folder "v-root", "/vagrant", "."

    config.vm.provision :puppet do |puppet|
        puppet.manifests_path = "manifests"
        puppet.manifest_file  = "zetta.pp"
        puppet.module_path = "modules"
    end
  end

end
