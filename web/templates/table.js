class Table extends WebManager {
    constructor(data) {
        super();
        this.values = data.values;
        this.table = this.createElement({
            at: data.at,
            styles: data.style,
            id: data.id,
            elementName: "table"
        });

        this.thStyle = data.thStyle;
        this.tdStyle = data.tdStyle;
        var tr = this.createElement({
            at: this.table,
            elementName: "tr"
        });

        this.values.forEach(value => {
            this.createElement({
                at: tr,
                elementName: "th",
                styles: this.thStyle,
                content: value
            });
        });
    }

    addValues(arr) {
        var tr = this.createElement({
            at: this.table,
            elementName: "tr"
        });

        arr.forEach(value => {
            this.createElement({
                at: tr,
                elementName: "td",
                styles: this.tdStyle,
                content: value
            });
        });
    }
}