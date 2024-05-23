from pwd import getpwnam
from grp import getgrnam
from ipaddress import ip_address as ip_addr
from getpass import getpass
import os
import subprocess
import shutil
import json
import random
import string
import re
import socket

def get_linux_distribution():
    try:
        result = subprocess.run(['lsb_release', '-is'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        distribution_id = result.stdout.decode('utf-8').strip()
        return distribution_id
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
def check_root_privileges():
    if os.geteuid() == 0:
        return
    else:
        print("Please run this setup script with root privileges.")
        quit()

def wrap_with_color(string, color=37):
    return f"\033[1;{color}m{string}\033[0m"

def wrapped_print(func):
    def wrapper(*args, **kwargs):
        include_color = kwargs.pop('include_color', True)
        if include_color:
            args = [wrap_with_color(str(arg)) for arg in args]
        return func(*args, **kwargs)
    return wrapper
print = wrapped_print(print)

def wrapped_input(func):
    def wrapper(arg, **kwargs):
        include_color = kwargs.pop('include_color', True)
        if include_color:
            arg = wrap_with_color(str(arg))
        return func(arg, **kwargs)
    return wrapper
input = wrapped_input(input)

def wrapped_getpass(func):
    def wrapper(**kwargs):
        include_color = kwargs.pop('include_color', True)
        if include_color:
            prompt = kwargs.pop('prompt')
            kwargs['prompt'] = wrap_with_color(prompt)
        return func(**kwargs)
    return wrapper
getpass = wrapped_getpass(getpass)

def generate_random_string(length=30):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please enter 'Y' or 'N'.")

def confirm_user_input(prompt):
    while True:
        user_input = input(f'{prompt}: ')
        if yes_or_no(f'Confirm {user_input}? Y/N: '):
            break
        else:
            continue
    return user_input

invalid_user_group_chars = [
    '/', ':', ';', '|', ',', '&', '*', '<', '>', '?', '\\', '"', "'", '(', ')', '[', ']', '{', '}', ' ', '\t', '\n', '\r', '\0', '\x0b'
]
def validate_user_group_chars(s):
    for char in invalid_user_group_chars:
        if char in s:
            raise Exception(f'Invalid character in {s}: {char}')
    return

def validate_service_bind(service_bind):
    def is_port_in_use(port, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((ip, int(port)))
            s.close()
            return False
        except socket.error:
            return True
        
    if service_bind.count(':')!= 1:
        raise Exception('Service bind does not include a port.')
    
    ip_address, port = service_bind.split(':')
    
    try:
        ip_addr(ip_address)
    except:
        raise Exception('Invalid address format.')

    if not port.isdigit() or int(port) < 0 or int(port) > 65535:
        raise Exception('Port number is outside the valid range (0-65535).')
    
    if is_port_in_use(port, ip_address):
        raise Exception('Port is in use or address is out of range.')
    
    return True

def is_valid_domain_name(domain):
    return re.match(r"^(?!:\/\/)(?:[-A-Za-z0-9]+\.)+[A-Za-z]{2,6}$", domain) is not None

def validate_proj_cwd(proj_cwd, cwd):
    if proj_cwd.startswith(cwd):
        raise Exception(f'Directory cannot be a subdirectory of setup source.')
    
    s = ''.join(proj_cwd.split('/'))
    for char in invalid_user_group_chars:
        if char in s:
            raise Exception(f'Invalid character in {proj_cwd}: {char}')
    try:
        if os.path.exists(proj_cwd):
            return True
        else:
            os.makedirs(proj_cwd)
            return True
    except Exception as e:
        raise Exception(f'Invalid directory: {e}')

def systemd_service_exists(service_name):
    result = subprocess.run(['systemctl', 'status', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if f'unit {service_name}.service could not be found'.lower() in result.stderr.lower():
        return False
    return True

def user_exists(username):
    try:
        getpwnam(username)
        return True
    except:
        return False

def create_user(username):
    class PopenWithCheck(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            self.check = kwargs.pop('check', False)
            super().__init__(*args, **kwargs)

        def wait(self, timeout=1):
            returncode = super().wait(timeout)
            if self.check and returncode!= 0:
                raise subprocess.CalledProcessError(returncode, self.argv)

    while True:
        try:
            while True:
                password = getpass(prompt=f"Enter password for '{username}': ")
                confirm = getpass(prompt=f"Confirm password for '{username}': ")
                if password == confirm:
                    break
                else:
                    print('Passwords do not match.')

            subprocess.run(['adduser', '--disabled-password', '--gecos', '', username], check=True)
            
            proc = PopenWithCheck(['passwd', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, check=True)
            proc.stdin.write(f'{password}\n'.encode())  
            proc.stdin.write(password.encode())  
            proc.stdin.flush()
            proc.communicate()
            proc.wait()

            print(f"User '{username}' created successfully.")
            break
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create user '{username}': {e}")

def create_group(group_name):
    print(f'Creating group {group_name}...')
    c = 0
    while True:
        c += 1
        result = subprocess.run(['getent', 'group', group_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True).stdout.strip()
        if result != '':
            print(f'Group {group_name} already exists. Using {group_name}{c} instead...')
            group_name = group_name+str(c)
            continue
        break
    
    subprocess.run(['groupadd', group_name])
    return group_name

def add_user_to_group(user_name, group_name):
    subprocess.run(['usermod', '-aG', group_name, user_name])

def change_directory_ownership(directory_path, uid, gid ):
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.chown(file_path, uid, gid)
                
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                os.chown(dir_path, uid, gid)
    except OSError as e:
        print(f"Failed to change ownership recursively for directory '{directory_path}': {e}")

def create_venv(proj_cwd):
    result = subprocess.run(["python3", "-m", "venv", f"{proj_cwd}/venv"], capture_output=True, text=True)
    error = result.returncode
    if error != 0:
        cmd = result.stdout.splitlines()[4].strip().split(' ')
        cmd.insert(2, '-y')
        subprocess.run(cmd)
        return create_venv(proj_cwd)

def install_packages(proj_cwd):
    subprocess.run([os.path.join(proj_cwd, 'venv', "bin", "pip"), "install", "-r", "requirements.txt"])

def match_item(item, ignore_list):
    for pattern in ignore_list: 
        if re.match(pattern, item):
            return True
    return False

def copy_directory(source, target, ignore_list):
    os.mkdir(target+'/flask')

    for item in os.listdir(source):
        if match_item(item, ignore_list):
            continue

        source_item = os.path.join(source, item)
        target_item = os.path.join(target+'/flask', item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, target_item, ignore=shutil.ignore_patterns(*ignore_list), dirs_exist_ok=True)
        else:
            shutil.copy2(source_item, target_item)

def create_systemd_service(service_name, service_user, proj_cwd):
    with open(f"/etc/systemd/system/{service_name}.service", "w") as f:
        f.write(f"""[Unit]
Description=Gunicorn instance to serve {service_name}
After=network.target

[Service]
User={service_user}
Group=www-data
WorkingDirectory={proj_cwd}/flask
Environment="PATH={proj_cwd}/venv/bin"
ExecStart={proj_cwd}/venv/bin/gunicorn --config {proj_cwd}/flask/gunicorn.conf.py main:app

[Install]
WantedBy=multi-user.target
""")
        f.close()


def get_cert_or_key_path_from_nginx_conf(nginx_conf_file_path, key_or_cert):
    with open(f'{nginx_conf_file_path}', 'r') as f:
        conf = f.readlines()
        for line in conf:
            stripped_line = line.strip()
            if stripped_line.startswith(key_or_cert):
                return ''.join(stripped_line.split(' ')).replace(key_or_cert, '')

def create_certbot_deploy_hook_script(proj_cwd, nginx_conf_file_path, uid, gid):
    script = """import shutil
import os

def get_cert_or_key_path_from_nginx_conf(nginx_conf_file_path, key_or_cert):
    with open(nginx_conf_file_path, 'r') as f:
        conf = f.readlines()
        for line in conf:
            stripped_line = line.strip()
            if stripped_line.startswith(key_or_cert):
                return  ''.join(stripped_line.split(' ')).replace(key_or_cert, '') 

ssl_key_path = get_cert_or_key_path_from_nginx_conf('{nginx_conf_file_path}', 'ssl_certificate')
ssl_key_fname = ssl_key_path.split('/')[-1]
ssl_cert_path = get_cert_or_key_path_from_nginx_conf('{nginx_conf_file_path}', 'ssl_certificate_key')
ssl_cert_fname = ssl_cert_path.split('/')[-1]

new_ssl_cert_path = f"{proj_cwd}/flask/{{ssl_cert_fname}}"
new_ssl_key_path = f"{proj_cwd}/flask/{{ssl_key_fname}}"

shutil.copy(ssl_cert_path, new_ssl_cert_path)
os.chown(new_ssl_cert_path, {uid}, {gid})
os.chmod(new_ssl_cert_path, 0o640)

shutil.copy(ssl_key_path, new_ssl_key_path)
os.chown(new_ssl_key_path, {uid}, {gid})
os.chmod(new_ssl_key_path, 0o640)

""".format(uid=str(uid), gid=str(gid), nginx_conf_file_path=nginx_conf_file_path, proj_cwd=proj_cwd)

    return script

def set_certbot_deploy_hook(script, domain_name, proj_cwd, cwd):
    with open(f'{cwd}/certbot_deploy_hook.py', 'w') as f:
        f.write(script)
        f.close()
    
    with open(f'/etc/letsencrypt/renewal/{domain_name}.conf', 'r') as f:
        cfg = ""
        cfg_ = f.readlines()
        for line in cfg_:
            if line.startswith(f'[renewalparams]'):
                line = f'{line}\ndeploy-hook = python3 {proj_cwd}/flask/certbot_deploy_hook.py'
            cfg += f'{line}\n'
        f.close()
    
    with open(f'/etc/letsencrypt/renewal/{domain_name}.conf', 'w') as f:
        f.write(cfg)
        f.close()
        
    return

def set_nginx_reverse_proxy(domain_name, service_bind, max_body_size, uid, gid, proj_cwd, cwd):
    def handle_https_nginx_conf_line(line):
        stripped_line = line.strip()
        if stripped_line.startswith('listen 80'):
            return ''
        elif stripped_line.startswith('listen [::]:80'):
            return ''
        elif stripped_line.startswith('proxy_pass http'):
            return line.replace('proxy_pass http', 'proxy_pass https')
        else:
            return line

    max_body_size = str(max_body_size)
    use_https = False
    use_certbot = False

    site_conf = """server {{
    listen 80;
    listen [::]:80;
    server_name {domain_name};
    client_max_body_size {max_body_size};

    location / {{
        proxy_pass http://{service_bind};
        include proxy_params;
    }}
    
}}
""".format(domain_name=domain_name, max_body_size=max_body_size, service_bind=service_bind)

    subprocess.run(['apt', 'install', '-y', 'nginx'])

    nginx_conf_file_path = f"/etc/nginx/sites-available/{domain_name}"

    with open(nginx_conf_file_path, 'w') as f:
        f.write(site_conf)
        f.close()

    subprocess.run(['ln', '-s', nginx_conf_file_path, '/etc/nginx/sites-enabled/'])
    subprocess.run(['nginx', '-t'])
    subprocess.run(['systemctl', 'restart', 'nginx'])
    
    if yes_or_no('Use HTTPS? Y/N (You should definitely press N, this needs much more testing. Set up SSL manually for now after setup if you want to use it): '):
        use_https = True
        if not ''.join(domain_name.split('.')).isdigit():
            if yes_or_no('Run certbot for site? (Requires an actual domain name that you own) Y/N: '):
                use_certbot = True
                while True:
                    try:
                        subprocess.run(['apt', 'install', '-y', 'certbot', 'python3-certbot-nginx'], check=True)
                        
                        if yes_or_no('Run certbot with --register-unsafely-without-email option? Y/N: '):
                            subprocess.run(['certbot', '--register-unsafely-without-email'], check=True)
                        subprocess.run(['certbot', '--nginx', domain_name], check=True)
                        
                        ssl_key_path = get_cert_or_key_path_from_nginx_conf(nginx_conf_file_path, 'ssl_certificate')
                        ssl_key_fname = ssl_key_path.split('/')[-1]
                        ssl_cert_path = get_cert_or_key_path_from_nginx_conf(nginx_conf_file_path, 'ssl_certificate_key')
                        ssl_cert_fname = ssl_cert_path.split('/')[-1]

                        shutil.copy(ssl_key_path, f'{cwd}/{ssl_key_fname}')
                        shutil.copy(ssl_cert_path, f'{cwd}/{ssl_cert_fname}')
                        
                        deploy_hook_script = create_certbot_deploy_hook_script(proj_cwd, domain_name, nginx_conf_file_path, uid, gid)
                        set_certbot_deploy_hook(deploy_hook_script, domain_name, proj_cwd, cwd)
                        break
                    except Exception as e:
                        print('Error:', e, 'Try Again.')
                        continue

            else:
                while True:
                    ssl_key_path = confirm_user_input('Enter ssl key absolute path: ').strip()
                    ssl_cert_path = confirm_user_input('Enter ssl cert absolute path: ').strip()
                    try:
                        ssl_key_fname = ssl_key_path.split('/')[-1]
                        shutil.copy(ssl_key_path, f'{cwd}/{ssl_key_fname}')
                        
                        ssl_cert_fname = ssl_cert_path.split('/')[-1]
                        shutil.copy(ssl_cert_path, f'{cwd}/{ssl_cert_fname}')

                        break
                    
                    except Exception as e:
                        print('Error:', e)
                        if yes_or_no('Retry? Y/N: '):
                            continue
                        
                        use_https = False
                        print(f'If you would like to enable HTTPS entirely manually, copy your cert and key to {proj_cwd}/flask after setup is completed, then')
                        print('edit the gunicorn.conf.py certfile and keyfile vars to their filenames respectively and set cert_reqs from 0 to 2, and don\'t forget to edit the /etc/nginx/sites-available file accordingly also')
                        break
                    
        else:
            #TODO LOGIC FOR LOCAL SSL
            pass

    if use_https:
        set_gconf(service_bind, ssl_reqs=(ssl_key_fname, ssl_cert_fname))
        
        with open(nginx_conf_file_path, 'r') as f:
            site_conf = [handle_https_nginx_conf_line(line) for line in f.readlines()]
            f.close()

        if not use_certbot:
            site_conf_ = ""
            for line in site_conf:
                if line.startswith('    client_max_body_size'):
                    line = f'{line}\n    ssl_certificate {proj_cwd}/flask/{ssl_cert_fname};\n    ssl_certificate_key {proj_cwd}/flask/{ssl_key_fname};'
                site_conf_ += f"{line}\n"
                
            with open(nginx_conf_file_path, 'w') as f:
                f.write(site_conf_)
                f.close()
        else:
            with open(nginx_conf_file_path, 'w') as f:
                f.writelines(site_conf)
                f.close()

    return use_https

def set_cfg(domain_name, service_bind, auth_token, max_body_size, use_https=False):
    cfg = json.dumps({
    "domain_name" : domain_name,
    "max_body_size" : max_body_size,
    "service_bind" : service_bind,
    "auth_token" : auth_token,
    "use_https" : use_https
    }, indent=1)
    
    with open('cfg.json', 'w') as f:
        f.write(cfg)
        f.close()
    print("\x1b[4;33m!!!!MAKE SURE TO COPY THIS TO YOUR scraper_cfg.json IN THE DEEP ROCK GALACTIC\BINARIES\WIN64 FOLDER!!!!\x1b[0m\n", include_color=False)
    print(cfg)
    print('\n------------------------------------------------------------------------------------------------------')
    return cfg

def set_gconf(service_bind, ssl_reqs=None):
    gconf = ""
    if ssl_reqs:
        key_fname, cert_fname = ssl_reqs
        
    with open('gunicorn.conf.py', 'r') as f:
        gconf_ = f.readlines()
        
        for line in gconf_:
            if line.startswith('bind'):
                line = f"bind = '{service_bind}'"
            if ssl_reqs:
                if line.startswith('keyfile'):
                    line = f"keyfile = '{key_fname}'"
                elif line.startswith('certfile'):
                    line = f"certfile = {cert_fname}"
                elif line.startswith('cert_reqs'):
                    line = 'cert_reqs = 2'
                    
            gconf += f'{line}\n'

        f.close()
        
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gconf)
        f.close()
        
def initialize_service(service_name):
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "start", service_name])
    subprocess.run(["systemctl", "enable", service_name])

def main():
    cwd = os.path.abspath(__file__)
    cwd = '/'.join(cwd.split('/')[:-1])
    to_cleanup = os.listdir(cwd)
    cleanup_all = True
    
    print('Welcome to the drgmissions service setup. Follow the prompts and make sure to copy down the cfg.json when it is generated.')
    print('------------------------------------------------------------------------------------------------------------------------')
    
    while True:
        service_name = confirm_user_input('Enter service name')
        if service_name in to_cleanup:
            print('Invalid service name.')
            continue

        try:
            validate_user_group_chars(service_name)
            if systemd_service_exists(service_name):
                print(f'{service_name} systemd service already exists. Please choose a different name.')
                continue
            break
        except Exception as e:
            print(f'Error: {e}')
    
    while True:
        service_user = confirm_user_input('Enter service user')
        try:
            validate_user_group_chars(service_user)
        except Exception as e:
            print(f'Error: {e}')
            continue
        
        if user_exists(service_user):
            break
        else:
            if yes_or_no(f'{service_user} is not an existing user. Create user? Y/N: '):
                create_user(service_user)
                break
            
    group_name = create_group(service_name)
    print(f'Adding {service_user} to {group_name} group...')
    add_user_to_group(service_user, group_name)
    
    uid = getpwnam(service_user).pw_uid
    gid = getgrnam(group_name).gr_gid
    
    proj_cwd = f'/home/{service_user}/{service_name}'
    print()
    while True:
        try:
            validate_proj_cwd(proj_cwd, cwd)
            print(f'Project root set to {proj_cwd}.')
            break
        except Exception as e:
            print(f'Error: {e}')
            proj_cwd = confirm_user_input('Specify Project root').strip()
            continue

    if yes_or_no(f'Specify a different project root directory? Y/N: '):
        while True:
            proj_cwd = confirm_user_input('Enter Project root').strip()
            try:
                validate_proj_cwd(proj_cwd, cwd)
                break
            except Exception as e:
                print(f'Error: {e}')
                continue

    while True:
        service_bind = confirm_user_input('Enter service bind (eg 127.0.0.1:5000)')
        try:
            validate_service_bind(service_bind)
            break
        except Exception as e:
            print(f'Invalid service bind: {e}')
    set_gconf(service_bind)
    
    print('Creating venv...')
    create_venv(proj_cwd)
    print('Installing packages...')
    install_packages(proj_cwd)
    
    domain_name = ""
    max_body_size = 200000000
    use_https = False
    if yes_or_no('Set up nginx reverse proxy? Y/N: '):
        while True:
            domain_name = confirm_user_input('Enter domain name for site eg example.com, or enter your machine\'s LAN address (be sure it\'s configured to be static)')
            if ''.join(domain_name.split('.')).isdigit():
                try:
                    ip_addr(domain_name)
                    break
                except:
                    print('Invalid address format. Please enter a valid address.')
                    continue
            else:
                if is_valid_domain_name(domain_name):
                    break
                print('Please enter a valid domain format.')
        
        while True:
            try:
                max_body_size = int(confirm_user_input('Enter max_body_size byte integer value for uploads (leave blank for default 200M, minimum 1M)'))
                if max_body_size < 1000000:
                    print('Please enter a max size equal to or greater than 1,000,000')
                    continue
                if yes_or_no(f'max_body_size set to {max_body_size}. Proceed? Y/N: '):
                    break
            except:
                if yes_or_no(f'max_body_size set to {max_body_size}. Proceed? Y/N: '):
                    break
                
        use_https = set_nginx_reverse_proxy(domain_name, service_bind, max_body_size, service_user, service_name, proj_cwd, cwd)
    
    print('Generating auth token...')
    auth_token = generate_random_string()
    set_cfg(domain_name, service_bind, auth_token, max_body_size, use_https=use_https)
    
    print('Copying files...')
    copy_directory(cwd, proj_cwd, ignore_list=['requirements.txt', 'setup.py', 'test.py', 'split_timestamps.py', 'test.js', 'imgest.js', '\..*'])
    
    print('Creating systemd service...')
    create_systemd_service(service_name, service_user, proj_cwd)
    
    print(f'Changing directory owner to {service_user}...')
    change_directory_ownership(proj_cwd, uid, gid)
    
    print('Initializing service...')
    initialize_service(service_name)
    print(f"{service_name} service enabled and running.")
    
    if cleanup_all:
        print('Cleaning up...')
        if os.getcwd() == cwd:
            os.chdir('..')
        shutil.rmtree(cwd)
    else:
        for f in to_cleanup:
            absf = f"{cwd}/{f}"
            if os.path.isfile(absf):
                os.remove(absf)
            elif os.path.isdir(absf):
                shutil.rmtree(absf)

if __name__ == "__main__":
    distribution_name = get_linux_distribution()
    if distribution_name:
        distribution_name = distribution_name.lower().strip()
        if distribution_name == 'debian' or distribution_name == 'ubuntu':
            check_root_privileges()
            main()
        else:
            print("This setup script is made for Debian or Ubuntu. If you're using something else then edit it to bring it in line with whatever you're using, or emulate it manually however you feel like.")
    else:
        print("This setup script is made for Debian or Ubuntu. If you're using something else then edit it to bring it in line with whatever you're using, or emulate it manually however you feel like.")