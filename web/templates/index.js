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
web.html.style.backgroundColor = color;
web.body.style.backgroundColor = color;
const foregroundColor = getForegroundColor();
document.title = title;

const navbar = new NavbarManager({
    Home: "buttonHome",
    Commands: "commandsBoard",
    Changelog: "changelogBoard"
});

// PREPARE FOR THE BEST CODE EVER MADE

web.createElement({
    id: "mainBigText",
    content: title,
    styles: {
        color: foregroundColor,
        fontFamily: defaultFont
    }
});

const changelog = new ChangelogParser(CHANGELOG);

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
        color: foregroundColor,
        display: "none"
    }
});

web.createElement({
    id: "commandsTitle",
    at: "commandsBoard",
    content: "COMMANDS",
    styles: {
        fontFamily: defaultFont,
        color: foregroundColor,
        userSelect: "none"
    }
});


web.createElement({
    id: "copyright",
    content: COPYRIGHT_INFO,
    styles: {
        fontFamily: defaultFont,
        color: foregroundColor
    }
});

// NAVBAR PART
navbar.start();