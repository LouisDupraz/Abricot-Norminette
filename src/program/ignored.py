import os


def getIgnoredFiles():
    try:
        os.system("git check-ignore $(find . -type f -print) > .abricotgitignore 2> /dev/null")
        with open(".abricotgitignore", "r") as f:
            git_ignored = f.readlines()
        os.system("rm .abricotgitignore")
    except:
        git_ignored = []
    try:
        with open(".abricotignore", "r") as f:
            abricot_ignored = f.readlines()
    except:
        abricot_ignored = []
    try:
        with open(".plumignore", "r") as f:
            plum_ignored = f.readlines()
    except:
        plum_ignored = []
    ignored = git_ignored + abricot_ignored + plum_ignored
    return [x[2:].replace("\n", "") if x.startswith("./") else x.replace("\n", "") for x in ignored]
