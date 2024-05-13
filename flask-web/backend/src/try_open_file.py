file_path = '/Users/jeffreylu/Desktop/24s1/mutimedia/CUB_200/CUB_200_2011/after-images/063.Ivory_Gull/Ivory_Gull_0101_49790.jpg'
try:
    with open(file_path, 'rb') as file:
        # Perform operations on the file
        file_contents = file.read()
        print(file_contents)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except IOError as e:
    print(f"Error opening file: {e}")