import subprocess
import logging

# Set up logging
logging.basicConfig(filename='cis_benchmark_enforcement.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to set account lockout threshold
def set_account_lockout_threshold(threshold):
    try:
        # Execute the command to set the account lockout threshold
        command = f"secedit /configure /db secedit.sdb /cfg \"C:\\Windows\\inf\\defltbase.inf\" /areas SECURITYPOLICY /areas ACCOUNTLOCKOUT /override"
        subprocess.run(command, check=True, shell=True)
        # Now set the specific account lockout threshold
        command = f"net accounts /lockoutthreshold:{threshold}"
        subprocess.run(command, check=True, shell=True)
        
        logging.info(f'Successfully set account lockout threshold to {threshold} invalid logon attempts')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error setting account lockout threshold: {e}')

# Main function to enforce CIS benchmark
def enforce_cis_benchmark():
    account_lockout_threshold = 5  # Recommended value as per CIS benchmark
    set_account_lockout_threshold(account_lockout_threshold)

if __name__ == '__main__':
    enforce_cis_benchmark()
