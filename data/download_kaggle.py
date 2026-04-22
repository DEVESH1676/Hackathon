import kagglehub

def main():
    print("Downloading dataset from Kaggle...")
    # Download latest version
    path = kagglehub.dataset_download("tobiasbueck/multilingual-customer-support-tickets")

    print("Path to dataset files:", path)

if __name__ == "__main__":
    main()
