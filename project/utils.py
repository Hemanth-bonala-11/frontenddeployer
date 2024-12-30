import re
from frontenddeployer.settings import HOST_URL
import subprocess


def reverse_parse_string(input_string):
    # words = re.split(r'[.,/:]', input_string)
    # print(words)
    # # Filter out empty strings
    # words = [word for word in words if word]
    # words.reverse()
    # if words:
    #     if len(words) == 2:  # aiktech.com, aiktech.in
    #         extension = words[0]
    #         domain = words[1]
    #         subdomain = None
    #         protocol = None
    #         return protocol, subdomain, (domain if domain else '') + '.' + (extension if extension else '')
    #     elif len(words) == 3:  # www.aiktech.in, aikam.co.in, eatcake.aiktech.in
    #         if "www" in words:  # www.aiktech.in
    #             extension = words[0]
    #             domain = words[1]
    #             subdomain = None
    #             protocol = words[2]
    #             return protocol, subdomain, (domain if domain else '') + '.' + (extension if extension else '')
    #         elif "aiktech" in words:  # eatcake.aiktech.in
    #             extension = words[0]
    #             domain = words[1]
    #             subdomain = words[2]
    #             protocol = None
    #             return protocol, subdomain, (domain if domain else '') + '.' + (extension if extension else '')
    #         else:  # aikam.co.in
    #             extension = words[0]
    #             domain = words[1]
    #             subdomain = words[2]
    #             protocol = None
    #             return (protocol, subdomain, (subdomain if subdomain else '') +
    #                     '.' + (domain if domain else '') + '.' + (extension if extension else ''))
    #     elif len(words) == 4:  # www.aikam.co.in, www.eatcake.aiktech.in
    #         if "aiktech" in words:  # www.eatcake.aiktech.in
    #             extension = words[0]
    #             domain = words[1]
    #             subdomain = words[2]
    #             protocol = words[3]
    #             return protocol, subdomain, (domain if domain else '') + '.' + (extension if extension else '')
    #         else:  # www.aikam.co.in
    #             extension = words[0]
    #             domain = words[1]
    #             subdomain = words[2]
    #             protocol = words[3]
    #             return (protocol, subdomain, (subdomain if subdomain else '') +
    #                     '.' + (domain if domain else '') + '.' + (extension if extension else ''))
    # else:
    #     return '', '', ''

    try:
        if input_string.endswith(HOST_URL):
            subdomain = input_string[: -len(HOST_URL) - 1]
            return subdomain
        return None
    except Exception as e:
        print(str(e))
        return None

def clone_repo(github_url, subdomain):
    repo_clone_command = ['git', 'clone', github_url, f'templates/{subdomain}']
    with subprocess.Popen(repo_clone_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout.readline():
            yield f"data: {line.strip()}\n\n"  # Print each line as it is received

        # Optionally handle errors
        for error_line in process.stderr:
            yield f"data: {error_line.strip()}\n\n"

def install_packages(subdomain):
    packages_install_command = ['npm', 'i']

    with subprocess.Popen(packages_install_command, cwd=f"templates/{subdomain}",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True) as process:
        for line in process.stdout.readline():
            yield f"data: {line.strip()}\n\n"  # Print each line as it is received

        # Optionally handle errors
        for error_line in process.stderr:
            yield f"data: {error_line.strip()}\n\n"

def build_package(subdomain):
    build_command = ['npm', 'run', 'build']

    with subprocess.Popen(build_command,cwd=f"templates/{subdomain}", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, shell=True) as process:
        for line in process.stdout.readline():
            yield f"data: {line.strip()}\n\n"  # Print each line as it is received

        # Optionally handle errors
        for error_line in process.stderr:
            yield f"data: {error_line.strip()}\n\n"
def change_direcory(subdomain):
    change_directory_command = ['cd', f'templates/{subdomain}']
    with subprocess.Popen(change_directory_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                          text=True) as process:
        for line in process.stdout:
            yield f"data: {line.strip()}\n\n"  # Print each line as it is received

        # Optionally handle errors
        for error_line in process.stderr:
            yield f"data: {error_line.strip()}\n\n"


def deploy_app(github_url, subdomain):
    yield from clone_repo(github_url, subdomain)
    # # yield from change_direcory(subdomain)
    yield from install_packages(subdomain)
    yield from build_package(subdomain)



