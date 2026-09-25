start {

    text name = "Sajib";
    text message = name + " Compiler";

    num x = 10;

    check (x > 5 && x < 20) {
        show message;
    }

    do {
        x = x - 1;
    } during (x > 0);

}
