import subprocess


def get_latest_commit_hash(src_path, module_name):
    try:
        # get latest commit where the module was changed excluding the __version__.py file
        git_command = f'git log -1 --pretty=format:%H -- {src_path}/{module_name} ":^{src_path}/{module_name}/__version__.py"'
        result = subprocess.run(git_command, shell=True, capture_output=True, text=True, check=True)
        # print(git_command)
        # print(result_ := result.stdout.split("\n")[0].strip())
        result_ = result.stdout.split("\n")[0].strip()
        return result_
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def has_code_changed(source_folder: str, module_name: str, sources_data: dict) -> bool|str:
    """
    Check if the code for the module has been modified since last saved commit
    Args:
        module_name:
        source_folder:
        sources_data:

    Returns:

    """

    latest_commit_hash = get_latest_commit_hash(source_folder, module_name)
    latest_hash = sources_data.get(module_name, {}).get('commit_hash')
    if latest_hash and latest_hash == latest_commit_hash:
        return False
    else:
        return latest_commit_hash
