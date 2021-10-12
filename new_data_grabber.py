import base64
import paramiko # used for ssh and sftp
import os
import time
# from icecream import ic

remote_path = '~/Projects/Attune/scope_control_app/static/captured_pics/'

# Get a list of local directoriess
panormas_path = "app/static/caps_img/"
local_dirs = [ name for name in os.listdir(panormas_path) if os.path.isdir(os.path.join(panormas_path, name)) ]
print(local_dirs)

# create a SSH client instance, Create a 'host_keys' object and load our local known hosts  
# and Connect to our remote host using the SSH client
client = paramiko.SSHClient()
host_keys = client.load_system_host_keys()
client.connect('attune-jetson.local', username='attune', password='attune2020')


# Assign our input, output and error variables to a command we will be issuing to the remote system 
stdin, stdout, stderr = client.exec_command(
    f'ls {remote_path}'
)
# Wait for the command to finish 
time.sleep(2)

# Make a list of remote directories
remote_dirs = []
for line in stdout:
    remote_dirs.append(line.strip('\n'))
    # print('... ' + line.strip('\n'))
print(remote_dirs)

# compare local dirs and remote dirs and crete missing local dirs
new_dirs = list(set(remote_dirs) - set(local_dirs))
if len(new_dirs) > 0:
    print(f'Found {len(new_dirs)} New directories: {str(new_dirs)}')
    for new_dir in new_dirs:
        new_path = os.path.join(panormas_path, new_dir)
        os.mkdir(new_path)
else:
    print("No new directories found")


# Download new panorama files from the new directories detected on the JetScope
for dir in new_dirs:
    
    stdin, stdout, stderr = client.exec_command(
        f'find {remote_path + dir} -name "*stitched..png" -o -name "*.csv"'
    )
    time.sleep(1)

    try:    
        sftp = client.open_sftp()
        
        for line in stdout:
            remote_file = line.strip('\n')
            local_file = os.path.join(panormas_path, dir, remote_file.split('/')[-1])            
            print(f"Copiying : {remote_file} to {local_file}")            
            
            sftp.get(remote_file, local_file)
            print("File copied")
            # return ["OK",0,0]
        
        sftp.close()
    except IOError as e:
        print(str(e)+" IOERROR")
        # return ["IOERROR: " + str(e),0,0]
    except Exception as e:
        print(str(e)+" OTHER EXCEPTION")
        # return ["Error: " + str(e),0,0]
        

# And finally we close the connection to our client
client.close()