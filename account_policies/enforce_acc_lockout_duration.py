import subprocess
import logging

# Set up logging
logging.basicConfig(filename='enforce_account_lockout_duration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to apply account lockout duration setting
def set_account_lockout_duration(duration_minutes):
    try:
        # Create a temporary INF file with the required security settings
        inf_content = f"""
[Unicode]
Unicode=yes
[System Access]
LockoutDuration={duration_minutes}
[Version]
signature="$CHICAGO$"
Revision=1
        """
        inf_path = 'account_lockout_duration.inf'
        with open(inf_path, 'w') as inf_file:
            inf_file.write(inf_content)

        # Apply the security settings using secedit
        command = f'secedit /configure /db secedit.sdb /cfg {inf_path} /areas SECURITYPOLICY'
        subprocess.run(command, check=True, shell=True)
        
        # Remove the temporary INF file
        os.remove(inf_path)
        
        logging.info(f'Successfully set account lockout duration to {duration_minutes} minutes')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error setting account lockout duration: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

if __name__ == '__main__':
    # Set the account lockout duration to 15 minutes
    set_account_lockout_duration(15)
