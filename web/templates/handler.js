class WebManager {
    constructor() {
        this.body = document.getElementById("body");
        this.html = document.getElementsByTagName("html")[0];
        this.body.style.margin = "0";
    }

    usingCSS(path) {
        this.createElement({
            elementName: "link",
            attributes: {
                rel: "stylesheet",
                href: path
            }
        });
    }

    createElement(data) {
        const target = data.at ? (typeof data.at == "object" ? data.at : document.getElementById(data.at)) : this.body;
        const element = document.createElement(data.elementName ? data.elementName : "div");
        
        if (data.id)
            element.setAttribute("id", data.id);
        
        if (data.styles)
            Object.keys(data.styles).forEach(key => {
                element.style[key] = data.styles[key];
            });

        if (data.content)
            element.innerHTML = data.content;

        if (data.onhover && data.styles) {
            element.style.transition = "0.3s";
            element.addEventListener("mouseover", function() {
                Object.keys(data.onhover).forEach(key => {
                    this.style[key] = data.onhover[key];
                });
            });

            element.addEventListener("mouseleave", function() {
                Object.keys(data.styles).forEach(key => {
                    this.style[key] = data.styles[key];
                });
            });
        }

        if (data.attributes)
            Object.keys(data.attributes).forEach(key => {
                element.setAttribute(key, data.attributes[key]);
            });

        target.appendChild(element);
        return element;
    }

    createButton(parameters) {
        const element = document.createElement("button");

        if (parameters.styles)
            Object.keys(parameters.styles).forEach(key => {
                element.style[key] = parameters.styles[key];
            });
        
        if (parameters.content)
            element.innerHTML = parameters.content;

        if (parameters.attributes)
            Object.keys(parameters.attributes).forEach(attribute => {
                element.setAttribute(attribute, parameters.attributes[attribute]);
            });

        if (parameters.link)
            element.addEventListener("click", function() { window.location.href = parameters.link });
        else if (parameters.onclick)
            element.addEventListener("click", parameters.onclick);

        if (parameters.onhover && parameters.styles) {
            element.style.transition = "0.3s";
            element.addEventListener("mouseover", function() {
                Object.keys(parameters.onhover).forEach(key => {
                    this.style[key] = parameters.onhover[key];
                });
            });

            element.addEventListener("mouseleave", function() {
                Object.keys(parameters.styles).forEach(key => {
                    this.style[key] = parameters.styles[key];
                });
            });
        }

        const target = parameters.at ? document.getElementById(parameters.at) : this.body;
        target.appendChild(element);
        return element;
    }

    openLink(url) {
        document.write(`Redirecting you to <a href="${url}">${url}</a>...`);
        window.location.href = url;
    }
}