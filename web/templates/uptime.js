class UptimeHandler extends WebManager {
    constructor(up, data, offsetSince) {
        super();
        this.up = up;
        this.offsetSince = offsetSince;
        this.data = JSON.parse(data).reverse();
        this.utc = this.UTC();
    }

    createElements() {
        if (this.up == undefined) return;

        this.board =  this.createElement({
            id: "uptimeBoard",
            styles: {
                backgroundColor: lowerContrast(20),
                fontFamily: defaultFont,
                userSelect: "none",
                display: "none",
                paddingBottom: "50px"
            }
        });
        
        this.createElement({
            at: this.board,
            id: "uptimeText",
            content: `● ${this.up ? 'UP' : 'DOWN'} for ${this.offsetSince}`,
            styles: {
                color: this.up ? "#00ff00" : "#333333",
                textAlign: "center"
            }
        });
        delete this.up;

        this.createTable();
    }
    
    createTable() {
        if ((this.up != undefined) || this.table) return;

        this.table = new Table({
            at: this.board,
            id: "tableCenter",
            values: [
                "Down Time",
                "Event happens at",
                "Uptime during session"
            ],
            style: {
                borderCollapse: "collapse",
                border: "none",
                width: "100%",
                color: foregroundColor
            },
            thStyle: {
                backgroundColor: lowerContrast(50),
                padding: "5px 20px"
            },
            tdStyle: {
                backgroundColor: lowerContrast(40),
                padding: "5px 20px"
            }
        });

        this.data.forEach(data => {
            const date = new Date(data.split("|")[0]);
            this.table.addValues([
                date.toUTCString().split(" GMT")[0], this.parseDelta(this.utc - this.UTC(date)), data.split("|")[1] 
            ]);
        });
    }
}