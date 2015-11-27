from PIL import Image
name = "sample5"
im = Image.open(name+".jpg")
# im.rotate(90).show()
im.rotate(180).save(name+"_2.ppm")