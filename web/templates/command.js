class Command {
    constructor(category, command) {
        this.src = category;
        this.command = command;
        this.index = this.src.manager.commands[this.src.name].indexOf(command);
        this.active = false;
        this.element = this.src.manager.manager.createElement({
            at: this.src.element,
            id: "commandDiv",
            content: botPrefix + command.name,
            styles: {
                backgroundColor: lowerContrast(80),
                color: foregroundColor,
                display: "none",
                transition: "0.3s"
            },
            attributes: {
                onmousedown: `cmds.commandCall(${this.index}, ${this.src.index})`
            }
        });

        this.element.addEventListener("mouseover", function() {
            this.style.backgroundColor = lowerContrast(100);
        });

        this.element.addEventListener("mouseleave", function() {
            this.style.backgroundColor = lowerContrast(80);
        });

        if (this.index == 0) {
            this.element.style.marginTop = "20px";
            this.element.style.borderRadius = "20px 20px 0px 0px";
        } else if (this.index == (this.src.manager.commands[this.src.name].length - 1)) {
            this.element.style.borderRadius = "0px 0px 20px 20px";
        }
    }

    show() {
        this.active = true;
        const parameters = this.command.parameters.length ? `<br><commandsubfont>Parameters:</commandsubfont><br><codeblock>` + this.command.parameters.map(x => x.replace(`<`, `&lt;`).replace(`>`, `&gt;`)).join("<br>") + `</codeblock>` : `<br>`;
        const apis = this.command.apis.length ? (`<commandsubfont>APIs used:</commandsubfont><br>` + (this.command.apis.map(x => `<div id="linkText" onmousedown="web.openLink('${x}')">${x}</div>`).join("<br>"))) : ``;
        this.element.innerHTML = `${this.element.innerHTML}<br><commandDesc>${this.command.function}</commandDesc>${parameters}${apis}`;
    }

    hide() {
        this.active = false;
        this.element.innerHTML = this.element.innerHTML.split("<br>")[0];
    }
}

class Category {
    constructor(object, element) {
        this.manager = object;
        this.element = element;
        this.commandInfos = new Array();
        this.index = this.manager.categoryDivs.indexOf(element);
        this.name = this.manager.categories[this.index];
        this.manager.commands[this.name].forEach(command => {
            const commandElement = new Command(this, command);
            this.commandInfos.push(commandElement);
        });
        this.commandActive = false;
        this.active = false;
    }

    setActive() {
        if (this.commandActive) {
            this.commandActive = false;
            return;
        }

        this.commandInfos.forEach(command => {
            command.element.style.display = this.active ? "none" : "block";
        });
        this.active = !this.active;
    }
}

class CommandManager {
    constructor(web, data) {
        data = JSON.parse(data);

        this.categories = data.map(x => Object.keys(x)[0]).filter(x => x.toLowerCase() != "owner");
        this.commands = {};
        this.manager = web;
        this.categoryDivs = new Array();
        this.categoryClasses = new Array();

        this.categories.forEach(category => {
            const element = this.manager.createElement({
                at: "commandsBoard",
                content: category,
                styles: {
                    fontFamily: defaultFont,
                    color: foregroundColor,
                    backgroundColor: lowerContrast(50),
                    userSelect: "none"
                },
                onhover: {
                    backgroundColor: lowerContrast(70),
                    cursor: "pointer"
                },
                id: "categorySection"
            });
            this.categoryDivs.push(element);

            this.commands[category] = [];
            data[this.categories.indexOf(category)][category].forEach(command => {
                this.commands[category].push({
                    name: command.n,
                    function: command.f,
                    parameters: command.p.map(x => botPrefix + x.split(`: `)[1]),
                    apis: command.a
                });
            });
        });

        this.categoryDivs.forEach(div => {
            div.setAttribute("onmousedown", `cmds.categoryCall(${this.categoryDivs.indexOf(div)});`);

            const category = new Category(this, div);
            this.categoryClasses.push(category);
        });
        delete this.categoryDivs;
    }

    categoryCall(index) {
        this.categoryClasses[index].setActive();
    }

    commandCall(commandIndex, categoryIndex) {
        this.categoryClasses[categoryIndex].commandActive = true;
        const commandClass = this.categoryClasses[categoryIndex].commandInfos[commandIndex];
        if (commandClass.active)
            commandClass.hide();
        else
            commandClass.show();
    }
}