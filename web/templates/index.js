function getForegroundColor() {
    const sum = Math.round(color.slice(4, -1).split(", ").map(n => parseInt(n)).reduce((a, b) => a + b, 0) / 3);
    if (sum < 127)
        return `rgb(255, 255, 255)`;
    return `rgb(0, 0, 0)`;
}

function lowerContrast(amount) {
    const colorValues = color.slice(4, -1).split(", ").map(number => {
        const newNumber = parseInt(number) - amount;
        if (newNumber < 0)
            return "0";
        return newNumber.toString()
    });
    return `rgb(${colorValues.join(", ")})`;
}

function loadFlex(flexObject) {
    web.createElement({
        at: "buttonHome",
        id: "flexer",
        styles: {
            color: foregroundColor,
            fontFamily: defaultFont
        }
    });
    
    Object.keys(flexObject).forEach(key => {
        web.createElement({
            at: "flexer",
            id: "flexerSections",
            content: `<flexerElement>${flexObject[key].toLocaleString()}</flexerElement><br><flexerDesc>${key}</flexerDesc>`
        });
    })
}

var web = new WebManager();

// colors!
var color = `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`;
document.getElementsByTagName("html")[0].style.backgroundColor = color;
const foregroundColor = getForegroundColor();
web.body.style.backgroundColor = color;
document.title = title;

// PREPARE FOR THE BEST CODE EVER MADE

web.createElement({
    id: "mainBigText",
    content: title,
    styles: {
        color: foregroundColor,
        fontFamily: defaultFont
    }
});

web.createElement({
    id: "buttonHome",
    styles: {
        backgroundColor: lowerContrast(20)
    }
});

web.createElement({
    at: "buttonHome",
    elementName: "p",
    content: description,
    styles: {
        color: foregroundColor,
        fontFamily: defaultFont,
        userSelect: "none",
        fontWeight: "bold",
        fontSize: "150%"
    }
});

web.createButton({
    at: "buttonHome",
    content: "Invite the Bot!",
    styles: {
        backgroundColor: lowerContrast(40),
        color: foregroundColor,
        fontFamily: defaultFont,
    },
    onhover: {
        backgroundColor: lowerContrast(80),
        cursor: "pointer"
    },
    attributes: {
        id: "inviteButton"
    },
    link: inviteLink
});

web.createElement({
    id: "commandsBoard",
    styles: {
        backgroundColor: lowerContrast(30),
        fontFamily: defaultFont,
        color: foregroundColor
    }
});

web.createElement({
    id: "commandsTitle",
    at: "commandsBoard",
    content: "COMMANDS",
    styles: {
        fontFamily: defaultFont,
        userSelect: "none"
    }
});