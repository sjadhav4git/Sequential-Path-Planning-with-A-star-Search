# read the data from patterns.json and represent on canvas
import json
import utils.color_pallet_image_generator as cpig
import cv2
CPIG = cpig.image_generator()

# Read data from JSON file
with open("src/database/patterns.json", "r") as json_file:
    data = json.load(json_file)


puzzle_pattern = data["puzzle_pattern"]
raw_target_pattern = data["raw_target_pattern"]

latest_puzzle = CPIG.generate_image_puzzle_pattern(puzzle_pattern,5)
latest_target = CPIG.generate_image(raw_target_pattern,3)

cv2.imwrite('src/database/puzzle.png',latest_puzzle)
cv2.imwrite('src/database/target.png',latest_target)

# print(puzzle_pattern)
# print()
# print(target_pattern)

#visualize: 
cv2.imshow("puzzle_pattern",latest_puzzle)
cv2.imshow("target_pattern",latest_target)
cv2.waitKey(0)
