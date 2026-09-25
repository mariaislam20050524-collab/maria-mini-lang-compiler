start {

    logic a = yes;
    logic b = no;

    check (a && b) {
        show "Both true";
    }

    check (a || b) {
        show "At least one true";
    }

}