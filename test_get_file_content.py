from functions.get_file_content import get_file_content

def main():
    lorem = get_file_content("calculator", "lorem.txt")
    print(len(lorem))
    print(lorem[10000-len(lorem):])
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()