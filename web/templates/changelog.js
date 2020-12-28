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
        this.currentTime = Math.round(new Date(new Date().toUTCString()).getTime() / 1000);
        this.lastTime = null;
        this.timeData = {
            "31536000": "year",
            "2592000": "month",
            "86400": "day",
            "3600": "hour",
            "60": "minute"
        }
        this.currentElement = null;

        this.data.forEach(change => {
            const dateChange = new Date(change.slice(2).split(' UTC]')[0]);
            const time = this.parseDelta(this.currentTime - Math.round(dateChange.getTime() / 1000));
            const log = this.parseCodeBlock(change.split(" UTC]` ")[1]);
            
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

    parseDelta(seconds) {
        if (seconds < 60) return `${seconds} second${seconds == 1 ? '' : 's'} ago`;

        const keys = Object.keys(this.timeData).map(x => parseInt(x)).reverse();
        for (let i = 0; i < 5; i++) {
            if (seconds >= keys[i]) {
                seconds = Math.round(seconds / keys[i]);
                return `${seconds} ${this.timeData[keys[i].toString()]}${seconds == 1 ? '' : 's'} ago`;
            }
        }

        seconds = Math.round(seconds / 31536000);
        return `${seconds} year${seconds == 1 ? '' : 's'} ago`;
    }
}