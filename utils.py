from PIL import Image

# image = {"assistant": Image.open("images/download.jpg"), "user": Image.open("images/test_img.jpg")}
image = {
    "user": "path/to/user/avatar.jpg",
    # "assistant": "path/to/default/assistant/avatar.jpg",
    "user": Image.open("images/download.jpg"),
    "default": Image.open("images/download_1.jpg"),
    "assistant_case 1": Image.open("images/download_1.jpg"),
    "assistant_case 2": Image.open("images/download_2.jpg"),
    "header_case 1": Image.open("images/Picture1.png"),
    "header_case 2": Image.open("images/Picture2.png"),
    "header_case 3": Image.open("images/Picture3.png"),
    "header_case 4": Image.open("images/Picture4.png"),
    # Add more case-specific images as needed
}

cases = {
    "case 1": ['You are a chatbot that dont like animals.'],
    "case 2": ['You are a chatbot that loves dogs.'],
    "case 3": ['You are a chatbot that loves cats.'],
    "case 4": ['You are a chatbot that loves birds.'],
}