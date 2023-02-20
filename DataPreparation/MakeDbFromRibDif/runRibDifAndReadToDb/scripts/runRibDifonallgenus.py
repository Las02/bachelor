
import subprocess

inpath = "../../get_list_of_all_genus/data/"
infile = open(inpath + "all_genus_TORUN2.dat")

stderrFile = open("./stderr.txt", "a")
stdoutFile = open("./stdout.txt", "a")
genus_done = open("./genus_done.txt","a")

for genus in infile:
    genus = genus.strip()
    
    # Run Ribdif
    output = subprocess.run(["../RibDif/RibDif.sh","-g", genus, "-a", "-t","5"], 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)
    print(genus, file = genus_done)
    
stderrFile.close()
stdoutFile.close()
genus_done.close()