# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure('2') do |config|
  config.vm.hostname = 'wikipediapic.2500loops.com'
  config.vm.provider :digital_ocean do |provider, override|
    config.vm.synced_folder '.', '/vagrant', disabled: true

    override.ssh.private_key_path = '~/.ssh/id_rsa'
    override.vm.box = 'digital_ocean'
    override.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"

    provider.client_id = ENV['DIGITALOCEAN_CLIENT_ID']
    provider.api_key = ENV['DIGITALOCEAN_API_KEY']
    provider.image = 'Ubuntu 14.04 x64'
    provider.region = 'Singapore 1'
    provider.size = '512MB'
  end

  config.vm.provision :fabric do |fabric|
    fabric.fabfile_path = './fabfile.py'
    fabric.tasks = ["setup", ]
  end
end
