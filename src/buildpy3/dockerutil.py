import docker
import git
import os
import json
import logging



def check_docker():
    client = docker.from_env()
    
    for container in client.containers.list():
        print(container.__dict__)
        print(container.image.tags)
        print(container.name)
        print(container.status)
        print(container.short_id)
        print(container.id)
        print(container.attrs)
        print(container.logs())
        print(container.top())
        print(container.stats())
        
    

def build_and_stop_containers(git_url, ssh_key_path):
    print("Clone the git repository using SSH key")
    
    project_dir = git_url.split('/')[-1].split('.')[0]
    
    if os.path.exists(f"./{project_dir}"):
        print(f"removing existing project dir ./{project_dir}")
        #os.rmdir(f"./{project_dir}")
        os.system(f'rm -rf ./{project_dir}')
    
    
    logging.warn("Git clone")
    git.Repo.clone_from(git_url, project_dir, env={'GIT_SSH_COMMAND': f'ssh -i {ssh_key_path}'})
    
    docker_options={}
    if os.path.exists(f"./{project_dir}/docker_options.json"):
        with open(f"./{project_dir}/docker_options.json") as f:
            docker_options = json.load(f)            
            if docker_options.get("detach","true") == "true":
                docker_options["detach"]=True
            else:
                docker_options["detach"]=False
    
    
    container_name = ""
    if docker_options.get("name","") != "":
        container_name = docker_options.get("name","")
    
    
    # Get Docker client
    logging.warn("get docker client")
    client = docker.from_env()
    
    # Build the Docker image from the Dockerfile in the cloned repository
    rc=True
    try:
        print(f"building repo {project_dir}")
        client.images.build(path=f'{project_dir}', tag=f'{project_dir}', rm=True)
        for container in client.containers.list():
            print(container.__dict__)
        print(f"Image {project_dir} built successfully.")
    except docker.errors.BuildError as e:
        print(f"Error building Docker image: {e}")
        rc=False
    finally:
        # Remove the cloned repository
        if os.path.exists(f"./{project_dir}"):
            print("would remove now")
            os.system(f'rm -rf ./{project_dir}')
            #os.system('rm -rf webbuilder')

    if rc:
#        container = client.containers.get(container_name)

#        if container is not None:
#            container.stop()
            # Remove the container
#            container.remove()

                
        #Find containers using the same image and stop them
        for container in client.containers.list():
            print(container.image.tags)
            if container_name in container.name:
                logging.warn(f"will stop any {project_dir} containers {container_name}")
                container.stop()
                container.remove
    return docker_options

# Example usage:



def start_container(image_name, docker_options):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # # Define container options
        # container_options = {
        #     'image': 'webbuilder',  # Replace with your image name and tag
        #     'ports': {'5000/tcp': 5000},     # Map port 5000 of the host to port 5000 of the container
        #     'detach': True,                # Run the container in detached mode
        #     'network': 'pickaxe', 
        #     'name' : 'build'
        # }
        
        container_options = docker_options
        
        print(container_options)

        # Run the container
        container = client.containers.run(**container_options)
        print(f"Container {container.id[:12]} started successfully.")
    except docker.errors.APIError as e:
        print(f"Error starting container: {e}")

import logging

def rebuild(git_url,ssh_key_path):
    try:
        project_dir = git_url.split('/')[-1].split('.')[0]
        options = build_and_stop_containers(git_url, ssh_key_path)
        logging.warn(f"Start container")
        start_container(f"{project_dir}", options)
    except Exception as e:
        print(f"Error: {e}")
# Call the function to start the container

if __name__ == "__main__":
    git_url = 'git@github.com:matsvitt/plainagile.git'
    #ssh_key_path = '/Users/matthiasvitt/.ssh/id_rsanop'
    ssh_key_path = '/Users/matthiasvitt/.ssh/id_rsanopasswd'  
    check_docker()
    # try:  
    #     options = build_and_stop_containers(git_url, ssh_key_path)  
    #     start_container("plainagile", options)
    # except Exception as e:
    #     print(f"Error: {e}")
