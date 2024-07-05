# main logic behind the code 
# use the secedit command to export current password policy setting, parse the .inf file and print the relevant settings in structured mannser. 
import subprocess
# to allow external runnign commands to capture output
import os
# provides functions to interact with operating system 
import logging
#to facilitate logging messages to a file or other output for debugging and monitoring 

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='check_password_policy.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_password_policy():
    try:
        # use secedit to export the current security policy settings
        result = subprocess.run(['secedit', '/export', '/cfg', 'exported_policy.inf', '/areas', 'SECURITYPOLICY'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            # print the entire contents of the exported_policy.inf file for debugging
            with open('exported_policy.inf', 'r') as file:
                inf_contents = file.read()
                print("Exported Policy Contents:\n")
                print(inf_contents)
                logging.info("Exported Policy Contents:\n")
                logging.info(inf_contents)

            # parse the exported settings from the inf file
            # separate key and value 
            policy_settings = {}
            with open('exported_policy.inf', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=')
                        policy_settings[key.strip()] = value.strip()

            # print and log the relevant password policy settings
            print("\nCurrent Password Policy Settings:")
            #print a header and check in policy setting for each setting 
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
            #in case of failure of secedit command
            print("Error exporting security policy settings.")
            logging.error("Error exporting security policy settings.")
        
    except subprocess.CalledProcessError as e:
        logging.error(f'Error exporting security policy settings: {e}')
        print(f'Error exporting security policy settings: {e}')

if __name__ == '__main__':
    check_password_policy()
