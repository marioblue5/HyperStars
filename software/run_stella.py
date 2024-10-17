import paramiko
import time
import os

class ShellHandler:

    def __init__(self, host, user, psw):
        """Initialize and open an interactive shell session on the Jetson Nano."""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, password=psw, port=22)

        # Open an interactive shell channel
        self.channel = self.ssh.invoke_shell()
        self.stdin = self.channel.makefile('wb')
        self.stdout = self.channel.makefile('r')

    def __del__(self):
        """Close the SSH connection when the object is destroyed."""
        self.ssh.close()

    def execute(self, cmd):
        """
        Execute a command in the interactive shell and return the output and error.
        
        :param cmd: Command to be executed on the remote machine.
        :return: stdout and stderr output.
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = f'echo {finish} $?'
        self.stdin.write(echo_cmd + '\n')
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                shout = []  # Reset output buffer for real command output
            elif str(line).startswith(finish):
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    sherr = shout  # Capture the stderr in case of failure
                    shout = []
                break
            else:
                # Clean output by removing special characters
                shout.append(line.strip())

        return shout, sherr

    def transfer_file_from_remote(self, remote_path, local_path):
        """
        Transfer a file from the Jetson Nano to the local machine.
        
        :param remote_path: Full path of the file on the Jetson Nano.
        :param local_path: Destination path on the local machine.
        """
        try:
            # Open SFTP connection
            sftp = self.ssh.open_sftp()
            
            # Transfer file from Jetson Nano to local machine
            sftp.get(remote_path, local_path)
            print(f"Successfully transferred {remote_path} to {local_path}")
            
            # Close SFTP connection
            sftp.close()
        except Exception as e:
            print(f"Failed to transfer file: {e}")

def main():
    # Jetson Nano login details
    host = '192.168.137.244'  # Replace with Jetson Nano's IP address
    username = 'stella'  # Replace with your Jetson Nano username
    password = 'chamber3'  # Replace with your Jetson Nano password
    
    # Create a ShellHandler to manage interactive SSH session
    shell = ShellHandler(host, username, password)
    
    try:
        # # Step 2: Run 'run_system.py' in the interactive shell
        # print("Running 'run_system.py'...")
        # shout, sherr = shell.execute('python HyperStars/run_system/run_system.py')
        # if not sherr:
        #     print("run_system.py executed successfully.")
        #     print("\n".join(shout))
        # else:
        #     print("Error during run_system.py execution.")
        #     print("\n".join(sherr))
        
        # Step 3: Transfer a .ply file from the Jetson Nano to the laptop
        remote_ply_file = '/home/stella/HyperStars/run_system/20241014_Data3/camera_intrinsics.json'  # Change this to the actual .ply file path
        local_ply_file = 'C:/Users/Mario/Downloads/camera_intrinsics.json'  # Change this to where you want to store the file locally
        
        print(f"Transferring {remote_ply_file} to {local_ply_file}...")
        shell.transfer_file_from_remote(remote_ply_file, local_ply_file)
        
        print("All processes finished.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        del shell  # Ensure the SSH connection is closed properly

if __name__ == '__main__':
    main()
