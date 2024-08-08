import subprocess
import os
import logging

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='enforce_minimum_password_age.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enforce_minimum_password_age(setting_value):
    try:
        # Create a temporary inf file with the required setting
        with open('password_policy.inf', 'w') as file:
            file.write(f'''
[Unicode]
Unicode=yes
[System Access]
MinimumPasswordAge = {setting_value}
[Version]
signature="$CHICAGO$"
Revision=1
''')

        # Use secedit to apply the security policy settings from the inf file
        subprocess.run(['secedit', '/configure', '/db', 'secedit.sdb', '/cfg', 'password_policy.inf', '/overwrite'], check=True)

        # Clean up the temporary inf file
        os.remove('password_policy.inf')

        logging.info(f'Successfully enforced minimum password age to {setting_value} day(s).')
        print(f'Successfully enforced minimum password age to {setting_value} day(s).')

    except subprocess.CalledProcessError as e:
        logging.error(f'Error applying minimum password age setting: {e}')
        print(f'Error applying minimum password age setting: {e}')

def check_password_policy():
    try:
        # Use secedit to export the current security policy settings
        result = subprocess.run(['secedit', '/export', '/cfg', 'exported_policy.inf', '/areas', 'SECURITYPOLICY'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            # Parse the exported settings from the inf file
            policy_settings = {}
            with open('exported_policy.inf', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=')
                        policy_settings[key.strip()] = value.strip()

            # Print and log the relevant password policy settings
            print("\nCurrent Password Policy Settings:")
            logging.info("Current Password Policy Settings:")
            for setting in ["MaximumPasswordAge", "MinimumPasswordAge", "PasswordHistorySize", "PasswordComplexity"]:
                if setting in policy_settings:
                    print(f"{setting}: {policy_settings[setting]}")
                    logging.info(f"{setting}: {policy_settings[setting]}")
                else:
                    print(f"{setting}: Not found")
                    logging.info(f"{setting}: Not found")

            # Clean up the temporary inf file
            os.remove('exported_policy.inf')
        else:
            print("Error exporting security policy settings.")
            logging.error("Error exporting security policy settings.")
        
    except subprocess.CalledProcessError as e:
        logging.error(f'Error exporting security policy settings: {e}')
        print(f'Error exporting security policy settings: {e}')

if __name__ == '__main__':
    # Set the minimum password age to 1 day
    enforce_minimum_password_age(1)
    # Check the current password policy settings
    check_password_policy()
