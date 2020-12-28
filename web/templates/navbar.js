class NavbarButton {
    constructor(object, name, element) {
        this.manager = object;
        this.name = name;
        this.element = element;
        this.referenceElement = document.getElementById(this.manager.data[this.name]);
    }

    resolveClick(clickedClass) {
        clickedClass.referenceElement.style.display = "none";
        this.referenceElement.style.display = "block";
    }

    set(bool) {
        this.element.style.backgroundColor = bool ? "red" : lowerContrast(25);
        this.element.style.color = bool ? "white" : foregroundColor;
        this.element.style.cursor = bool ? "not-allowed" : "pointer";
        this.element.onmouseover = bool ? null : function() {
            this.style.backgroundColor = lowerContrast(65);
        };

        this.element.onmouseleave = bool ? null : function() {
            this.style.backgroundColor = lowerContrast(25);
        };
    }
}

class NavbarManager extends WebManager {
    constructor(data) {
        super();
        this.mainElement = this.createElement({
            id: "navbar",
            styles: {
                backgroundColor: lowerContrast(25),
                width: "100%",
                userSelect: "none"
            }
        });
        this.data = data;
    }

    start() {
        this.divs = new Array();
        this.classes = new Array();
        this.index = 0;
        Object.keys(this.data).forEach(pageName => {
            const navbarPage = this.createElement({
                at: this.mainElement,
                id: "navbarButton",
                content: pageName,
                styles: {
                    backgroundColor: lowerContrast(25),
                    color: foregroundColor,
                    fontFamily: defaultFont,
                    fontSize: "150%",
                    fontWeight: "bold",
                    padding: "10px 35px",
                    textAlign: "center",
                    display: "inline-block",
                    cursor: "pointer",
                    transition: "0.3s linear"
                }
            });
            this.divs.push(navbarPage);
            navbarPage.onmouseover = function() {
                this.style.backgroundColor = lowerContrast(65);
            };

            navbarPage.onmouseleave = function() {
                this.style.backgroundColor = lowerContrast(25);
            };

            navbarPage.addEventListener("click", function() {
                navbar.resolve(this);
            });

            const elementClass = new NavbarButton(this, pageName, navbarPage);
            this.classes.push(elementClass);
        });


        this.classes[0].set(true);
    }

    resolve(element) {
        const index = this.divs.indexOf(element);
        if (index == this.index) return;

        const beforeClicked = this.classes[this.index];
        this.index = index;
        this.classes[index].resolveClick(beforeClicked);
        
        this.classes[index].set(true);
        beforeClicked.set(false);
    }
}