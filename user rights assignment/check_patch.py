import subprocess
import logging
import re

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='installed_patches.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_hotfix_name(hotfix_id):
    hotfix_names = {
        'KB5037591': 'Windows 11 Cumulative Update for .NET Framework 3.5 & 4.8.1',
        'KB5027397': 'Feature Update to Windows 11, version 23H2',
        'KB5031274': 'Windows 11, version 22H2 out-of-box experience (OOBE)',
        'KB5032381': 'Windows 11, version 22H2 out-of-box experience (OOBE)',
        'KB5039302': 'Windows 11 23H2 update',
        'KB5039338': 'Windows 11 servicing stack update',
    }
    return hotfix_names.get(hotfix_id, 'Unknown')

def get_windows_version(hotfix_id):
    hotfix_versions = {
        'KB5037591': 'Windows 11, version 21H2',
        'KB5027397': 'Windows 11, version 23H2',
        'KB5031274': 'Windows 11, version 22H2',
        'KB5032381': 'Windows 11, version 22H2',
        'KB5039302': 'Windows 11, version 23H2',
        'KB5039338': 'Windows 11, version 21H2',
    }
    return hotfix_versions.get(hotfix_id, 'Unknown')

def get_installed_patches():
    try:
        # Use wmic to get the list of installed patches
        result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            # Split the output into lines
            lines = result.stdout.splitlines()
            
            # Print and log the header
            if lines:
                header = lines[0]
                print(header)
                logging.info(header)
                
                hotfix_details = []
                for line in lines[1:]:
                    print(line)
                    logging.info(line)
                    
                    # Extract HotFixID
                    match = re.search(r'KB\d+', line)
                    if match:
                        hotfix_id = match.group(0)
                        hotfix_name = get_hotfix_name(hotfix_id)
                        hotfix_version = get_windows_version(hotfix_id)
                        hotfix_details.append((hotfix_id, hotfix_name, hotfix_version))
                
                if hotfix_details:
                    # Print and log the hotfix details in tabular form
                    print("\n{:<10} {:<60} {:<30}".format("HotFixID", "Name", "Windows Version"))
                    logging.info("{:<10} {:<60} {:<30}".format("HotFixID", "Name", "Windows Version"))
                    for hotfix_id, hotfix_name, hotfix_version in hotfix_details:
                        print("{:<10} {:<60} {:<30}".format(hotfix_id, hotfix_name, hotfix_version))
                        logging.info("{:<10} {:<60} {:<30}".format(hotfix_id, hotfix_name, hotfix_version))
                else:
                    print("No HotFixIDs found.")
                    logging.info("No HotFixIDs found.")
            else:
                print("No patches found.")
                logging.info("No patches found.")
        else:
            # In case of failure of wmic command
            print("Error querying installed patches.")
            logging.error("Error querying installed patches.")
        
    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying installed patches: {e}')
        print(f'Error querying installed patches: {e}')

if __name__ == '__main__':
    get_installed_patches()
