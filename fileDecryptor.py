import json, argparse, binascii, os, sys

def terminate(msg:str): #End the script with a print
    print(msg)
    sys.exit()

def xor(data, key): #XOR Encryption/Decryption
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 

def getKey(path:str):
    f = open(path, 'rb')
    data = json.loads(f.read())
    key = data["encryptionKey"] #This is the name of the dict key
    print('The key is: '+key)
    return bytearray(binascii.unhexlify(key))

def getFilename(path): #Change the extension for the consequent
    if path.endswith(".rpgmvo"):
        return path[:-7]+".ogg"
    elif path.endswith(".rpgmvm"):
        return path[:-7] + ".m4a"
    elif path.endswith(".rpgmvp"):
        return path[:-7] + ".png"

def getFileDecrypted(path, key, output): #Decrypt the file
    file = open(path, "rb").read()
    file = file[16:]
    text1 = bytearray(file[:16])
    text2 = xor(text1, key)
    file = file[16:]

    dirPath = getFilename(path)
    newFile = os.path.basename(dirPath) #get filename

    if output == os.getcwd()+'/output' and not os.path.exists(os.getcwd()+'/output'): #If output doesn't exist
        os.mkdir(os.getcwd()+'/output')

    open(output+'/'+newFile, "wb").write(text2 + file) #Create the file

def main():
    parser = argparse.ArgumentParser(prog='fileDecryptor', description='decrypt a file from your RPG Maker MV game')
    parser.add_argument("--i", help='define the directory path', type=str, required=True)
    parser.add_argument("--f", help='define the file path', type=str, required=True)
    parser.add_argument("--o", help='define the output path', type=str, default=os.getcwd()+'/output') #Optional
    args = parser.parse_args()
    i = args.i
    f = args.f
    o = args.o

    if not os.path.exists(i) or not os.path.exists(f) or not os.path.exists(o): #Check if paths exist
        terminate('You must introduce an existing path.')
    elif not os.path.exists(i+'/data'): #Check if directory 'data' exists
        terminate("The directory '/dir/data' is missing.")
    elif not os.path.exists(i+'/data/System.json'): #Check if file 'System.json' exists
        terminate("The file 'System.json' is missing in '/dir/data'.")
    else:
        k = getKey(i+'/data/System.json') #Extract key from System.json
        getFileDecrypted(f, k, o) #Decrypt the file then create the file in output

if __name__ == '__main__':
    main()
