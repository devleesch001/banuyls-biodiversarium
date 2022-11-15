from os import listdir, path, mkdir
import sys
from PIL import Image
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
from random import sample
import shutil

def get_image_name_from_txt(txt_name,images_list):
    part_name = txt_name.split(".")
    file_name = ""
    for i in range(len(part_name)-1):
        if file_name !="":
            file_name+="."
        file_name+=part_name[i]
    file_full_name = file_name+"."+images_list[file_name]
    return file_full_name

def main(source,dest,train,test,valid):
    print(source,dest,train,test,valid)
    add_car = "/"
    if source[-1]=="/":
        add_car = ""
    labels_src = source+add_car+"labels/"
    images_src = source+add_car+"images/"
    images_extension = {}
    images = listdir(images_src)
    if dest[-1]!="/":
        dest=dest+"/"

    for img in images:
        part_name = img.split(".")
        name = ""
        for i in range(len(part_name)-1):
            if name !="":
                name+="."
            name+=part_name[i]
        images_extension[name] = part_name[-1]
    for name,ext in images_extension.items():
        print(name,ext)
        break
    if not path.exists(dest):
        mkdir(dest)
    files = listdir(labels_src)
    labels = []
    with open(source+"/classes.txt","r") as f:
        for l in f:
            labels.append(l.replace("\n",""))
    dataset = {}
    for label in labels:
        dataset[label] = []
    for file in files:
        with open(labels_src+file,"r") as f:
            for line in f:
                c,cx,cy,w,h= line.replace("\n","").split(" ")
                classe = labels[int(c)]
                point1 = (float(cx)-float(w)/2,float(cy)-float(h)/2)
                point2 = (float(cx)+float(w)/2,float(cy)+float(h)/2)
                dataset[classe].append({"file":file,"point1":point1,"point2":point2})
    for key,value in dataset.items():
        print(key,len(value))
    # effects = [BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN]
    # for key,value in dataset.items():
    #     if key == "Sar tambour":
    #         for elem in value:
    #             print(elem)
    #             part_name = elem["file"].split(".")
    #             file_name = ""
    #             for i in range(len(part_name)-1):
    #                 if file_name !="":
    #                     file_name+="."
    #                 file_name+=part_name[i]
    #             file_full_name = file_name+"."+images_extension[file_name]
    #             im = Image.open(images_src+file_full_name)
    #             width, height = im.size
                

    #             left = elem["point1"][0]*width
    #             top = elem["point1"][1]*height
    #             right = elem["point2"][0]*width
    #             bottom = elem["point2"][1]*height
    #             print(left,top,right,bottom)
    #             # Cropped image of above dimension
    #             # (It will not change original image)
    #             im1 = im.crop((left, top, right, bottom))
    #             im1.show()
    #             im1.transpose(Image.FLIP_LEFT_RIGHT).show()
    #             im1.filter(BLUR).show()
                
    #             # Shows the image in image viewer
    #             break

    mkdir(dest+"images/")
    mkdir(dest+"labels/")
    mkdir(dest+"images/test/")
    mkdir(dest+"labels/test/")
    mkdir(dest+"images/train/")
    mkdir(dest+"labels/train/")
    mkdir(dest+"images/valid/")
    mkdir(dest+"labels/valid/")

    nb_data = len(files)
    train_list = files
    valid_list = sample(files,int(nb_data*(valid/100)))
    for f in valid_list:
        train_list.remove(f)
    test_list = sample(files,int(nb_data*(test/100)))
    for f in test_list:
        train_list.remove(f)
    
    for f in train_list:
        image_name = get_image_name_from_txt(f,images_extension)
        shutil.copyfile(labels_src+f,dest+"labels/train/"+f)
        shutil.copyfile(images_src+image_name,dest+"images/train/"+image_name)
    
    for f in valid_list:
        image_name = get_image_name_from_txt(f,images_extension)
        shutil.copyfile(labels_src+f,dest+"labels/valid/"+f)
        shutil.copyfile(images_src+image_name,dest+"images/valid/"+image_name)
    
    for f in test_list:
        image_name = get_image_name_from_txt(f,images_extension)
        shutil.copyfile(labels_src+f,dest+"labels/test/"+f)
        shutil.copyfile(images_src+image_name,dest+"images/test/"+image_name)

    with open(dest+"data.yaml","w") as data_conf_file:
        data_conf_file.write("train: "+dest+"images/train\n")
        data_conf_file.write("val: "+dest+"images/valid\n")
        data_conf_file.write("test: "+dest+"images/test\n")
        data_conf_file.write("\n")
        data_conf_file.write("nc: "+str(len(labels))+"\n")
        data_conf_file.write("names: "+str(labels)+"\n")


if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))