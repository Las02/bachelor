
import subprocess

inpath = "../in/"
infile = open(inpath + "allGenusSmall.txt")

stderrFile = open("./stderr.txt", "w")
stdoutFile = open("./stdout.txt", "w")
genus_done = open("./genus_done.txt","w")

for genus in infile:
    genus = genus.strip()
    
    # Run Ribdif
    output = subprocess.run(["./RibDif/RibDif.sh","-g", genus, "-a", "-t","18"], 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)
    print(genus, file = genus_done)
    
stderrFile.close()
stdoutFile.close()
genus_done.close()