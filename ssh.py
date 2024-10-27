import random
import subprocess
import sys

def generate_account_details(inisial):
    """Generate a random username and fixed password."""
    random_digits = random.randint(10000, 99999)
    username = f"{inisial}{random_digits}"
    password = "123"  # Fixed password
    return username, password

def create_vpn_account(command, inisial):
    """Create a VPN account using a given command."""
    username, password = generate_account_details(inisial)
    limit_ip = random.randint(100, 999)  # Define IP limit
    duration = 30  # Default expiry duration in days
    
    print(f"Generating account for command: {command}")
    
    try:
        # Split the command into a list for subprocess.run
        command_list = command.split()
        subprocess.run(command_list + [username, password, str(limit_ip), str(duration)], check=True)
        print(f"Account successfully created: Username = {username}, Password = {password}")
    except FileNotFoundError:
        print(f"Error: The file '{command_list[0]}' was not found. Check the path.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating account: {e}")


def main(command, inisial):
    """Main function to create VPN accounts based on the command and inisial."""
    print("\n════════════════════════════════════════════════")
    print("      Creating VPN Account")
    print("════════════════════════════════════════════════\n")
    

    create_vpn_account(command, inisial)

    print("\n════════════════════════════════════════════════")
    print("       VPN Account Creation Complete")
    print("════════════════════════════════════════════════")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 vpn.py <command> <inisial>")
        sys.exit(1)

    command = sys.argv[1]  # Get command from command line argument
    inisial = sys.argv[2]  # Get inisial from command line argument
    main(command, inisial)
