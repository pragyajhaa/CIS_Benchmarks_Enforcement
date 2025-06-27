# CIS Benchmarks Enforcement Tool

## Project Overview
This project is a comprehensive Windows security compliance tool designed to enforce and verify Center for Internet Security (CIS) Benchmarks across various Windows operating systems. The tool automates the process of checking and applying security configurations to ensure systems meet industry-standard security best practices.

## Key Features
- **Multi-OS Support**: Compatible with Windows 7, 8, 10, and 11
- **Automated Security Audits**: Scans system configurations against CIS benchmarks
- **Remediation Scripts**: Automated scripts to enforce security policies
- **Detailed Logging**: Comprehensive logging of all security checks and changes
- **Account Policy Management**: Tools to manage password policies and account lockout settings
- **Security Options Configuration**: Scripts to configure various security-related system settings

## Technologies Used
- **Python**: Core scripting language for automation
- **Windows Security Policy**: For system configuration management
- **Batch Scripting**: For system-level operations
- **Windows Registry**: For accessing and modifying system settings

## Project Structure
```
cis_benchmarks/
├── account_policies/      # Scripts for enforcing account policies
├── compiled_scripts/     # OS-specific compiled scripts
├── security_options/     # Security configuration scripts
├── user_rights_assignment/ # User privilege management
├── current_security_settings.inf  # Current system security settings
├── README.md             # This file
└── LICENSE               # Project license
```

## Getting Started

### Prerequisites
- Windows 7/8/10/11 operating system
- Python 3.6 or higher
- Administrative privileges (required for policy enforcement)

### Installation
1. Clone this repository:
   ```
   git clone [repository-url]
   ```
2. Navigate to the project directory:
   ```
   cd cis_benchmarks
   ```

## Usage

### Running Security Audits
To check your system's compliance with CIS benchmarks:

1. Open Command Prompt as Administrator
2. Navigate to the script directory
3. Run the appropriate script for your OS:
   ```
   python compiled_scripts/W10_compiled_script.py  # For Windows 10
   ```

### Enforcing Security Policies
To enforce security policies:

1. Open Command Prompt as Administrator
2. Navigate to the specific policy directory
3. Run the enforcement script:
   ```
   python account_policies/enforce_minimum_password_age_policy.py
   ```

## Logs
All operations are logged in the respective `.log` files within each directory. Check these logs for detailed information about the operations performed.

## License
This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
For any questions or feedback, please open an issue in the repository.