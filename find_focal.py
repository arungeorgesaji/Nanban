import math

# Function to calculate focal length using image width and field of view
def calculate_focal_length(image_width, field_of_view):
    return (image_width / 2) / math.tan(math.radians(field_of_view / 2))

# Function to calculate horizontal and vertical field of view from diagonal field of view
def calculate_hfov_vfov(dfov, image_width, image_height):
    diagonal = math.sqrt(image_width ** 2 + image_height ** 2)
    hfov = 2 * math.atan(math.tan(math.radians(dfov / 2)) * math.cos(math.atan(image_height / image_width)))
    vfov = 2 * math.atan(math.tan(math.radians(dfov / 2)) * math.sin(math.atan(image_height / image_width)))
    return math.degrees(hfov), math.degrees(vfov)

# Given parameters
image_width = 1280  # Width of the image in pixels
image_height = 720  # Height of the image in pixels
diagonal_fov = 78  # Diagonal field of view in degrees

# Calculate focal length
focal_length = calculate_focal_length(image_width, diagonal_fov)
print("Approximate focal length:", focal_length)

# Calculate horizontal and vertical field of view
hfov, vfov = calculate_hfov_vfov(diagonal_fov, image_width, image_height)
print("Horizontal field of view:", hfov)
print("Vertical field of view:", vfov)
