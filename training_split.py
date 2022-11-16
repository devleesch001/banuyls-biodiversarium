from os import listdir, path, mkdir
import sys
from PIL import Image
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
from random import sample
import shutil
import argparse
import random
from pathlib import Path

def get_image_name_from_txt(txt_name,images_list):
    part_name = txt_name.split(".")
    file_name = ""
    for i in range(len(part_name)-1):
        if file_name !="":
            file_name+="."
        file_name+=part_name[i]
    file_full_name = file_name+"."+images_list[file_name]
    return file_full_name

def transform_image(image):

    filters = [BLUR, DETAIL, EDGE_ENHANCE_MORE, SMOOTH, SMOOTH_MORE, SHARPEN]
    rotation = random.randint(-30,30)
    filt = filters[random.randint(0,len(filters)-1)]
    im = image.filter(filt)
    if random.randint(0,1)==1:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = im.rotate(rotation)
    return im


def main(source,dest,train,test,valid,generate_images):
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
    generated_images = []
    if generate_images:
        if not path.exists("/tmp/analyse_fish/"):
            mkdir("/tmp/analyse_fish/")
        max_class_number = 0
        for key,value in dataset.items():
            size = len(value)
            if size>max_class_number:
                max_class_number = size
        for key,value in dataset.items():
            nb_images_to_gen = max_class_number-len(value)
            if nb_images_to_gen!=0:
                nb_generated = 0
                print("generating images",nb_images_to_gen,"for",key)
                for i in range(len(value)):
                    nb_to_gen = int((nb_images_to_gen-nb_generated)/(len(value)-i))
                    if nb_to_gen!=0:
                        elem = value[i]
                        part_name = elem["file"].split(".")
                        file_name = ""
                        for k in range(len(part_name)-1):
                            if file_name !="":
                                file_name+="."
                            file_name+=part_name[k]
                        file_full_name = file_name+"."+images_extension[file_name]
                        im = Image.open(images_src+file_full_name)
                        width, height = im.size                        

                        left = elem["point1"][0]*width
                        top = elem["point1"][1]*height
                        right = elem["point2"][0]*width
                        bottom = elem["point2"][1]*height
                        try:
                            for j in range(nb_to_gen):
                                im1 = im.crop((left, top, right, bottom))
                                im1 = transform_image(im1)
                                name = key.replace(" ","_")+"_"+str(i)+"_"+str(j)
                                path_image = "/tmp/analyse_fish/"+name+".jpg"
                                generated_images.append({"name":name,"label":key,"path":path_image})
                                im1.save(Path(path_image))
                                nb_generated+=1
                        except Image.DecompressionBombError:
                            print("Image trop grande pour la génération")

    print("Split des images")
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

    if len(generated_images) !=0:
        print("Déplacement des images générés")
        random.shuffle(generated_images)
        ind = int(len(generated_images)*(train/100))
        print(len(generated_images))
        train_list = generated_images[:ind]
        remaining_list =generated_images[ind:]
        print("train generated",len(train_list))
        for data in train_list:
            name = data["name"]
            shutil.copyfile(data["path"],dest+"images/train/"+name+".jpg")
            with open(dest+"labels/train/"+name+".txt","w") as img_conf_file:
                img_conf_file.write(str(labels.index(data["label"]))+" 0.5 0.5 1.0 1.0")
        ind = int(len(generated_images)*(test/100))
        test_list = remaining_list[:ind]
        valid_list = remaining_list[ind:]
        print("test generated",len(test_list))
        for data in test_list:
            name = data["name"]
            shutil.copyfile(data["path"],dest+"images/test/"+name+".jpg")
            with open(dest+"labels/test/"+name+".txt","w") as img_conf_file:
                img_conf_file.write(str(labels.index(data["label"]))+" 0.5 0.5 1.0 1.0")
        print("valid generated",len(valid_list))
        for data in valid_list:
            name = data["name"]
            shutil.copyfile(data["path"],dest+"images/valid/"+name+".jpg")
            with open(dest+"labels/valid/"+name+".txt","w") as img_conf_file:
                img_conf_file.write(str(labels.index(data["label"]))+" 0.5 0.5 1.0 1.0")
    #shutil.rmtree("/tmp/analyse_fish")
    with open(dest+"data.yaml","w") as data_conf_file:
        data_conf_file.write("train: "+dest+"images/train\n")
        data_conf_file.write("val: "+dest+"images/valid\n")
        data_conf_file.write("test: "+dest+"images/test\n")
        data_conf_file.write("\n")
        data_conf_file.write("nc: "+str(len(labels))+"\n")
        data_conf_file.write("names: "+str(labels)+"\n")
    print("End")

if __name__ == "__main__":
    
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument('source', type=str,help='Chemin de la source du dataset au format de sortie de label studio pour yolo')
    parser.add_argument('destination', type=str,help='Chemin de destination du dataset')
    parser.add_argument('training', type=int,help='Pourcentage du dataset utilisé pour l\'entrainement')
    parser.add_argument('test', type=int,help='Pourcentage du dataset utilisé pour le test')
    parser.add_argument('validation', type=int,help='Pourcentage du dataset utilisé pour la validation')
    parser.add_argument("-g", "--generate-images", help = "Génère des images pour équilibrer les classes", action="store_true")
    
    # Read arguments from command line
    args = parser.parse_args()

    main(args.source,args.destination,args.training,args.test,args.validation,args.generate_images)