import numpy as np
import random
import cv2
import math
#Function for distance btw circles
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
# Function to generate random circles in a mask
def generate_random_circles(mask_shape, num_circles, radius):
    mask = np.zeros(mask_shape, dtype=np.uint8) #mask of black colour (array of zeroes)
    height, width = mask_shape[:2]
    pts=[]
    for i in range(num_circles):
        center_x = random.randint(radius, width - radius)
        center_y = random.randint(radius, height - radius)
        lst=[center_x,center_y]
        pts.append(lst)
        color = 255
        cv2.circle(mask, (center_x, center_y), radius, color, -1)  # Draw filled circle
    return pts,mask
#Function to check distance between points
# we define the distaance between any two fan to be 40 (from the centres of the circles)
def check_dist(values):
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            if distance(values[i],values[j])<40:
                return False
    return True

#main program
mask_shape = (500, 500)  # Shape of the mask image
height, width = mask_shape[:2]
num_circles = 10          # Number of circles to generate
radius = 10         #  radius of circles

while True:
    pts,mask = generate_random_circles(mask_shape, num_circles, radius)
    a=check_dist(pts)#spawned by a gap of 40 or not
    if a== False:
        continue
    else:
        break
print (pts)

#bhai comes into the field :-)))
bhaix,bhaiy=(random.randint(20,width-20),random.randint(20,height-20))
cv2.circle(mask,(bhaix,bhaiy),20,125,-1)
# Display the generated mask

print(bhaix,bhaiy)
colorc = 255  # White color
thicknessc = 2  # Thickness of the circle's outline
cv2.circle(mask,(bhaix,bhaiy), 70, colorc, thicknessc)

cv2.imshow('initial Mask', mask)



# to find the final points
finpts=[]
for i in range(10):
        angle = 2 * math.pi * i / 10
        x = bhaix + int(70 * math.cos(angle))
        y = bhaiy + int(70 * math.sin(angle))
        finpts.append([x, y])
print (finpts)

for i in range(len(finpts)):
        for j in range(i+1, len(finpts)):
             print(distance(finpts[i],finpts[j]))

mask_final = np.zeros((500, 500), dtype=np.uint8)
#Bhai did not move
colorc = 255  # White color
thicknessc = 2  # Thickness of the circle's outline
cv2.circle(mask_final,(bhaix,bhaiy),20,125,-1) #Bhai
cv2.circle(mask_final,(bhaix,bhaiy), 70, colorc, thicknessc) #Bhai"s circle of bodygaurds :-))
#new pos of fans
for i in range(10):
        center_x = finpts[i][0]
        center_y = finpts[i][1]
        color = 255
        cv2.circle(mask_final, (center_x, center_y), radius, color, -1)
cv2.imshow('Finalpos', mask_final)



def find_shortest_path(coord1, coord2):
    dupli = coord2.copy()  # Create a duplicate list of coord2
    sd = []
    for point1 in coord1:
        min_distance = float('inf')
        closest_point2 = None
        for point2 in dupli:
            dst = distance(point1, point2)
            if dst < min_distance:
                min_distance = dst
                closest_point2 = point2
        sd.append([point1, closest_point2])
        dupli.remove(closest_point2)  # Remove closest_point2 from dupli
    return sd
sd= find_shortest_path(pts,finpts)
print(sd)

masksecfin = np.zeros((500, 500), dtype=np.uint8)
for point1, point2 in sd:
        cv2.line(masksecfin, point1, point2, (255, 255, 255), 2)

cv2.imshow('Mask with lines', masksecfin)
giant_mask = np.zeros((500, 500), dtype=np.uint8)

# Perform bitwise OR operations to combine the masks
giant_mask = cv2.bitwise_or(giant_mask, mask)
giant_mask = cv2.bitwise_or(giant_mask, masksecfin)
giant_mask = cv2.bitwise_or(giant_mask, mask_final)

# Display the giant mask
cv2.imshow('Giant Mask', giant_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

def create_mask(image_size, center, radius):
    mask = np.zeros(image_size, dtype=np.uint8)
    cv2.circle(mask, center, 10, 255, -1)
    return mask


def interpolate_points(start_point, end_point, num_steps):
    interpolated_points = []
    for i in range(num_steps + 1):
        x = int(start_point[0] + (end_point[0] - start_point[0]) * i*0.1)
        y = int(start_point[1] + (end_point[1] - start_point[1]) *i*0.1)
        interpolated_points.append((x, y))
    return interpolated_points
    
num_steps = 10
step_by_step_masks = []
interpol_history=[]
for i in range(10):
    ip=sd[i][0]
    fp=sd[i][1]
    interpol=interpolate_points(ip, fp, 10)
    interpol_history.append(interpol)
    intermask=[]
    for pt in interpol:
        mask = create_mask((500, 500), pt, radius)
        intermask.append(mask)
    step_by_step_masks.append(intermask)
print(interpol_history)#coord of eveery intermediate step to all the 10 points
#---------------------------------------------------------------------------------------------------------------------------
#WORK IN PROGRESS....
"""
frames=[]
for i in range(1,10):
     frame=[]
     for j in range(10):
        frame.append(interpol_history[j][i])
     frames.append(frame)
print("frames")
print(frames)

#WORK IN PROGRESS....
for i in range(10):
     for j in range(10):
          d=distance(frames[j][i])
"""
#---------------------------------------------------------------------------------------------------------------------------
output_video_path = 'movement_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 1
frame_size = (500, 500)
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

for i in range(num_steps + 1):
    merged_frame = np.zeros(frame_size, dtype=np.uint8)
    for intermask in step_by_step_masks:
        merged_frame = cv2.bitwise_or(merged_frame, intermask[i])
    video_writer.write(cv2.cvtColor(merged_frame, cv2.COLOR_GRAY2BGR))
video_writer.release()


