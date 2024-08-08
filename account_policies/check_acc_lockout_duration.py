import subprocess
import os
import logging

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='check_account_lockout_policy.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_account_lockout_policy():
    try:
        # Use secedit to export the current security policy settings
        result = subprocess.run(['secedit', '/export', '/cfg', 'exported_policy.inf', '/areas', 'SECURITYPOLICY'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            # Print the entire contents of the exported_policy.inf file for debugging
            with open('exported_policy.inf', 'r') as file:
                inf_contents = file.read()
                print("Exported Policy Contents:\n")
                print(inf_contents)
                logging.info("Exported Policy Contents:\n")
                logging.info(inf_contents)

            # Parse the exported settings from the inf file
            policy_settings = {}
            with open('exported_policy.inf', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=')
                        policy_settings[key.strip()] = value.strip()

            # Print and log the relevant account lockout policy settings
            print("\nCurrent Account Lockout Policy Settings:")
            logging.info("Current Account Lockout Policy Settings:")
            for setting in ["LockoutDuration", "LockoutBadCount", "ResetLockoutCount"]:
                if setting in policy_settings:
                    print(f"{setting}: {policy_settings[setting]}")
                    logging.info(f"{setting}: {policy_settings[setting]}")
                else:
                    print(f"{setting}: Not found")
                    logging.info(f"{setting}: Not found")

            # Clean up the temporary inf file
            os.remove('exported_policy.inf')
        else:
            # In case of failure of secedit command
            print("Error exporting security policy settings.")
            logging.error("Error exporting security policy settings.")
        
    except subprocess.CalledProcessError as e:
        logging.error(f'Error exporting security policy settings: {e}')
        print(f'Error exporting security policy settings: {e}')

if __name__ == '__main__':
    check_account_lockout_policy()
