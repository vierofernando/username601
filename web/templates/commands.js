class CategoryButton {
    constructor(name) {
        this.name = name;
        this.element = document.createElement("button");
        this.element.textContent = name;
        this.element.setAttribute("id", "categoryButton");
    }
    onHover() {
        this.element.style.transition = "0.2s linear";
        this.element.style.cursor = "pointer";
        this.element.style.backgroundColor = "#666666";
    }/*
    onLeave() {
        this.element.style.backgroundColor = "gray";
    }
    onClick() {
        this.element.style.transition = "0.2s";
        this.element.style.backgroundColor = "red";
    }*/
}

class categoryHandler {
    constructor(data, categoriesList) {
        const parameters = new URLSearchParams(window.location.search);

        this.prefix = parameters.has("prefix") ? parameters.get("prefix") : "1";
        this.categoriesList = categoriesList;
        this.currentCategoryId = null;
        this.categoryButtons = [];
        this.commandInfo = JSON.parse(data);
        this.commandInfoElements = [];
        this.commandInfoExtraElements = [];
        this.commandInfoExtraShowedData = new Array(this.commandInfo.length).fill([]);
        
        for (let i = 0; i < this.commandInfoExtraShowedData.length; i++)
            for (let j = 0; j < this.commandInfo[i][this.categoriesList[i]].length; j++)
                this.commandInfoExtraShowedData[i][j] = true;

        this.backgroundColorSeek = ["#666666", "gray", "red"];
    }
    onHelpEvent(index, type) {
        /*if (type != 0) {
            this.commandInfoElements[index].style.transition = (type == 2) ? "0.2s" : "0.2s linear";
        }*/
        //this.commandInfoElements[index].style.transition = "0.2s";
        //this.commandInfoElements[index].style.backgroundColor = this.backgroundColorSeek[type];
        if (type == 2) {
            const status = this.commandInfoExtraShowedData[this.currentCategoryId][index];
            this.commandInfoExtraShowedData[this.currentCategoryId][index] = status ? false : true;
            if (status) this.commandInfoExtraElements[index].removeAttribute("hidden");
            else this.commandInfoExtraElements[index].setAttribute("hidden", "");
        }// else if (type == 1) this.commandInfoElements[index].style.cursor = "pointer";
    }
    hoverEvent(index) {
        this.categoryButtons[index].style.transition = "0.2s linear";
        this.categoryButtons[index].style.backgroundColor = "gray";
    }
    loadCommandInfo() {
        this.commandInfoElements = [];
        this.commandInfoExtraElements = [];

        const divWrapper = document.getElementById("displayCommandsList");
        divWrapper.innerHTML = "";
        let index = 0;
        this.commandInfo[this.currentCategoryId][this.categoriesList[this.currentCategoryId]].forEach(info => {
            const element = document.createElement("div");
            element.setAttribute("id", "commandInfo");
            element.setAttribute("onclick", `handler.onHelpEvent(${index}, 2);`);
            element.setAttribute("onmouseover", `handler.onHelpEvent(${index}, 1);`);
            element.setAttribute("onmouseleave", `handler.onHelpEvent(${index}, 0);`);
            
            const title = document.createElement("div");
            title.setAttribute("id", "commandTitle");
            title.textContent = this.prefix + info.n;

            const desc = document.createElement("div");
            desc.setAttribute("id", "commandDesc");
            desc.textContent = info.f;

            const parameters = (!info.p.length) ? "None" : info.p.join("<br>");
            const apis = (!info.a.length) ? "No APIs used." : info.a.join("<br>");

            const extra = document.createElement("div");
            extra.setAttribute("id", "commandExtraDesc");
            extra.setAttribute("hidden", "");
            extra.innerHTML = `<b>Parameters:</b><br>${parameters}<br><b>APIs:</b><br>${apis}`;
            
            element.appendChild(title);
            element.appendChild(desc);

            divWrapper.appendChild(element);
            divWrapper.appendChild(extra);
            this.commandInfoElements.push(element);
            this.commandInfoExtraElements.push(extra);
            index++;
        });
    }
    clickEvent(index) {
        this.currentCategoryId = index;
        this.loadCommandInfo();
    }
}