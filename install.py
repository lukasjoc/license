import os
from os import path
import sys
import stat
import git
import pathlib
from datetime import datetime

def main():
    env_user_name = os.getenv("USER")
    env_user_home = os.getenv("HOME")
    xdg_data_home = f"{env_user_home}/.local/share"
    current_year  = datetime.now().strftime("%Y")
                  
    if not env_user_home or not env_user_name:
        print("What is wrong with you :/", file=sys.stderr)
        sys.exit(1)

    out_dir     = f"{xdg_data_home}/license"
    scripts_dir = f"{xdg_data_home}/license/scripts"
    repo_name = "choose_a_license"

    if not path.exists(xdg_data_home):
        os.system(f"mkdir -p {xdg_data_home}")

    if path.exists(out_dir):
        os.system("rm -rf {out_dir}")

    os.system(f"mkdir -p {out_dir}")
    os.system(f"mkdir -p {scripts_dir}")

    if path.exists(f"./{repo_name}"):
        os.system(f"rm -rf {repo_name}")

    try:
        print("Cloning...")
        git.Repo.clone_from(
            "https://github.com/github/choosealicense.com",
            repo_name
        )
    except Exception:
        print("Failed cloning choosealicense repo from github.com", file=sys.stderr)
        sys.exit(1)

    os.system(f"cp ./license {out_dir}")
    scripts = [child
               for child in pathlib.Path(f"./{repo_name}/_licenses").iterdir()
               if child.is_file()]

    for script in scripts:
        basename, _ = path.splitext(path.basename(script)) 
        filename=f"{scripts_dir}/license-{basename}"
        print(f"[Reading <=]: {basename}\t./{repo_name}/_licenses/{basename}")
        ldata = ""
        with open(script, "r+") as f:
            # TODO: try rsplit for split at last occurance
            ldata = f.read().replace("`", "'").split("---")
            text = ldata[len(ldata)-1] #?? maybe wonky (a bit)

            # room for improvement ###
            text = text.replace("[year]"                   , current_year)
            text = text.replace("<year>"                   , current_year)
            text = text.replace("[yyyy]"                   , current_year)
            text = text.replace("<name of author>"         , env_user_name)
            text = text.replace("[name of copyright owner]", env_user_name)
            text = text.replace("[fullname]"               , env_user_name)
            ####

        with open(filename, "w+") as f:
            print(f"[Writing =>]: {basename}\t{filename}")
            f.write("#!/bin/bash\n")
            f.write("cat <<- EOM\n")
            for line in text.split("\n"):
                f.write(f"{line}\n")
            f.write("EOM")
        os.system(f"chmod u+x {filename}")

    print(f"\nAdd:\t{xdg_data_home}/license into your path")
    print(f"Add:\t{xdg_data_home}/license/scripts into your path\n")
    sys.exit(0)

if __name__ == "__main__":
    main()

