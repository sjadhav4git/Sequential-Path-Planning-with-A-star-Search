import json
from color_pallet_image_generator import image_generator
from Algorithm import Algorithm
import cv2

CPIG = image_generator()
ALGO = Algorithm()
raw_puzzle_pattern = CPIG.read_pattern(True)
raw_target_pattern = CPIG.read_pattern(False)
puzzle_pattern, target_pattern = CPIG.rowwise_patterns(raw_puzzle_pattern, raw_target_pattern)

data = {
    "puzzle_pattern" : puzzle_pattern.tolist(),
    "target_pattern" : target_pattern.tolist(),
    "raw_puzzle_pattern" : raw_puzzle_pattern,
    "raw_target_pattern" : raw_target_pattern   
}

with open("patterns.json","w") as json_file:
    json.dump(data,json_file,indent=4)

with open("patterns_copy.json","w") as json_file:
    json.dump(data,json_file,indent=4)

print("data saved to patterns.json")
print("press '0' to continue..")

# print created puzzle
latest_puzzle = CPIG.generate_image_puzzle_pattern(puzzle_pattern,5)
latest_target = CPIG.generate_image(raw_target_pattern,3)

cv2.imshow("puzzle_pattern",latest_puzzle)
cv2.imshow("target_pattern",latest_target)
cv2.waitKey(0)