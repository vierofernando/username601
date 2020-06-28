import os
import sys
def main():
    main_file = input("Input your main python bot file. \n>>> ")
    if main_file=="": exit()
    if not main_file.endswith(".py"): main_file += '.py'
    with open("Procfile", "w+") as proc:
        proc.write("worker: python {}".format(main_file))
        proc.close()
    if os.name=='nt': os.system("pip freeze >> requirements.txt")
    else: os.system("pip3 freeze >> requirements.txt")
    os.system("echo {} >> runtime.txt".format('python-'+str(sys.version).split(' ')[0]))
    if os.name=='nt':
        resp = input('Do you have git installed in your system?\nAnd use automatic heroku deployments from a github repo?\n(y/n) >>>')
        if 'y' in resp.lower():
            with open("update.bat", "w+") as f:
                f.write("git add . && git commit -a -m \"Updated files and stuff (AUTO)\" && git push")
                f.close()
        else: print("No? OK then.")
    print("Done.")
if __name__=='__main__': main()
