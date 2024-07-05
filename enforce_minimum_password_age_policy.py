import subprocess
import os
import logging

# set up logging
# to capture the activity and any errors that occur
# writes the necessary configuration to a temporary .inf file.
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
        # /configure option to apply the settings from the .inf file
        # /db option specifies the security database file
        # /overwrite option ensures that existing settings in the database are overwritten
        subprocess.run(['secedit', '/configure', '/db', 'secedit.sdb', '/cfg', 'password_policy.inf', '/overwrite'], check=True)

        # Clean up the temporary inf file
        os.remove('password_policy.inf')

        logging.info(f'Successfully enforced minimum password age to {setting_value} day(s).')
        print(f'Successfully enforced minimum password age to {setting_value} day(s).')

    # if error during execution of secedit command, logged and printed to console 
    except subprocess.CalledProcessError as e:
        logging.error(f'Error applying minimum password age setting: {e}')
        print(f'Error applying minimum password age setting: {e}')

if __name__ == '__main__':
    # Set the minimum password age to 1 day
    enforce_minimum_password_age(1)
