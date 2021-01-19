class ChangelogParser extends WebManager {
    constructor(data) {
        super();
        this.mainElement = this.createElement({
            id: "changelogBoard",
            styles: {
                backgroundColor: lowerContrast(30),
                fontFamily: defaultFont,
                display: "none"
            }
        });
        this.data = JSON.parse(data).reverse();
        this.currentTime = this.UTC();
        this.lastTime = null;
        this.currentElement = null;

        this.data.forEach(change => {
            const dateChange = new Date(change.slice(2).split(' UTC]')[0]);
            const log = this.parseCodeBlock(change.split(" UTC]` ")[1]);
            const time = this.parseDelta(this.currentTime - Math.round(dateChange.getTime() / 1000));

            if (this.lastTime != time) {
                this.createElement({
                    at: this.mainElement,
                    content: time,
                    id: `changelogTime`,
                    styles: {
                        backgroundColor: lowerContrast(50),
                        color: foregroundColor
                    }
                });
                
                this.currentElement = this.createElement({
                    at: this.mainElement,
                    id: `changelogPart`,
                    content: `${dateChange.toString().split(' GMT')[0]} - ${log}`,
                    styles: {
                        color: foregroundColor
                    }
                });
            } else if (this.currentElement) // current element exists and its the same time
                this.currentElement.innerHTML += `<br>${dateChange.toString().split(' GMT')[0]} - ${log}`;
            this.lastTime = time;
        });

        delete this.lastTime;
        delete this.currentElement;
    }

    parseCodeBlock(log) {
        if (!(/\`/g.test(log))) return log;

        const matches = log.match(/\`.*?\`/g);
        if (!matches) return log;
        matches.forEach(match => {
            log = log.replace(match, `<inlinecodeblock>${match.slice(1, -1)}</inlinecodeblock>`);
        });
        return log;
    }
}