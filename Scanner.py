import requests
import argparse

ip=""

def readtxt(filename):
    with open(filename) as file:
        content = file.read()
    return content
def parser(doc):
    doc.replace('\n',"")
    index=doc.find("<BinaryURL>")
    index1=doc.find("<ImageOrientation>")
    if(index==-1 or index1==-1):
        print("[!]Failed to get image url,exitting.")
        exit(0)
    return doc[index+11:index1-18]
def createScanJob(url,imgdir):
    req=requests.post(url=url,data=readtxt("scanjob.xml"))
    try:
        new_url=req.headers['Location']
    except :
        print("[!]Error,pls check up ip or scanjob.html")
        exit(0)
    print("[-]job created.")
    req2=requests.get(url=new_url)
    link2=parser(req2.text)
    imglink="http://"+ip+link2
    print("[-]Image link is "+imglink)
    print("[-]Downloading images.")
    r=requests.get(url=imglink)
    print("[-]Downloaded images.Wrtiiing.")
    with open(imgdir,'wb') as f:
        f.write(r.content) 
    print("[-]Done,image saved to "+imgdir)

if __name__=="__main__":
    parse = argparse.ArgumentParser(description='ip savepath')
    parse.add_argument('ip', type=str, help='printer ip')
    parse.add_argument('savepath', type=str, help='savepath')
    args = parse.parse_args()
    ip = args.ip
    path = args.savepath
    createScanJob("http://"+ip+"/Scan/Jobs",path)