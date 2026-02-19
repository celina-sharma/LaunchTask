from src.pipelines.ask_image_pipeline import ask_image

result = ask_image("What percentage is Northeast region?")

print("\nANSWER:\n", result["answer"])
print("\nEVALUATION:\n", result["evaluation"])
print("\nRETRIEVED IMAGES:\n", result["retrieved_images"])
