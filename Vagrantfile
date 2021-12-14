Vagrant.configure(2) do |config|

# ... your existing config

  # Custom configuration for docker
  config.vm.provider "docker" do |docker, override|
    # docker doesnt use boxes
    override.vm.box = nil

    # this is where your Dockerfile lives
    docker.build_dir = "."

    # Make sure it sets up ssh with the Dockerfile
    # Vagrant is pretty dependent on ssh
    override.ssh.insert_key = true
    docker.has_ssh = true

    # Configure Docker to allow access to more resources
    docker.privileged = true
  end

# ...

end

 
