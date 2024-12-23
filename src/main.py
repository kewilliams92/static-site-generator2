from textnode import TextNode, TextType


def main():
    textnode = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(textnode)


main()
