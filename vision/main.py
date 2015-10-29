from readTag import TagInfo
import time

print "Program starts."

Tag = TagInfo()

while (1):
	Tag.Capture()
	if Tag.TagDetected:
		print "Distance: "+ str(Tag.Distance)
		print "Orientation: "+ str(Tag.Orientation)
		print "Value: "+ str(Tag.Value)
	time.sleep(1)