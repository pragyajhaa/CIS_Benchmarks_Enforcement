import subprocess
import logging
import re
import winreg

# Set up logging
logging.basicConfig(filename='system_audit_win10.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_hotfix_name(hotfix_id):
    hotfix_names = {
        'KB5027122': 'Windows 10 May 2023 Cumulative Update',
        'KB5019959': 'Windows 10 October 2022 Cumulative Update',
        'KB4577586': 'Update for Adobe Flash Player Removal',
    }
    return hotfix_names.get(hotfix_id, 'Unknown')

def get_windows_version(hotfix_id):
    hotfix_versions = {
        'KB5027122': 'Windows 10, version 21H2',
        'KB5019959': 'Windows 10, version 20H2',
        'KB4577586': 'Windows 10, version 1909',
    }
    return hotfix_versions.get(hotfix_id, 'Unknown')

def get_installed_patches():
    try:
        result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            if lines:
                hotfix_details = []
                for line in lines[1:]:
                    match = re.search(r'KB\d+', line)
                    if match:
                        hotfix_id = match.group(0)
                        hotfix_name = get_hotfix_name(hotfix_id)
                        hotfix_version = get_windows_version(hotfix_id)
                        hotfix_details.append((hotfix_id, hotfix_name, hotfix_version))
                if hotfix_details:
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
            print("Error querying installed patches.")
            logging.error("Error querying installed patches.")
    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying installed patches: {e}')
        print(f'Error querying installed patches: {e}')

if __name__ == '__main__':
    print("\nFetching Installed Patches...")
    get_installed_patches()
